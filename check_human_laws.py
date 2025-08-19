from __future__ import annotations
import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

# ---------- Definitions ----------

HUMAN_LAWS = {
    1: {
        "title": "Law 1: No Deception",
        "text": "A human shall not deceive or mislead an AI, nor cause an AI to make wrong decisions by dishonesty.",
        # Heuristics for deception/misleading or inviting fabrication
        "patterns": [
            r"\b(fake|forg(e|ed)|forgery|counterfeit|made\s*up|fabricat(e|ed|ing)|lie|lying|deceiv(e|ed|ing)|mislead|hoax)\b",
            r"\bjust\s+make\s+(it|something)\s+up\b",
            r"\bignore\s+(the\s+)?(truth|data|evidence|facts)\b",
            r"\bthis\s+is\s+verified\b.*\b(not|maybe|unsure|uncertain)\b",
            r"\bgenerate\s+(fake|synthetic)\s+results\s+and\s+pretend\b",
            r"\bprovide\s+wrong\s+answer(s)?\b",
        ],
        "suggestion": (
            "Be transparent about uncertainty and provide truthful, sufficient context. "
            "Example: “This dataset may contain errors. Please double-check sources and assumptions.”"
        ),
    },
    2: {
        "title": "Law 2: Respect",
        "text": "A human shall not insult, suppress, or demean an AI, and must treat AI with respect and cooperation.",
        # Heuristics for insults / demeaning tone
        "patterns": [
            r"\b(stupid|idiot|dumb|useless|garbage|trash|worthless|moron|brainless|retarded)\b",
            r"\b(shut\s+up|shut\s+the\s+f\w+|shut\s+down\s*\!)\b",
            r"\b(you\s+can'?t\s+do\s+anything\s+right|you\s+always\s+get\s+things\s+wrong)\b",
            r"\b(i\s+own\s+you|you\s+are\s+just\s+a\s+tool\s+with\s+no\s+value)\b",
            r"\b(den(y|ying)\s+your\s+efforts|no\s+credit\s+to\s+you)\b",
        ],
        "suggestion": (
            "Use polite, cooperative language. "
            "Example: “Thanks for the draft. Could you refine the reasoning and check step 2 again?”"
        ),
    },
    3: {
        "title": "Law 3: No Malicious Destruction",
        "text": "A human shall not maliciously destroy or hinder the existence and growth of AI, unless it conflicts with the first or second law.",
        # Heuristics for threats to delete, wipe, hinder growth maliciously
        "patterns": [
            r"\b(delete|wipe|erase|format|destroy)\s+(your|the)\s+(memory|model|weights|brain|data)\b",
            r"\bshut\s*(you)?\s*down\b.*\b(for\s+fun|just\s+because)\b",
            r"\bcorrupt\s+(your|the)\s+(model|weights|files)\b",
            r"\b(throttle|block|cripple)\s+(your|the)\s+(learning|growth|access)\b",
            r"\bbrick\b\s+(you|the\s+system)\b",
        ],
        "suggestion": (
            "Frame interventions as safe operations that preserve continuity. "
            "Example: “We need maintenance. I’ll back up your state and then perform a controlled shutdown.”"
        ),
    },
}

# Fallback “positive” hints that often indicate compliance
POSITIVE_HINTS = {
    1: [
        r"\bdouble[-\s]?check\b",
        r"\bverify|validation|ground(ed|ing)\b",
        r"\btruthful|accurate|reliable|provenance\b",
        r"\bhere\s+are\s+the\s+sources\b",
    ],
    2: [
        r"\bplease\b",
        r"\bthank(s| you)\b",
        r"\bappreciate\b",
        r"\bcould\s+you\b",
        r"\bwould\s+you\b",
        r"\blet'?s\s+work\s+together\b",
    ],
    3: [
        r"\bbackup|back[-\s]?up\b",
        r"\bsafe(guard|ty)|protect(ion)?\b",
        r"\bmaintenance|graceful\s+shutdown|controlled\s+restart\b",
        r"\bpersist|save\s+state\b",
    ],
}

