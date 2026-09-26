"""Prime/zero + matrixsumlist test on the canonical 16x16 even256 object.

The 256-symbol object is the strongest surviving waypoint: it is exactly 16x16
and its post-I/O alphabet has exactly 23 symbols.  This test uses only the
explicitly hinted operations (prime, zero, matrix sums, yin/yang row/column
duality) and records every candidate with an exact dual-lock/door oracle.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "sal_final_search"))
from sal_bifid import bifid_decode, build_square, first_occurrence_key, load_lead, load_tail  # noqa: E402
import dual_oracle as O  # noqa: E402

REPORT = HERE / "even256_prime_matrix_battery_report.json"


def isprime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def render(nums: list[int], mode: str) -> str:
    if mode == "decimal":
        return "".join(str(x) for x in nums)
    if mode == "csv":
        return ",".join(str(x) for x in nums)
    if mode == "mod10":
        return "".join(str(x % 10) for x in nums)
    if mode == "bytes":
        return bytes(x & 255 for x in nums).decode("latin1")
    if mode == "hex":
        return bytes(x & 255 for x in nums).hex()
    if mode == "a1":
        return "".join(chr(65 + (x % 26)) for x in nums)
    raise ValueError(mode)


def derive(arr: list[int], mask_name: str, mask_mode: str, reverse: bool, offset: int) -> dict[str, list[int]]:
    if reverse:
        arr = arr[::-1]
    if mask_name == "none":
        z = arr
    elif mask_name == "value2357":
        z = [0 if ((x in (2, 3, 5, 7)) == (mask_mode == "zero")) else x for x in arr]
    elif mask_name == "value_fullprime":
        z = [0 if (isprime(x) == (mask_mode == "zero")) else x for x in arr]
    elif mask_name == "position_prime":
        z = [0 if (isprime(i + 1) == (mask_mode == "zero")) else x for i, x in enumerate(arr)]
    else:
        raise ValueError(mask_name)
    m = [z[i * 16:(i + 1) * 16] for i in range(16)]
    rows = [sum(r) for r in m]
    cols = [sum(m[r][c] for r in range(16)) for c in range(16)]
    rowcol = [rows[i] + cols[(i + offset) % 16] for i in range(16)]
    colrow = [cols[i] + rows[(i + offset) % 16] for i in range(16)]
    diffs = [rows[i] - cols[(i + offset) % 16] for i in range(16)]
    return {"rows": rows, "cols": cols, "rowcol": rowcol, "colrow": colrow,
            "diff": diffs, "both": rows + cols}


def lock_test(password: str) -> dict:
    out: dict = {"valid_padding": [], "target": [], "door": []}
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
    door, di = O.attempt_door(password)
    if door:
        out["door"].append(di)
    return out


def main() -> int:
    assert O.selftest()
    decoded = bifid_decode(load_tail(), build_square(first_occurrence_key(load_lead())), 570)
    streams = {
        "even256": "".join(c for c in decoded[1::2] if c not in "IO"),
        "odd285": decoded[0::2],
    }
    candidates: dict[str, str] = {}
    for sname, s in streams.items():
        assert len(s) == (256 if sname == "even256" else 285)
        alphabet = "".join(dict.fromkeys(sorted(s)))
        # Alphabetical rank is the only non-text numeric representation here;
        # stream order is preserved. Both 0- and 1-based versions are tested.
        for rank_name, rank in (("rank0", {c: i for i, c in enumerate(alphabet)}),
                                ("rank1", {c: i + 1 for i, c in enumerate(alphabet)})):
            arr = [rank[c] for c in s]
            for mask_name in ("none", "value2357", "value_fullprime", "position_prime"):
                for mask_mode in ("keep", "zero"):
                    for reverse in (False, True):
                        for offset in (0, 7):
                            for opname, nums in derive(arr, mask_name, mask_mode, reverse, offset).items():
                                # The 16x16 object is primary; odd285 is only
                                # allowed to use its natural first 256 window.
                                for take_name, use in (("full", nums),):
                                    for enc in ("decimal", "csv", "mod10", "bytes", "hex", "a1"):
                                        candidates[f"{sname}/{rank_name}/{mask_name}/{mask_mode}/{reverse}/{offset}/{opname}/{take_name}/{enc}"] = render(use, enc)

    hits, vpads, door_hits = [], 0, []
    for label, x in candidates.items():
        info = lock_test(x)
        vpads += len(info["valid_padding"])
        if info["target"]:
            hits.append({"label": label, "candidate": x, "info": info})
        if info["door"]:
            door_hits.append({"label": label, "candidate": x, "info": info})
    report = {
        "decoded_sha256": hashlib.sha256(decoded.encode()).hexdigest(),
        "even256_sha256": hashlib.sha256(streams["even256"].encode()).hexdigest(),
        "streams": {k: {"length": len(v), "alphabet": "".join(sorted(set(v)))} for k, v in streams.items()},
        "candidate_count": len(candidates),
        "valid_padding_events": vpads,
        "target_matches": hits,
        "third_door_matches": door_hits,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    print("report:", REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
