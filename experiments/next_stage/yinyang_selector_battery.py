"""Test the aligned yin/yang pair left by the canonical Bifid decode.

After the exact 570-character decode, the two 285-character halves are not
independent: the locked half is B/C/D/E, while the other half has 29 I/O
markers. Removing those 29 markers leaves exactly 256 aligned pairs.  This
test treats the four-symbol half as a four-way selector or a 2-bit stream and
tests only stable, reversible readings against the exact oracles.
"""
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

REPORT = HERE / "yinyang_selector_battery_report.json"


def lock_bytes(b: bytes) -> dict:
    out = {"valid_padding": [], "target": [], "door": []}
    forms = [("raw", b), ("sha256", hashlib.sha256(b).hexdigest().encode())]
    for bname, blob in (("small", O.BLOB_SMALL), ("p32", O.BLOB_P32)):
        for fname, pw in forms:
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
    # Exact third-door constructions on byte strings are a useful discriminator.
    for name, key in O.third_door_keys(b.decode("latin1")):
        try:
            addrs = O.priv_to_addrs(key)
        except Exception:
            continue
        for comp, addr in addrs.items():
            if addr in O.PLANTED:
                out["door"].append({"construction": name, "compression": comp, "addr": addr})
    return out


def main() -> int:
    assert O.selftest()
    decoded = bifid_decode(load_tail(), build_square(first_occurrence_key(load_lead())), 570)
    yin, yang = decoded[0::2], decoded[1::2]
    keep = [i for i, c in enumerate(yang) if c not in "IO"]
    selector = "".join(yin[i] for i in keep)
    payload = "".join(yang[i] for i in keep)
    assert len(selector) == len(payload) == 256
    assert set(selector) <= set("BCDE")

    alpha = "ABCDEFGHKLMNPQRSTUVWXYZ"
    rank = {c: i for i, c in enumerate(alpha)}
    srank = {c: i for i, c in enumerate("BCDE")}
    p = [rank[c] for c in payload]
    s = [srank[c] for c in selector]
    candidates: dict[str, bytes] = {}

    def add(label: str, b: bytes) -> None:
        candidates.setdefault(label, b)

    # The locked half as a 2-bit stream, in all bit-polarity/order variants.
    for perm in itertools.permutations(range(4)):
        vals = [perm[x] for x in s]
        bits = "".join(f"{x:02b}" for x in vals)
        raw = bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))
        add("selector-2bit/" + "".join("BCDE"[i] for i in perm), raw)
        add("selector-2bit-rev/" + "".join("BCDE"[i] for i in perm), raw[::-1])

    # Four-way stable bucket routes: a selector is a natural route key, and
    # all 24 orderings are the complete non-arbitrary family.
    for order in itertools.permutations(range(4)):
        route = []
        for k in order:
            route.extend(i for i, x in enumerate(s) if x == k)
        q = [p[i] for i in route]
        lab = "bucket/" + "".join("BCDE"[i] for i in order)
        for shift in (0, 1, -1):
            add(f"{lab}/shift{shift}/ascii", bytes((x + shift) % 23 + 65 for x in q))
            add(f"{lab}/shift{shift}/rank", bytes(q))
            add(f"{lab}/shift{shift}/hex", bytes(q).hex().encode())

    # Selector arithmetic with the aligned 23-symbol stream.
    for op in ("add", "sub", "xor", "mul"):
        q = []
        for a, b in zip(p, s):
            q.append({"add": (a + b) % 23, "sub": (a - b) % 23,
                      "xor": (a ^ b) % 23, "mul": (a * (b + 1)) % 23}[op])
        for rev in (False, True):
            z = q[::-1] if rev else q
            add(f"aligned/{op}/{rev}/letters", "".join(alpha[x] for x in z).encode())
            add(f"aligned/{op}/{rev}/rank", bytes(z))
            add(f"aligned/{op}/{rev}/hex", bytes(z).hex().encode())
            add(f"aligned/{op}/{rev}/sha", hashlib.sha256(bytes(z)).hexdigest().encode())

    # Pair encodings preserve both halves and are bounded by the exact 256
    # length; these are not arbitrary wordlist candidates.
    for pair_order in ("sp", "ps"):
        pairs = [(s[i], p[i]) if pair_order == "sp" else (p[i], s[i]) for i in range(256)]
        for mode in ("nibble", "byte"):
            if mode == "nibble":
                b = bytes(((a << 5) | x) if pair_order == "sp" else ((a << 2) | x)
                          for a, x in pairs)
            else:
                b = bytes((((a << 5) | x) if pair_order == "sp" else ((a << 2) | x)) & 255
                          for a, x in pairs)
            add(f"pairs/{pair_order}/{mode}", b)
            add(f"pairs/{pair_order}/{mode}/rev", b[::-1])

    hits, vpads, door_hits = [], 0, []
    for label, b in candidates.items():
        info = lock_bytes(b)
        vpads += len(info["valid_padding"])
        if info["target"]:
            hits.append({"label": label, "bytes_hex": b.hex(), "info": info})
        if info["door"]:
            door_hits.append({"label": label, "bytes_hex": b.hex(), "info": info})
    report = {
        "decoded_sha256": hashlib.sha256(decoded.encode()).hexdigest(),
        "selector_sha256": hashlib.sha256(selector.encode()).hexdigest(),
        "payload_sha256": hashlib.sha256(payload.encode()).hexdigest(),
        "selector_len": len(selector), "payload_len": len(payload),
        "candidate_count": len(candidates), "valid_padding_events": vpads,
        "target_matches": hits, "third_door_matches": door_hits,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    print("report:", REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
