"""Flask web application for AI-based career counselling."""
import os
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

from career_info import get_topic_info
from questionnaire import (
    INITIAL_QUESTIONS,
    OCEAN_QUESTIONS,
    APTITUDE_QUESTIONS,
    APTITUDE_ANSWERS,
    calculate_initial_question_averages,
    calculate_ocean_averages,
)
from recommender import load_recommender, predict_career, create_ocean_chart

load_dotenv()
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# Keep API credentials outside source control. AI chat is optional.
api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=api_key) if api_key else None

try:
    scaler, model = load_recommender()
except (FileNotFoundError, RuntimeError) as exc:
    app.logger.warning("Career model unavailable: %s", exc)
    scaler, model = None, None


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/chat")
def chat():
    """Handle general questions and step-by-step assessment responses."""
    payload = request.get_json(silent=True) or request.form
    user_input = str(payload.get("user_input", "")).strip()
    if not user_input:
        return jsonify({"response": "Please enter a message."}), 400

    lower_input = user_input.lower()

    if lower_input == "ai":
        return jsonify({"response": "AI chat mode requested. Ask your question."})
    if lower_input == "exit":
        return jsonify({"response": "You can now ask about capabilities or career recommendations."})

    if lower_input == "recommend":
        return jsonify({
            "response": "To begin the assessment, select a response from 1 to 5 for each statement.",
            "assessment": True,
            "questions": {
                "initial": INITIAL_QUESTIONS + APTITUDE_QUESTIONS,
                "ocean": OCEAN_QUESTIONS,
            },
        })

    if "capabilities" in lower_input:
        return jsonify({"response": (
            "You can ask about careers in science, technology, engineering, medicine, "
            "business, arts, law, education, agriculture, design, and psychology. "
            "Type 'recommend' to begin the assessment."
        )})

    topic_keywords = [
        "science", "technology", "tech", "engineering", "medicine", "healthcare",
        "business", "management", "arts", "humanities", "law", "legal", "education",
        "teaching", "agriculture", "farming", "design", "creative", "psychology",
        "counseling",
    ]
    if any(topic in lower_input for topic in topic_keywords):
        return jsonify({"response": get_topic_info(lower_input)})

    if openai_client:
        try:
            completion = openai_client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Your name is Mr. Krish. You are a career counselling "
                            "expert primarily addressing students in classes 8 to 10. "
                            "Focus on the Indian education system, explain options clearly, "
                            "and avoid presenting career predictions as guarantees."
                        ),
                    },
                    {"role": "user", "content": user_input},
                ],
            )
            return jsonify({"response": completion.choices[0].message.content})
        except Exception:
            app.logger.exception("OpenAI request failed")
            return jsonify({"response": "AI chat is temporarily unavailable. Please try again."}), 502

    return jsonify({
        "response": "General chat is not configured. Set OPENAI_API_KEY in your environment, "
                    "or ask about a career topic / type 'capabilities'."
    })


@app.post("/recommend")
def recommend():
    """Accept questionnaire responses and return a predicted career label and chart."""
    if scaler is None or model is None:
        return jsonify({
            "error": "The trained model files are missing. Run train_model.py first."
        }), 503

    payload = request.get_json(silent=True) or request.form
    try:
        initial_responses = [int(value) for value in payload.getlist("initial_responses")] \
            if hasattr(payload, "getlist") else [int(value) for value in payload.get("initial_responses", [])]
        ocean_responses = [int(value) for value in payload.getlist("ocean_responses")] \
            if hasattr(payload, "getlist") else [int(value) for value in payload.get("ocean_responses", [])]
    except (TypeError, ValueError):
        return jsonify({"error": "Responses must be numeric."}), 400

    expected_initial = len(INITIAL_QUESTIONS) + len(APTITUDE_QUESTIONS)
    if len(initial_responses) != expected_initial or len(ocean_responses) != len(OCEAN_QUESTIONS):
        return jsonify({
            "error": f"Submit {expected_initial} initial/aptitude answers and "
                     f"{len(OCEAN_QUESTIONS)} OCEAN answers."
        }), 400
    if any(value < 1 or value > 5 for value in initial_responses[:len(INITIAL_QUESTIONS)] + ocean_responses):
        return jsonify({"error": "Personality answers must be between 1 and 5."}), 400

    averages = calculate_initial_question_averages(
        initial_responses, APTITUDE_ANSWERS, len(INITIAL_QUESTIONS)
    )
    try:
        career, aptitude_score = predict_career(scaler, model, averages)
    except Exception:
        app.logger.exception("Career prediction failed")
        return jsonify({"error": "The model could not make a prediction. Check training data columns."}), 500

    ocean_averages = calculate_ocean_averages(ocean_responses)
    chart_path = create_ocean_chart(ocean_averages)
    return jsonify({
        "career": str(career),
        "aptitude_score": aptitude_score,
        "ocean_scores": dict(zip(
            ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"],
            ocean_averages,
        )),
        "chart": "/" + chart_path.replace(os.sep, "/"),
    })


if __name__ == "__main__":
    # Use debug=False outside local development.
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
