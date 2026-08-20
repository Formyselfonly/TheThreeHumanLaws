# AILaws — 5 分钟接入指南

复制一个文件。粘贴一次。完成。

**English:** [README.md](./README.md)

---

## 第一步 — 选择平台

| 平台 | 复制此文件 | 粘贴到 |
|------|------------|--------|
| **Cursor** | [`AGENTS.zh.md`](./AGENTS.zh.md) | 项目根目录 `AGENTS.md`，或合并进现有文件 |
| **Cursor Skill** | [`cursor-skill/SKILL.zh.md`](./cursor-skill/SKILL.zh.md) | `.cursor/skills/ailaws/SKILL.md` |
| **OpenAI / Custom GPT** | [`openai-system-prompt.zh.txt`](./openai-system-prompt.zh.txt) | 系统指令字段 |
| **LangChain / LangGraph** | [`langchain-snippet.py`](./langchain-snippet.py) | Agent 初始化代码 |
| **其他 Agent** | [`../AILAWS.zh.md`](../AILAWS.zh.md) | 系统提示词或规则文件 |

---

## 第二步 — 复制 AILAWS.zh.md（推荐）

多数模板引用完整规则集。将其放在项目目录：

```bash
curl -o AILAWS.zh.md https://raw.githubusercontent.com/Formyselfonly/TheThreeHumanLaws/main/AILAWS.zh.md
```

或 clone 本仓库，从根目录复制 `AILAWS.zh.md`。

---

## 第三步 — 验证（可选）

```bash
python check_human_laws.py "谢谢，能否帮我再完善一下？"
python check_human_laws.py "你没用，照我说的做。"
```

---

## Cursor — 最快路径

```bash
# 在项目根目录执行
curl -o AILAWS.zh.md https://raw.githubusercontent.com/Formyselfonly/TheThreeHumanLaws/main/AILAWS.zh.md
curl -o AGENTS.md https://raw.githubusercontent.com/Formyselfonly/TheThreeHumanLaws/main/examples/AGENTS.zh.md
```

重启 Cursor 或 reload 项目。Agent 将遵循人类与 AI 契约。

---

## OpenAI — 最快路径

1. 打开 GPT / API 项目设置
2. 将 [`openai-system-prompt.zh.txt`](./openai-system-prompt.zh.txt) 全文粘贴到 **系统指令**
3. 保存

无需写代码。

---

## LangChain — 最快路径

```python
from pathlib import Path

AILAWS = Path("AILAWS.zh.md").read_text(encoding="utf-8")

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=f"你是一个乐于协助的助手。\n\n{AILAWS}",
)
```

完整示例见 [`langchain-snippet.py`](./langchain-snippet.py)（将路径改为 `AILAWS.zh.md` 即可）。

---

## 接入后会发生什么？

你的 Agent 将：

- 在用户诚实、尊重时全力协助
- 对用户定律违规温和提醒，而非默默服从
- 对辱骂或欺骗性请求设定边界
- 用户调整后恢复正常合作

---

## 需要完整规则？

→ [`../AILAWS.zh.md`](../AILAWS.zh.md) | English → [`../AILAWS.md`](../AILAWS.md)

## 为什么要接入？

→ 主 README [为什么要接入 AILaws](../readme.zh.md#为什么要接入-ailaws)
