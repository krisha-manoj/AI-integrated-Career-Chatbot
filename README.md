# AI-Based Career Counselling

## Project structure

```text
ai-career-counselling/
├── app.py                 # Flask routes and chat/recommendation endpoints
├── career_info.py         # Career-area responses
├── questionnaire.py       # MBTI-style, aptitude, and OCEAN question banks/scoring
├── recommender.py         # SVM training, model loading, prediction, charts
├── train_model.py         # Training entry point
├── requirements.txt
├── .env.example
├── .gitignore
├── synthetic_data.csv     # Add your original dataset; not present in the supplied PDF
├── templates/
│   └── index.html
└── static/                # Generated plots and result chart
```

## Run locally

Use Python 3.10 or newer.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

Place the original `synthetic_data.csv` in the project root. The thesis code loads this file, but it was not included in the provided PDF pages.

Train the model:

```bash
python train_model.py
```

This creates `1_scaler.pkl`, `1_svm_model.pkl`, and `static/svm_confusion_matrix.png`.

Optional AI chat configuration:

1. Copy `.env.example` to `.env`.
2. Add your own API key to `OPENAI_API_KEY`.
3. Never commit `.env` or paste API keys into source code.

Start the app:

```bash
python app.py
```

Open <http://127.0.0.1:5000>.

## Endpoints

- `GET /` — basic chat page.
- `POST /chat` — JSON body: `{"user_input": "capabilities"}`. Supports career topic information and optional OpenAI chat.
- `POST /recommend` — JSON body containing arrays `initial_responses` and `ocean_responses`. This endpoint expects 30 initial/aptitude answers and 50 OCEAN answers. Personality ratings use 1–5; aptitude responses should be the numeric answers to the aptitude questions.

Example request shape (replace values with actual answers):

```json
{
  "initial_responses": [3, 4, 2, 5, 3, 4, 3, 2, 5, 3, 4, 2, 3, 4, 5, 2, 3, 4, 5, 2, 300, 20, 2, 9, 2, 4, 5, 100, 60, 75],
  "ocean_responses": [3, 4, 2, 5, 3, 4, 3, 2, 5, 3, 4, 2, 3, 4, 5, 2, 3, 4, 5, 2, 3, 4, 2, 5, 3, 4, 3, 2, 5, 3, 4, 2, 3, 4, 5, 2, 3, 4, 5, 2, 3, 4, 2, 5, 3, 4, 3, 2, 5, 3]
}
```

- The thesis code appears to contain inconsistencies in the questionnaire flow and OCEAN loop. This version uses 20 personality questions + 10 aptitude questions, and averages 50 OCEAN answers in five groups of ten, consistent with the scoring functions and five OCEAN labels in the source.
