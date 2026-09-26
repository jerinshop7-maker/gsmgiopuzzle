"""Test the bounded 16-item / seven-token synthesis interpretation.

The list is taken in published stage order.  Only source-order, reversal,
odd/even interleaving, SHA-256, and XOR-of-digests forms are admitted; this is
an evidence-led continuation of the author's ``intertwined`` wording, not a
general permutation sweep.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parents[1] / "sal_final_search"
sys.path.insert(0, str(HERE))
import dual_oracle as O  # noqa: E402

OUT = Path(__file__).with_name("full_password_synthesis_probe_report.json")

GENESIS_HEX = (
    "736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E614843"
    "20393030322F6E614A2F33302073656D695420656854"
)
GENESIS_REVERSED = bytes.fromhex(GENESIS_HEX).decode()
GENESIS_SOURCE = GENESIS_REVERSED[::-1]
# The published hex is authoritative; its decoded source contains ``CHancellor``
# (capital H).  Also retain the conventional headline spelling as a separate,
# explicitly labeled semantic variant.
GENESIS_DISPLAY = (
    "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"
)
assert len(GENESIS_SOURCE) == len(GENESIS_DISPLAY) == 69

ITEMS = [
    "causality", "Safenet", "Luna", "HSM", "11110",
    "GENESIS_HEX_LITERAL",
    "B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1",
    "jacquefresco", "giveitjustonesecond", "heisenbergsuncertaintyprinciple",
    "matrixsumlist", "enter", "lastwordsbeforearchichoice", "thispassword",
    "yourlastcommand", "secondanswer",
]

ITEMS[5] = "0x" + GENESIS_HEX
SEVEN = ["matrixsumlist", "enter", "lastwordsbeforearchichoice", "thispassword",
         "matrixsumlist", "yourlastcommand", "secondanswer"]


def xor_digests(parts: list[str]) -> bytes:
    out = bytearray(32)
    for part in parts:
        d = hashlib.sha256(part.encode()).digest()
        for i, b in enumerate(d):
            out[i] ^= b
    return bytes(out)


def candidates() -> dict[str, str]:
    out: dict[str, str] = {}

    def add(label: str, value: str):
        if value and label not in out:
            out[label] = value

    corpora = {
        "full16-hex": ITEMS,
        "full16-reversed": ITEMS[:5] + [GENESIS_REVERSED] + ITEMS[6:],
        "full16-source": ITEMS[:5] + [GENESIS_SOURCE] + ITEMS[6:],
        "full16-display": ITEMS[:5] + [GENESIS_DISPLAY] + ITEMS[6:],
        "seven": SEVEN,
    }
    for name, parts in corpora.items():
        joins = {
            "concat": "".join(parts),
            "concat-lower": "".join(parts).lower(),
            "spaced": " ".join(parts),
            "reverse": "".join(parts)[::-1],
            "reverse-items": "".join(reversed(parts)),
            "odd-items": "".join(parts[::2]),
            "even-items": "".join(parts[1::2]),
        }
        for label, value in joins.items():
            add(f"{name}/{label}", value)
            add(f"{name}/{label}/sha256-hex", hashlib.sha256(value.encode()).hexdigest())
            add(f"{name}/{label}/sha256-raw-hex", hashlib.sha256(value.encode()).digest().hex())
        add(f"{name}/xor-sha256-hex", xor_digests(parts).hex())
        add(f"{name}/xor-sha256-raw-hex", xor_digests(list(reversed(parts))).hex())
    return out


def main() -> int:
    assert O.selftest()
    cands = candidates()
    records = []
    for label, value in cands.items():
        lock, linfo = O.attempt_locks(value)
        door, dinfo = O.attempt_door(value)
        records.append({"label": label, "candidate": value[:160],
                        "sha256": hashlib.sha256(value.encode()).hexdigest(),
                        "lock": lock, "door": door,
                        "lock_info": linfo, "door_info": dinfo})
    hits = [r for r in records if r["lock"] or r["door"]]
    report = {"full16_count": len(ITEMS), "seven_count": len(SEVEN),
              "candidate_count": len(records), "hits": hits, "records": records}
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"candidate_count": len(records), "hits": hits,
                      "report": str(OUT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
