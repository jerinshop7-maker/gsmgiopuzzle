"""Bounded test of the aligned B/C/D/E -> 2/3/5/7 prime-basics mapping."""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "sal_final_search"))
from sal_bifid import bifid_decode, build_square, first_occurrence_key, load_lead, load_tail  # noqa: E402
import dual_oracle as O  # noqa: E402

REPORT = HERE / "prime_selector_battery_report.json"


def render(nums: list[int], kind: str, alphabet: str) -> str:
    if kind == "letters":
        return "".join(alphabet[n % len(alphabet)] for n in nums)
    if kind == "rankbytes":
        return bytes(n % 256 for n in nums).decode("latin1")
    if kind == "hexbytes":
        return bytes(n % 256 for n in nums).hex()
    if kind == "decimal":
        return "".join(str(n) for n in nums)
    if kind == "csv":
        return ",".join(str(n) for n in nums)
    if kind == "sha256":
        return hashlib.sha256(bytes(n % 256 for n in nums)).hexdigest()
    raise ValueError(kind)


def lock_test(x: str) -> dict:
    out = {"valid_padding": [], "target": [], "door": []}
    for bname, blob in (("small", O.BLOB_SMALL), ("p32", O.BLOB_P32)):
        for fname, pw in (("direct", x.encode()),
                          ("sha256_hex", hashlib.sha256(x.encode()).hexdigest().encode())):
            for dg in ("sha256", "md5"):
                pt = O.dec_blob(blob, pw, dg)
                if pt is None:
                    continue
                out["valid_padding"].append(f"{bname}/{fname}/{dg}")
                for rname, key in O.readings(pt):
                    if len(key) != 32:
                        continue
                    try:
                        addr = O.priv_to_addrs(key)["uncompressed"]
                    except Exception:
                        continue
                    if addr == O.TARGET1:
                        out["target"].append({"blob": bname, "form": fname,
                                               "digest": dg, "reading": rname,
                                               "priv": key.hex()})
    door, di = O.attempt_door(x)
    if door:
        out["door"].append(di)
    return out


def main() -> int:
    assert O.selftest()
    decoded = bifid_decode(load_tail(), build_square(first_occurrence_key(load_lead())), 570)
    yin, yang = decoded[0::2], decoded[1::2]
    keep = [i for i, c in enumerate(yang) if c not in "IO"]
    sel = "".join(yin[i] for i in keep)
    payload = "".join(yang[i] for i in keep)
    alpha = "ABCDEFGHKLMNPQRSTUVWXYZ"
    ranks = {c: i for i, c in enumerate(alpha)}
    p0 = [ranks[c] for c in payload]
    p1 = [x + 1 for x in p0]
    candidates: dict[str, str] = {}

    for perm in itertools.permutations((2, 3, 5, 7)):
        pm = dict(zip("BCDE", perm))
        q = [pm[c] for c in sel]
        for base_name, p in (("rank0", p0), ("rank1", p1)):
            for op in ("add", "sub", "mul", "xor", "pow2", "pow3"):
                if op == "add": vals = [a + b for a, b in zip(p, q)]
                elif op == "sub": vals = [a - b for a, b in zip(p, q)]
                elif op == "mul": vals = [a * b for a, b in zip(p, q)]
                elif op == "xor": vals = [a ^ b for a, b in zip(p, q)]
                elif op == "pow2": vals = [(a + b) ** 2 for a, b in zip(p, q)]
                else: vals = [(a + b) ** 3 for a, b in zip(p, q)]
                for mod_name, arr in (("raw", vals), ("mod23", [x % 23 for x in vals]),
                                      ("mod256", [x % 256 for x in vals])):
                    for rev in (False, True):
                        z = arr[::-1] if rev else arr
                        for enc in ("letters", "rankbytes", "hexbytes", "decimal", "csv", "sha256"):
                            candidates[f"{''.join(map(str, perm))}/{base_name}/{op}/{mod_name}/{rev}/{enc}"] = render(z, enc, alpha)
                # matrix sums are the only second-stage operation tested here.
                for mod_name, arr in (("raw", vals), ("mod23", [x % 23 for x in vals])):
                    m = [arr[i * 16:(i + 1) * 16] for i in range(16)]
                    rs, cs = [sum(r) for r in m], [sum(m[r][c] for r in range(16)) for c in range(16)]
                    for nums_name, nums in (("rows", rs), ("cols", cs),
                                            ("both", rs + cs),
                                            ("rc7", [rs[i] + cs[(i + 7) % 16] for i in range(16)])):
                        for enc in ("letters", "rankbytes", "hexbytes", "decimal", "csv", "sha256"):
                            candidates[f"{''.join(map(str, perm))}/{base_name}/{op}/{mod_name}/{nums_name}/{enc}"] = render(nums, enc, alpha)

    # The prime stream alone is also a legitimate 2/3/5/7 reading control.
    for perm in itertools.permutations((2, 3, 5, 7)):
        q = [dict(zip("BCDE", perm))[c] for c in sel]
        for rev in (False, True):
            z = q[::-1] if rev else q
            for enc in ("rankbytes", "hexbytes", "decimal", "csv", "sha256"):
                candidates[f"prime-only/{''.join(map(str, perm))}/{rev}/{enc}"] = render(z, enc, alpha)

    hits, vpads, door_hits = [], 0, []
    for label, x in candidates.items():
        info = lock_test(x)
        vpads += len(info["valid_padding"])
        if info["target"]:
            hits.append({"label": label, "candidate": x, "info": info})
        if info["door"]:
            door_hits.append({"label": label, "candidate": x, "info": info})
    report = {"decoded_sha256": hashlib.sha256(decoded.encode()).hexdigest(),
              "selector_len": len(sel), "candidate_count": len(candidates),
              "valid_padding_events": vpads, "target_matches": hits,
              "third_door_matches": door_hits}
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    print("report:", REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
