"""Finite structural search: SalPhaseIon -> primes -> zeroing -> matrix -> sum list -> yin/yang.

Deterministic enumeration over structurally justified interpretations only.
No Half/Better Half/103x103/1327-byte/Issue108/private-key inputs are used.

Every candidate emits:
  experiment_id, input_hash, stream, orientation, prime_definition, indexing,
  zeroing_rule, matrix_shape, matrix_transform, sum_operation,
  yin_yang_operation, output, output_hash, rank

Ranks: EXACT_MATCH, KNOWN_TOKEN, KNOWN_LENGTH, VALID_CIPHERTEXT,
       PARTIAL_STRUCTURAL_MATCH, NO_MATCH

Acceptance (EXACT_MATCH) requires exact Base58Check equality with a target
via the offline verifier. Nothing else promotes a candidate.

Streams come byte-identically from sal_regions.json (CHECKPOINT-2026-09-04-SALFINAL).
"""
from __future__ import annotations
import base64
import binascii
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGIONS_PATH = HERE / "sal_regions.json"
REPORT_PATH = HERE / "sal_final_report.jsonl"
SUMMARY_PATH = HERE / "sal_final_summary.json"

TARGET1 = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"
TARGET2 = "17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa"
KNOWN_TOKENS = [
    "matrixsumlist", "enter", "lastwordsbeforearchichoice", "thispassword",
    "yourlastcommand", "secondanswer", "ourfirsthintis", "ourlastcommand",
    "shabef", "BTCSEED", "Salted__",
]
KNOWN_LENGTHS = {32, 64, 79, 80, 95, 96, 103, 128, 256}

# 14x14 prompt vectors (preserved, not trusted as solution)
R14 = (6, 10, 8, 7, 6, 6, 5, 4, 9, 9, 7, 8, 7, 9)
C14 = (8, 10, 8, 10, 8, 7, 3, 6, 7, 5, 9, 6, 6, 8)


