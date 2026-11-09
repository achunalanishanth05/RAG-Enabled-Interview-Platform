from pydantic import BaseModel, Field


class QuestionList(BaseModel):
    questions: list[str]


class Evaluation(BaseModel):
    correctness: int = Field(ge=0, le=10, description="Is the answer factually right?")
    relevance: int = Field(ge=0, le=10, description="Does it answer what was asked?")
    completeness: int = Field(ge=0, le=10, description="Does it cover the key points?")
    overall: int = Field(ge=0, le=10)
    strengths: list[str]
    weaknesses: list[str]
    ideal_answer: str