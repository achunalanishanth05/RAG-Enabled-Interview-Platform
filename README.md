# 🎤 AI Interview Coach

An AI-powered mock interview application that asks technical questions, evaluates your answers, and coaches you on how to improve.

Built with **Python, LangGraph, LiteLLM, Pydantic, LlamaIndex, Qdrant, Jina AI and Streamlit**.

---

## 📌 Features

- **Mock interviews:** generates technical questions on Python, SQL, Data Structures, Machine Learning and System Design, at Easy, Medium or Hard difficulty.
- **Answer evaluation:** scores each answer from 0 to 10 on correctness, relevance and completeness, and lists strengths, weaknesses and an ideal answer.
- **Personal coaching:** gives specific tips to improve each answer.
- **Final report:** shows your average score, top weak areas and a 5-point study plan.
- **Custom study notes (RAG):** add your own notes or a job description in the `knowledge/` folder, and questions and evaluations will be grounded in them.
- **Reliable AI calls:** automatic retries and an optional fallback model for temporary API errors.

---

## 🧠 How It Works

```
Choose topic and difficulty
        ↓
RAG finds relevant study notes (optional)
        ↓
Interviewer generates questions
        ↓
You type your answer
        ↓
LangGraph workflow:  Evaluator → Coach
        ↓
Scores, feedback and coaching tips
        ↓
Final report and study plan
```

---

## 🛠️ Tech Stack

Python 3.11-->Main language
Streamlit-->Web interface
LangGraph-->Connects the evaluate and coach steps
LiteLLM-->One interface for different LLM providers
Pydantic-->Validates structured AI output (scores 0 to 10)
LlamaIndex-->Loads and splits notes into chunks
Qdrant-->Vector database for similarity search
Jina AI-->Embeddings and reranking
python-dotenv-->Loads API keys from .env

---

## 📁 Project Structure

```
interview-coach/
├── app.py                 # Streamlit web interface
├── requirements.txt       # Python dependencies
├── .env                   # API keys
├── knowledge/
│   └── python_notes.md    # study notes (used for RAG)
└── core/
    ├── __init__.py
    ├── llm.py             # Calls the LLM, with retries and JSON parsing
    ├── schemas.py         # Pydantic models for questions and scores
    ├── interviewer.py     # Generates interview questions
    ├── evaluator.py       # Scores answers using a rubric
    ├── coach.py           # Gives improvement tips and the final report
    ├── rag.py             # Chunks, embeds, stores and retrieves notes
    └── workflow.py        # LangGraph workflow (evaluate → coach)
```

---