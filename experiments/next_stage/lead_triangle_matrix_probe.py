"""Test the exact triangular interpretation of the 91-symbol lead stream.

LEAD91 has length 91 = 1 + ... + 13.  This is the smallest clue-backed
``matrixsumlist`` shape that was not covered by the earlier rectangular
7x13 sweep.  The probe uses only the published bifid9/a1 value maps,
orientation/alignment, prime-value/prime-position zeroing, and row/column
sums.  Every rendered result goes through the exact two-lock and planted-door
oracles.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parents[1] / "sal_final_search"
sys.path.insert(0, str(HERE))
import dual_oracle as O  # noqa: E402
from sal_bifid import load_lead  # noqa: E402

OUT = Path(__file__).with_name("lead_triangle_matrix_probe_report.json")
PRIME_VALUES = {2, 3, 5, 7}


def is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def matrix_values(values: list[int], align: str) -> list[list[int]]:
    m = [[0] * 13 for _ in range(13)]
    k = 0
    for row_len in range(1, 14):
        start = 0 if align == "left" else 13 - row_len
        m[row_len - 1][start:start + row_len] = values[k:k + row_len]
        k += row_len
    assert k == 91
    return m


def masked(values: list[int], mode: str) -> list[int]:
    if mode == "plain":
        return values
    if mode == "value-prime-zero":
        return [0 if x in PRIME_VALUES else x for x in values]
    if mode == "value-nonprime-zero":
        return [0 if x not in PRIME_VALUES else x for x in values]
    if mode == "position-prime-zero":
        return [0 if is_prime(i + 1) else x for i, x in enumerate(values)]
    if mode == "position-nonprime-zero":
        return [0 if not is_prime(i + 1) else x for i, x in enumerate(values)]
    raise ValueError(mode)


def forms(label: str, values: list[int]) -> dict[str, str]:
    out: dict[str, str] = {}
    strings = {
        "raw": "".join(str(x) for x in values),
        "mod10": "".join(str(x % 10) for x in values),
        "csv": ",".join(str(x) for x in values),
        "ascii": "".join(chr(48 + (x % 10)) for x in values),
    }
    for kind, value in strings.items():
        out[f"{label}/{kind}"] = value
        out[f"{label}/{kind}/reverse"] = value[::-1]
        out[f"{label}/{kind}/sha256"] = hashlib.sha256(value.encode()).hexdigest()
    return out


def main() -> int:
    assert O.selftest()
    raw = load_lead()
    maps = {
        "a1": {c: i + 1 for i, c in enumerate("abcdefghi")},
        "bifid9": {c: i for i, c in enumerate("dbifhcega")},
    }
    candidates: dict[str, str] = {}
    for map_name, mp in maps.items():
        base = [mp[c] for c in raw]
        for reverse in (False, True):
            oriented = base[::-1] if reverse else base
            for mask_name in ("plain", "value-prime-zero", "value-nonprime-zero",
                              "position-prime-zero", "position-nonprime-zero"):
                arr = masked(oriented, mask_name)
                for align in ("left", "right"):
                    m = matrix_values(arr, align)
                    rows = [sum(row) for row in m]
                    cols = [sum(m[r][c] for r in range(13)) for c in range(13)]
                    vectors = {
                        "rows": rows,
                        "cols": cols,
                        "rows-cols": [a - b for a, b in zip(rows, cols)],
                        "cols-rows": [b - a for a, b in zip(rows, cols)],
                        "rows+cols": rows + cols,
                        "cols+rows": cols + rows,
                    }
                    for op, vector in vectors.items():
                        candidates.update(forms(
                            f"{map_name}/{reverse}/{mask_name}/{align}/{op}", vector
                        ))

    records = []
    for label, candidate in candidates.items():
        lock, lock_info = O.attempt_locks(candidate)
        door, door_info = O.attempt_door(candidate)
        records.append({"label": label, "candidate": candidate[:160],
                        "sha256": hashlib.sha256(candidate.encode()).hexdigest(),
                        "lock": lock, "door": door,
                        "lock_info": lock_info, "door_info": door_info})
    hits = [r for r in records if r["lock"] or r["door"]]
    report = {"lead_sha256": hashlib.sha256(raw.encode()).hexdigest(),
              "length": len(raw), "candidate_count": len(records),
              "hits": hits, "records": records}
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"candidate_count": len(records), "hits": hits,
                      "report": str(OUT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
