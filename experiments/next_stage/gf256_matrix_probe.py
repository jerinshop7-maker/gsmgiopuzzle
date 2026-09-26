"""Probe the clue-backed matrix readings of the GF(256) level-3 row.

The exploratory GF(256) branch produces a particularly natural 4x16 object
at triangle level 3.  This script tests only a finite, named family around
that object: row/column serializations, their reversals, row/column sum
lists, and byte-wise XOR/sum reductions.  Each representation is finalized
with SHA-256 or double SHA-256 and checked against the exact target and the
known planted-address controls.

It deliberately does not search arbitrary strings, integer encodings, or
unbounded permutations.  The report records hashes rather than private-key
bytes so that it remains safe to publish locally.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from functools import reduce
from pathlib import Path

from coincurve import PrivateKey

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "sal_final_search"))
import dual_oracle as O  # noqa: E402
from gf256_polynomial_probe import LABELS, irreducible, points, triangle  # noqa: E402

TARGET = bytes.fromhex("a9553269572a317e39f0f518cb87c1a0ee1dbae4")
PLANTED_ADDRS = set(O.PLANTED)
HOT_ORDER = ("00", "0f", "0c", "fc", "02", "04", "1b")
ORDERS = [o for o in itertools.permutations(LABELS) if o <= tuple(reversed(o))]


def h160(key: bytes) -> bytes | None:
    try:
        pub = PrivateKey(key).public_key.format(compressed=False)
    except ValueError:
        return None
    return hashlib.new("ripemd160", hashlib.sha256(pub).digest()).digest()


def prefix(got: bytes | None, target: bytes = TARGET) -> int:
    if got is None:
        return -1
    for i, (a, b) in enumerate(zip(got, target)):
        if a != b:
            return i
    return len(target)


def orientations(m: list[list[int]]) -> dict[str, list[list[int]]]:
    """Return the eight row/column orientations of a rectangular matrix."""
    out: dict[str, list[list[int]]] = {}
    for transpose in (False, True):
        base = [row[:] for row in m]
        if transpose:
            base = [list(col) for col in zip(*base)]
        for rev_rows in (False, True):
            rows = base[::-1] if rev_rows else base
            for rev_cols in (False, True):
                named = rows
                if rev_cols:
                    named = [row[::-1] for row in rows]
                tag = f"{'T' if transpose else 'R'}{'r' if rev_rows else ''}{'c' if rev_cols else ''}"
                out[tag] = named
    return out


def flatten(m: list[list[int]]) -> bytes:
    return bytes(x & 0xFF for row in m for x in row)


def matrix_inputs(level: list[bytes]) -> dict[str, bytes]:
    m = [list(block) for block in level]
    out: dict[str, bytes] = {}

    # Serialization family: the direct row-major form is the external
    # branch's level_bytes(); column-major and reversals are its finite route
    # controls, not arbitrary block permutations.
    for name, oriented in orientations(m).items():
        out[f"serialize/{name}"] = flatten(oriented)

    row_xor = [reduce(lambda a, b: a ^ b, row, 0) for row in m]
    col_xor = [reduce(lambda a, r: a ^ r[c], m, 0) for c in range(len(m[0]))]
    row_sum = [sum(row) & 0xFF for row in m]
    col_sum = [sum(m[r][c] for r in range(len(m))) & 0xFF for c in range(len(m[0]))]

    # "matrixsumlist": retain the named row/column list, with only the
    # natural orientation/reversal controls and byte modulo-256 convention.
    for rname, rows in (("xor", row_xor), ("sum", row_sum)):
        for cname, cols in (("xor", col_xor), ("sum", col_sum)):
            for first in ("rows", "cols"):
                a, b = (rows, cols) if first == "rows" else (cols, rows)
                for ra, rb in ((False, False), (True, False), (False, True), (True, True)):
                    aa = a[::-1] if ra else a
                    bb = b[::-1] if rb else b
                    out[f"matrix/{rname}{cname}/{first}/r{int(ra)}c{int(rb)}"] = bytes(aa + bb)

    # The two reductions by themselves are also meaningful lists; they are
    # included because a list need not be concatenated with its counterpart.
    out["reduce/row_xor"] = bytes(row_xor)
    out["reduce/col_xor"] = bytes(col_xor)
    out["reduce/row_sum"] = bytes(row_sum)
    out["reduce/col_sum"] = bytes(col_sum)
    return out


def check_input(source: str, input_bytes: bytes, meta: dict) -> list[dict]:
    results = []
    for transform, key in (
        ("sha256", hashlib.sha256(input_bytes).digest()),
        ("double_sha256", hashlib.sha256(hashlib.sha256(input_bytes).digest()).digest()),
    ):
        got = h160(key)
        score = prefix(got)
        row = {**meta, "source": source, "transform": transform,
               "prefix_bytes": score, "h160": None if got is None else got.hex(),
               "input_sha256": hashlib.sha256(input_bytes).hexdigest()}
        if got == TARGET:
            row["match"] = "target_uncompressed"
        elif got is not None:
            try:
                addrs = O.priv_to_addrs(key)
            except Exception:
                addrs = {}
            planted = [addr for addr in addrs.values() if addr in PLANTED_ADDRS]
            if planted:
                row["match"] = "planted:" + ",".join(planted)
        if score >= 2:
            results.append(row)
    return results


def scan_case(args: tuple[int, tuple[str, ...]]) -> list[dict]:
    poly, order = args
    p = points(poly)
    level = triangle([p[label] for label in order])[3]
    meta = {"poly": hex(poly), "order": list(order), "level": 3}
    rows = []
    for source, blob in matrix_inputs(level).items():
        rows.extend(check_input(source, blob, meta))
    return rows


def main() -> int:
    polys = [p for p in range(0x101, 0x200, 2) if p & 1 and irreducible(p)]
    cases = []
    # First run every field for the externally reported order, then every
    # order in the AES field.  This is enough to separate field-choice from
    # ordering without multiplying the full scan by another arbitrary axis.
    tasks = [(poly, HOT_ORDER) for poly in polys if poly != 0x11B]
    tasks += [(0x11B, order) for order in ORDERS]
    with ProcessPoolExecutor(max_workers=8) as pool:
        for rows in pool.map(scan_case, tasks, chunksize=8):
            cases.extend(rows)
    exact = [r for r in cases if r.get("match")]

    cases.sort(key=lambda r: (r["prefix_bytes"], r["poly"], r["source"], r["transform"]), reverse=True)
    report = {
        "polynomial_count": len(polys),
        "aes_order_count": len(ORDERS),
        "tested_matrix_inputs": len(matrix_inputs([bytes(16)] * 4)),
        "tested_order_field_pairs": len(polys) + len(ORDERS) - 1,
        "reported_prefix_at_least_2": len(cases),
        "top": cases[:40],
        "exact_or_planted_matches": exact,
    }
    out = HERE / "gf256_matrix_probe_report.json"
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("polynomial_count", "aes_order_count",
                                              "tested_matrix_inputs", "tested_order_field_pairs",
                                              "reported_prefix_at_least_2", "exact_or_planted_matches")}, indent=2))
    print("top:", json.dumps(cases[:10], indent=2))
    print("report:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
