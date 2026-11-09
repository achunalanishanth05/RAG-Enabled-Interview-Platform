from core.llm import ask_json
from core.schemas import Evaluation

SYSTEM = """You are a strict but fair technical interview evaluator.
Score the candidate's answer from 0 to 10 on:
- correctness: is it factually right?
- relevance: does it actually answer the question?
- completeness: does it cover the important points?
Also give 'overall' (0-10), 2-3 strengths, 2-3 weaknesses,
and a short ideal_answer. Do not be generous: a vague answer scores below 5."""


def evaluate_answer(question: str, answer: str, context: str = "") -> Evaluation:
    prompt = f"Question: {question}\n\nCandidate's answer: {answer}"
    if context:
        prompt += f"\n\nReference notes (use to check facts):\n{context}"
    return ask_json(SYSTEM, prompt, Evaluation)