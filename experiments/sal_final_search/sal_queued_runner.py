"""Queued branches runner: last-words non-literal + Bifid + dropped-29 + esrever.

Uses dual_oracle (both locks x {hexdigest,direct} x {sha256,md5} + third door
6 constructions). Strict EXACT acceptance only. All negatives logged.
"""
from __future__ import annotations
import base64
import hashlib
import json
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dual_oracle as O

HERE = Path(__file__).resolve().parent
REGIONS = json.loads((HERE / "sal_regions.json").read_text())["raws"]
OUT = HERE / "sal_queued_report.json"
ROOT = HERE.parents[1]


def phase_texts() -> dict[str, str]:
    out = {}
    # phase3.2 English head (Architect monologue, before EBCDIC block)
    b = (ROOT / "raw/github/Naddiseo-gsmgio-5btc-puzzle/working/phase3-assets/phase3.2.txt").read_bytes()
    head = b.split(b"\r\n\r\n")[0].decode("utf-8", "replace")
    out["arch_monologue"] = head
    # 149-digit string
    m = re.search(r"\d{100,}", b.decode("latin1"))
    out["digits149"] = m.group(0) if m else ""
    # checkerboard riddle sentence
    txt = b.decode("latin1")
    i = txt.find("Raising the stakes")
    out["riddle"] = txt[i:txt.find("U2Fsd", i)].strip() if i >= 0 else ""
    # live phase2+phase3 plaintexts under known passwords
    html = (ROOT / "raw/web/live/phase2/response.bin").read_bytes().decode("utf-8", "replace")
    tas = re.findall(r"<textarea[^>]*>(.*?)</textarea>", html, re.S)
    blobs = ["".join(t.split()) for t in tas]
    import hashlib as hl
    p2 = O.dec_blob(blobs[0], hl.sha256(b"causality").hexdigest().encode(), "sha256")
    out["phase2pt"] = (p2.decode("utf-8", "replace") if p2 else "")[:4000]
    # phase3 password: 7-part concat sha (community value recomputed if available?)
    out["sal_r3eng"] = REGIONS["R3ENG35"]
    out["sal_r4c"] = REGIONS["R4C12"]
    return out


