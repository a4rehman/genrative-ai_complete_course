"""
Practice: LoRA
A dependency-light starter so the lab runs before API keys or LangChain providers are configured.
Extend this into a real LangChain/OpenAI implementation as you progress.
"""

from dataclasses import dataclass


@dataclass
class PromptCase:
    role: str
    task: str
    context: str


def build_prompt(case: PromptCase) -> str:
    return (
        f"Role: {case.role}\n"
        f"Task: {case.task}\n"
        f"Context: {case.context}\n"
        "Answer with: intuition, steps, and one production note."
    )


def mock_llm(prompt: str) -> str:
    return f"Mock response for prompt length {len(prompt)} characters. Replace this with a real LLM call."


def main():
    case = PromptCase(
        role="AI engineering mentor",
        task="Explain LoRA",
        context="Beginner learner building production GenAI apps",
    )
    prompt = build_prompt(case)
    print(prompt)
    print("---")
    print(mock_llm(prompt))


if __name__ == "__main__":
    main()