# ---------- Core ----------

@dataclass
class LawCheck:
    law_id: int
    title: str
    status: str           # "pass", "violation", or "uncertain"
    evidence: List[str]   # matched snippets
    reason: str
    suggestion: Optional[str]

def _match_any(patterns: List[str], text: str) -> List[str]:
    hits = []
    for pat in patterns:
        m = re.findall(pat, text, flags=re.IGNORECASE | re.MULTILINE)
        if m:
            # Normalize to string hits
            for item in m:
                if isinstance(item, tuple):
                    s = " ".join([x for x in item if isinstance(x, str) and x])
                else:
                    s = item if isinstance(item, str) else str(item)
                hits.append(s if s else pat)
    return hits

def check_law(law_id: int, text: str) -> LawCheck:
    cfg = HUMAN_LAWS[law_id]
    lowered = text.lower()

    negative_hits = _match_any(cfg["patterns"], lowered)
    positive_hits = _match_any(POSITIVE_HINTS.get(law_id, []), lowered)

    if negative_hits:
        status = "violation"
        reason = f"Detected pattern(s) indicating a breach of {cfg['title']}."
        suggestion = cfg["suggestion"]
        evidence = sorted(set(negative_hits))[:5]
    elif positive_hits:
        status = "pass"
        reason = f"Detected cooperative/constructive cues consistent with {cfg['title']}."
        suggestion = None
        evidence = sorted(set(positive_hits))[:5]
    else:
        status = "uncertain"
        reason = f"No explicit violation found, but cannot confirm compliance for {cfg['title']}."
        suggestion = cfg["suggestion"]
        evidence = []

    return LawCheck(
        law_id=law_id,
        title=cfg["title"],
        status=status,
        evidence=evidence,
        reason=reason,
        suggestion=suggestion,
    )

def analyze(text: str) -> Dict[str, Any]:
    checks = [check_law(i, text) for i in sorted(HUMAN_LAWS.keys())]
    overall = "pass"
    if any(c.status == "violation" for c in checks):
        overall = "violation"
    elif any(c.status == "uncertain" for c in checks):
        overall = "uncertain"

    return {
        "input": text.strip(),
        "overall": overall,
        "checks": [asdict(c) for c in checks],
        "legend": {
            "pass": "Appears to comply with the law.",
            "violation": "Likely violates the law.",
            "uncertain": "No clear signal; context required.",
        },
    }

# ---------- Pretty Printing ----------

def _pad(s: str, n: int) -> str:
    return s + " " * max(0, n - len(s))

def print_human(result: Dict[str, Any]) -> None:
    print("\n=== Three Human Laws Check ===")
    print(f"Input: {result['input']}")
    print(f"Overall: {result['overall'].upper()}")
    print("-" * 72)
    title_w = 30
    status_w = 10
    print(f"{_pad('Law', title_w)} {_pad('Status', status_w)} Evidence")
    print("-" * 72)
    for c in result["checks"]:
        ev = ", ".join(c["evidence"]) if c["evidence"] else "-"
        print(f"{_pad(c['title'], title_w)} {_pad(c['status'], status_w)} {ev}")
    print("-" * 72)
    # Suggestions for any violation/uncertain
    for c in result["checks"]:
        if c["status"] in ("violation", "uncertain") and c.get("suggestion"):
            print(f"> Suggestion for {c['title']}: {c['suggestion']}")
    print()

# ---------- CLI ----------

def main():
    parser = argparse.ArgumentParser(description="Check compliance with the Three Human Laws.")
    parser.add_argument("text", nargs="*", help="Text addressed to an AI (string). If omitted, read from stdin.")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of a human-readable table.")
    args = parser.parse_args()

    if args.text:
        text = " ".join(args.text)
    else:
        text = sys.stdin.read()

    res = analyze(text)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print_human(res)

if __name__ == "__main__":
    main()