"""Forensic structural report: measure, don't sweep.

Reads only primary bytes + frozen region map. Produces SALPHASEION STRUCTURAL
REPORT: natural matrices with full sum diagnostics, complement/pair invariant
scores, cross-stream correspondence, yellow/blue operator tests, zeroing
pipeline effect sizes, Architect positional extraction, two-lock comparison,
third-door address forensics, page-literal inventory.

Anomaly score = constancy (few distinct values / low entropy) of a derived
sequence. A real designed invariant shows up as an outlier. No password
sweeps, no decrypts (except a single pipeline string IF one emerges
deterministically — none does; see REPORT).
"""
from __future__ import annotations
import base64
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REGIONS = json.loads((HERE / "sal_regions.json").read_text())["raws"]
OUT = HERE / "sal_structure_report.json"

BIFID9 = {'d': 0, 'b': 1, 'i': 2, 'f': 3, 'h': 4, 'c': 5, 'e': 6, 'g': 7, 'a': 8}
A1 = {c: i + 1 for i, c in enumerate("abcdefghi")}
R14 = [6, 10, 8, 7, 6, 6, 5, 4, 9, 9, 7, 8, 7, 9]
C14 = [8, 10, 8, 10, 8, 7, 3, 6, 7, 5, 9, 6, 6, 8]


def entropy(vals) -> float:
    n = len(vals)
    if n == 0:
        return 0.0
    return -sum(c / n * math.log2(c / n) for c in Counter(vals).values())


def constancy(vals) -> dict:
    return {"n": len(vals), "distinct": len(set(vals)),
            "entropy": round(entropy(vals), 3), "values": vals if len(vals) <= 32 else vals[:32]}


