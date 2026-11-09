from core.llm import ask_llm

COACH_SYSTEM = (
    "You are a supportive interview coach. Be specific and encouraging. "
    "Give practical tips, not generic advice. Keep it under 150 words."
)


def coach_answer(question: str, answer: str, evaluation: dict) -> str:
    prompt = (
        f"Question: {question}\nCandidate answer: {answer}\n"
        f"Evaluation: {evaluation}\n\n"
        "Tell the candidate how to improve THIS answer, and suggest a better "
        "structure for answering it in a real interview."
    )
    return ask_llm(COACH_SYSTEM, prompt)


def final_report(history: list[dict]) -> str:
    summary = "\n".join(
        f"Q: {h['question']}\nOverall: {h['evaluation']['overall']}/10\n"
        f"Weaknesses: {h['evaluation']['weaknesses']}\n"
        for h in history
    )
    prompt = (
        f"Here is the candidate's full mock interview:\n{summary}\n\n"
        "Write a final report with: 1) overall impression, 2) top 3 weak areas, "
        "3) a 5-point study plan for the next week."
    )
    return ask_llm(COACH_SYSTEM, prompt)