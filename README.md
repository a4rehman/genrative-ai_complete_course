# LangChain & Generative AI Mastery

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Premium_AI_Platform-FF4B4B.svg)
![LangChain](https://img.shields.io/badge/LangChain-Agentic_AI-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-API_Ready-black.svg)
![Level](https://img.shields.io/badge/Level-Beginner_to_Advanced-success.svg)

LangChain & Generative AI Mastery is a complete beginner-to-advanced course and premium AI engineering platform for building production-grade generative AI systems.

It covers LLMs, prompt engineering, LangChain, RAG, vector databases, memory, agents, LangGraph, fine-tuning, multimodal AI, automation, deployment, MLOps, enterprise architecture, and FAANG-level interview preparation.

## Features

- 20 structured learning phases
- 121 complete topic modules
- Every topic includes theory, practice, notebook, exercises, quiz, interview prep, mini project, and notes
- Premium Streamlit dashboard with dark/light mode
- Course search and sidebar navigation
- Prompt lab for testing prompt patterns
- RAG demo with document upload
- Agent workflow builder
- Embedding visualization
- Quiz system
- Interview preparation section
- AI mentor chatbot
- Progress tracker, leaderboard, achievement badges, and bookmarks
- Diagram assets for RAG, LangChain, agents, embeddings, transformers, and AI pipelines

## Learning Roadmap

1. Generative AI Fundamentals
2. Prompt Engineering
3. LLM Fundamentals
4. LangChain Basics
5. Prompts and Chains
6. Memory Systems
7. Retrieval Augmented Generation
8. Vector Databases
9. AI Agents
10. Tools and Function Calling
11. Multi-Agent Systems
12. LangGraph
13. LLM Fine-Tuning
14. Generative AI Projects
15. Multimodal AI
16. AI Automation
17. Enterprise AI Systems
18. Deployment and MLOps
19. Real-World Projects
20. Interview Preparation

## Topic Structure

Every topic contains:

- `theory.md`
- `practice.py`
- `notebook.ipynb`
- `exercises.md`
- `quiz.json`
- `interview_questions.md`
- `mini_project.md`
- `notes.md`

## Installation

```bash
cd LangChain_Generative_AI_Mastery
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

On macOS or Linux:

```bash
cd LangChain_Generative_AI_Mastery
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## OpenAI and API Key Setup

Set API keys as environment variables. Never commit keys to the repository.

PowerShell:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
$env:LANGCHAIN_API_KEY="your_langsmith_key_here"
```

macOS or Linux:

```bash
export OPENAI_API_KEY="your_api_key_here"
export LANGCHAIN_API_KEY="your_langsmith_key_here"
```

Optional provider keys:

```bash
export PINECONE_API_KEY="..."
export HUGGINGFACEHUB_API_TOKEN="..."
```

## Dashboard Screens

- Home Dashboard: roadmap, metrics, and daily AI challenge
- Course Modules: theory, code, exercises, quiz, interview prep, projects, notes, notebook export
- AI Playground: prompt lab, RAG demo, agent builder, embedding explorer
- Workflow Builder: plan drag-and-drop style AI pipelines
- Interview Prep: LangChain, LLM, RAG, vector DB, agents, system design, and FAANG questions
- AI Mentor: study guidance and architecture advice
- Progress: badges, leaderboard, bookmarks, and completion tracking

## Deployment Guide

Local:

```bash
streamlit run app.py
```

Streamlit Community Cloud:

1. Push the repository to GitHub.
2. Create a Streamlit app.
3. Set the entry point to `LangChain_Generative_AI_Mastery/app.py`.
4. Add API keys in Streamlit secrets.

Docker outline:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

## Enterprise AI Notes

Production generative AI systems should track:

- Prompt and chain versions
- Retrieval quality
- Tool calls and approvals
- Latency and model cost
- Hallucination and refusal rates
- Prompt injection attempts
- Sensitive data exposure
- User feedback and evaluation scores
- Monitoring, rollback, and incident response

## Screenshots

Place screenshots in `assets/screenshots/` after running the Streamlit platform.

## Contribution Guide

Contributions should improve clarity, correctness, or production usefulness.

1. Explain intuition before architecture.
2. Include runnable examples.
3. Add evaluation and security notes.
4. Keep API keys out of code.
5. Include enterprise trade-offs where relevant.

## Final Goal

This repository is designed to become:

- A complete LangChain bootcamp
- A portfolio-level GitHub project
- A production generative AI ecosystem
- An enterprise AI engineering platform
- A real-world RAG and agent application system
- A FAANG-level interview preparation platform
