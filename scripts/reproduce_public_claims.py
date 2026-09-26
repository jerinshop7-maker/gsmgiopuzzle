"""Reproduce public GSMG claims from raw inputs in isolated experiment records.

Each reproduction is a falsifiable test. A readable plaintext, valid padding,
matching length, or self-reported hash is not proof by itself. Failed
reproductions are recorded as dead ends rather than hidden.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from .paths import DERIVED, RAW, ensure_dirs
from .provenance import now_utc_iso, write_json

PUZZLE_GRID = [
    "00110100101100",
    "11110011101011",
    "11011101001001",
    "01101000011101",
    "01100011000110",
    "10011000100011",
    "10011100010000",
    "11100000001000",
    "00011101111101",
    "11111100110001",
    "11010000011011",
    "11110010101100",
    "01011101000110",
    "01101101101011",
]


def spiral_indices(rows: int, cols: int) -> list[tuple[int, int]]:
    """Down-first counterclockwise inward spiral starting at the top-left cell."""
    top, bottom, left, right = 0, rows - 1, 0, cols - 1
    indices: list[tuple[int, int]] = []
    while top <= bottom and left <= right:
        for row in range(top, bottom + 1):
            indices.append((row, left))
        left += 1
        for col in range(left, right + 1):
            indices.append((bottom, col))
        bottom -= 1
        if left <= right:
            for row in range(bottom, top - 1, -1):
                indices.append((row, right))
            right -= 1
        if top <= bottom:
            for col in range(right, left - 1, -1):
                indices.append((top, col))
            top += 1
    return indices


def decode_grid(grid: list[str]) -> str:
    rows = len(grid)
    cols = len(grid[0])
    bits = "".join(grid[r][c] for r, c in spiral_indices(rows, cols))
    chars = [chr(int(bits[i:i + 8], 2)) for i in range(0, len(bits) - len(bits) % 8, 8)]
    return "".join(chars)


def evp_bytes_to_key(password: bytes, salt: bytes, digest: str = "sha256") -> tuple[bytes, bytes]:
    d = b""
    block = b""
    while len(d) < 48:
        h = hashlib.new(digest)
        h.update(block + password + salt)
        block = h.digest()
        d += block
    return d[:32], d[32:48]


def aes_cbc_decrypt(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def openssl_blob_decrypt(b64_text: str, password: bytes, digest: str = "sha256") -> bytes:
    raw = base64.b64decode(b64_text)
    if raw[:8] != b"Salted__":
        raise ValueError("not an OpenSSL Salted__ blob")
    salt = raw[8:16]
    key, iv = evp_bytes_to_key(password, salt, digest=digest)
    return aes_cbc_decrypt(key, iv, raw[16:])


def extract_textarea(html_path: Path) -> str:
    text = html_path.read_bytes().decode("utf-8", "replace")
    match = re.search(r"<textarea[^>]*>(.*?)</textarea>", text, re.S)
    if not match:
        raise ValueError("no textarea found in HTML capture")
    return match.group(1).strip()


def experiment(name: str) -> Path:
    path = DERIVED / "reports" / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args(argv)
    ensure_dirs()

    # Claim 1: grid traversal yields gsmg.io/theseedisplanted.
    decoded = decode_grid(PUZZLE_GRID)
    write_json(experiment("01-grid-traversal") / "report.json", {
        "acquired_at_utc": now_utc_iso(),
        "input": "copied public grid",
        "decoded": decoded,
        "expected": "gsmg.io/theseedisplanted",
        "ok": decoded == "gsmg.io/theseedisplanted",
    })

    # Claim 2: Phase 2 AES-256-CBC with password=SHA256("causality") hex and EVP-SHA256.
    phase2_html = RAW / "web/live/phase2/response.bin"
    if phase2_html.exists():
        blob = extract_textarea(phase2_html)
        password = hashlib.sha256(b"causality").hexdigest().encode("ascii")
        plaintext = openssl_blob_decrypt(blob, password, digest="sha256")
        head = plaintext[:240].decode("utf-8", "replace")
        readable = "The ironic" in head
        report = {
            "acquired_at_utc": now_utc_iso(),
            "input_artifact": str(phase2_html),
            "password": "sha256('causality') hex string with EVP-SHA256",
            "plaintext_length": len(plaintext),
            "plaintext_sha256": hashlib.sha256(plaintext).hexdigest(),
            "plaintext_head": head,
            "readable_prefix_match": readable,
        }
        write_json(experiment("02-phase2") / "report.json", report)

    # Claim 3: SalPhaseIon textarea is present and non-trivial.
    salphaseion_html = RAW / "web/live/salphaseion/response.bin"
    if salphaseion_html.exists():
        body = extract_textarea(salphaseion_html)
        write_json(experiment("03-salphaseion") / "report.json", {
            "acquired_at_utc": now_utc_iso(),
            "input_artifact": str(salphaseion_html),
            "length": len(body),
            "sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
            "head": body[:240],
        })

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
