"""Canonical Bifid reproduction for TAIL570 (verified 2026-09-04).

Square: 5x5, key = LEAD91 first-occurrence order (DBIFHCEGA) + remaining
alphabet (J omitted). Mode: row-column standard DECODE, period = full
length (570). Output: head BTCSEED, single Z (@97), odd positions in
{B,C,D,E}. See discoveries.md #20, dead_ends.md #6.
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load_tail() -> str:
    doc = json.loads((HERE / "sal_regions.json").read_text())
    return doc["raws"]["TAIL570"]


def load_lead() -> str:
    doc = json.loads((HERE / "sal_regions.json").read_text())
    return doc["raws"]["LEAD91"]


def first_occurrence_key(s: str) -> str:
    seen: list[str] = []
    for c in s:
        if c not in seen:
            seen.append(c)
    return "".join(seen).upper()


def build_square(key9: str) -> list[str]:
    key = list(key9.upper())
    return key + [c for c in "ABCDEFGHIKLMNOPQRSTUVWXYZ" if c not in key]


def bifid_decode(msg: str, sq: list[str], period: int) -> str:
    pos = {ch: (i // 5, i % 5) for i, ch in enumerate(sq)}
    out: list[str] = []
    for b in range(0, len(msg), period):
        blk = [c for c in msg[b:b + period].upper()]
        coords: list[int] = []
        for ch in blk:
            coords += [pos[ch][0], pos[ch][1]]
        n = len(blk)
        rows, cols = coords[:n], coords[n:]
        out.append("".join(sq[rows[i] * 5 + cols[i]] for i in range(n)))
    return "".join(out)


def main() -> int:
    lead, tail = load_lead(), load_tail()
    key = first_occurrence_key(lead)
    sq = build_square(key)
    print("key:", key)
    for r in range(5):
        print("row%d:" % r, "".join(sq[r * 5:(r + 1) * 5]))
    r = bifid_decode(tail, sq, len(tail))
    (HERE / "bifid_out.txt").write_text(r)
    print("head:", r[:16], "| BTCSEED:", r.startswith("BTCSEED"),
          "| Z:", r.count("Z"), "at", r.find("Z"),
          "| odd-set:", sorted(set(r[0::2])), "| len:", len(r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
