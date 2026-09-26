"""Probe the recovered 161-token (7x23) author-hint matrix.

The 2023-02-23 image contains 161 exact bytes, each ending in binary ``110``.
Bit-reversing the bytes in reverse order gives the authenticated author hint.
The five upper bits form a 7x23 numerical object, which is the previously
blocked concrete 23-object in the 23/16/7 hypothesis.

This runner tests a finite, clue-named family only:
  * row/column routes and reversals of the 7x23 object;
  * prime rows {2,3,5,7} and prime columns in 1..23;
  * zero/keep masks and reinsertion of {2,3,5,7};
  * row/column matrix-sum lists and transparent encodings;
  * SHA-256/double-SHA-256 and the exact target/door address controls.

It records hashes and labels, never private-key bytes.
"""
from __future__ import annotations

import base64
import hashlib
import itertools
import json
import sys
from pathlib import Path

from coincurve import PrivateKey

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "sal_final_search"))
import dual_oracle as O  # noqa: E402

REPORT = HERE / "hint161_matrix_probe_report.json"
TARGET_H160 = bytes.fromhex("a9553269572a317e39f0f518cb87c1a0ee1dbae4")
TOKEN_HEX = (
    "26a6ce96b6f64e0e9e86ee86a66e96e6a6ae4e2e86ce960ea62ece2ece86369e"
    "4ea66e2e96e67696a6a6ce2ef676a64eaef69e2eae46cea69ea64eaef69e66f"
    "62e76f64e667696ce2e96264ef6eecece860ea6162e9e86ee86a66e96e62e7"
    "6f6eea6eee676869e76969ea6c696f616c69616c64e86a64ef666a646ce264"
    "ef6ee2ece86362ece9636b6aece1e964e2e86b6cea6b6964e0ea6ae3646eef6"
    "3636a69e"
)
TOKENS = bytes.fromhex(TOKEN_HEX)
P_ROWS = {1, 2, 4, 6}  # 1-based rows 2,3,5,7
P_COLS = {1, 2, 4, 6, 10, 12, 16, 18, 22}  # 1-based primes <=23
PRIMES = (2, 3, 5, 7)


def h160(key: bytes) -> bytes | None:
    try:
        pub = PrivateKey(key).public_key.format(compressed=False)
    except ValueError:
        return None
    return hashlib.new("ripemd160", hashlib.sha256(pub).digest()).digest()


def prefix(got: bytes | None) -> int:
    if got is None:
        return -1
    n = 0
    for a, b in zip(got, TARGET_H160):
        if a != b:
            break
        n += 1
    return n


def orientations(m: list[list[int]]) -> dict[str, list[list[int]]]:
    out: dict[str, list[list[int]]] = {}
    for trans in (False, True):
        base = [list(x) for x in zip(*m)] if trans else [row[:] for row in m]
        for rr in (False, True):
            for cc in (False, True):
                rows = base[::-1] if rr else base
                rows = [row[::-1] for row in rows] if cc else rows
                out[f"{'T' if trans else 'R'}{'r' if rr else ''}{'c' if cc else ''}"] = rows
    return out


def flatten(m: list[list[int]]) -> list[int]:
    return [v for row in m for v in row]


def matrix_values(m: list[list[int]]) -> dict[str, list[int]]:
    rows = [sum(row) for row in m]
    cols = [sum(m[r][c] for r in range(len(m))) for c in range(len(m[0]))]
    out = {
        "rows": rows,
        "cols": cols,
        "rows+cols": rows + cols,
        "cols+rows": cols + rows,
        "row-col": [a - b for a, b in zip(rows, cols[:len(rows)])],
        "row+col": [a + b for a, b in zip(rows, cols[:len(rows)])],
        "row-xor-col": [a ^ b for a, b in zip(rows, cols[:len(rows)])],
    }
    return out


def encode(nums: list[int], kind: str) -> bytes:
    if kind == "raw8":
        return bytes(x & 0xFF for x in nums)
    if kind == "raw5":
        return bytes(x & 31 for x in nums)
    if kind == "decimal":
        return "".join(str(x) for x in nums).encode()
    if kind == "csv":
        return ",".join(str(x) for x in nums).encode()
    if kind == "hex":
        return bytes(x & 0xFF for x in nums).hex().encode()
    if kind == "base32":
        return "".join("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"[x & 31] for x in nums).encode()
    if kind == "base32decode":
        text = "".join("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"[x & 31] for x in nums)
        if len(text) % 8 == 1:
            return b""
        try:
            return base64.b32decode(text + "=" * ((8 - len(text) % 8) % 8))
        except ValueError:
            return b""
    raise ValueError(kind)


def add_candidate(dst: dict[str, bytes], label: str, data: bytes) -> None:
    if 1 <= len(data) <= 2048:
        dst.setdefault(data.hex(), (label, data))


