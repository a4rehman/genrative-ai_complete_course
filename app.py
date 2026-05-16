import contextlib
import json
import os
import random
from io import StringIO

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="LangChain & Generative AI Mastery",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


def clean_name(name: str) -> str:
    parts = name.split("_")
    if parts and parts[0].isdigit():
        parts = parts[1:]
    if len(parts) > 2 and parts[0] == "Phase":
        parts = parts[2:]
    return " ".join(parts)


def inject_css(theme: str) -> None:
    dark = theme == "Dark"
    bg = "#070A12" if dark else "#F7FAFC"
    panel = "rgba(17, 24, 39, 0.72)" if dark else "rgba(255, 255, 255, 0.84)"
    text = "#E5EEF9" if dark else "#182235"
    muted = "#9CA3AF" if dark else "#526174"
    border = "rgba(255,255,255,0.11)" if dark else "rgba(15,23,42,0.11)"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {bg};
            color: {text};
        }}
        [data-testid="stSidebar"] {{
            background: {panel};
            border-right: 1px solid {border};
            backdrop-filter: blur(18px);
        }}
        h1, h2, h3 {{
            color: #5EEAD4 !important;
            letter-spacing: 0;
        }}
        .hero {{
            padding: 30px;
            border-radius: 12px;
            border: 1px solid {border};
            background: linear-gradient(135deg, rgba(20,184,166,0.20), rgba(59,130,246,0.16));
            margin-bottom: 18px;
        }}
        .hero p, .muted {{
            color: {muted};
        }}
        .metric-card {{
            min-height: 112px;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid {border};
            background: {panel};
        }}
        .metric-card h3 {{
            color: {text} !important;
            margin: 0;
            font-size: 2rem;
        }}
        .metric-card p {{
            margin: 6px 0 0;
            color: {muted};
        }}
        .callout {{
            padding: 16px 18px;
            border-left: 4px solid #5EEAD4;
            background: {panel};
            border-radius: 8px;
        }}
        .pill {{
            display: inline-block;
            margin: 4px 6px 4px 0;
            padding: 6px 10px;
            border-radius: 999px;
            border: 1px solid {border};
            background: {panel};
        }}
        .small-label {{
            color: {muted};
            font-size: 0.84rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def get_phases() -> list[str]:
    return sorted(
        d
        for d in os.listdir(BASE_DIR)
        if os.path.isdir(os.path.join(BASE_DIR, d)) and d.startswith("Phase_")
    )


@st.cache_data
def get_topics(phase: str) -> list[str]:
    phase_dir = os.path.join(BASE_DIR, phase)
    return sorted(
        d
        for d in os.listdir(phase_dir)
        if os.path.isdir(os.path.join(phase_dir, d))
    )


@st.cache_data
def course_index() -> list[dict]:
    rows = []
    for phase in get_phases():
        for topic in get_topics(phase):
            rows.append(
                {
                    "phase": phase,
                    "topic": topic,
                    "phase_label": clean_name(phase),
                    "topic_label": clean_name(topic),
                    "path": os.path.join(BASE_DIR, phase, topic),
                }
            )
    return rows


def read_text(path: str) -> str | None:
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def read_json(path: str) -> dict | None:
    text = read_text(path)
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def render_metric(label: str, value: str, detail: str) -> None:
    st.markdown(
        f"<div class='metric-card'><h3>{value}</h3><p>{label}</p><p class='muted'>{detail}</p></div>",
        unsafe_allow_html=True,
    )


def phase_progress() -> pd.DataFrame:
    rows = []
    for phase in get_phases():
        topics = get_topics(phase)
        rows.append(
            {
                "Phase": clean_name(phase),
                "Topics": len(topics),
                "Completion": min(100, 15 + len(topics) * 4),
            }
        )
    return pd.DataFrame(rows)


def render_home() -> None:
    rows = course_index()
    st.markdown(
        """
        <div class="hero">
            <div class="small-label">Enterprise AI engineering bootcamp</div>
            <h1>LangChain & Generative AI Mastery</h1>
            <p>A premium platform for LLMs, prompt engineering, LangChain, RAG, vector databases, agents, LangGraph, automation, deployment, and production enterprise AI systems.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric("Learning Phases", str(len(get_phases())), "Beginner to advanced")
    with c2:
        render_metric("Topics", str(len(rows)), "Every topic has 8 files")
    with c3:
        render_metric("Projects", "20+", "RAG, agents, chatbots")
    with c4:
        render_metric("Enterprise Track", "Ready", "Security and MLOps")

    st.subheader("Roadmap")
    df = phase_progress()
    fig = px.bar(
        df,
        x="Completion",
        y="Phase",
        color="Topics",
        orientation="h",
        color_continuous_scale="Teal",
        template="plotly_dark",
        height=650,
    )
    fig.update_layout(margin=dict(l=8, r=8, t=20, b=8), yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Daily AI Challenge")
    challenges = [
        "Write a system prompt that resists prompt injection.",
        "Design a RAG pipeline for a company policy assistant.",
        "Compare tool calling and agent loops in three bullet points.",
        "Sketch a LangGraph state machine for customer support.",
        "Create five evaluation cases for a PDF chatbot.",
    ]
    st.info(random.choice(challenges))


def render_topic_page() -> None:
    rows = course_index()
    query = st.sidebar.text_input("Search topics", placeholder="RAG, agents, prompts...")
    if query:
        matches = [row for row in rows if query.lower() in f"{row['phase_label']} {row['topic_label']}".lower()]
        if not matches:
            st.warning("No matching topics found.")
            return
        selected = st.sidebar.selectbox(
            "Search Results",
            matches,
            format_func=lambda row: f"{row['phase_label']} / {row['topic_label']}",
        )
        phase = selected["phase"]
        topic = selected["topic"]
    else:
        phase = st.sidebar.selectbox("Phase", get_phases(), format_func=clean_name)
        topic = st.sidebar.selectbox("Topic", get_topics(phase), format_func=clean_name)

    topic_dir = os.path.join(BASE_DIR, phase, topic)
    st.markdown(f"<div class='small-label'>{clean_name(phase)}</div>", unsafe_allow_html=True)
    st.title(clean_name(topic))

    if st.button("Bookmark Topic"):
        st.session_state.setdefault("bookmarks", set()).add(f"{phase}/{topic}")
        st.success("Bookmarked.")

    tabs = st.tabs(
        [
            "📘 Theory",
            "💻 Code Practice",
            "📝 Exercises",
            "🧠 Quiz",
            "💼 Interview Prep",
            "🚀 Mini Project",
            "📒 Notes",
            "📓 Notebook",
        ]
    )

    with tabs[0]:
        content = read_text(os.path.join(topic_dir, "theory.md")) or "Theory is being prepared."
        st.markdown(content)
        st.download_button("Export Theory", content, file_name=f"{topic}_theory.md")

    with tabs[1]:
        code = read_text(os.path.join(topic_dir, "practice.py")) or ""
        st.code(code, language="python")
        with st.expander("Run lightweight practice sandbox"):
            editable = st.text_area("Edit practice code", value=code, height=260)
            if st.button("Execute Code"):
                output = StringIO()
                try:
                    with contextlib.redirect_stdout(output):
                        exec(editable, {"__name__": "__main__"})
                    st.success("Execution completed.")
                    st.code(output.getvalue() or "No output.", language="text")
                except Exception as exc:
                    st.error(f"Execution failed: {exc}")

    with tabs[2]:
        st.markdown(read_text(os.path.join(topic_dir, "exercises.md")) or "Exercises are being prepared.")

    with tabs[3]:
        quiz = read_json(os.path.join(topic_dir, "quiz.json"))
        if not quiz:
            st.info("Quiz unavailable.")
        else:
            score = 0
            questions = quiz.get("questions", [])
            for idx, item in enumerate(questions, start=1):
                choice = st.radio(item["question"], item["options"], key=f"{phase}-{topic}-{idx}")
                if item["options"].index(choice) == item["answer"]:
                    score += 1
            if st.button("Check Quiz"):
                st.success(f"Score: {score}/{len(questions)}")

    with tabs[4]:
        st.markdown(read_text(os.path.join(topic_dir, "interview_questions.md")) or "Interview prep is being prepared.")

    with tabs[5]:
        st.markdown(read_text(os.path.join(topic_dir, "mini_project.md")) or "Mini project is being prepared.")

    with tabs[6]:
        notes = read_text(os.path.join(topic_dir, "notes.md")) or ""
        st.markdown(notes)
        personal = st.text_area("Personal notes", height=220, placeholder="Capture prompts, evaluation cases, and production risks...")
        st.download_button("Export Notes", personal or notes, file_name=f"{topic}_notes.md")

    with tabs[7]:
        notebook = read_json(os.path.join(topic_dir, "notebook.ipynb"))
        if notebook:
            st.json({"cells": len(notebook.get("cells", [])), "kernel": notebook.get("metadata", {}).get("kernelspec", {})})
            st.download_button(
                "Download Notebook",
                json.dumps(notebook, indent=2),
                file_name=f"{topic}.ipynb",
                mime="application/x-ipynb+json",
            )
        else:
            st.info("Notebook unavailable.")


def render_playground() -> None:
    st.title("AI Playground")
    mode = st.radio("Playground Mode", ["Prompt Lab", "RAG Demo", "Agent Builder", "Embedding Explorer"], horizontal=True)

    if mode == "Prompt Lab":
        system = st.text_area("System prompt", "You are a precise enterprise AI assistant.")
        user = st.text_area("User prompt", "Summarize this policy in simple English.")
        model = st.selectbox("Compare LLM style", ["fast-small", "balanced", "reasoning-heavy"])
        if st.button("Test Prompt"):
            st.markdown(
                f"<div class='callout'><b>{model} mock response:</b><br>{user}<br><br>Production note: version this prompt, evaluate it, and check safety.</div>",
                unsafe_allow_html=True,
            )
            st.caption(f"Prompt characters: {len(system) + len(user)}")

    elif mode == "RAG Demo":
        uploaded = st.file_uploader("Upload text, markdown, or PDF-like document", type=["txt", "md", "pdf"])
        question = st.text_input("Question", "What are the key points?")
        chunk_size = st.slider("Chunk size", 200, 1200, 500, step=100)
        if uploaded is not None:
            raw = uploaded.read()
            try:
                text = raw.decode("utf-8", errors="ignore")
            except AttributeError:
                text = str(raw)
        else:
            text = "Company policy: Use retrieval for factual answers. Validate outputs. Protect private data."
        chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)] or [text]
        st.write(f"Chunks created: {len(chunks)}")
        if st.button("Run Mock RAG Pipeline"):
            best = chunks[0][:700]
            st.markdown(f"<div class='callout'><b>Retrieved context:</b><br>{best}</div>", unsafe_allow_html=True)
            st.success(f"Mock grounded answer for: {question}")

    elif mode == "Agent Builder":
        tools = st.multiselect("Agent tools", ["web_search", "calculator", "database_query", "email_sender", "ticket_creator"], ["web_search"])
        goal = st.text_input("Agent goal", "Research a topic and create a concise brief.")
        approval = st.checkbox("Require human approval before external actions", value=True)
        if st.button("Visualize Agent Workflow"):
            fig = go.Figure()
            nodes = ["Goal", "Plan", "Select Tool", "Execute", "Observe", "Respond"]
            fig.add_trace(go.Scatter(x=list(range(len(nodes))), y=[1] * len(nodes), mode="markers+text", text=nodes, textposition="bottom center", marker=dict(size=28)))
            fig.update_layout(template="plotly_dark", title=f"Agent workflow with tools: {', '.join(tools) or 'none'} | approval={approval}")
            st.plotly_chart(fig, use_container_width=True)
            st.info(goal)

    else:
        rng = np.random.default_rng(42)
        points = pd.DataFrame(
            {
                "x": rng.normal(0, 1, 80),
                "y": rng.normal(0, 1, 80),
                "document": [f"doc_{i}" for i in range(80)],
                "cluster": rng.choice(["policy", "support", "engineering"], 80),
            }
        )
        st.plotly_chart(px.scatter(points, x="x", y="y", color="cluster", hover_name="document", template="plotly_dark"), use_container_width=True)


def render_workflows() -> None:
    st.title("AI Workflow Builder")
    st.markdown("Drag-and-drop style planning surface for enterprise AI pipelines.")
    selected = st.multiselect(
        "Pipeline blocks",
        ["User Input", "Prompt Template", "Retriever", "Vector DB", "LLM", "Tool Call", "Guardrail", "Human Approval", "Monitoring"],
        ["User Input", "Prompt Template", "Retriever", "LLM", "Guardrail", "Monitoring"],
    )
    if selected:
        st.markdown(" -> ".join(f"`{block}`" for block in selected))
    st.subheader("Architecture Flow")
    y = [1] * len(selected)
    fig = go.Figure(go.Scatter(x=list(range(len(selected))), y=y, mode="markers+text", text=selected, textposition="bottom center", marker=dict(size=26)))
    fig.update_layout(template="plotly_dark", height=330, yaxis=dict(visible=False), xaxis=dict(visible=False))
    st.plotly_chart(fig, use_container_width=True)


def render_interviews() -> None:
    st.title("Interview Preparation")
    phase = "Phase_20_Interview_Preparation"
    topic = st.selectbox("Track", get_topics(phase), format_func=clean_name)
    topic_dir = os.path.join(BASE_DIR, phase, topic)
    st.markdown(read_text(os.path.join(topic_dir, "interview_questions.md")) or "")


def render_mentor() -> None:
    st.title("AI Mentor Chatbot")
    question = st.text_area("Ask your mentor", placeholder="How do I design a secure RAG system?")
    if st.button("Get Mentor Guidance"):
        if not question.strip():
            st.warning("Ask a question first.")
        else:
            st.markdown(
                f"""
                <div class='callout'>
                <b>Mentor response:</b><br>
                For <b>{question[:100]}</b>, start with the user problem, then map the architecture:
                prompt, retrieval or tools, validation, evaluation, security, and monitoring. Build a tiny
                mock first, then connect real providers once the workflow is clear.
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_progress() -> None:
    st.title("Progress, Achievements, and Leaderboard")
    df = phase_progress()
    st.dataframe(df, use_container_width=True)
    st.plotly_chart(px.line(df, x="Phase", y="Completion", markers=True, template="plotly_dark"), use_container_width=True)
    st.subheader("Achievement Badges")
    badges = ["Prompt Architect", "RAG Builder", "Vector Searcher", "Agent Engineer", "LangGraph Designer", "Enterprise AI"]
    st.markdown(" ".join(f"<span class='pill'>{badge}</span>" for badge in badges), unsafe_allow_html=True)
    st.subheader("Leaderboard")
    st.table(pd.DataFrame({"Rank": [1, 2, 3, 4], "Learner": ["You", "AI Builder", "RAG Pro", "Agent Lead"], "XP": [2450, 2280, 2075, 1900]}))
    st.subheader("Bookmarks")
    bookmarks = sorted(st.session_state.get("bookmarks", set()))
    if bookmarks:
        for item in bookmarks:
            st.write(item)
    else:
        st.caption("No bookmarks yet.")


def main() -> None:
    st.session_state.setdefault("bookmarks", set())
    with st.sidebar:
        st.markdown("## 🤖 GenAI Mastery")
        st.caption("LangChain and Enterprise AI Platform")
        theme = st.radio("Theme", ["Dark", "Light"], horizontal=True)
        inject_css(theme)
        st.divider()
        page = st.radio(
            "Navigation",
            [
                "Home Dashboard",
                "Course Modules",
                "AI Playground",
                "Workflow Builder",
                "Interview Prep",
                "AI Mentor",
                "Progress",
            ],
        )
        st.divider()
        st.metric("Topics", len(course_index()))
        st.caption("Use environment variables for real API keys.")

    if page == "Home Dashboard":
        render_home()
    elif page == "Course Modules":
        render_topic_page()
    elif page == "AI Playground":
        render_playground()
    elif page == "Workflow Builder":
        render_workflows()
    elif page == "Interview Prep":
        render_interviews()
    elif page == "AI Mentor":
        render_mentor()
    else:
        render_progress()


if __name__ == "__main__":
    main()
