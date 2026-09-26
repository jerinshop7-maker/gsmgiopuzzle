#!/usr/bin/env python3
"""Reproduce the public cosmic 39-block address witnesses.

The current public witness report gives a precise construction for two outputs:
split the canonical 1327-byte Cosmic plaintext into 32-byte blocks, take
bytes 16:32 from a selected block, append the block index as BE32, and encode
the resulting 20-byte payload as a version-0 P2PKH Base58Check address.

This is a witness audit, not a claim that the 39-block construction is the
creator's final key derivation.  It records all 39 raw outputs and checks the
target address directly.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "experiments/004-cosmic/cosmic_decrypted.bin"
REPORT = Path(__file__).with_name("cosmic_39_block_witness_report.json")
TARGET = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"
WITNESSES = {
    "1Hby7BYWaQmuUE57761xrPjJ9rN3d58V8Y": 10,
    "1Bwq9PKdsrafTFhzDeFzBBk9NF5N8NZCw9": 4,
}
BLOCK_COUNT = 39
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def base58_encode(value: int) -> str:
    out = ""
    while value:
        value, rem = divmod(value, 58)
        out = ALPHABET[rem] + out
    return out or "1"


def p2pkh_from_hash160(payload: bytes) -> str:
    versioned = b"\x00" + payload
    checksum = hashlib.sha256(hashlib.sha256(versioned).digest()).digest()[:4]
    # The version byte is zero, so Base58Check carries one leading `1`.
    return "1" + base58_encode(int.from_bytes(versioned + checksum, "big"))


def main() -> None:
    data = SOURCE.read_bytes()
    rows = []
    for index in range(BLOCK_COUNT):
        block = data[index * 32 : (index + 1) * 32]
        payload = block[16:32] + index.to_bytes(4, "big")
        rows.append(
            {
                "index": index,
                "block_sha256": hashlib.sha256(block).hexdigest(),
                "payload_hex": payload.hex(),
                "address": p2pkh_from_hash160(payload),
            }
        )

    by_address = {row["address"]: row["index"] for row in rows}
    report = {
        "source": str(SOURCE.relative_to(ROOT)),
        "source_size": len(data),
        "source_sha256": hashlib.sha256(data).hexdigest(),
        "block_size": 32,
        "block_count": len(rows),
        "ignored_tail_bytes": len(data) - BLOCK_COUNT * 32,
        "construction": "block[16:32] || BE32(index) -> version-0 P2PKH Base58Check",
        "target_address": TARGET,
        "target_match": by_address.get(TARGET),
        "published_witnesses": {
            address: {"expected_index": expected, "observed_index": by_address.get(address)}
            for address, expected in WITNESSES.items()
        },
        "prefix_counts": {
            prefix: sum(row["address"].startswith(prefix) for row in rows)
            for prefix in ("1H", "1B", "1G")
        },
        "rows": rows,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    assert report["source_sha256"] == "4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081"
    assert report["block_count"] == BLOCK_COUNT
    assert report["ignored_tail_bytes"] == 79
    assert report["target_match"] is None
    for address, expected in WITNESSES.items():
        assert report["published_witnesses"][address]["observed_index"] == expected
    print(json.dumps({
        "block_count": len(rows),
        "ignored_tail_bytes": report["ignored_tail_bytes"],
        "target_match": report["target_match"],
        "published_witnesses": report["published_witnesses"],
        "prefix_counts": report["prefix_counts"],
        "report": str(REPORT.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