def main() -> int:
    assert len(TOKENS) == 161, len(TOKENS)
    assert all(x & 7 == 6 for x in TOKENS)
    values = [x >> 3 for x in TOKENS]
    matrix = [values[i * 23:(i + 1) * 23] for i in range(7)]
    candidates: dict[str, tuple[str, bytes]] = {}

    # Verify and retain the primary message as an artifact-level control.
    bitrev = lambda x: int(f"{x:08b}"[::-1], 2)
    message = bytes(bitrev(x) for x in TOKENS[::-1])
    assert message.startswith(b"yellowblueprimesmatrixsumlist")
    add_candidate(candidates, "message", message)

    for oname, oriented in orientations(matrix).items():
        arrays = {"all": flatten(oriented)}
        rows = len(oriented)
        cols = len(oriented[0])
        row_prime = {i for i in range(rows) if (i + 1) in P_ROWS}
        col_prime = {i for i in range(cols) if (i + 1) in P_COLS}
        flat = arrays["all"]
        add_candidate(candidates, f"{oname}/values", encode(flat, "raw5"))
        add_candidate(candidates, f"{oname}/base32", encode(flat, "base32"))
        add_candidate(candidates, f"{oname}/base32decode", encode(flat, "base32decode"))
        for mask_name, keep in (
            ("zero-prime-rows", lambda r, c: r not in row_prime),
            ("keep-prime-rows", lambda r, c: r in row_prime),
            ("zero-prime-cols", lambda r, c: c not in col_prime),
            ("keep-prime-cols", lambda r, c: c in col_prime),
            ("zero-prime-row-or-col", lambda r, c: r not in row_prime and c not in col_prime),
            ("keep-prime-row-or-col", lambda r, c: r in row_prime or c in col_prime),
        ):
            masked = [x if keep(r, c) else 0 for r, row in enumerate(oriented)
                      for c, x in enumerate(row)]
            for kind in ("raw5", "decimal", "csv", "hex", "base32", "base32decode"):
                add_candidate(candidates, f"{oname}/{mask_name}/{kind}", encode(masked, kind))

        # The only reinsertion family retained: assign the four named prime
        # basics to the four prime rows, or cycle them down prime columns.
        for perm in itertools.permutations(PRIMES):
            by_row = {r: perm[i] for i, r in enumerate(sorted(row_prime))}
            rein = [[by_row.get(r, oriented[r][c]) for c in range(cols)] for r in range(rows)]
            for kind in ("raw5", "decimal", "csv", "hex", "base32", "base32decode"):
                add_candidate(candidates, f"{oname}/reinsert-rows/{''.join(map(str, perm))}/{kind}", encode(flatten(rein), kind))
            by_col = {c: perm[i % 4] for i, c in enumerate(sorted(col_prime))}
            rein = [[by_col.get(c, oriented[r][c]) for c in range(cols)] for r in range(rows)]
            for kind in ("raw5", "decimal", "csv", "hex", "base32", "base32decode"):
                add_candidate(candidates, f"{oname}/reinsert-cols/{''.join(map(str, perm))}/{kind}", encode(flatten(rein), kind))

        for sname, nums in matrix_values(oriented).items():
            for kind in ("raw8", "decimal", "csv", "hex", "base32", "base32decode"):
                add_candidate(candidates, f"{oname}/matrix/{sname}/{kind}", encode(nums, kind))

    rows = []
    exact = []
    for key_hex, (label, data) in candidates.items():
        for transform, key in (
            ("sha256", hashlib.sha256(data).digest()),
            ("double_sha256", hashlib.sha256(hashlib.sha256(data).digest()).digest()),
        ):
            got = h160(key)
            score = prefix(got)
            row = {"label": label, "transform": transform, "length": len(data),
                   "prefix_bytes": score, "h160": None if got is None else got.hex(),
                   "input_sha256": hashlib.sha256(data).hexdigest()}
            if got == TARGET_H160:
                row["match"] = "target_uncompressed"
                exact.append(row)
            rows.append(row)

    rows.sort(key=lambda x: (x["prefix_bytes"], x["label"], x["transform"]), reverse=True)
    report = {
        "token_count": len(TOKENS),
        "token_sha256": hashlib.sha256(TOKENS).hexdigest(),
        "message": message.decode(),
        "matrix_shape": [7, 23],
        "candidate_count": len(candidates),
        "hash_checks": len(rows),
        "top": rows[:40],
        "exact_matches": exact,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("token_count", "token_sha256", "matrix_shape",
                                              "candidate_count", "hash_checks", "exact_matches")}, indent=2))
    print("top:", json.dumps(rows[:12], indent=2))
    print("report:", REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
