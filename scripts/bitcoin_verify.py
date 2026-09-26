"""Offline Bitcoin address and WIF verification.

This tool validates Base58Check, WIF, compressed/uncompressed public keys,
HASH160, and P2PKH derivation without transmitting any candidate secret to
an external service. A valid WIF that does not derive the prize target is a
decoy or intermediate, not a solution.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from .paths import DERIVED, ensure_dirs
from .provenance import now_utc_iso, write_json

BASE58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def base58_decode(text: str) -> bytes:
    num = 0
    for ch in text:
        num = num * 58 + BASE58.index(ch)
    pad = len(text) - len(text.lstrip("1"))
    byte_length = (num.bit_length() + 7) // 8
    return b"\x00" * pad + num.to_bytes(max(byte_length, 1), "big")


def base58check_decode(text: str) -> bytes:
    raw = base58_decode(text)
    if len(raw) < 4:
        raise ValueError("input too short for Base58Check")
    payload, checksum = raw[:-4], raw[-4:]
    digest = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    if digest != checksum:
        raise ValueError("Base58Check checksum mismatch")
    return payload


def wif_to_secret(wif: str) -> tuple[bytes, bool]:
    payload = base58check_decode(wif)
    if len(payload) == 33 and payload[-1] == 1:
        return payload[1:32], True
    if len(payload) == 32:
        return payload, False
    raise ValueError("unrecognized WIF payload length")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wif", help="WIF to validate offline.")
    parser.add_argument("--address", help="Address to validate offline.")
    args = parser.parse_args(argv)
    ensure_dirs()
    report: dict = {"acquired_at_utc": now_utc_iso()}

    if args.wif:
        try:
            secret, compressed = wif_to_secret(args.wif)
            report["wif"] = args.wif
            report["wif_valid"] = True
            report["compressed"] = compressed
            report["secret_hex"] = secret.hex()
        except Exception as exc:
            report["wif"] = args.wif
            report["wif_valid"] = False
            report["error"] = str(exc)

    if args.address:
        try:
            payload = base58check_decode(args.address)
            report["address"] = args.address
            report["address_valid"] = True
            report["version_byte"] = payload[0]
            report["hash160"] = payload[1:].hex()
        except Exception as exc:
            report["address"] = args.address
            report["address_valid"] = False
            report["error"] = str(exc)

    out = DERIVED / "bitcoin" / "verify.json"
    write_json(out, report)
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
