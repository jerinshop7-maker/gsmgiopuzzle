"""Test the author's explicit ``giveit in front`` convention on final objects.

The Phase-3 notebook says to add ``giveit`` in front of the answer, and its
saved execution records the normalized concatenation.  This probe transfers
that operation to objects literally visible on the canonical puzzle image and
to the final-page vocabulary.  It deliberately does not expand into a
dictionary or permutation search.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "sal_final_search"))
import dual_oracle as O  # noqa: E402

REPORT = Path(__file__).with_name("front_prefix_probe_report.json")


BASE_OBJECTS = {
    "image_title": "GSMG.IO 5 BTC PUZZLE CHALLENGE",
    "image_target": "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe",
    "image_url": "gsmg.io/theseedisplanted",
    "hint_final_giveaway": "very last step is a true giveaway",
    "hint_front_of_eyes": "in front of your eyes",
    "hint_secret_head": "secret in my head",
    "hint_share_planet": "share with the planet",
    "hint_understand": "for those who can understand what I meant",
    "hint_close_friends": "close friends",
    "hint_best_chance": "best chance of solving it",
    "hint_hardest_done": "hardest part is done",
    "hint_same_day": "same day",
    "hint_theory_everything": "theory of everything",
    "hint_puzzle_talks": "the puzzle talks for me",
    "hint_not_actual_prize": "the 5 btc was never the actual prize",
    "hint_new_year": "Happy new year! Make the best of everything. Oh, and here's a tiny hint <3.",
    "matrixsumlist": "matrixsumlist",
    "lastwordsbeforearchichoice": "lastwordsbeforearchichoice",
    "thispassword": "thispassword",
    "yourlastcommand": "yourlastcommand",
    "secondanswer": "secondanswer",
}


def normalizations(value: str) -> list[tuple[str, str]]:
    words = re.findall(r"[A-Za-z0-9]+", value)
    compact = "".join(words).lower()
    spaced = " ".join(words).lower()
    return [("exact", value), ("lower", value.lower()),
            ("compact", compact), ("spaced", spaced)]


def main() -> int:
    assert O.selftest()
    # Known-answer witness for the historical convention: the Phase-3 answer
    # was normalized to this exact concatenation and funded a planted address.
    witness = "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"
    assert O.priv_to_addrs(hashlib.sha256(witness.encode()).digest())["compressed"] == (
        "1K23RS1y2fnuZRkhw5nUpFr5Jk5WN11Zeq"
    )
    candidates: dict[str, str] = {}
    for name, obj in BASE_OBJECTS.items():
        for form, value in normalizations(obj):
            for prefix in ("giveit", "give it", "giveit "):
                # Keep the operation explicit: prefix only, never suffix or
                # an arbitrary insertion point.
                candidate = prefix + value
                candidates.setdefault(f"{name}:{form}:prefix={prefix!r}", candidate)

    hits = []
    target_hashes = []
    valid_padding = []
    for label, candidate in candidates.items():
        lock_hit, lock_info = O.attempt_locks(candidate)
        door_hit, door_info = O.attempt_door(candidate)
        digest = hashlib.sha256(candidate.encode()).digest()
        addresses = O.priv_to_addrs(digest)
        if addresses["uncompressed"] == O.TARGET1:
            target_hashes.append({"label": label})
        if lock_info.get("valid_padding"):
            valid_padding.extend({"label": label, "event": event}
                                 for event in lock_info["valid_padding"])
        if lock_hit or door_hit:
            hits.append({"label": label, "candidate": candidate,
                         "lock": lock_info, "door": door_info})

    report = {
        "operation": "prefix giveit / give it",
        "base_object_count": len(BASE_OBJECTS),
        "candidate_count": len(candidates),
        "sha256_target_hits": target_hashes,
        "oracle_hits": hits,
        "valid_padding_events": len(valid_padding),
        "valid_padding_examples": valid_padding[:20],
        "status": "NO_MATCH" if not hits and not target_hashes else "MATCH",
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in (
        "operation", "base_object_count", "candidate_count",
        "sha256_target_hits", "oracle_hits", "valid_padding_events", "status")},
        indent=2))
    print("report:", REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
