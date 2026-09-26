"""Small exact-oracle test of the two 6+5 southeast B/Y chains.

The image audit identified two long parallel down-right diagonals among the
24 B/Y frame cells.  This tests only their direct color/bit readings and
transparent encodings; it is not a general image-route sweep.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import extract_grid as G  # noqa: E402
sys.path.insert(0, str(ROOT / "experiments" / "sal_final_search"))
import dual_oracle as O  # noqa: E402

REPORT = HERE / "by_diagonal_chain_battery_report.json"


def add(cands: dict[str, str], label: str, value: str) -> None:
    if value:
        cands.setdefault(label, value)


def main() -> int:
    assert O.selftest()
    M = G.extract_matrix(G.load_pixels(ROOT / "raw/github/puzzlehunt-gsmgio-5btc-puzzle/working/puzzle.png"))
    # The image audit's two contiguous down-right B/Y components, lengths 6+5.
    # A component means every next cell is exactly one row and one column away.
    points = {(r, c): M[r][c] for r in range(14) for c in range(14)
             if M[r][c] in "BY"}
    chains = []
    for start in sorted(points):
        if (start[0] - 1, start[1] - 1) in points:
            continue
        cur, text = start, []
        while cur in points:
            text.append(points[cur])
            cur = (cur[0] + 1, cur[1] + 1)
        if len(text) >= 2:
            chains.append("".join(text))
    assert sorted(chains, key=len, reverse=True)[:2] == ["BYYBYB", "YYYYB"]
    lines = {0: "BYYBYB", 1: "YYYYB"}

    # Proven frame relation: B/Y positions are the last bit of URL bytes.
    # Carry the same chain coordinates through the spiral to test the
    # corresponding URL characters as a selector output.
    n = 14
    seen, coords = set(), []
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    x = y = d = 0
    for _ in range(n * n):
        coords.append((y, x))
        seen.add((y, x))
        nx, ny = x + dirs[d][0], y + dirs[d][1]
        if not (0 <= nx < n and 0 <= ny < n and (ny, nx) not in seen):
            d = (d + 1) % 4
            nx, ny = x + dirs[d][0], y + dirs[d][1]
        x, y = nx, ny
    url = "gsmg.io/theseedisplanted"
    chain_coords = {
        0: [(8, 5), (9, 6), (10, 7), (11, 8), (12, 9), (13, 10)],
        1: [(4, 9), (5, 10), (6, 11), (7, 12), (8, 13)],
    }
    url_selected = {}
    for k, ps in chain_coords.items():
        chars = []
        for p in ps:
            i = coords.index(p)
            assert i >= 7 and (i - 7) % 8 == 0
            chars.append(url[(i - 7) // 8])
        url_selected[k] = "".join(chars)
    assert url_selected == {0: "enpetm", 1: "tldhg"}

    candidates: dict[str, str] = {}
    for perm in itertools.permutations((0, 1)):
        for polarity in ("BY", "YB"):
            bits = ["".join("1" if ch == polarity[0] else "0" for ch in lines[d])
                    for d in perm]
            colors = [lines[d].translate(str.maketrans("BY", polarity)) for d in perm]
            for order_name, b, c in (("concat", "".join(bits), "".join(colors)),
                                     ("separate", bits[0], colors[0]),
                                     ("separate2", bits[1], colors[1])):
                for rev in (False, True):
                    bb = b[::-1] if rev else b
                    cc = c[::-1] if rev else c
                    prefix = f"d{perm[0]}_{perm[1]}/{polarity}/{order_name}/{rev}"
                    add(candidates, prefix + "/bits", bb)
                    add(candidates, prefix + "/colors", cc)
                    n = int(bb, 2)
                    for form, value in (("decimal", str(n)),
                                        ("hex", format(n, "x")),
                                        ("hex0x", "0x" + format(n, "x")),
                                        ("ascii_if8", chr(n) if 0 <= n < 128 else ""),
                                        ("sha256_bits", hashlib.sha256(bb.encode()).hexdigest()),
                                        ("sha256_bytes", hashlib.sha256(bytes([n])).hexdigest()
                                         if n < 256 else "")):
                        add(candidates, prefix + "/" + form, value)

    for perm in itertools.permutations((0, 1)):
        for rev in (False, True):
            vals = [url_selected[d][::-1] if rev else url_selected[d] for d in perm]
            for kind, value in (("first", vals[0]), ("second", vals[1]),
                                ("concat", "".join(vals))):
                prefix = f"url/{perm[0]}_{perm[1]}/{rev}/{kind}"
                add(candidates, prefix, value)
                add(candidates, prefix + "/sha256", hashlib.sha256(value.encode()).hexdigest())

    hits, vpads, doors = [], 0, []
    for label, candidate in candidates.items():
        hit, info = O.attempt_locks(candidate)
        if info.get("valid_padding"):
            vpads += len(info["valid_padding"])
        if hit:
            hits.append({"label": label, "candidate": candidate, "info": info})
        dhit, dinfo = O.attempt_door(candidate)
        if dhit:
            doors.append({"label": label, "candidate": candidate, "info": dinfo})

    report = {"diagonals": {str(k): v for k, v in lines.items()},
              "candidate_count": len(candidates), "valid_padding_events": vpads,
              "target_matches": hits, "third_door_matches": doors}
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    print("report:", REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