def nonliteral_forms(text: str) -> list[tuple[str, str]]:
    words = re.findall(r"[A-Za-z0-9]+", text)
    forms = []
    if not words:
        return forms
    for n in (3, 5, 7, 10, 14, 20):
        if len(words) >= n:
            forms.append((f"last{n}", " ".join(words[-n:])))
            forms.append((f"last{n}-nospace-lower", "".join(words[-n:]).lower()))
            forms.append((f"last{n}-initials", "".join(w[0] for w in words[-n:]).lower()))
    forms.append(("full-sha-hex", hashlib.sha256(text.encode()).hexdigest()))
    forms.append(("full-nospace-lower", "".join(words).lower()[:128]))
    # prime-rank chars (1-indexed prime positions)
    def primes(n):
        is_p = bytearray(b"\x01") * (n + 1)
        is_p[0:2] = b"\x00\x00"
        for i in range(2, int(n ** 0.5) + 1):
            if is_p[i]:
                is_p[i * i:n + 1:i] = b"\x00" * ((n - i * i) // i + 1)
        return {i for i, v in enumerate(is_p) if v}
    flat = "".join(words).lower()
    pr = primes(len(flat))
    forms.append(("prime-rank", "".join(ch for i, ch in enumerate(flat, 1) if i in pr)[:128]))
    forms.append(("nonprime-rank", "".join(ch for i, ch in enumerate(flat, 1) if i not in pr)[:128]))
    forms.append(("reversed", text[::-1][:128]))
    return forms


def bifid_decode(msg: str, square: list[str], period: int) -> str:
    """Standard Bifid decode over N=rows*cols square given row-major. period=block len."""
    n = len(square)
    side = int(n ** 0.5)
    assert side * side == n
    pos = {ch: (i // side, i % side) for i, ch in enumerate(square)}
    out = []
    for b in range(0, len(msg), period):
        blk = msg[b:b + period]
        rs = [pos[ch][0] for ch in blk]
        cs = [pos[ch][1] for ch in blk]
        flat = rs + cs
        for i in range(0, len(flat) - 1, 2):
            out.append(square[flat[i] * side + flat[i + 1]])
    return "".join(out)


def main() -> int:
    log: dict = {"attempts": [], "matches": [], "bifid": [], "dropped": [], "esrever": []}
    ncand = 0

    def attempt(family: str, label: str, cand: str):
        nonlocal ncand
        if not (1 <= len(cand) <= 128):
            return
        ncand += 1
        hit_lock, info_lock = O.attempt_locks(cand)
        hit_door, info_door = O.attempt_door(cand)
        rec = {"id": f"Q-{ncand}", "family": family, "label": label,
               "cand": cand[:80], "lock_hit": hit_lock, "lock": info_lock,
               "door_hit": hit_door, "door": info_door, "rank": "NO_MATCH"}
        if hit_lock or hit_door:
            rec["rank"] = "EXACT_MATCH"
            log["matches"].append(rec)
        log["attempts"].append(rec)

    # ---- 1. non-literal last-words ----
    texts = phase_texts()
    for tname, text in texts.items():
        for fname, cand in nonliteral_forms(text):
            attempt("lastwords-nonliteral", f"{tname}:{fname}", cand)

    # ---- 2. Bifid end-to-end (3x3, period 570) ----
    tail = REGIONS["TAIL570"]
    squares = {
        # keyed orders built from DBIFHCEG + A (remaining letter), row-major variants
        "DBG-keyed-A-last": list("dbifhcega"),
        "DBG-alpha": sorted("dbifhcega"),
        "alpha-ai": list("abcdefghi"),
        "rev-ai": list("ihgfedcba"),
    }
    for sqname, sq in squares.items():
        try:
            dec = bifid_decode(tail, sq, 570)
        except Exception as e:
            log["bifid"].append({"square": sqname, "error": str(e)})
            continue
        up = dec.upper()
        printable = sum(1 for c in dec if c.isprintable()) / max(1, len(dec))
        has_btc = "BTCSEED" in up or "BTC" in up
        log["bifid"].append({"square": sqname, "head": dec[:80], "up_head": up[:80],
                             "btcseed": has_btc, "printable": round(printable, 3)})
        # feed outputs (raw + upper + digit-mapped) to harness
        attempt("bifid", f"{sqname}:raw", dec[:128])
        attempt("bifid", f"{sqname}:upper", up[:128])

    # ---- 3. dropped-29: remove I/O from candidate streams ----
    for sname in ("TAIL570", "LEAD91", "R1_63", "R2_29"):
        s = REGIONS[sname]
        dropped = "".join(ch for ch in s if ch.lower() in ("i", "o"))
        kept = "".join(ch for ch in s if ch.lower() not in ("i", "o"))
        log["dropped"].append({"stream": sname, "kept_len": len(kept),
                               "dropped_len": len(dropped), "dropped_head": dropped[:80]})
        attempt("dropped29", f"{sname}:kept", kept[:128])
        attempt("dropped29", f"{sname}:dropped-as-message", dropped[:128])

    # ---- 4. esrever ----
    for sname in ("LEAD91", "TAIL570", "R1_63", "R2_29", "R3B64A_63", "R4B64B_64"):
        s = REGIONS[sname]
        attempt("esrever", f"{sname}:reversed", s[::-1][:128])
    attempt("esrever", "url:reversed", "gsmg.io/theseedisplanted"[::-1])
    attempt("esrever", "blob-small:reversed", (REGIONS["R3B64A_63"] + "z" + REGIONS["R4B64B_64"])[::-1][:128])

    OUT.write_text(json.dumps(log, indent=2))
    print(f"queued: {len(log['attempts'])} harness attempts, matches={len(log['matches'])}")
    for b in log["bifid"]:
        print("BIFID", b["square"], "btcseed=", b.get("btcseed"), "head=", b.get("up_head", "")[:70])
    for d in log["dropped"]:
        print("DROPPED", d["stream"], "kept=", d["kept_len"], "dropped=", d["dropped_len"], repr(d["dropped_head"][:50]))
    vp = [a for a in log["attempts"] if "valid_padding" in json.dumps(a.get("lock", {}))]
    print(f"valid paddings: {len(vp)}")
    for a in vp[:10]:
        print("VPAD", a["id"], a["family"], a["label"], a["lock"])
    return 0 if not log["matches"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
