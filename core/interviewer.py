from core.llm import ask_json
from core.schemas import QuestionList

SYSTEM = (
    "You are a senior technical interviewer. You ask clear, realistic "
    "interview questions. Each question must be answerable in 1-2 paragraphs."
)


def generate_questions(topic: str, difficulty: str, n: int, context: str = "") -> list[str]:
    prompt = f"Generate {n} {difficulty} interview questions about {topic}."
    if context:
        prompt += f"\n\nUse these study notes as inspiration:\n{context}"
    result = ask_json(SYSTEM, prompt, QuestionList)
    return result.questions[:n]