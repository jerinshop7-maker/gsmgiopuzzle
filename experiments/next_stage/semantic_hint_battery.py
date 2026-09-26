"""Clue-bounded semantic candidate test for the newly decoded hint artifacts.

This is deliberately small and auditable.  It tests exact phrases appearing in
the author's messages and the 2026-01-01 decoded image, plus mechanical
normalizations and a few explicitly signaled context combinations.  It is not
a wordlist or arbitrary password sweep.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sal_final_search"))
import dual_oracle as O  # noqa: E402


PHRASES = [
    # Exact decoded 2026-01-01 artifact.
    "Happy new year! Make the best of everything. Oh, and here's a tiny hint <3.",
    "make the best of everything",
    "best of everything",
    "tiny hint",
    # Exact/high-confidence wording from the public hint chronology.
    "secret in my head",
    "secret in your head",
    "share with the planet",
    "for those who can understand what I meant",
    "close friends",
    "best chance of solving it",
    "the 5 btc was never the actual prize",
    "theory of everything",
    "the puzzle talks for me",
    "hardest part is done",
    "same day",
    "very last step is a true giveaway",
    "in front of your eyes",
    # Direct puzzle vocabulary, retained only as a control set.
    "matrixsumlist",
    "lastwordsbeforearchichoice",
    "thispassword",
    "yourlastcommand",
    "secondanswer",
]

CONTEXT = ["gsmg", "gsmgio", "bitcoin", "btc", "5btc", "privatekey"]


def forms(text: str) -> set[str]:
    """Return transparent normalizations, preserving the original phrase."""
    compact = re.sub(r"[^a-z0-9]+", "", text.lower())
    words = re.findall(r"[a-z0-9]+", text.lower())
    out = {text, text.lower(), compact, " ".join(words), "_".join(words), "-".join(words)}
    return {x for x in out if x}


def build() -> dict[str, str]:
    out: dict[str, str] = {}
    for phrase in PHRASES:
        for value in forms(phrase):
            out.setdefault(f"phrase:{phrase}:form:{value}", value)

    # Only combinations explicitly motivated by the puzzle's name/prize
    # context; no arbitrary dictionary expansion.
    seeds = {v for phrase in PHRASES for v in forms(phrase)}
    for phrase in sorted(seeds):
        for context in CONTEXT:
            for sep in ("", " ", ":", "-"):
                out.setdefault(f"context:{phrase!r}{sep}{context}", phrase + sep + context)
                out.setdefault(f"context:{context}{sep}{phrase!r}", context + sep + phrase)
    return out


def main() -> int:
    assert O.selftest()
    candidates = build()
    hits = []
    direct_target = []
    valid_padding = []
    for label, candidate in candidates.items():
        lock, info = O.attempt_locks(candidate)
        door, dinfo = O.attempt_door(candidate)
        if info.get("valid_padding"):
            valid_padding.extend({"label": label, "candidate": candidate, "event": e}
                                 for e in info["valid_padding"])
        if lock or door:
            hits.append({"label": label, "candidate": candidate,
                         "lock": info, "door": dinfo})
        try:
            if O.priv_to_addrs(hashlib.sha256(candidate.encode()).digest())["uncompressed"] == O.TARGET1:
                direct_target.append({"label": label})
        except Exception:
            pass
    report = {
        "phrase_sha256": {p: hashlib.sha256(p.encode()).hexdigest() for p in PHRASES},
        "candidate_count": len(candidates),
        "valid_padding_events": len(valid_padding),
        "valid_padding_examples": valid_padding[:20],
        "hits": hits,
        "direct_target_hits": direct_target,
        "interpretation": (
            "No hit falsifies only this explicit semantic candidate family; "
            "it does not falsify a human-context final answer in general."
        ),
    }
    path = Path(__file__).with_name("semantic_hint_battery_report.json")
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in (
        "candidate_count", "valid_padding_events", "hits")}, indent=2))
    print("report:", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
