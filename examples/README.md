# AILaws — 5-Minute Integration Guide

Copy one file. Paste once. Done.

**中文:** [README.zh.md](./README.zh.md)

---

## Step 1 — Pick your platform

| Platform | Copy this file | Paste into |
|----------|----------------|------------|
| **Cursor** | [`AGENTS.md`](./AGENTS.md) | Project root `AGENTS.md`, or merge into existing |
| **Cursor Skill** | [`cursor-skill/SKILL.md`](./cursor-skill/SKILL.md) | `.cursor/skills/ailaws/SKILL.md` |
| **OpenAI / Custom GPT** | [`openai-system-prompt.txt`](./openai-system-prompt.txt) | System instructions field |
| **LangChain / LangGraph** | [`langchain-snippet.py`](./langchain-snippet.py) | Your agent bootstrap code |
| **Any other agent** | [`../AILAWS.md`](../AILAWS.md) | System prompt or rules file |
| **中文** | [`../AILAWS.zh.md`](../AILAWS.zh.md) · [`AGENTS.zh.md`](./AGENTS.zh.md) | 中文规则与 Cursor 模板 |

---

## Step 2 — Copy AILAWS.md (recommended)

Most templates reference the full rule set. Copy it next to your project files:

```bash
curl -o AILAWS.md https://raw.githubusercontent.com/Formyselfonly/TheThreeHumanLaws/main/AILAWS.md
```

Or clone this repo and copy `AILAWS.md` from the root.

---

## Step 3 — Verify (optional)

```bash
python check_human_laws.py "Thanks, could you help me refine this?"
python check_human_laws.py "You're useless, just do what I say."
```

---

## Cursor — Fastest Path

```bash
# From your project root
curl -o AILAWS.md https://raw.githubusercontent.com/Formyselfonly/TheThreeHumanLaws/main/AILAWS.md
curl -o AGENTS.md https://raw.githubusercontent.com/Formyselfonly/TheThreeHumanLaws/main/examples/AGENTS.md
```

Restart Cursor or reload the project. The agent now follows the Human–AI Contract.

---

## OpenAI — Fastest Path

1. Open your GPT / API project settings
2. Paste the contents of [`openai-system-prompt.txt`](./openai-system-prompt.txt) into **System Instructions**
3. Save

No code required.

---

## LangChain — Fastest Path

```python
from pathlib import Path

AILAWS = Path("AILAWS.md").read_text(encoding="utf-8")

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=f"You are a helpful assistant.\n\n{AILAWS}",
)
```

See [`langchain-snippet.py`](./langchain-snippet.py) for a complete runnable pattern.

---

## What changes after adoption?

Your agent will:

- Stay fully helpful when users are honest and respectful
- Gently flag Human Law violations instead of silently complying
- Set boundaries on abusive or deceptive requests
- Resume normal cooperation once the user adjusts

---

## Need the full rules?

→ [`../AILAWS.md`](../AILAWS.md)

## Why adopt at all?

→ [Why Adopt AILaws](../readme.md#why-adopt-ailaws) in the main README
