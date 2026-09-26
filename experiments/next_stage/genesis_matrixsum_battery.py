"""Clue-bounded Genesis 3x23 matrix-sum battery.

The source-code literal is exactly 69 bytes = 3x23.  This runner tests the
literal operation named by the final page, ``matrixsumlist``, before adding a
small, explicit family for the independently stated prime/zero/reinsert and
yellow/blue operations.  It does not search arbitrary matrix routes.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sal_final_search"))
import dual_oracle as O  # noqa: E402


GENESIS_HEX = (
    "736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E616843"
    "20393030322F6E614A2F33302073656D695420656854"
)
SOURCE = bytes.fromhex(GENESIS_HEX).decode()[::-1]
assert len(SOURCE) == 69

PRIME_COLS = {p - 1 for p in (2, 3, 5, 7, 11, 13, 17, 19, 23)}
BY = "111101110011110110010010"


def emit(out: dict[str, str], label: str, value: str) -> None:
    if value:
        out.setdefault(label, value)


def enc(values: list[int]) -> dict[str, str]:
    # The first two are the literal list renderings; the rest are transparent
    # byte/letter renderings, not wordlist guesses.
    return {
        "digits": "".join(str(v) for v in values),
        "csv": ",".join(str(v) for v in values),
        "hex": bytes(v & 255 for v in values).hex(),
        "bytes": bytes(v & 255 for v in values).decode("latin1"),
        "a1z26": "".join(chr(96 + (v - 1) % 26 + 1) for v in values),
    }


def sums(matrix: list[list[int]]) -> dict[str, list[int]]:
    rows = [sum(row) for row in matrix]
    cols = [sum(matrix[r][c] for r in range(3)) for c in range(23)]
    return {
        "rows": rows,
        "cols": cols,
        "rows+cols": rows + cols,
        "cols+rows": cols + rows,
        "rows-cols-head": rows + [cols[i] - cols[-1 - i] for i in range(3)],
        "col-pair-diff": [cols[i] - cols[-1 - i] for i in range(12)],
        "col-pair-sum": [cols[i] + cols[-1 - i] for i in range(12)],
    }


def add_sum_forms(out: dict[str, str], name: str, matrix: list[list[int]]) -> None:
    for sum_name, values in sums(matrix).items():
        for form, value in enc(values).items():
            emit(out, f"{name}/{sum_name}/{form}", value)
            emit(out, f"{name}/{sum_name}/{form}/reverse", value[::-1])


def build() -> dict[str, str]:
    rect = [[ord(SOURCE[r * 23 + c]) for c in range(23)] for r in range(3)]
    out: dict[str, str] = {}

    # Direct matrixsumlist readings on the source-code byte matrix.
    add_sum_forms(out, "ascii", rect)
    add_sum_forms(out, "ascii/zero-prime-cols", [
        [v if c not in PRIME_COLS else 0 for c, v in enumerate(row)]
        for row in rect
    ])
    add_sum_forms(out, "ascii/zero-nonprime-cols", [
        [v if c in PRIME_COLS else 0 for c, v in enumerate(row)]
        for row in rect
    ])

    # A second natural numeric reading: alphabetic characters as A1Z26 and
    # punctuation/space as zero, then the same matrix-sum operation.
    a1 = [[(ord(ch.lower()) - 96) if ch.isalpha() else 0
           for ch in SOURCE[r * 23:(r + 1) * 23]] for r in range(3)]
    add_sum_forms(out, "a1z26", a1)

    # Reinsert the prime basics into the 1-based prime columns.  The only
    # free choice retained is the permutation of the four explicitly named
    # values, repeated across the nine prime columns.
    prime_positions = sorted(PRIME_COLS)
    for perm in itertools.permutations((2, 3, 5, 7)):
        for orientation in ("replace", "add"):
            m = [row[:] for row in rect]
            for r in range(3):
                for j, c in enumerate(prime_positions):
                    p = perm[(j + r) % 4]
                    m[r][c] = p if orientation == "replace" else m[r][c] + p
            add_sum_forms(out, f"prime-{orientation}-{''.join(map(str, perm))}", m)

    # The proven 24-cell B/Y frame has 24 bits while the source has 69 bytes.
    # Test only the two obvious repeated-mask alignments as a selector before
    # summing: frame bits repeat over the flattened 3x23 object, or over rows.
    frame = [int(x) for x in BY]
    flat = [v for row in rect for v in row]
    for offset in range(8):
        selected = [v if frame[(i + offset) % 24] else 0 for i, v in enumerate(flat)]
        m = [selected[r * 23:(r + 1) * 23] for r in range(3)]
        add_sum_forms(out, f"by-repeat-offset-{offset}", m)

    # The older secondary image notes mention the pair 490/497 without a
    # reproducible derivation.  Test that exact object only as a diagnostic,
    # including the pair found in the prime-basic ASCII column-pair sums.
    for label, values in {
        "reported-b3-forward": [490, 497],
        "reported-b3-reverse": [497, 490],
    }.items():
        for form, value in enc(values).items():
            emit(out, f"{label}/{form}", value)

    # Remove exact duplicate values while retaining first-label provenance.
    return out


def main() -> int:
    assert O.selftest()
    candidates = build()
    hits = []
    valid = 0
    for label, candidate in candidates.items():
        lock, info = O.attempt_locks(candidate)
        door, dinfo = O.attempt_door(candidate)
        valid += len(info.get("valid_padding", []))
        if lock or door:
            hits.append({"label": label, "candidate": candidate, "lock": info, "door": dinfo})
    report = {
        "source": SOURCE,
        "source_sha256": hashlib.sha256(SOURCE.encode()).hexdigest(),
        "prime_columns_1based": [2, 3, 5, 7, 11, 13, 17, 19, 23],
        "candidate_count": len(candidates),
        "valid_padding_events": valid,
        "hits": hits,
    }
    path = Path(__file__).with_name("genesis_matrixsum_battery_report.json")
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("candidate_count", "valid_padding_events", "hits")}, indent=2))
    print("report:", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
