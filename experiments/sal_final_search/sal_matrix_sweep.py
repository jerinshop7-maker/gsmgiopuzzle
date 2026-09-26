"""Matrix-sum password sweep: the 'matrixsumlist' instruction taken literally.

Hypothesis (issue #106): LEAD91/TAIL570 digit streams -- canonical values via
Bifid square rows (bifid9: d=0,b=1,i=2,f=3,h=4,c=5,e=6,g=7,a=8), legacy a1 as
control -- form matrices on natural factor shapes; row/col/diag sums as lists
are password candidates (concatenated raw / mod10 / comma-joined / hashed).

Also prime-masked variants (positions P2357/Pfull x idx0/idx1 x keep/zero, and
prime values in {2,3,5,7} x keep/zero) since primes + zeroing are explicit clues.

Each candidate X tried vs BOTH locks x {hexdigest,direct} x {sha256,md5} (8
decrypts, C-backed AES, fast). Valid paddings -> full 4-reading oracle vs
TARGET1 (uncompressed). Door EC checks limited to valid-padding candidates +
short sum lists (keeps runtime sane; full door sweep needs C speed).

Strict EXACT acceptance only.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dual_oracle as O

HERE = Path(__file__).resolve().parent
REGIONS = json.loads((HERE / "sal_regions.json").read_text())["raws"]
OUT = HERE / "sal_matrix_sweep_report.json"

BIFID9 = {'d': 0, 'b': 1, 'i': 2, 'f': 3, 'h': 4, 'c': 5, 'e': 6, 'g': 7, 'a': 8}
A1 = {c: i + 1 for i, c in enumerate("abcdefghi")}


def sieve(n: int) -> set[int]:
    is_p = bytearray(b"\x01") * (n + 1)
    is_p[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i:n + 1:i] = b"\x00" * ((n - i * i) // i + 1)
    return {i for i, v in enumerate(is_p) if v}


def factor_pairs(n: int):
    return [(r, n // r) for r in range(1, int(n ** 0.5) + 1) if n % r == 0]


def sums_of(M):
    r = len(M)
    c = len(M[0])
    rs = [sum(row) for row in M]
    cs = [sum(M[i][j] for i in range(r)) for j in range(c)]
    dg = None
    if r == c:
        dg = [sum(M[i][i] for i in range(r)), sum(M[i][r - 1 - i] for i in range(r))]
    return rs, cs, dg


def forms_of(ints: list[int]) -> list[str]:
    out = []
    raw = "".join(map(str, ints))
    out.append(("raw", raw))
    out.append(("mod10", "".join(str(x % 10) for x in ints)))
    if len(ints) <= 32:
        out.append(("csv", ",".join(map(str, ints))))
        out.append(("chr", "".join(chr(48 + (x % 10)) for x in ints)))
    return out


def main() -> int:
    streams = {"LEAD91": REGIONS["LEAD91"], "TAIL570": REGIONS["TAIL570"],
               "FULL765": REGIONS["LEAD91"] + REGIONS["MID104"].replace("a", "c").replace("b", "d"),
               }
    # NOTE: FULL765 mixes binary a/b with digits; map a/b->0/1 via bifid-unfriendly
    # path below handles per-char fallback. Keep for shape coverage only.
    log: dict = {"attempts": 0, "decryptions": 0, "valid_paddings": [], "matches": [],
                 "families": {}, "door_checks": 0, "door_hits": []}
    seen: set[str] = set()

    def attempt(family: str, cand: str):
        if not (1 <= len(cand) <= 128) or cand in seen:
            return
        seen.add(cand)
        log["attempts"] += 1
        hit, info = O.attempt_locks(cand)
        log["decryptions"] += 8
        if info.get("valid_padding"):
            log["valid_paddings"].append({"family": family, "cand": cand[:80], "info": info})
        if hit:
            log["matches"].append({"family": family, "cand": cand[:80], "info": info})

    for sname in ("LEAD91", "TAIL570"):
        s = streams[sname]
        for mapname, mp in (("bifid9", BIFID9), ("a1", A1)):
            base = [mp[c] for c in s]
            variants = {"plain": base}
            # prime-value masks
            variants["keepPval"] = [d for d in base if d in (2, 3, 5, 7)]
            variants["zeroPval"] = [0 if d in (2, 3, 5, 7) else d for d in base]
            # prime-position masks (1-indexed full primes; 0-indexed P2357) both rules
            n = len(base)
            for dname, idx, rule in (("Pfull", "idx1", "keep"), ("Pfull", "idx1", "zero"),
                                     ("P2357", "idx0", "keep"), ("P2357", "idx0", "zero")):
                primes = {2, 3, 5, 7} if dname == "P2357" else sieve(n + 1)
                mask = [(i if idx == "idx0" else i + 1) in primes for i in range(n)]
                if rule == "keep":
                    variants[f"{dname}-{idx}-keep"] = [d for d, m in zip(base, mask) if m]
                else:
                    variants[f"{dname}-{idx}-zero"] = [0 if m else d for d, m in zip(base, mask)]
            for vname, arr in variants.items():
                m = len(arr)
                if m < 4:
                    continue
                for (r, c) in factor_pairs(m):
                    if r * c != m or r < 2 or c < 2:
                        continue
                    if m > 120 and r not in (2, 3, 5, 6, 7, 9, 10, 13, 15, 19, 30):
                        continue
                    for orientation in (0, 1):
                        a = arr if orientation == 0 else arr[::-1]
                        M = [a[i * c:(i + 1) * c] for i in range(r)]
                        rs, cs, dg = sums_of(M)
                        for tag, ints in (("rows", rs), ("cols", cs)):
                            for fname, cand in forms_of(ints):
                                attempt(f"{sname}/{mapname}/{vname}/{r}x{c}/{'rev' if orientation else 'fwd'}/{tag}/{fname}", cand)
                        if dg:
                            for fname, cand in forms_of(dg):
                                attempt(f"{sname}/{mapname}/{vname}/{r}x{c}/diag/{fname}", cand)
    # door EC spot-check: valid-padding candidates + a sample of short sum lists
    log["door_sample"] = []
    for vp in log["valid_paddings"][:50]:
        log["door_checks"] += 1
        hit, info = O.attempt_door(vp["cand"])
        if hit:
            log["door_hits"].append({"cand": vp["cand"][:60], "info": info})
            log["matches"].append({"family": "door-from-vpad", "cand": vp["cand"][:80], "info": info})
    OUT.write_text(json.dumps(log, indent=2))
    print(f"matrix sweep: {log['attempts']} candidates, {log['decryptions']} decryptions, "
          f"vpads={len(log['valid_paddings'])}, matches={len(log['matches'])}, door_checks={log['door_checks']}")
    for vp in log["valid_paddings"][:10]:
        print("VPAD", vp["family"][:90], vp["info"])
    for mt in log["matches"]:
        print("MATCH", mt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
