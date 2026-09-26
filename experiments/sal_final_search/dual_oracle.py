"""Dual-lock + planted-door offline harness (no network, no broadcast).

Blobs (both 128 b64 chars -> 96 bytes: Salted__ + 8 salt + 80 ct):
  SMALL: SalPhaseIon A+z+B, salt 3ab585348552415d -> TARGET1 1GSMG1JC...
  P32:   phase3.2 tail, salt b45a5e3d827593ca -> same TARGET1 (both locks shape)

Password forms per candidate X: direct X | hexdigest(sha256(X)).
Digests: SHA-256 (creator convention, primary) + MD5 (control).
Mode: AES-256-CBC + PKCS7 (creator convention). Stream modes queued, not here.

Key readings per valid plaintext: sha256(pt), first32, last32, sha256(first64)
  -> uncompressed P2PKH vs TARGET1.
Third door: 6 constructions (sha256 / raw-lpad / raw-rpad / bits-reversed /
  bytes-reversed / sha256-of-reversed) × {compressed, uncompressed} vs planted
  list (9 addresses, 8 known + 1 open). Known preimages re-derived as selftest.
"""
from __future__ import annotations
import base64
import hashlib
import json
from pathlib import Path

import base58
from ecdsa import SECP256k1, SigningKey
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

HERE = Path(__file__).resolve().parent
REGIONS = json.loads((HERE / "sal_regions.json").read_text())["raws"]

BLOB_SMALL = REGIONS["R3B64A_63"] + "z" + REGIONS["R4B64B_64"]
BLOB_P32 = ("U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46z"
            "gKlIi8aaqY5gpJPPEzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4")
TARGET1 = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"
PLANTED = {
    "1AD2wfwXukZ1kUAy848hTQQ72aSBZPB75r": ("sha256", "theflowerblossomsthroughwhatseemstobeaconcretesurface"),
    "1Jqq37KkZEt4F3Dt6qXdtyiMEFBBdawbkJ": ("sha256", "causality"),
    "1K23RS1y2fnuZRkhw5nUpFr5Jk5WN11Zeq": ("sha256", "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"),
    "1GyT5WrLYpwFkuiVoPDJZa1Q6jtjbjuBff": ("sha256", "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"),
    "148XH2YBmLr4oAJXQcG84FpNYoBmqnVPHQ": ("raw", "gsmg.io/theseedisplanted"),
    "13HGhjkmKUkP8sk9k63BLmhkxRjy7uK4Rp": ("bits-reversed", "gsmg.io/theseedisplanted"),
    "1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9": ("unknown", "open: third door"),
}
PHASE2_BLOB = None  # loaded from live capture at runtime (raw/web/live/phase2/response.bin textarea 0)


def _phase2_blob() -> str:
    import re
    from pathlib import Path as _P
    html = (_P(__file__).resolve().parents[2] / "raw/web/live/phase2/response.bin").read_bytes().decode("utf-8", "replace")
    m = re.findall(r"<textarea[^>]*>(.*?)</textarea>", html, re.S)
    return "".join(m[0].split())


def evp(password: bytes, salt: bytes, digest: str):
    H = hashlib.sha256 if digest == "sha256" else hashlib.md5
    d, block = b"", b""
    while len(d) < 48:
        block = H(block + password + salt).digest()
        d += block
    return d[:32], d[32:48]


def dec_blob(blob_b64: str, password: bytes, digest: str):
    raw = base64.b64decode(blob_b64)
    salt, ct = raw[8:16], raw[16:]
    k, iv = evp(password, salt, digest)
    pt = Cipher(algorithms.AES(k), modes.CBC(iv)).decryptor()
    out = pt.update(ct) + pt.finalize()
    pad = out[-1]
    if 1 <= pad <= 16 and out[-pad:] == bytes([pad]) * pad:
        return out[:-pad]
    return None


def readings(pt: bytes):
    out = [("sha256(pt)", hashlib.sha256(pt).digest())]
    if len(pt) >= 32:
        out += [("first32", pt[:32]), ("last32", pt[-32:])]
    if len(pt) >= 64:
        out += [("sha256(first64)", hashlib.sha256(pt[:64]).digest())]
    return out