def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def sieve(n: int) -> set[int]:
    if n < 2:
        return set()
    is_p = bytearray(b"\x01") * (n + 1)
    is_p[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i:n + 1:i] = b"\x00" * ((n - i * i) // i + 1)
    return {i for i, v in enumerate(is_p) if v}


def is_prime_small(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(n ** 0.5)
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True


def prime_mask(n: int, definition: str, indexing: str) -> list[bool]:
    """True = position is prime under the definition/indexing."""
    mask = []
    if definition == "P2357":
        primes = {2, 3, 5, 7}
    elif definition == "Pfull":
        # prime numbers within 0..n (for 1-indexed) or 0..n-1 (for 0-indexed)
        primes = sieve(n + 1)
    else:
        raise ValueError(definition)
    for i in range(n):
        pos = i if indexing == "idx0" else i + 1
        mask.append(pos in primes)
    return mask


def zero_stream(stream: str, mask: list[bool], rule: str, alphabet: str) -> str:
    """rule: keepPrime (retain primes, zero others) | zeroPrime (zero primes, retain others)."""
    if alphabet == "ab":
        zero = "a"
    elif alphabet == "ai":
        zero = "o"  # maps to 0 in the page's own a=1..i=9,o=0 convention
    else:
        zero = "0"
    out = []
    for ch, m in zip(stream, mask):
        keep = (m and rule == "keepPrime") or ((not m) and rule == "zeroPrime")
        out.append(ch if keep else zero)
    return "".join(out)


def factor_pairs(n: int) -> list[tuple[int, int]]:
    pairs = []
    for r in range(1, int(n ** 0.5) + 1):
        if n % r == 0:
            pairs.append((r, n // r))
    return pairs


def triangular_root(n: int) -> int | None:
    # n = k(k+1)/2 -> k^2+k-2n=0
    k = int((math.sqrt(1 + 8 * n) - 1) // 2)
    return k if k * (k + 1) // 2 == n else None


def reshape(row: list[int], rows: int, cols: int) -> list[list[int]]:
    return [row[r * cols:(r + 1) * cols] for r in range(rows)]


def transform_matrix(M: list[list[int]], op: str) -> list[list[int]]:
    if op == "id":
        return [r[:] for r in M]
    if op == "hmirror":
        return [r[::-1] for r in M]
    if op == "vmirror":
        return M[::-1]
    if op == "rot180":
        return [r[::-1] for r in M[::-1]]
    if op == "transpose":
        return [list(r) for r in zip(*M)]
    if op == "antitranspose":
        # rotate 90 cw then flip = reflection across anti-diagonal
        t = [list(r) for r in zip(*M)]
        return [r[::-1] for r in t[::-1]]
    if op == "complement":
        return [[1 - v for v in r] for r in M]
    raise ValueError(op)


def row_sums(M: list[list[int]]) -> list[int]:
    return [sum(r) for r in M]


def col_sums(M: list[list[int]]) -> list[int]:
    return [sum(M[r][c] for r in range(len(M))) for c in range(len(M[0]))]


def rank_output(output: str, extra: dict) -> str:
    low = output.lower()
    for t in KNOWN_TOKENS:
        if t.lower() in low and len(output) < 500:
            # only promote short legible outputs, not noise containing fragments
            if output.strip().isascii() and sum(c.isprintable() for c in output) / max(1, len(output)) > 0.9:
                return "KNOWN_TOKEN"
    if extra.get("exact_match"):
        return "EXACT_MATCH"
    if extra.get("valid_ciphertext"):
        return "VALID_CIPHERTEXT"
    if extra.get("length") in KNOWN_LENGTHS:
        return "KNOWN_LENGTH".upper()
    if extra.get("structural"):
        return "PARTIAL_STRUCTURAL_MATCH"
    return "NO_MATCH"


def load_streams() -> dict[str, dict]:
    doc = json.loads(REGIONS_PATH.read_text())
    raws = doc["raws"]
    return {
        "LEAD91": {"s": raws["LEAD91"], "alpha": "ai"},
        "TAIL570": {"s": raws["TAIL570"], "alpha": "ai"},
        "LEAD_TAIL661": {"s": raws["LEAD91"] + raws["TAIL570"], "alpha": "ai"},
        "FULL765": {"s": raws["LEAD91"] + raws["MID104"] + raws["TAIL570"], "alpha": "mixed"},
        "MID104": {"s": raws["MID104"], "alpha": "ab"},
        "R4A40": {"s": raws["R4A40"], "alpha": "ab"},
        "R1_63": {"s": raws["R1_63"], "alpha": "aio"},
        "R2_29": {"s": raws["R2_29"], "alpha": "aio"},
    }


def stream_to_ints(s: str, alpha: str) -> list[int]:
    if alpha == "ab":
        return [0 if c == "a" else 1 for c in s]
    mp = {c: i + 1 for i, c in enumerate("abcdefghi")}
    mp["o"] = 0
    if alpha in ("ai", "aio"):
        return [mp[c] for c in s]
    # mixed FULL765: map a/b to 0/1, c-i to 3-9
    out = []
    for c in s:
        if c in ("a", "b"):
            out.append(0 if c == "a" else 1)
        else:
            out.append(mp[c])
    return out


def bits_of_ints(ints: list[int], mode: str) -> list[int]:
    if mode == "mod2":
        return [v % 2 for v in ints]
    if mode == "primeval":
        return [1 if is_prime_small(v) else 0 for v in ints]
    if mode == "nonprimeval":
        return [0 if is_prime_small(v) else 1 for v in ints]
    raise ValueError(mode)


def main() -> int:
    streams = load_streams()
    results: list[dict] = []
    exp = 0

    def emit(rec: dict):
        nonlocal exp
        exp += 1
        rec["experiment_id"] = f"SALFINAL-{exp:05d}"
        rec["output_hash"] = hashlib.sha256(rec["output"].encode()).hexdigest()
        results.append(rec)

    # ---- A. prime mask + zeroing on digit/binary streams ----
    for sname, meta in streams.items():
        s = meta["s"]
        alpha = meta["alpha"]
        n = len(s)
        in_hash = hashlib.sha256(s.encode()).hexdigest()[:16]
        for orientation in ("normal", "reversed"):
            so = s if orientation == "normal" else s[::-1]
            for definition in ("P2357", "Pfull"):
                for indexing in ("idx0", "idx1"):
                    try:
                        mask = prime_mask(n, definition, indexing)
                    except ValueError:
                        continue
                    nprime = sum(mask)
                    for rule in ("keepPrime", "zeroPrime"):
                        z = zero_stream(so, mask, rule, alpha if alpha != "mixed" else "ai")
                        # legibility probe: for ab streams decode ascii if len%8==0
                        probe = ""
                        structural = False
                        if alpha == "ab" and len(z) % 8 == 0:
                            bits = z.replace("a", "0").replace("b", "1")
                            try:
                                probe = "".join(chr(int(bits[i:i + 8], 2)) for i in range(0, len(bits), 8))
                            except ValueError:
                                probe = ""
                        # factor/triangular structure flags
                        facs = factor_pairs(n)
                        tri = triangular_root(n)
                        if tri is not None or len(facs) > 2 or nprime in (2, 3, 5, 7, 29, 63, 91):
                            structural = True
                        out = f"{sname}:{orientation}:{definition}:{indexing}:{rule}:nprime={nprime}:zeroed_head={z[:64]}:probe={probe!r}:factors={facs}:tri={tri}"
                        emit({
                            "input_hash": in_hash, "stream": sname,
                            "orientation": orientation, "prime_definition": definition,
                            "indexing": indexing, "zeroing_rule": rule,
                            "matrix_shape": f"1x{n}", "matrix_transform": "id",
                            "sum_operation": "none", "yin_yang_operation": "none",
                            "output": out,
                            "rank": rank_output(probe or z[:32], {"structural": structural or bool(probe)}),
                        })

    # ---- B. matrix shapes + transforms + sums + prime-valued masks ----
    for sname in ("LEAD91", "TAIL570", "MID104", "R4A40"):
        meta = streams[sname]
        s = meta["s"]
        alpha = meta["alpha"]
        n = len(s)
        in_hash = hashlib.sha256(s.encode()).hexdigest()[:16]
        for orientation in ("normal", "reversed"):
            so = s if orientation == "normal" else s[::-1]
            for bitmode in (["mod2", "primeval", "nonprimeval"] if alpha != "ab" else ["direct"]):
                ints = stream_to_ints(so, alpha) if alpha != "ab" else [0 if c == "a" else 1 for c in so]
                bits = ints if alpha == "ab" else bits_of_ints(ints, bitmode)
                for (rows, cols) in factor_pairs(n):
                    if rows * cols != n or rows < 2 or cols < 2:
                        continue
                    # cap explosion: only near-square + extreme for large n
                    if n > 120 and (rows, cols) not in [(1, n), (n, 1), (2, n // 2), (n // 2, 2)]:
                        # keep smallest non-trivial too
                        sq = int(n ** 0.5)
                        if not (abs(rows - sq) <= 4 or rows in (5, 6, 7, 10, 13, 14, 15, 19, 30)):
                            continue
                    M = reshape(bits, rows, cols)
                    for top in ("id", "hmirror", "vmirror", "rot180", "complement") + (("transpose", "antitranspose") if rows == cols else ()):
                        try:
                            T = transform_matrix(M, top)
                        except ValueError:
                            continue
                        rs, cs = row_sums(T), col_sums(T)
                        # yin/yang pair ops
                        yy = {
                            "none": "",
                            "rowpair_sum": str([rs[i] + rs[len(rs) - 1 - i] for i in range(len(rs) // 2)]),
                            "rowpair_diff": str([rs[i] - rs[len(rs) - 1 - i] for i in range(len(rs) // 2)]),
                            "colpair_sum": str([cs[i] + cs[len(cs) - 1 - i] for i in range(len(cs) // 2)]),
                            "colpair_diff": str([cs[i] - cs[len(cs) - 1 - i] for i in range(len(cs) // 2)]),
                        }
                        rpm = "".join("1" if is_prime_small(v) else "0" for v in rs)
                        cpm = "".join("1" if is_prime_small(v) else "0" for v in cs)
                        xnor = "".join("1" if a == b else "0" for a, b in zip(rpm, cpm[:len(rpm)]))
                        xor = "".join("1" if a != b else "0" for a, b in zip(rpm, cpm[:len(rpm)]))
                        for sumop in ("rows", "cols"):
                            for yyname, yyval in yy.items():
                                out = (f"{sname}:{orientation}:{bitmode}:{rows}x{cols}:{top}:{sumop}:{yyname}:"
                                       f"R={rs}:C={cs}:Rpm={rpm}:Cpm={cpm}:XOR={xor}:XNOR={xnor}:YY={yyval}")
                                # structural: complementary constancy (yin/yang hint)
                                structural = False
                                if yyname in ("rowpair_sum", "colpair_sum") and yyval:
                                    vals = json.loads(yyval)
                                    if len(set(vals)) == 1:
                                        structural = True
                                if set(rpm) == {"0", "1"} and set(cpm) == {"0", "1"}:
                                    structural = structural or (xor.count("1") in (2, 3, 5, 7))
                                emit({
                                    "input_hash": in_hash, "stream": sname,
                                    "orientation": orientation,
                                    "prime_definition": f"values:{bitmode}",
                                    "indexing": "n/a",
                                    "zeroing_rule": "n/a",
                                    "matrix_shape": f"{rows}x{cols}",
                                    "matrix_transform": top,
                                    "sum_operation": sumop,
                                    "yin_yang_operation": yyname,
                                    "output": out,
                                    "rank": rank_output(out, {"structural": structural}),
                                })

    # ---- C. prompt R/C vectors under prime-value + yin/yang ops ----
    for vecname, vec in (("R14", list(R14)), ("C14", list(C14))):
        in_hash = hashlib.sha256(json.dumps(vec).encode()).hexdigest()[:16]
        rpm = "".join("1" if is_prime_small(v) else "0" for v in vec)
        for opname, out in {
            "prime_mask": rpm,
            "nonprime_mask": "".join("0" if is_prime_small(v) else "1" for v in vec),
            "mod2": "".join(str(v % 2) for v in vec),
            "mod3": "".join(str(v % 3) for v in vec),
            "mod5": "".join(str(v % 5) for v in vec),
            "mod7": "".join(str(v % 7) for v in vec),
            "diff7": str([v - 7 for v in vec]),
            "diff8": str([v - 8 for v in vec]),
            "diff9": str([v - 9 for v in vec]),
            "abs": str([abs(v) for v in vec]),
            "R-C": str([a - b for a, b in zip(R14, C14)]),
            "R-revC": str([a - b for a, b in zip(R14, C14[::-1])]),
        }.items():
            emit({
                "input_hash": in_hash, "stream": vecname, "orientation": "normal",
                "prime_definition": "values:is_prime", "indexing": "n/a",
                "zeroing_rule": "n/a", "matrix_shape": "14x1",
                "matrix_transform": "id", "sum_operation": vecname,
                "yin_yang_operation": opname, "output": f"{vecname}:{opname}={out}",
                "rank": rank_output(out, {"structural": opname in ("prime_mask", "R-C", "R-revC")}),
            })
    # XOR/XNOR between R/C prime masks (yin/yang equality hint)
    rpm = "".join("1" if is_prime_small(v) else "0" for v in R14)
    cpm = "".join("1" if is_prime_small(v) else "0" for v in C14)
    for opname, out in {
        "Rpm_XOR_Cpm": "".join("1" if a != b else "0" for a, b in zip(rpm, cpm)),
        "Rpm_XNOR_Cpm": "".join("1" if a == b else "0" for a, b in zip(rpm, cpm)),
    }.items():
        emit({
            "input_hash": hashlib.sha256((rpm + cpm).encode()).hexdigest()[:16],
            "stream": "R14+C14", "orientation": "normal",
            "prime_definition": "values:is_prime", "indexing": "n/a",
            "zeroing_rule": "n/a", "matrix_shape": "14x1",
            "matrix_transform": "id", "sum_operation": "prime_masks",
            "yin_yang_operation": opname, "output": f"{opname}={out} (Rpm={rpm} Cpm={cpm})",
            "rank": "PARTIAL_STRUCTURAL_MATCH",
        })

    # ---- D. Base64 fragments (A, B, A+B, B+A, A+z+B) ----
    doc = json.loads(REGIONS_PATH.read_text())
    A = doc["raws"]["R3B64A_63"]
    B = doc["raws"]["R4B64B_64"]
    for label, s in (("A", A), ("B", B), ("A+B", A + B), ("B+A", B + A), ("A+z+B", A + "z" + B)):
        info = {"raw_length": len(s)}
        try:
            raw = base64.b64decode(s, validate=False)
            info.update({"decoded_length": len(raw), "hex_head": raw[:32].hex(),
                         "header": raw[:8].decode("latin1", "replace"),
                         "salt": raw[8:16].hex() if len(raw) >= 16 else "",
                         "ct_mod16": (len(raw) - 16) % 16 if len(raw) >= 16 else -1,
                         "entropy": float(hashlib.sha256(raw).hexdigest()[:8] and 0) or 0})
            valid = (raw[:8] == b"Salted__" and (len(raw) - 16) % 16 == 0)
        except (binascii.Error, ValueError):
            valid = False
            info.update({"b64_error": True})
        emit({
            "input_hash": hashlib.sha256(s.encode()).hexdigest()[:16],
            "stream": f"frag:{label}", "orientation": "normal",
            "prime_definition": "n/a", "indexing": "n/a", "zeroing_rule": "n/a",
            "matrix_shape": "n/a", "matrix_transform": "n/a",
            "sum_operation": "n/a", "yin_yang_operation": "n/a",
            "output": f"{label}: {json.dumps(info, sort_keys=True)}",
            "rank": rank_output("", {"valid_ciphertext": valid, "length": info.get("decoded_length", -1)}),
        })

    # ---- E. seven-token sequence (no hashing as solution; structural only) ----
    toks7 = ["matrixsumlist", "enter", "lastwordsbeforearchichoice", "thispassword",
             "matrixsumlist", "yourlastcommand", "secondanswer"]
    seqs = {
        "concat_order": "".join(toks7),
        "concat_reverse": "".join(toks7[::-1]),
        "odd1357": "".join(toks7[i] for i in (0, 2, 4, 6)),
        "even246": "".join(toks7[i] for i in (1, 3, 5)),
        "lengths": str([len(t) for t in toks7]),
        "firsts": "".join(t[0] for t in toks7),
        "lasts": "".join(t[-1] for t in toks7),
        "sha_each": str([hashlib.sha256(t.encode()).hexdigest()[:16] for t in toks7]),
        "repeat_equal": str(toks7[0] == toks7[4]),
    }
    for name, out in seqs.items():
        emit({
            "input_hash": hashlib.sha256("".join(toks7).encode()).hexdigest()[:16],
            "stream": "tokens7", "orientation": "normal" if "reverse" not in name else "reversed",
            "prime_definition": "n/a", "indexing": name, "zeroing_rule": "n/a",
            "matrix_shape": "n/a", "matrix_transform": "n/a",
            "sum_operation": "sequence", "yin_yang_operation": name,
            "output": f"tokens7:{name}={out}",
            "rank": rank_output(out, {"structural": True}),
        })

    REPORT_PATH.write_text("\n".join(json.dumps(r, sort_keys=True) for r in results) + "\n")
    by_rank: dict[str, int] = {}
    for r in results:
        by_rank[r["rank"]] = by_rank.get(r["rank"], 0) + 1
    SUMMARY_PATH.write_text(json.dumps({
        "total": len(results), "by_rank": by_rank,
        "targets": [TARGET1, TARGET2],
        "note": "No EXACT_MATCH without exact address equality. See CHECKPOINT.",
    }, indent=2))
    print(f"wrote {len(results)} candidates; ranks={by_rank}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
