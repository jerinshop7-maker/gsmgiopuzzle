"""Derive a P2PKH Bitcoin address from a private key and compare to a target.

Used to test whether a candidate private key controls the prize address.
A valid secp256k1 scalar that does NOT derive the target is a decoy or
intermediate, not a solution.
"""

from __future__ import annotations

import argparse
import hashlib

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def inv(a: int, m: int) -> int:
    return pow(a, m - 2, m)


def pt_add(ax: int | None, ay: int | None, bx: int | None, by: int | None):
    if ax is None:
        return bx, by
    if bx is None:
        return ax, ay
    if ax == bx and ay == by:
        lam = (3 * ax * ax) * inv(2 * ay, P) % P
    else:
        lam = (by - ay) * inv(bx - ax, P) % P
    rx = (lam * lam - ax - bx) % P
    ry = (lam * (ax - rx) - ay) % P
    return rx, ry


def scalar_mult(k: int):
    rx, ry = None, None
    qx, qy = GX, GY
    while k:
        if k & 1:
            rx, ry = pt_add(rx, ry, qx, qy)
        qx, qy = pt_add(qx, qy, qx, qy)
        k >>= 1
    return rx, ry


def hash160(data: bytes) -> bytes:
    return hashlib.new("ripemd160", hashlib.sha256(data).digest()).digest()


def b58check(payload: bytes) -> str:
    raw = payload + hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    n = int.from_bytes(raw, "big")
    s = ""
    while n:
        s = ALPHABET[n % 58] + s
        n //= 58
    pad = len(payload) - len(payload.lstrip(b"\x00"))
    return "1" * pad + s


def privkey_to_address(hexkey: str, compressed: bool = True) -> str:
    k = int.from_bytes(bytes.fromhex(hexkey), "big")
    x, y = scalar_mult(k)
    if compressed:
        prefix = b"\x02" if y % 2 == 0 else b"\x03"
        pubkey = prefix + x.to_bytes(32, "big")
    else:
        pubkey = b"\x04" + x.to_bytes(32, "big") + y.to_bytes(32, "big")
    return b58check(b"\x00" + hash160(pubkey))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hexkey", required=True, help="Candidate private key hex.")
    parser.add_argument("--target", required=True, help="Target prize address.")
    args = parser.parse_args(argv)

    value = int.from_bytes(bytes.fromhex(args.hexkey), "big")
    valid = 0 < value < N
    print(f"valid secp256k1 scalar: {valid}")
    for compressed in (True, False):
        address = privkey_to_address(args.hexkey, compressed=compressed)
        match = address == args.target
        print(f"compressed={compressed}: {address}  {'MATCH' if match else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
