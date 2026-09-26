"""Known-answer cryptographic controls for the GSMG investigation.

Before any candidate is tested, the implementations used here must reproduce
published test vectors and the known solved stages of the puzzle. A passing
control does not prove a candidate; it only proves the implementation is not
broken.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from .paths import DERIVED, ensure_dirs
from .provenance import now_utc_iso, write_json


def evp_bytes_to_key(password: bytes, salt: bytes, key_len: int = 32, iv_len: int = 16,
                     digest: str = "md5") -> tuple[bytes, bytes]:
    d = b""
    block = b""
    while len(d) < key_len + iv_len:
        h = hashlib.new(digest)
        h.update(block + password + salt)
        block = h.digest()
        d += block
    return d[:key_len], d[key_len:key_len + iv_len]


def aes_cbc_decrypt(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def assert_eq(name: str, actual: bytes | str, expected: bytes | str) -> dict:
    ok = actual == expected
    record = {"name": name, "ok": ok}
    if not ok:
        record["expected"] = expected
        record["actual"] = actual
    return record


def run_controls() -> list[dict]:
    results = []

    results.append(assert_eq(
        "sha256_empty",
        hashlib.sha256(b"").hexdigest(),
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ))

    results.append(assert_eq(
        "md5_empty",
        hashlib.md5(b"").hexdigest(),
        "d41d8cd98f00b204e9800998ecf8427e",
    ))

    results.append(assert_eq(
        "sha256_abc",
        hashlib.sha256(b"abc").hexdigest(),
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
    ))

    key, iv = evp_bytes_to_key(b"password", b"salt" * 2, digest="md5")
    results.append(assert_eq(
        "evp_md5_key",
        (key + iv).hex(),
        "fdbdf3419fff98bdb0241390f62a9db35f4aba29d77566377997314ebfc709f20b5ca7b1081f94b1ac12e3c8ba87d05a",
    ))

    plaintext = b"0123456789abcdef" * 2
    cipher = Cipher(algorithms.AES(bytes(16)), modes.CBC(bytes(16))).encryptor()
    ciphertext = cipher.update(plaintext) + cipher.finalize()
    results.append(assert_eq(
        "aes_cbc_roundtrip",
        aes_cbc_decrypt(bytes(16), bytes(16), ciphertext),
        plaintext,
    ))

    results.append(assert_eq(
        "base64_decode",
        base64.b64decode("U2FsdGVkX18="),
        b"Salted__",
    ))

    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args(argv)
    ensure_dirs()
    results = run_controls()
    failures = [r for r in results if not r["ok"]]
    report = {
        "acquired_at_utc": now_utc_iso(),
        "total": len(results),
        "failures": len(failures),
        "results": results,
    }
    out = DERIVED / "crypto" / "controls.json"
    write_json(out, report)
    print(json.dumps(report, indent=2))
    return 2 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
