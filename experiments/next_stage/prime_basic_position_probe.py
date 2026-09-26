"""Test the literal source-position interpretation of ``prime basics``.

The primary README contains the 69-byte Genesis headline.  This probe limits
the interpretation to the four named prime basics (2, 3, 5, 7): replace those
1-based source positions with every permutation of ``2357``, and separately
insert the four digits at those positions.  Only direct text, reversed text,
and standard digest forms are sent to the exact lock/door oracle.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parents[1] / "sal_final_search"
sys.path.insert(0, str(HERE))
import dual_oracle as O  # noqa: E402

SOURCE = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"
PRIME_POSITIONS = (2, 3, 5, 7)  # 1-based, as stated by the clue
DIGITS = "2357"
OUT = Path(__file__).with_name("prime_basic_position_probe_report.json")


def transformed() -> dict[str, str]:
    out: dict[str, str] = {}

    def add(label: str, value: str) -> None:
        if label not in out:
            out[label] = value

    def forms(label: str, value: str) -> None:
        add(label, value)
        add(label + "/reverse", value[::-1])
        add(label + "/sha256", hashlib.sha256(value.encode()).hexdigest())
        add(label + "/md5", hashlib.md5(value.encode()).hexdigest())

    for perm in sorted(set(itertools.permutations(DIGITS))):
        digits = "".join(perm)
        chars = list(SOURCE)
        for pos, digit in zip(PRIME_POSITIONS, digits):
            chars[pos - 1] = digit
        forms("replace/" + digits, "".join(chars))

        # Insertions are kept separate from replacements because they change
        # the 69-byte object rather than mutating its established length.
        for before in (True, False):
            for offset, pos in enumerate(PRIME_POSITIONS):
                chars = list(SOURCE)
                index = pos - 1 + (0 if before else 1) + offset
                chars[index:index] = [digits[offset]]
                forms(f"insert/{'before' if before else 'after'}/{digits}/{pos}",
                      "".join(chars))
    return out


def main() -> int:
    assert O.selftest()
    candidates = transformed()
    records = []
    for label, candidate in candidates.items():
        lock, lock_info = O.attempt_locks(candidate)
        door, door_info = O.attempt_door(candidate)
        records.append({
            "label": label,
            "candidate": candidate[:160],
            "sha256": hashlib.sha256(candidate.encode()).hexdigest(),
            "lock": lock,
            "door": door,
            "lock_info": lock_info,
            "door_info": door_info,
        })
    hits = [r for r in records if r["lock"] or r["door"]]
    report = {
        "source": SOURCE,
        "prime_positions_1based": list(PRIME_POSITIONS),
        "candidate_count": len(records),
        "hits": hits,
        "records": records,
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"candidate_count": len(records), "hits": hits,
                      "report": str(OUT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
