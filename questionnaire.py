"""Question bank and scoring helpers."""
from typing import Sequence

INITIAL_QUESTIONS = [
    "mbti20. I prefer small gatherings over large parties.",
    "mbti19. I feel energized after spending time alone.",
    "mbti18. I enjoy one-on-one conversations more than group discussions.",
    "mbti17. I need time to recharge after socializing.",
    "mbti16. I am comfortable with long periods of solitude.",
    "mbti15. I do not often trust my instincts and gut feelings.",
    "mbti14. I do not enjoy brainstorming and coming up with new ideas.",
    "mbti13. I am not drawn to abstract and theoretical concepts.",
    "mbti12. I find routine and predictability comforting.",
    "mbti11. I rely on my practical experiences and observations.",
    "mbti10. I prioritize logic and reason in decision-making.",
    "mbti9. I find it easy to detach myself emotionally from situations.",
    "mbti8. I value honesty and directness over tactfulness.",
    "mbti7. I prefer to make decisions based on objective criteria.",
    "mbti6. I am more analytical than empathetic.",
    "mbti5. I like to plan and organize my activities in advance.",
    "mbti4. I feel uncomfortable with uncertainty and prefer a clear plan.",
    "mbti3. I enjoy setting and achieving specific goals.",
    "mbti2. I prefer to have a routine and stick to it.",
    "mbti1. I find it satisfying to complete tasks before deadlines.",
]

OCEAN_QUESTIONS = [
    "ocean50. I enjoy trying new and unfamiliar activities.",
    "ocean49. I am curious about different cultures and ways of life.",
    "ocean48. I appreciate art and creativity.",
    "ocean47. I often come up with novel ideas and solutions.",
    "ocean46. I enjoy exploring abstract concepts and theories.",
    "ocean45. I am open to unconventional beliefs and ideas.",
    "ocean44. I enjoy discussing philosophical and theoretical topics.",
    "ocean43. I am interested in trying new and exotic foods.",
    "ocean42. I enjoy reading fiction and exploring imaginary worlds.",
    "ocean41. I am open to changing my opinions based on new information.",
    "ocean40. I am organized and keep my belongings in order.",
    "ocean39. I set clear goals for myself and work towards them.",
    "ocean38. I am disciplined and stick to my plans.",
    "ocean37. I pay attention to detail and strive for accuracy.",
    "ocean36. I prioritize my tasks and manage my time effectively.",
    "ocean35. I am reliable and fulfill my commitments.",
    "ocean34. I find it easy to stay focused on my work.",
    "ocean33. I prefer to plan ahead rather than be spontaneous.",
    "ocean32. I am careful and cautious in my decision-making.",
    "ocean31. I take my responsibilities seriously.",
    "ocean30. I enjoy socializing and being around people.",
    "ocean29. I am outgoing and enjoy meeting new people.",
    "ocean28. I feel comfortable in group settings and parties.",
    "ocean27. I often take the initiative in social situations.",
    "ocean26. I enjoy being the center of attention at times.",
    "ocean25. I am talkative and enjoy expressing my thoughts.",
    "ocean24. I prefer to spend time with others rather than being alone.",
    "ocean23. I find social events and gatherings energizing.",
    "ocean22. I enjoy participating in group activities and team projects.",
    "ocean21. I often seek out social engagements and opportunities.",
    "ocean20. I am considerate of others' feelings.",
    "ocean19. I enjoy helping others and providing support.",
    "ocean18. I value cooperation and collaboration.",
    "ocean17. I avoid conflicts and disagreements when possible.",
    "ocean16. I am empathetic and understanding towards others.",
    "ocean15. I am forgiving and don't hold grudges easily.",
    "ocean14. I try to be polite and considerate in my interactions.",
    "ocean13. I find it easy to trust others.",
    "ocean12. I enjoy working in collaborative and team-oriented environments.",
    "ocean11. I value harmony and avoid confrontation.",
    "ocean10. I am prone to worry and anxiety.",
    "ocean9. I often feel stressed about various aspects of my life.",
    "ocean8. I am easily upset or irritated.",
    "ocean7. I experience mood swings and emotional highs/lows.",
    "ocean6. I tend to dwell on negative experiences.",
    "ocean5. I often feel anxious about the future.",
    "ocean4. I am easily stressed in challenging situations.",
    "ocean3. I am sensitive to criticism and negative feedback.",
    "ocean2. I find it difficult to let go of worries.",
    "ocean1. I experience a wide range of emotions in my daily life.",
]

APTITUDE_QUESTIONS = [
    "apti10. If a car travels at 60 km/hour, how many kilometers will it travel in 5 hours?",
    "apti9. A shopkeeper sells a shirt for $25, making a profit of 25%. What is the cost price?",
    "apti8. If 3 pencils cost $0.75, how much will 8 pencils cost?",
    "apti7. If the perimeter of a square is 36 cm, what is the length of one side?",
    "apti6. If 4 workers can build a wall in 4 days, how many days will 8 workers take?",
    "apti5. A train travels at 80 km/hour. How long will it take to travel 320 kilometers?",
    "apti4. If a rectangle's area is 60 square meters and its length is 12 meters, what is its width?",
    "apti3. If the selling price is $120 and the profit earned is 20%, what is the cost price?",
    "apti2. If one quarter of a number is 15, what is the number?",
    "apti1. A box contains 12 chocolates and 3 are taken out. What percentage remains?",
]

# Answers transcribed from the thesis; these are retained as source values.
APTITUDE_ANSWERS = [300, 20, 2, 9, 2, 4, 5, 100, 60, 75]


def calculate_initial_question_averages(
    responses: Sequence[int],
    aptitude_answers: Sequence[int] = APTITUDE_ANSWERS,
    personality_question_count: int = len(INITIAL_QUESTIONS),
):
    """Return four personality averages plus aptitude score percentage.

    The thesis uses the first 20 answers in four groups of five and compares
    the final 10 responses with the listed answer key.
    """
    if len(responses) != personality_question_count + len(aptitude_answers):
        raise ValueError("Unexpected number of initial and aptitude responses.")

    personality = responses[:personality_question_count]
    groups = [personality[i:i + 5] for i in range(0, 20, 5)]
    averages = [sum(group) / len(group) for group in groups]
    aptitude_responses = responses[personality_question_count:]
    correct = sum(
        answer == expected
        for answer, expected in zip(aptitude_responses, aptitude_answers)
    )
    aptitude_percentage = correct / len(aptitude_answers) * 100
    return averages + [aptitude_percentage]


def calculate_ocean_averages(responses: Sequence[int]):
    """Average the 50 OCEAN responses as five consecutive groups of ten."""
    if len(responses) != len(OCEAN_QUESTIONS):
        raise ValueError(f"Expected {len(OCEAN_QUESTIONS)} OCEAN responses.")
    return [
        sum(responses[start:start + 10]) / 10
        for start in range(0, len(responses), 10)
    ]
