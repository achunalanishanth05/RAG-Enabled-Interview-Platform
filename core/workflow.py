from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from core.evaluator import evaluate_answer
from core.coach import coach_answer


class State(TypedDict, total=False):   # the shared clipboard
    question: str
    answer: str
    context: str
    evaluation: dict
    coaching: str


def evaluate_node(state: State):
    result = evaluate_answer(state["question"], state["answer"], state.get("context", ""))
    return {"evaluation": result.model_dump()}


def coach_node(state: State):
    tips = coach_answer(state["question"], state["answer"], state["evaluation"])
    return {"coaching": tips}


builder = StateGraph(State)
builder.add_node("evaluate", evaluate_node)
builder.add_node("coach", coach_node)
builder.add_edge(START, "evaluate")
builder.add_edge("evaluate", "coach")
builder.add_edge("coach", END)

graph = builder.compile()