"""Focused test of the live SalPhaseIon order: Bifid -> prime/zero -> sums.

This is deliberately narrow.  It tests the one family suggested by the
author's words rather than another unconstrained permutation search:

    TAIL570 --(5x5 DBIFHCEGA, period 570)--> BTCSEED...
             --(prime-valued zeroing)--> matrices
             --(matrixsumlist)--> row/column sum lists

The 7x13 LEAD shape (91 = triangular T13) and 19x30 TAIL shape are the
natural factor choices in the local evidence.  The combined 20+49=69-digit
route is recorded because it is the only previously identified untested
construction with a clue-backed shape and no arbitrary trim.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "sal_final_search"))
import dual_oracle as O  # noqa: E402
from sal_bifid import bifid_decode, build_square, first_occurrence_key, load_lead, load_tail  # noqa: E402

REPORT = HERE / "bifid_prime_matrix_battery_report.json"


def prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def values(raw: str, mode: str) -> list[int]:
    if mode == "a1":
        return [ord(c) - 96 for c in raw]
    if mode == "bifid9":
        mp = {c: i for i, c in enumerate("dbifhcega")}
        return [mp[c] for c in raw]
    raise ValueError(mode)


def zero_prime(vals: list[int], indexing: str, zero_primes: bool) -> list[int]:
    out = []
    for i, v in enumerate(vals):
        pos = i + 1 if indexing == "idx1" else i
        is_p = pos in {2, 3, 5, 7}  # the explicitly named prime basics
        # This function is for prime-VALUE zeroing; position variants are
        # included separately below so the report distinguishes them.
        _ = is_p
        out.append(0 if (prime(v) == zero_primes) else v)
    return out


def zero_position(vals: list[int], indexing: str, zero_primes: bool) -> list[int]:
    out = []
    for i, v in enumerate(vals):
        pos = i + 1 if indexing == "idx1" else i
        is_p = prime(pos)
        out.append(0 if (is_p == zero_primes) else v)
    return out


def matrix_sums(vals: list[int], rows: int, cols: int, offset: int = 0) -> list[int]:
    assert rows * cols == len(vals)
    m = [vals[r * cols:(r + 1) * cols] for r in range(rows)]
    rs = [sum(row) for row in m]
    cs = [sum(m[r][c] for r in range(rows)) for c in range(cols)]
    # R+C with the clue-backed cyclic offset used in the old 14x14 worked
    # example.  It is also tested at offset 0 as the control.
    paired = [rs[i] + cs[(i + offset) % cols] for i in range(rows)]
    return rs + cs + paired


def render(nums: list[int], kind: str) -> str:
    if kind == "raw":
        return "".join(str(x) for x in nums)
    if kind == "mod10":
        return "".join(str(x % 10) for x in nums)
    if kind == "hex":
        return bytes(x % 256 for x in nums).hex()
    if kind == "csv":
        return ",".join(str(x) for x in nums)
    raise ValueError(kind)


def lock_test(password: str) -> dict:
    """Test password as direct and SHA-256-hexdigest under both KDF digests."""
    out: dict = {"valid_padding": [], "target": []}
    for bname, blob in (("small", O.BLOB_SMALL), ("p32", O.BLOB_P32)):
        for pname, pw in (("direct", password.encode()),
                          ("sha256_hex", hashlib.sha256(password.encode()).hexdigest().encode())):
            for dg in ("sha256", "md5"):
                pt = O.dec_blob(blob, pw, dg)
                if pt is None:
                    continue
                out["valid_padding"].append(f"{bname}/{pname}/{dg}")
                for rname, key in O.readings(pt):
                    if len(key) != 32:
                        continue
                    try:
                        addr = O.priv_to_addrs(key)["uncompressed"]
                    except Exception:
                        continue
                    if addr == O.TARGET1:
                        out["target"].append({"blob": bname, "form": pname,
                                               "digest": dg, "reading": rname,
                                               "priv": key.hex()})
    return out


def main() -> int:
    assert O.selftest()
    lead, tail = load_lead(), load_tail()
    square = build_square(first_occurrence_key(lead))
    decoded = bifid_decode(tail, square, len(tail))
    assert decoded.startswith("BTCSEED")

    # LEAD stays in the digit alphabet; the Bifid-derived TAIL is represented
    # in two ways: square rank (0..24), and the observed 0..8 key alphabet.
    # The latter is the exact prime-value convention used by the old notes.
    tail_rank = [square.index(c) for c in decoded]
    tail_key9 = values(tail[:], "bifid9")
    lead_key9 = values(lead, "bifid9")
    sources = {
        "lead_key9": (lead_key9, (7, 13)),
        "tail_key9_raw": (tail_key9, (19, 30)),
        "tail_bifid_rank": (tail_rank, (19, 30)),
    }

    candidates: dict[str, str] = {}
    for sname, (base, shape) in sources.items():
        for zname, zfn in (("value_zero_prime", zero_prime),
                           ("value_zero_nonprime", lambda a, i, z: zero_prime(a, i, not z)),
                           ("position_zero_prime", zero_position),
                           ("position_zero_nonprime", lambda a, i, z: zero_position(a, i, not z))):
            for indexing in ("idx0", "idx1"):
                # idx affects only position masks; retaining both labels for
                # all modes makes the tested convention explicit in the log.
                for reverse in (False, True):
                    arr = zfn(base, indexing, True)
                    if reverse:
                        arr = arr[::-1]
                    for off in (0, 7):
                        sums = matrix_sums(arr, *shape, offset=off)
                        for kind in ("raw", "mod10", "hex", "csv"):
                            x = render(sums, kind)
                            candidates[f"{sname}/{zname}/{indexing}/{reverse}/{off}/{kind}"] = x

    # The strongest composite proposal: LEAD 7x13 R+C (20 values) followed
    # by TAIL 19x30 R+C (49 values), with no trim and both mask conventions.
    for lzname, lfn in (("value", zero_prime), ("position", zero_position)):
        for indexing in ("idx0", "idx1"):
            l = lfn(lead_key9, indexing, True)
            for tzname, tfn in (("value", zero_prime), ("position", zero_position)):
                t = tfn(tail_key9, indexing, True)
                for reverse_l, reverse_t in ((False, False), (True, False), (False, True), (True, True)):
                    ll = l[::-1] if reverse_l else l
                    tt = t[::-1] if reverse_t else t
                    for off in (0, 7):
                        nums = matrix_sums(ll, 7, 13, off) + matrix_sums(tt, 19, 30, off)
                        for kind in ("raw", "mod10", "hex", "csv"):
                            candidates[f"composite/{lzname}/{tzname}/{indexing}/{reverse_l}/{reverse_t}/{off}/{kind}"] = render(nums, kind)

    results = []
    vpads = 0
    for label, x in candidates.items():
        info = lock_test(x)
        vpads += len(info["valid_padding"])
        if info["target"]:
            results.append({"label": label, "candidate": x, "info": info})

    report = {
        "decoded_sha256": hashlib.sha256(decoded.encode()).hexdigest(),
        "decoded_head": decoded[:16],
        "even256_sha256": hashlib.sha256("".join(c for c in decoded[1::2] if c not in "IO").encode()).hexdigest(),
        "candidate_count": len(candidates),
        "valid_padding_events": vpads,
        "target_matches": results,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    print("report:", REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
