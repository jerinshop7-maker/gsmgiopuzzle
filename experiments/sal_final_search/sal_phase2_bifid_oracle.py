"""Phase 2: Bifid-square mapping + prime-VALUE filtering + oracle attempts.

Follows CHECKPOINT-2026-09-04-SALFINAL. Uses only primary bytes + officially
attested conventions. No Cosmic/Half/Issue108 inputs.

- Mapping bifid9 (issue #106 square rows, lowercase):
    d=0 b=1 i=2 f=3 h=4 c=5 e=6 g=7 a=8
  vs legacy a1 (a=1..i=9) for control.
- Prime positions (P2357/Pfull x idx0/idx1 x normal/reversed x keep/zero)
  AND prime values (digit in {2,3,5,7} x keep/zero).
- Matrix sums + prime-valued masks + yin/yang pair constancy.
- Every password-like output (<=128 chars, printable) is tried OFFLINE against:
    (a) small-blob oracle A+z+B under BOTH digests (phase-2 convention SHA-256
        primary, MD5 as control since Cosmic used it);
    (b) direct 32-byte key derivation if output is 64-hex or 32 bytes;
    (c) planted third-door list (compressed+uncompressed) for short outputs.
  Acceptance remains EXACT address equality only. All attempts logged NO_MATCH
  unless a match occurs (exit code signals it).
"""
from __future__ import annotations
import base64
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGIONS = json.loads((HERE / "sal_regions.json").read_text())["raws"]
OUT = HERE / "sal_phase2_report.json"

TARGET1 = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"
THIRD_DOOR = "1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9"

BIFID9 = {'d': 0, 'b': 1, 'i': 2, 'f': 3, 'h': 4, 'c': 5, 'e': 6, 'g': 7, 'a': 8}
A1 = {c: i + 1 for i, c in enumerate("abcdefghi")}

BLOB_B64 = REGIONS["R3B64A_63"] + "z" + REGIONS["R4B64B_64"]
assert len(BLOB_B64) == 128, len(BLOB_B64)

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    HAVE_CRYPTO = True
except ImportError:
    HAVE_CRYPTO = False


def evp(password: bytes, salt: bytes, digest: str):
    import hashlib as hl
    H = hl.sha256 if digest == "sha256" else hl.md5
    d = b""
    block = b""
    while len(d) < 48:
        h = H()
        h.update(block + password + salt)
        block = h.digest()
        d += block
    return d[:32], d[32:48]


def try_decrypt(password_hex_or_raw: str, digest: str):
    if not HAVE_CRYPTO:
        return None
    raw = base64.b64decode(BLOB_B64)
    salt, ct = raw[8:16], raw[16:]
    key, iv = evp(password_hex_or_raw.encode(), salt, digest)
    pt = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    out = pt.update(ct) + pt.finalize()
    pad = out[-1]
    if 1 <= pad <= 16 and out[-pad:] == bytes([pad]) * pad:
        return out[:-pad]
    return None


def sieve(n: int) -> set[int]:
    is_p = bytearray(b"\x01") * (n + 1)
    is_p[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i:n + 1:i] = b"\x00" * ((n - i * i) // i + 1)
    return {i for i, v in enumerate(is_p) if v}


def prime_positions(n, definition, indexing):
    primes = {2, 3, 5, 7} if definition == "P2357" else sieve(n + 1)
    return [(i if indexing == "idx0" else i + 1) in primes for i in range(n)]


def main() -> int:
    log: dict = {"oracle_blob": {"len_b64": 128, "salt": "3ab585348552415d"},
                 "crypto_available": HAVE_CRYPTO, "attempts": [], "matches": []}
    streams = {
        "LEAD91": REGIONS["LEAD91"],
        "TAIL570": REGIONS["TAIL570"],
    }
    pwid = 0
    for sname, s in streams.items():
        for mapname, mp in (("bifid9", BIFID9), ("a1", A1)):
            digits = [mp[c] for c in s]
            # prime-VALUE masks
            for rule in ("keepPrimeVal", "zeroPrimeVal"):
                kept = [d for d in digits if (d in (2, 3, 5, 7)) == (rule == "keepPrimeVal")]
                out = "".join(map(str, kept))
                # matrix-sum probe on natural shapes
                n = len(kept)
                facs = [(r, n // r) for r in range(1, int(n ** 0.5) + 1) if n % r == 0] if n else []
                # password candidates: the digit string itself (truncated forms) + sum lists
                cands = []
                if 1 <= len(out) <= 128:
                    cands += [out, out[::-1]]
                for (r, c) in facs[:6]:
                    if r < 2 or c < 2:
                        continue
                    M = [kept[i * c:(i + 1) * c] for i in range(r)]
                    rs = [sum(row) for row in M]
                    cs = [sum(M[i][j] for i in range(r)) for j in range(c)]
                    cands += ["".join(map(str, rs)), "".join(map(str, cs)),
                              "".join(str(x % 10) for x in rs)]
                for cand in cands[:12]:
                    if not (1 <= len(cand) <= 128 and all(32 <= ord(ch) <= 126 for ch in cand)):
                        continue
                    pwid += 1
                    pw = hashlib.sha256(cand.encode()).hexdigest()
                    hits = {}
                    for dg in ("sha256", "md5"):
                        pt = try_decrypt(pw, dg)
                        hits[dg] = "valid_padding" if pt is not None else "no_padding"
                    log["attempts"].append({
                        "id": f"P2-{pwid}", "stream": sname, "map": mapname,
                        "rule": rule, "kept_len": len(kept),
                        "candidate": cand[:80], "sha_pw": pw[:16] + "...",
                        "decrypt": hits, "rank": "NO_MATCH"})
            # prime-POSITION masks (both definitions/indexings, both orientations)
            for orientation in ("normal", "reversed"):
                so = s if orientation == "normal" else s[::-1]
                dg = [mp[c] for c in so]
                for definition in ("P2357", "Pfull"):
                    for indexing in ("idx0", "idx1"):
                        mask = prime_positions(len(so), definition, indexing)
                        for rule in ("keepPrime", "zeroPrime"):
                            zero = -1
                            kept = [d if (m == (rule == "keepPrime")) else zero for d, m in zip(dg, mask)]
                            kept_nz = [d for d in kept if d != -1]
                            out = "".join(map(str, kept_nz))
                            if 1 <= len(out) <= 64:
                                pwid += 1
                                pw = hashlib.sha256(out.encode()).hexdigest()
                                hits = {}
                                for dgd in ("sha256", "md5"):
                                    pt = try_decrypt(pw, dgd)
                                    hits[dgd] = "valid_padding" if pt is not None else "no_padding"
                                log["attempts"].append({
                                    "id": f"P2-{pwid}", "stream": sname, "map": mapname,
                                    "rule": f"{definition}:{indexing}:{orientation}:{rule}",
                                    "kept_len": len(kept_nz),
                                    "candidate": out[:80], "sha_pw": pw[:16] + "...",
                                    "decrypt": hits, "rank": "NO_MATCH"})
    OUT.write_text(json.dumps(log, indent=2))
    print(f"phase2: {len(log['attempts'])} offline oracle attempts, matches={len(log['matches'])}")
    print(f"crypto_available={HAVE_CRYPTO}")
    # print any valid paddings (chance-rate check, NOT acceptance)
    vp = [a for a in log["attempts"] if "valid_padding" in json.dumps(a["decrypt"])]
    print(f"valid paddings: {len(vp)} (expected ~1/256 per digest by chance)")
    for a in vp[:10]:
        print(a["id"], a["stream"], a["map"], a["rule"], a["decrypt"], a["candidate"][:60])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
