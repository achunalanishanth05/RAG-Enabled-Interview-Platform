import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from core.interviewer import generate_questions
from core.workflow import graph
from core.coach import final_report
from core.rag import build_index, retrieve

st.set_page_config(page_title="Interview Coach", page_icon="🎤")
st.title("🎤 Personal Interview Coach")


@st.cache_resource  # build the notes index only once
def get_index():
    return build_index("knowledge")


index = get_index()

# Streamlit re-runs this file on every click, so we keep data in session_state
defaults = {"questions": [], "i": 0, "history": [], "result": None,
            "started": False, "report": None}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# ---------- Sidebar: choose your interview ----------
with st.sidebar:
    topic = st.selectbox("Topic", ["Python", "SQL", "Data Structures",
                                   "Machine Learning", "System Design"])
    difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"], value="Medium")
    n = st.slider("Number of questions", 1, 10, 3)
    if st.button("Start interview"):
        with st.spinner("Preparing questions..."):
            context = retrieve(index, topic)
            st.session_state.questions = generate_questions(topic, difficulty, n, context)
        st.session_state.update(i=0, history=[], result=None, started=True, report=None)

if not st.session_state.started:
    st.info("👈 Pick a topic in the sidebar and click **Start interview**.")
    st.stop()

qs = st.session_state.questions
i = st.session_state.i

# ---------- Interview finished: show the report ----------
if i >= len(qs):
    st.header("📋 Final report")
    hist = st.session_state.history
    avg = sum(h["evaluation"]["overall"] for h in hist) / max(len(hist), 1)
    st.metric("Average score", f"{avg:.1f} / 10")
    if st.session_state.report is None:
        with st.spinner("Writing your report..."):
            st.session_state.report = final_report(hist)
    st.markdown(st.session_state.report)
    st.stop()

# ---------- Ask the question, accept the answer ----------
st.subheader(f"Question {i + 1} of {len(qs)}")
st.write(qs[i])
answer = st.text_area("Your answer", key=f"ans_{i}", height=200)

if st.button("Submit answer") and answer.strip():
    with st.spinner("Evaluating..."):
        context = retrieve(index, qs[i])
        out = graph.invoke({"question": qs[i], "answer": answer, "context": context})
    st.session_state.result = out
    st.session_state.history.append(out)

# ---------- Show scores and coaching ----------
res = st.session_state.result
if res and res["question"] == qs[i]:
    ev = res["evaluation"]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Correctness", ev["correctness"])
    c2.metric("Relevance", ev["relevance"])
    c3.metric("Completeness", ev["completeness"])
    c4.metric("Overall", ev["overall"])

    st.success("**Strengths:** " + "; ".join(ev["strengths"]))
    st.warning("**Weaknesses:** " + "; ".join(ev["weaknesses"]))
    st.markdown("### 🧑‍🏫 Coach says")
    st.write(res["coaching"])
    with st.expander("See an ideal answer"):
        st.write(ev["ideal_answer"])

    if st.button("Next question ➡️"):
        st.session_state.i += 1
        st.session_state.result = None
        st.rerun()