"""Offline Bitcoin compact-signature verification (no Core, no network)."""
import base64
import hashlib
import sys

import base58
from ecdsa import SECP256k1, VerifyingKey, util


def btc_verify(addr: str, sig_b64: str, message: str) -> str:
    raw = base64.b64decode(sig_b64)
    if len(raw) != 65:
        return f"INVALID-LEN {len(raw)}"
    header, sig = raw[0], raw[1:]
    if not 27 <= header <= 42:
        return f"INVALID-HEADER {header}"
    compressed = bool(header & 4)
    msg = b"Bitcoin Signed Message:\n" + bytes([len(message.encode())]) + message.encode()
    h = hashlib.sha256(hashlib.sha256(msg).digest()).digest()
    try:
        vks = VerifyingKey.from_public_key_recovery_with_digest(
            sig, h, SECP256k1, hashfunc=hashlib.sha256, sigdecode=util.sigdecode_string)
    except Exception as e:  # noqa: BLE001
        return f"RECOVER-FAIL {e}"
    addrs = []
    for vk in vks:
        s = vk.to_string()
        pub = ((b"\x02" if vk.pubkey.point.y() % 2 == 0 else b"\x03") + s[:32]) if compressed else (b"\x04" + s)
        a = base58.b58encode_check(b"\x00" + hashlib.new("ripemd160", hashlib.sha256(pub).digest()).digest()).decode()
        addrs.append(a)
        if a == addr:
            return f"VALID (compressed={compressed})"
    return f"INVALID recovered={addrs}"


if __name__ == "__main__":
    msg = "GSMG PUZZLE PHASE 3 SOLVED - HALF & BETTER HALF DERIVED FROM COSMIC DUALITY MATRIX"
    print("half  :", btc_verify("1JG648yaB7Wp2dpUfcZoRSD4q35oq47vCu",
          "H0J8rDTlveWI92nJZzCheBfpwpJqg85MJkFJpid+HNorm86L/gMR7dGKpBxjJiFUjN3di+cK6cqaAvJReUVg63w=", msg))
    print("better:", btc_verify("145ZQ9siLrsXBKf465wjdyQYAP5dRwhRhQ",
          "H931mqgbkoGbuip5/3Musu5Bn+YmurkCC249Y1l/JZL57/tW4XAzsJuF7mMWu5bqL8RFqPcwN0/E1i7FrNabdTc=", msg))