def priv_to_addrs(priv: bytes):
    sk = SigningKey.from_string(priv, curve=SECP256k1)
    vk = sk.get_verifying_key()
    out = {}
    for comp in (False, True):
        if comp:
            pub = (b"\x02" if vk.pubkey.point.y() % 2 == 0 else b"\x03") + vk.to_string()[:32]
        else:
            pub = b"\x04" + vk.to_string()
        h160 = hashlib.new("ripemd160", hashlib.sha256(pub).digest()).digest()
        out["compressed" if comp else "uncompressed"] = base58.b58encode_check(b"\x00" + h160).decode()
    return out


def bit_reverse_bytes(b: bytes) -> bytes:
    return bytes(int(f"{byte:08b}"[::-1], 2) for byte in b)


def third_door_keys(candidate: str) -> list[tuple[str, bytes]]:
    b = candidate.encode()
    outs = [("sha256", hashlib.sha256(b).digest())]
    if len(b) <= 32:
        outs += [("raw-lpad", b.rjust(32, b"\x00")), ("raw-rpad", b.ljust(32, b"\x00"))]
    if len(b) <= 64:
        outs += [("bits-reversed", bit_reverse_bytes(b).rjust(32, b"\x00")[-32:]),
                 ("bytes-reversed", b[::-1].rjust(32, b"\x00")[-32:]),
                 ("sha256-reversed", hashlib.sha256(b[::-1]).digest())]
    return outs


def attempt_locks(candidate: str) -> tuple[bool, dict]:
    info: dict = {}
    pw_hex = hashlib.sha256(candidate.encode()).hexdigest()
    for blob_name, blob in (("small", BLOB_SMALL), ("p32", BLOB_P32)):
        for form_name, pw in (("hexdigest", pw_hex.encode()), ("direct", candidate.encode())):
            for dg in ("sha256", "md5"):
                pt = dec_blob(blob, pw, dg)
                if pt is None:
                    continue
                for rname, key in readings(pt):
                    if len(key) != 32:
                        continue
                    try:
                        addrs = priv_to_addrs(key)
                    except Exception:
                        continue
                    if addrs["uncompressed"] == TARGET1:
                        return True, {"blob": blob_name, "form": form_name, "digest": dg,
                                      "reading": rname, "priv": key.hex(), "addr": addrs["uncompressed"]}
                info.setdefault("valid_padding", []).append(f"{blob_name}/{form_name}/{dg}")
    return False, info


def attempt_door(candidate: str) -> tuple[bool, dict]:
    for kname, key in third_door_keys(candidate):
        if len(key) != 32 or key == b"\x00" * 32:
            continue
        try:
            addrs = priv_to_addrs(key)
        except Exception:
            continue
        for addr in addrs.values():
            if addr in PLANTED:
                return True, {"construction": kname, "addr": addr, "candidate": candidate[:60]}
    return False, {}


def selftest() -> bool:
    ok = True
    phase2 = _phase2_blob()
    pw = hashlib.sha256(b"causality").hexdigest().encode()
    pt = dec_blob(phase2, pw, "sha256")
    t1 = pt is not None and b"keymakers" in pt
    print(f"phase2-sha256 known-blob: {'OK' if t1 else 'FAIL'}")
    t2 = dec_blob(phase2, pw, "md5") is None
    print(f"phase2-md5 must fail: {'OK' if t2 else 'FAIL'}")
    addrs = priv_to_addrs(hashlib.sha256(b"causality").digest())
    t3 = addrs["compressed"] == "1Jqq37KkZEt4F3Dt6qXdtyiMEFBBdawbkJ"
    print(f"planted causality re-derived: {'OK' if t3 else 'FAIL'} {addrs['compressed']}")
    raw = base64.b64decode(BLOB_SMALL)
    t4 = raw[:8] == b"Salted__" and len(raw) == 96 and raw[8:16].hex() == "3ab585348552415d"
    print(f"small blob shape: {'OK' if t4 else 'FAIL'}")
    raw2 = base64.b64decode(BLOB_P32)
    t5 = raw2[:8] == b"Salted__" and len(raw2) == 96 and raw2[8:16].hex() == "b45a5e3d827593ca"
    print(f"p32 blob shape: {'OK' if t5 else 'FAIL'}")
    ok = t1 and t2 and t3 and t4 and t5
    print("SELFTEST", "OK" if ok else "FAIL")
    return ok
