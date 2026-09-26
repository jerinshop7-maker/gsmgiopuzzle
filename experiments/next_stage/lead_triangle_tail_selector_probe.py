"""Test triangular LEAD row/column sums as direct TAIL selectors.

This is a deliberately narrow follow-up to the triangular matrix probe.  It
tests the natural ``LEAD -> TAIL`` relationship: each triangular row/column
sum supplies a direct 0- or 1-based index, optionally cumulative modulo the
TAIL length.  No permutation or fitted index map is admitted.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parents[1] / "sal_final_search"
sys.path.insert(0, str(HERE))
import dual_oracle as O  # noqa: E402
from sal_bifid import (bifid_decode, build_square, first_occurrence_key,
                       load_lead, load_tail)  # noqa: E402

OUT = Path(__file__).with_name("lead_triangle_tail_selector_probe_report.json")
PRIME_VALUES = {2, 3, 5, 7}


def is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def triangle(values: list[int], align: str) -> list[list[int]]:
    m = [[0] * 13 for _ in range(13)]
    k = 0
    for size in range(1, 14):
        start = 0 if align == "left" else 13 - size
        m[size - 1][start:start + size] = values[k:k + size]
        k += size
    return m


def apply_mask(values: list[int], mode: str) -> list[int]:
    if mode == "plain":
        return values
    if mode == "value-prime-zero":
        return [0 if x in PRIME_VALUES else x for x in values]
    if mode == "position-prime-zero":
        return [0 if is_prime(i + 1) else x for i, x in enumerate(values)]
    raise ValueError(mode)


def add_forms(out: dict[str, str], label: str, value: str) -> None:
    for suffix, candidate in (
        ("raw", value),
        ("reverse", value[::-1]),
        ("sha256", hashlib.sha256(value.encode()).hexdigest()),
    ):
        out[f"{label}/{suffix}"] = candidate


def main() -> int:
    assert O.selftest()
    lead = load_lead()
    tail = load_tail()
    decoded = bifid_decode(tail, build_square(first_occurrence_key(lead)), len(tail))
    maps = {
        "a1": {c: i + 1 for i, c in enumerate("abcdefghi")},
        "bifid9": {c: i for i, c in enumerate("dbifhcega")},
    }
    candidates: dict[str, str] = {}
    for map_name, mp in maps.items():
        base = [mp[c] for c in lead]
        for reverse in (False, True):
            oriented = base[::-1] if reverse else base
            for mask_name in ("plain", "value-prime-zero", "position-prime-zero"):
                arr = apply_mask(oriented, mask_name)
                for align in ("left", "right"):
                    m = triangle(arr, align)
                    rows = [sum(row) for row in m]
                    cols = [sum(m[r][c] for r in range(13)) for c in range(13)]
                    for axis, sums in (("rows", rows), ("cols", cols)):
                        for offset in (0, 1):
                            for cumulative in (False, True):
                                indices = []
                                total = 0
                                for s in sums:
                                    total = total + s if cumulative else s
                                    indices.append((total + offset) % len(tail))
                                for source_name, source in (
                                    ("tail-raw", tail),
                                    ("bifid", decoded),
                                    ("bifid-even256", "".join(c for c in decoded[1::2] if c not in "IO")),
                                ):
                                    selected = "".join(source[i % len(source)] for i in indices)
                                    add_forms(candidates, f"{map_name}/{reverse}/{mask_name}/{align}/{axis}/{offset}/{cumulative}/{source_name}", selected)

    records = []
    for label, candidate in candidates.items():
        lock, lock_info = O.attempt_locks(candidate)
        door, door_info = O.attempt_door(candidate)
        records.append({"label": label, "candidate": candidate,
                        "sha256": hashlib.sha256(candidate.encode()).hexdigest(),
                        "lock": lock, "door": door,
                        "lock_info": lock_info, "door_info": door_info})
    hits = [r for r in records if r["lock"] or r["door"]]
    report = {"lead_sha256": hashlib.sha256(lead.encode()).hexdigest(),
              "tail_sha256": hashlib.sha256(tail.encode()).hexdigest(),
              "candidate_count": len(records), "hits": hits, "records": records}
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"candidate_count": len(records), "hits": hits,
                      "report": str(OUT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
