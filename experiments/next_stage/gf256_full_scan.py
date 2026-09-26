"""Complete finite GF(256)-interpolation/XOR-triangle scan.

This extends the external near-miss branch over all 30 irreducible degree-8
binary polynomials, all 2520 orderings modulo reversal, every triangle level,
and SHA-256/double-SHA-256.  The target is the known uncompressed P2PKH
hash160, so no appearance or padding heuristic is used.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import itertools
import json
from pathlib import Path

from coincurve import PrivateKey

from gf256_polynomial_probe import LABELS, HOT_ORDER, irreducible, points, triangle

TARGET = bytes.fromhex("a9553269572a317e39f0f518cb87c1a0ee1dbae4")
ORDERS = [o for o in itertools.permutations(LABELS) if o <= tuple(reversed(o))]


def h160(key: bytes) -> bytes | None:
    try:
        pub = PrivateKey(key).public_key.format(compressed=False)
    except ValueError:
        return None
    return hashlib.new("ripemd160", hashlib.sha256(pub).digest()).digest()


def common_prefix(a: bytes | None) -> int:
    if a is None:
        return -1
    n = 0
    for x, y in zip(a, TARGET):
        if x != y:
            break
        n += 1
    return n


def scan_poly(poly: int) -> dict:
    p = points(poly)
    best = {"prefix_bytes": -1}
    matches = []
    for order in ORDERS:
        levels = triangle([p[label] for label in order])
        for level_index, level in enumerate(levels):
            raw = b"".join(level)
            sha = hashlib.sha256(raw).digest()
            for transform, key in (("sha256", sha),
                                   ("double_sha256", hashlib.sha256(sha).digest())):
                got = h160(key)
                score = common_prefix(got)
                row = {"poly": hex(poly), "order": order, "level": level_index,
                       "transform": transform, "prefix_bytes": score,
                       "h160": None if got is None else got.hex(),
                       "candidate": key.hex()}
                if score > best["prefix_bytes"]:
                    best = row
                if got == TARGET:
                    matches.append(row)
    return {"poly": hex(poly), "best": best, "matches": matches}


def main() -> int:
    polys = [p for p in range(0x101, 0x200, 2) if p & 1 and irreducible(p)]
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(scan_poly, polys))
    results.sort(key=lambda x: x["best"]["prefix_bytes"], reverse=True)
    matches = [m for r in results for m in r["matches"]]
    report = {"polynomial_count": len(polys), "order_count": len(ORDERS),
              "levels": 7, "hash_forms": 2, "results": results,
              "exact_matches": matches}
    out = Path(__file__).with_name("gf256_full_scan_report.json")
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"polynomial_count": len(polys), "order_count": len(ORDERS),
                      "tested_candidates": len(polys) * len(ORDERS) * 7 * 2,
                      "top": [r["best"] for r in results[:10]],
                      "exact_matches": matches}, indent=2))
    print("report:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
