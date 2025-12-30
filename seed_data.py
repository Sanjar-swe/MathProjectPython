from apps.bot.utils import setup_django
setup_django()

from apps.models import Question

questions = [
    {
        "text": "2 + 2 = ?",
        "option_a": "3",
        "option_b": "4",
        "option_c": "5",
        "option_d": "6",
        "correct_answer": "b"
    },
    {
        "text": "15 * 3 = ?",
        "option_a": "30",
        "option_b": "40",
        "option_c": "45",
        "option_d": "50",
        "correct_answer": "c"
    },
    {
        "text": "100 / 4 = ?",
        "option_a": "20",
        "option_b": "25",
        "option_c": "30",
        "option_d": "50",
        "correct_answer": "b"
    },
    {
        "text": "Square root of 81?",
        "option_a": "7",
        "option_b": "8",
        "option_c": "9",
        "option_d": "10",
        "correct_answer": "c"
    }
]

for q in questions:
    Question.objects.get_or_create(**q)

print(f"Successfully seeded {len(questions)} questions.")
