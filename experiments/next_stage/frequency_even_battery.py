"""Reproduce the bounded frequency/string family for even256."""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "sal_final_search"))
import dual_oracle as O  # noqa: E402
from sal_bifid import bifid_decode, build_square, first_occurrence_key, load_lead, load_tail  # noqa: E402

ALPHA = "ABCDEFGHKLMNPQRSTUVWXYZ"


def add(out: dict[str, str], label: str, value: str) -> None:
    if value and len(value) <= 10000:
        out.setdefault(label, value)


def main() -> int:
    assert O.selftest()
    out = bifid_decode(load_tail(), build_square(first_occurrence_key(load_lead())), 570)
    even = "".join(c for c in out[1::2] if c not in "IO")
    counts = Counter(even)
    first_order = {c: i for i, c in enumerate(dict.fromkeys(even))}
    candidates: dict[str, str] = {}

    def representations(name: str, value: str) -> None:
        add(candidates, name, value)
        add(candidates, name + "/reverse", value[::-1])
        add(candidates, name + "/sha256", hashlib.sha256(value.encode()).hexdigest())
        add(candidates, name + "/md5", hashlib.md5(value.encode()).hexdigest())

    vectors = [counts[c] for c in ALPHA]
    for name, vals in (("counts-alpha", vectors), ("counts-alpha-rev", vectors[::-1])):
        for sep, text in ((",", ",".join(map(str, vals))), ("", "".join(map(str, vals)))):
            representations(f"{name}/{sep or 'tight'}", text)
        for width in (1, 2, 4):
            for endian in ("big", "little"):
                b = b"".join(n.to_bytes(width, endian) for n in vals)
                representations(f"{name}/{width}-{endian}-hex", b.hex())
                representations(f"{name}/{width}-{endian}-latin", b.decode("latin1"))

    orders = {
        "alpha": list(ALPHA),
        "count-asc-alpha": sorted(ALPHA, key=lambda c: (counts[c], c)),
        "count-desc-alpha": sorted(ALPHA, key=lambda c: (-counts[c], c)),
        "count-asc-first": sorted(ALPHA, key=lambda c: (counts[c], first_order[c])),
        "count-desc-first": sorted(ALPHA, key=lambda c: (-counts[c], first_order[c])),
    }
    for name, order in orders.items():
        representations(f"alphabet/{name}", "".join(order))
        representations(f"expanded/{name}", "".join(c * counts[c] for c in order))
        rank = {c: i for i, c in enumerate(order)}
        representations(f"rank/{name}", "".join(ALPHA[rank[c]] for c in even))
        representations(f"rank-lower/{name}", "".join(ALPHA[rank[c]].lower() for c in even))

    # Selection strings at the natural count boundaries, with complement and reverse.
    levels = sorted(set(counts.values()))
    for level in levels:
        for cmp_name, keep in (("ge", lambda n: n >= level), ("gt", lambda n: n > level),
                               ("le", lambda n: n <= level), ("lt", lambda n: n < level)):
            selected = "".join(c for c in ALPHA if keep(counts[c]))
            representations(f"selected/{cmp_name}/{level}", selected)
            representations(f"selected/{cmp_name}/{level}/stream", "".join(c for c in even if c in selected))

    # Count-derived modular/XOR streams preserve the original positions.
    for op_name, vals in (
        ("count-mod", [counts[c] % 23 for c in even]),
        ("count-xor", [((ord(c) - 65) ^ counts[c]) % 23 for c in even]),
        ("rank-xor", [((ord(c) - 65) ^ i) % 23 for i, c in enumerate(even)]),
    ):
        for mode, text in (
            ("letters", "".join(ALPHA[n] for n in vals)),
            ("decimal", ",".join(map(str, vals))),
            ("hex", bytes(vals).hex()),
        ):
            representations(f"{op_name}/{mode}", text)

    hits = []
    padding = 0
    for label, candidate in candidates.items():
        ok_lock, lock_info = O.attempt_locks(candidate)
        ok_door, door_info = O.attempt_door(candidate)
        padding += len(lock_info.get("valid_padding", []))
        if ok_lock or ok_door:
            hits.append({"label": label, "candidate": candidate, "lock": lock_info, "door": door_info})
    report = {"candidate_count": len(candidates), "valid_padding_events": padding, "hits": hits,
              "even256_sha256": hashlib.sha256(even.encode()).hexdigest()}
    path = HERE / "frequency_even_battery_report.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    print("report:", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
