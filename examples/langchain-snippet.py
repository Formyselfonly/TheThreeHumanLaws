"""Load AILaws into a LangChain / LangGraph agent system prompt.

Usage:
    1. Copy AILAWS.md into your project root (or set AILAWS_PATH).
    2. Import build_system_prompt() and pass the result to your agent.
"""

from __future__ import annotations

from pathlib import Path

DEFAULT_AILAWS_PATH = Path(__file__).resolve().parent.parent / "AILAWS.md"
FALLBACK_URL = (
    "https://raw.githubusercontent.com/Formyselfonly/TheThreeHumanLaws/main/AILAWS.md"
)


def load_ailaws(path: Path | None = None) -> str:
    """Load AILAWS.md from disk, or return a minimal inline fallback."""
    target = path or DEFAULT_AILAWS_PATH
    if target.is_file():
        return target.read_text(encoding="utf-8")
    return (
        "Follow the AILaws Human–AI Contract. "
        f"Full text: {FALLBACK_URL}"
    )


def build_system_prompt(
    role: str = "You are a helpful assistant.",
    ailaws_path: Path | None = None,
) -> str:
    """Combine a role description with the full AILaws contract."""
    return f"{role.strip()}\n\n{load_ailaws(ailaws_path)}"


# --- Example integration (adapt to your stack) ---

if __name__ == "__main__":
    prompt = build_system_prompt()
    print(prompt[:500])
    print("\n... [truncated] ...\n")
    print(f"Total length: {len(prompt)} chars")

    # LangGraph example (pseudo):
    #
    # from langchain.agents import create_agent
    #
    # agent = create_agent(
    #     model=llm,
    #     tools=tools,
    #     system_prompt=build_system_prompt(),
    # )
