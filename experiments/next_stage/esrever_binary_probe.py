"""Apply the authenticated whole-bitstream ``esrever`` convention.

The known secondary witness is not a character reversal: the 192 ASCII bits of
``gsmg.io/theseedisplanted`` are read backwards and left-padded to 32 bytes.
This probe applies that exact operation to the confirmed Bifid-derived objects,
then checks only the certified lock and planted-door oracles.
"""
from __future__ import annotations

import base64
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sal_final_search"))
import dual_oracle as O

HERE = Path(__file__).resolve().parents[1] / "sal_final_search"
REGIONS = json.loads((HERE / "sal_regions.json").read_text())["raws"]


def reverse_bits_stream(data: bytes) -> bytes:
    bits = "".join(f"{b:08b}" for b in data)
    rev = bits[::-1]
    return int(rev, 2).to_bytes((len(rev) + 7) // 8, "big")


def reverse_each_byte(data: bytes) -> bytes:
    return bytes(int(f"{b:08b}"[::-1], 2) for b in data)


def forms(payload: bytes):
    """Yield password/key material with explicit labels, no arbitrary words."""
    seen: set[tuple[str, bytes]] = set()

    def add(label: str, value: bytes):
        item = (label, value)
        if item not in seen:
            seen.add(item)
            yield item

    for label, value in (
        ("raw", payload),
        ("raw-sha256", hashlib.sha256(payload).digest()),
        ("hex", payload.hex().encode()),
        ("base64", base64.b64encode(payload)),
    ):
        yield from add(label, value)
    # The historical lock convention hashes an answer and passes the hex
    # digest as the OpenSSL password; retain that exact spelling too.
    yield from add("sha256-hex", hashlib.sha256(payload).hexdigest().encode())


def check_payload(label: str, payload: bytes) -> list[dict]:
    hits: list[dict] = []
    for form, pw in forms(payload):
        # Reuse the oracle's certified decryption/readings, but permit binary
        # material that cannot be represented as a Python str.
        for blob_name, blob in (("small", O.BLOB_SMALL), ("p32", O.BLOB_P32)):
            raw = base64.b64decode(blob)
            for digest in ("sha256", "md5"):
                pt = O.dec_blob(blob, pw, digest)
                if pt is None:
                    continue
                for reading, key in O.readings(pt):
                    if len(key) != 32:
                        continue
                    try:
                        addr = O.priv_to_addrs(key)["uncompressed"]
                    except Exception:
                        continue
                    if addr == O.TARGET1:
                        hits.append({"kind": "lock", "label": label,
                                     "form": form, "blob": blob_name,
                                     "digest": digest, "reading": reading,
                                     "priv": key.hex(), "address": addr})
        # For direct binary 32-byte readings, check the exact door family too.
        if len(payload) == 32:
            for form_name, key in ((form, pw), (form + ":sha256", hashlib.sha256(pw).digest())):
                if len(key) != 32:
                    continue
                try:
                    addrs = O.priv_to_addrs(key)
                except Exception:
                    continue
                for style, addr in addrs.items():
                    if addr in O.PLANTED:
                        hits.append({"kind": "door", "label": label,
                                     "form": form_name, "style": style,
                                     "address": addr})
    return hits


def main() -> int:
    decoded = (HERE / "bifid_out.txt").read_text().strip().encode()
    even285 = decoded[1::2]
    even256 = bytes(c for c in even285 if c not in b"IO")
    objects = {
        "bifid570": decoded,
        "even285": even285,
        "even256": even256,
        "odd285": decoded[0::2],
    }
    records: list[dict] = []
    for name, data in objects.items():
        variants = {
            "identity": data,
            "whole-bit-reverse": reverse_bits_stream(data),
            "byte-bit-reverse": reverse_each_byte(data),
            "reverse-bytes-bit-reverse": reverse_bits_stream(data[::-1]),
        }
        for vname, payload in variants.items():
            # Whole objects, and every 32-byte aligned window, are the only
            # reductions used here; no wordlist or arbitrary scalar is added.
            candidates = [("whole", payload)]
            candidates += [(f"window-{i}", payload[i:i + 32])
                           for i in range(0, max(0, len(payload) - 31), 32)]
            for cname, candidate in candidates:
                records.append({"object": name, "variant": vname,
                                "candidate": cname, "length": len(candidate),
                                "sha256": hashlib.sha256(candidate).hexdigest(),
                                "hits": check_payload(f"{name}/{vname}/{cname}", candidate)})
    report = Path(__file__).with_name("esrever_binary_probe_report.json")
    report.write_text(json.dumps({"objects": {k: len(v) for k, v in objects.items()},
                                  "records": records}, indent=2) + "\n")
    hits = [h for r in records for h in r["hits"]]
    print(json.dumps({"records": len(records), "hits": hits,
                      "report": str(report)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