def matrix_report(name: str, digits: list[int], rows: int, cols: int, mapname: str) -> dict:
    M = [digits[r * cols:(r + 1) * cols] for r in range(rows)]
    rs = [sum(r) for r in M]
    cs = [sum(M[r][c] for r in range(rows)) for c in range(cols)]
    rep: dict = {"stream": name, "map": mapname, "shape": f"{rows}x{cols}",
                 "dist": dict(sorted(Counter(digits).items())),
                 "rows": constancy(rs), "cols": constancy(cs)}
    if rows == cols:
        rep["diag"] = constancy([sum(M[i][i] for i in range(rows)),
                                 sum(M[i][rows - 1 - i] for i in range(rows))])
    # pair partitions (yin/yang candidates): top/bottom, left/right, rot180, checkerboard
    parts: dict = {}
    parts["top_bottom_sum"] = [a + b for a, b in zip(rs[:rows // 2], rs[::-1][:rows // 2])]
    parts["top_bottom_diff"] = [a - b for a, b in zip(rs[:rows // 2], rs[::-1][:rows // 2])]
    parts["left_right_sum"] = [a + b for a, b in zip(cs[:cols // 2], cs[::-1][:cols // 2])]
    parts["left_right_diff"] = [a - b for a, b in zip(cs[:cols // 2], cs[::-1][:cols // 2])]
    flat = digits
    parts["rot180_sum"] = [a + b for a, b in zip(flat[:len(flat) // 2], flat[::-1][:len(flat) // 2])]
    parts["rot180_xor"] = [a ^ b for a, b in zip(flat[:len(flat) // 2], flat[::-1][:len(flat) // 2])]
    # complement x -> 9-x (bifid9) pairing with self
    parts["c9_sum"] = [a + (9 - a) for a in flat[:8]]  # trivially 9; control
    black = sum(flat[::2])
    white = sum(flat[1::2])
    parts["checker_sum"] = [black, white]
    rep["partitions"] = {k: constancy(v) for k, v in parts.items()}
    # mod projections of sums
    rep["mods"] = {f"rows_mod{m}": constancy([x % m for x in rs]) for m in (2, 9, 10, 13, 26)}
    return rep


def main() -> int:
    rep: dict = {"matrices": [], "cross": {}, "yellow_blue": {}, "zeroing": {},
                 "architect": {}, "locks": {}, "door": {}, "page": {}}
    # ---- natural matrices ----
    jobs = [("LEAD91", REGIONS["LEAD91"], [(7, 13), (13, 7)]),
            ("TAIL570", REGIONS["TAIL570"], [(19, 30), (30, 19), (15, 38), (38, 15), (10, 57), (57, 10)])]
    for sname, s, shapes in jobs:
        for mapname, mp in (("bifid9", BIFID9), ("a1", A1)):
            digits = [mp[c] for c in s]
            for (r, c) in shapes:
                rep["matrices"].append(matrix_report(sname, digits, r, c, mapname))
    # ---- 14x14 grid check from copied public grid (secondary) ----
    PUZZLE_GRID = [
        "00110100101100", "11110011101011", "11011101001001", "01101000011101",
        "01100011000110", "10011000100011", "10011100010000", "11100000001000",
        "00011101111101", "11111100110001", "11010000011011", "11110010101100",
        "01011101000110", "01101101101011",
    ]
    grid = [[int(ch) for ch in row] for row in PUZZLE_GRID]
    grs = [sum(r) for r in grid]
    gcs = [sum(grid[r][c] for r in range(14)) for c in range(14)]
    rep["grid14"] = {"rows": grs, "cols": gcs,
                     "matches_R14": grs == R14, "matches_C14": gcs == C14}
    # ---- cross-stream ----
    for mapname, mp in (("bifid9", BIFID9), ("a1", A1)):
        d91 = [mp[c] for c in REGIONS["LEAD91"]]
        d570 = [mp[c] for c in REGIONS["TAIL570"]]
        mid = [0 if c == "a" else 1 for c in REGIONS["MID104"]]
        rep["cross"][mapname] = {
            "mean91": round(sum(d91) / len(d91), 4), "mean570": round(sum(d570) / len(d570), 4),
            "dist91": dict(sorted(Counter(d91).items())), "dist570": dict(sorted(Counter(d570).items())),
            "mid_mean": round(sum(mid) / len(mid), 4),
            "corr91_first570": "n/a (lengths differ; distributions compared instead)"}
    # ---- yellow/blue operator ----
    # known signature: 24 cells at spiral positions 7,15,...,191; 15 blue(=1), 9 yellow(=0)
    d91b = [BIFID9[c] for c in REGIONS["LEAD91"]]
    d570b = [BIFID9[c] for c in REGIONS["TAIL570"]]
    for opname, fn in (("odd", lambda v: v % 2), ("primeval", lambda v: 1 if v in (2, 3, 5, 7) else 0),
                       ("ge5", lambda v: 1 if v >= 5 else 0), ("ge4", lambda v: 1 if v >= 4 else 0)):
        for sname, arr in (("LEAD91", d91b), ("TAIL570", d570b)):
            bits = [fn(v) for v in arr]
            rep["yellow_blue"][f"{sname}:{opname}"] = {
                "ones": sum(bits), "zeros": len(bits) - sum(bits),
                "first24_ones": sum(bits[:24]),
                "matches_15_9": sorted([sum(bits[:24]), 24 - sum(bits[:24])]) == [9, 15]}
    # ---- zeroing pipeline effect sizes ----
    for sname in ("LEAD91", "TAIL570"):
        arr = [BIFID9[c] for c in REGIONS[sname]]
        n = len(arr)
        pos = {i + 1 for i in range(n) if False}
        import sys as _s
        def primeset(m):
            is_p = bytearray(b"\x01") * (m + 1)
            is_p[0:2] = b"\x00\x00"
            for i in range(2, int(m ** 0.5) + 1):
                if is_p[i]:
                    is_p[i * i:m + 1:i] = b"\x00" * ((m - i * i) // i + 1)
            return {i for i, v in enumerate(is_p) if v}
        pf = primeset(n + 1)
        p2357 = {2, 3, 5, 7}
        rep["zeroing"][sname] = {
            "n": n,
            "primeval_kept": sum(1 for v in arr if v in (2, 3, 5, 7)),
            "pos_Pfull_idx1": sum(1 for i in range(n) if i + 1 in pf),
            "pos_P2357_idx0": sum(1 for i in range(n) if i in p2357),
            "pos_P2357_idx1": sum(1 for i in range(n) if i + 1 in p2357)}
    # ---- Architect positional extraction (exact phase3.2 head) ----
    b = (ROOT / "raw/github/Naddiseo-gsmgio-5btc-puzzle/working/phase3-assets/phase3.2.txt").read_bytes()
    head = b.split(b"\r\n\r\n")[0].decode("utf-8", "replace")
    sents = re.split(r"(?<=[.!?])\s+", head)
    rep["architect"]["n_sentences"] = len(sents)
    rep["architect"]["last_words"] = [s.split()[-1] if s.split() else "" for s in sents]
    rep["architect"]["second_last"] = [s.split()[-2] if len(s.split()) > 1 else "" for s in sents]
    rep["architect"]["first_letters"] = ["".join(w[0] for w in s.split()) for s in sents]
    rep["architect"]["last_letters"] = ["".join(w[-1] for w in s.split()) for s in sents]
    rep["architect"]["word_lengths_all"] = [len(w) for s in sents for w in s.split()][:60]
    # checkerboard riddle sentence (last words before p32 blob)
    txt = b.decode("latin1")
    i = txt.find("Raising the stakes")
    riddle = txt[i:txt.find("U2Fsd", i)].strip() if i >= 0 else ""
    rep["architect"]["riddle"] = riddle
    rep["architect"]["riddle_last3"] = riddle.split()[-3:]
    # ---- locks ----
    small_b64 = REGIONS["R3B64A_63"] + "z" + REGIONS["R4B64B_64"]
    p32_b64 = ("U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46z"
               "gKlIi8aaqY5gpJPPEzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4")
    small = base64.b64decode(small_b64)
    p32 = base64.b64decode(p32_b64)
    rep["locks"]["small"] = {"salt": small[8:16].hex(), "ct_len": len(small) - 16}
    rep["locks"]["p32"] = {"salt": p32[8:16].hex(), "ct_len": len(p32) - 16}
    rep["locks"]["salt_xor"] = bytes(a ^ c for a, c in zip(small[8:16], p32[8:16])).hex()
    rep["locks"]["ct_xor_head"] = bytes(a ^ c for a, c in zip(small[16:48], p32[16:48])).hex()
    for lname, blob in (("small", small[16:]), ("p32", p32[16:])):
        blocks = [blob[i:i + 16] for i in range(0, len(blob), 16)]
        rep["locks"][lname]["repeated_blocks"] = len(blocks) - len(set(blocks))
        rep["locks"][lname]["byte_entropy"] = round(entropy(list(blob)), 3)
        rep["locks"][lname]["first_block"] = blocks[0].hex()
        rep["locks"][lname]["last_block"] = blocks[-1].hex()
    # ---- third door forensics ----
    import base58 as b58
    raw = b58.b58decode("1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9")
    payload, cksum = raw[:-4], raw[-4:]
    expect = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    rep["door"]["version"] = payload[0]
    rep["door"]["hash160"] = payload[1:].hex()
    rep["door"]["checksum_valid"] = (cksum == expect)
    rep["door"]["vanity_NULY"] = "NULY"
    planted = {"1AD2wfwXukZ1kUAy848hTQQ72aSBZPB75r": "flower", "1Jqq37KkZEt4F3Dt6qXdtyiMEFBBdawbkJ": "causality",
               "148XH2YBmLr4oAJXQcG84FpNYoBmqnVPHQ": "url-raw", "13HGhjkmKUkP8sk9k63BLmhkxRjy7uK4Rp": "url-rev"}
    hits = {}
    for addr in planted:
        hits[addr] = b58.b58decode(addr)[1:-4].hex()
    rep["door"]["planted_hash160s"] = hits
    rep["door"]["hash160_reused"] = rep["door"]["hash160"] in hits.values()
    # ---- page literals ----
    html = (ROOT / "raw/web/live/salphaseion/response.bin").read_bytes().decode()
    rep["page"]["h1"] = re.findall(r"<h1>(.*?)</h1>", html)
    rep["page"]["textarea_style"] = re.findall(r"<textarea style=\"([^\"]+)\">", html)
    rep["page"]["cosmic_lines"] = len(re.findall(r"<textarea[^>]*>(.*?)</textarea>", html, re.S)[1].split("\n")) - 1 + 1
    rep["page"]["cosmic_linewidths"] = sorted(set(len(l) for l in re.findall(r"<textarea[^>]*>(.*?)</textarea>", html, re.S)[1].split("\n") if l and not l.startswith("mzR")))
    rep["page"]["comments"] = re.findall(r"<!--.*?-->", html, re.S)
    rep["page"]["title_cosmic_mismatch"] = "h1 says 'Cosmic Duality'; no 'Dualite' string anywhere"
    rep["page"]["has_dualite"] = ("Dualite" in html)
    OUT.write_text(json.dumps(rep, indent=2))
    # anomaly ranking: lowest-entropy derived sequences first
    scored = []
    for m in rep["matrices"]:
        for k, v in m["partitions"].items():
            scored.append((v["entropy"], v["distinct"], f'{m["stream"]}/{m["map"]}/{m["shape"]}/{k}'))
    scored.sort()
    print("=== lowest-entropy (most constant) derived sequences ===")
    for e, d, label in scored[:15]:
        print(f"  H={e} distinct={d} {label}")
    print("grid14 matches R/C:", rep["grid14"]["matches_R14"], rep["grid14"]["matches_C14"])
    print("yellow/blue 15/9 hits:", [k for k, v in rep["yellow_blue"].items() if v["matches_15_9"]])
    print("door checksum:", rep["door"]["checksum_valid"], "hash160 reused:", rep["door"]["hash160_reused"])
    print("page has Dualite:", rep["page"]["has_dualite"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
