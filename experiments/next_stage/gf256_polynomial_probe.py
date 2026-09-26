"""Probe the GF(256) interpolation near-miss under every degree-8 field.

The external exploratory branch used the AES polynomial 0x11b.  Since the
interpolation itself does not identify a basis, this runner checks the finite
set of irreducible degree-8 polynomials over GF(2), preserving the reported
hot order/level and then testing every level for that order.  It is a probe,
not a claim that the interpolation is author-defined.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

from ecdsa import SECP256k1, SigningKey

TARGET_H160 = bytes.fromhex("a9553269572a317e39f0f518cb87c1a0ee1dbae4")
XS = [0xFC, 0x0C, 0x1B, 0x02]
BLOCKS = [
    bytes.fromhex("0423d9115a1dc756d5d08d2de880ab50"),
    bytes.fromhex("8bd4745fc97709f4fcb513f2cb8fcc35"),
    bytes.fromhex("48cc46e66bdd36b09ae344552f606a76"),
    bytes.fromhex("1f9d90681f20dfefe2b43db18b623971"),
]
LABELS = ["fc", "00", "02", "04", "0c", "0f", "1b"]
HOT_ORDER = ["00", "0f", "0c", "fc", "02", "04", "1b"]


def mul(a: int, b: int, poly: int) -> int:
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 0x100:
            a ^= poly
    return out & 0xFF


def pow_gf(a: int, n: int, poly: int) -> int:
    out = 1
    while n:
        if n & 1:
            out = mul(out, a, poly)
        a = mul(a, a, poly)
        n >>= 1
    return out


def irreducible(poly: int) -> bool:
    # A degree-8 binary polynomial is irreducible iff x^(2^8)=x mod f and
    # gcd(x^(2^(8/q))-x, f)=1 for each prime q dividing 8 (q=2).
    def mod_mul(a: int, b: int) -> int:
        out = 0
        while b:
            if b & 1:
                out ^= a
            b >>= 1
            a <<= 1
            if a & 0x100:
                a ^= poly
        return out

    def mod_pow(a: int, n: int) -> int:
        out = 1
        while n:
            if n & 1:
                out = mod_mul(out, a)
            a = mod_mul(a, a)
            n >>= 1
        return out

    def degree(a: int) -> int:
        return a.bit_length() - 1

    def mod_poly(a: int, b: int) -> int:
        while a and degree(a) >= degree(b):
            a ^= b << (degree(a) - degree(b))
        return a

    def gcd(a: int, b: int) -> int:
        while b:
            a, b = b, mod_poly(a, b)
        return a

    x = 2
    if mod_pow(x, 1 << 8) != x:
        return False
    return gcd(mod_pow(x, 1 << 4) ^ x, poly) == 1


def inv(a: int, poly: int) -> int:
    if a == 0:
        raise ZeroDivisionError
    return pow_gf(a, 254, poly)


def lagrange(xs: list[int], ys: list[int], x: int, poly: int) -> int:
    value = 0
    for i, xi in enumerate(xs):
        num = den = 1
        for j, xj in enumerate(xs):
            if i == j:
                continue
            num = mul(num, x ^ xj, poly)
            den = mul(den, xi ^ xj, poly)
        value ^= mul(ys[i], mul(num, inv(den, poly), poly), poly)
    return value


def points(poly: int) -> dict[str, bytes]:
    out = {}
    for label in LABELS:
        x = int(label, 16)
        out[label] = bytes(
            lagrange(XS, [block[i] for block in BLOCKS], x, poly)
            for i in range(16)
        )
    return out


def triangle(leaves: list[bytes]) -> list[list[bytes]]:
    rows = [leaves]
    while len(rows[-1]) > 1:
        rows.append([bytes(a ^ b for a, b in zip(rows[-1][i], rows[-1][i + 1]))
                     for i in range(len(rows[-1]) - 1)])
    return rows


def h160(priv: bytes) -> bytes | None:
    n = int.from_bytes(priv, "big")
    if not 1 <= n < SECP256k1.order:
        return None
    vk = SigningKey.from_string(priv, curve=SECP256k1).verifying_key
    pub = b"\x04" + vk.to_string()
    return hashlib.new("ripemd160", hashlib.sha256(pub).digest()).digest()


def prefix(a: bytes | None) -> int:
    if a is None:
        return -1
    n = 0
    for x, y in zip(a, TARGET_H160):
        if x != y:
            break
        n += 1
    return n


def main() -> int:
    polys = [p for p in range(0x101, 0x200, 2) if p & 1 and irreducible(p)]
    assert len(polys) == 30, len(polys)
    rows = []
    for poly in polys:
        p = points(poly)
        levels = triangle([p[x] for x in HOT_ORDER])
        for li, level in enumerate(levels):
            raw = b"".join(level)
            for name, key in (("sha256", hashlib.sha256(raw).digest()),
                              ("double_sha256", hashlib.sha256(hashlib.sha256(raw).digest()).digest())):
                h = h160(key)
                rows.append({"poly": hex(poly), "level": li, "transform": name,
                             "prefix_bytes": prefix(h), "h160": None if h is None else h.hex()})
    rows.sort(key=lambda r: (r["prefix_bytes"], r["poly"], -r["level"]), reverse=True)
    report = {"polynomial_count": len(polys), "polynomials": [hex(p) for p in polys],
              "hot_order": HOT_ORDER, "best": rows[:20], "exact_matches": [r for r in rows if r["prefix_bytes"] == 20]}
    out = Path(__file__).with_name("gf256_polynomial_probe_report.json")
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"polynomial_count": len(polys), "best": rows[:10],
                      "exact_matches": report["exact_matches"]}, indent=2))
    print("report:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
