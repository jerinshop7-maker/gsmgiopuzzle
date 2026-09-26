"""Audit the two original image attachments from GitHub issue #67.

The issue calls out a ``merlon`` in the QR-like object and supplies a second
colour-marked rendering.  This runner treats the attachment as a separate
research object, never as the canonical puzzle grid.  It extracts the
deterministic 14x14 crop visible in the colour rendering and tests only direct
symbol/mask/route encodings against the exact offline oracles.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
IMAGE = ROOT / "raw/github/puzzlehunt-gsmgio-5btc-puzzle/issues/67/attachments/merlon_colors.png"
OUT = HERE / "issue67_merlon_battery_report.json"
sys.path.insert(0, str(ROOT / "experiments/sal_final_search"))
import dual_oracle as O  # noqa: E402


def crop_grid() -> list[list[str]]:
    im = Image.open(IMAGE).convert("RGB")
    # The attachment's marked object is exactly 560x560 at (118,118), i.e.
    # fourteen 40px modules.  This is an attachment-local crop, not puzzle
    # ground truth.
    x0, y0, size, n = 118, 118, 560, 14
    fills = {(255, 50, 50): "R", (255, 255, 240): "W", (30, 30, 60): "K"}
    out = []
    for r in range(n):
        row = []
        for c in range(n):
            box = (x0 + c * 40, y0 + r * 40, x0 + (c + 1) * 40, y0 + (r + 1) * 40)
            counts = Counter(im.crop(box).getdata())
            row.append(fills[max(fills, key=lambda rgb: counts[rgb])])
        out.append(row)
    return out


def routes(m: list[list[str]]) -> dict[str, str]:
    n = len(m)
    mats = {
        "id": m,
        "hflip": [row[::-1] for row in m],
        "vflip": m[::-1],
        "rot180": [row[::-1] for row in m[::-1]],
    }
    mats["transpose"] = [[m[r][c] for r in range(n)] for c in range(n)]
    out = {}
    for name, mat in mats.items():
        out[name] = "".join("".join(row) for row in mat)
    return out


def spiral(m: list[list[str]]) -> str:
    n = len(m)
    out = []
    top, bottom, left, right = 0, n - 1, 0, n - 1
    while left <= right and top <= bottom:
        for r in range(top, bottom + 1): out.append(m[r][left])
        left += 1
        for c in range(left, right + 1): out.append(m[bottom][c])
        bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1): out.append(m[r][right])
            right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1): out.append(m[top][c])
            top += 1
    return "".join(out)


def emit(out: dict[str, str], label: str, value: str) -> None:
    if value:
        out.setdefault(label, value)


def packed(bits: str, lsb_first: bool = False) -> bytes:
    """Pack complete 8-bit groups; the 4-bit tail is intentionally dropped."""
    out = bytearray()
    for i in range(0, len(bits) - 7, 8):
        group = bits[i:i + 8]
        if lsb_first:
            group = group[::-1]
        out.append(int(group, 2))
    return bytes(out)


def build(m: list[list[str]]) -> dict[str, str]:
    out: dict[str, str] = {}
    base_routes = routes(m)
    base_routes["spiral"] = spiral(m)
    for rname, s in base_routes.items():
        emit(out, f"symbols/{rname}", s)
        emit(out, f"symbols/{rname}/reverse", s[::-1])
        for symbol in "RWK":
            emit(out, f"mask/{symbol}/{rname}", "".join("1" if x == symbol else "0" for x in s))
        for perm in itertools.permutations("RWK"):
            code = {ch: str(i) for i, ch in enumerate(perm)}
            emit(out, f"ternary/{''.join(perm)}/{rname}", "".join(code[x] for x in s))

    # The merlon is the non-central colour pattern.  Keep the crop rule
    # explicit: remove the central 8x8 black chamber, then preserve route.
    perimeter = [m[r][c] for r in range(14) for c in range(14)
                 if not (3 <= r < 11 and 3 <= c < 11)]
    for name, s in {"raster": "".join(perimeter), "spiral": "".join(
        x for i, x in enumerate(base_routes["spiral"]) if not (3 <= i // 14 < 11 and 3 <= i % 14 < 11)
    )}.items():
        emit(out, f"perimeter/symbols/{name}", s)
        for pair in ("RW", "WR"):
            emit(out, f"perimeter/{pair}/{name}", "".join("1" if x == pair[0] else "0" for x in s if x in pair))

    # A colour-play object can reasonably be read as packed bits.  Enumerate
    # only the six nonconstant assignments of R/W/K to {0,1}; this is a finite
    # representation check, not a key search.  The byte output is kept as
    # Latin-1 text for the existing text oracle and is also checked as raw
    # SHA-256 bytes below.
    for rname, s in base_routes.items():
        for ones in ("R", "W", "K"):
            for zeros in ("R", "W", "K"):
                if ones == zeros:
                    continue
                bits = "".join("1" if x == ones else "0" for x in s)
                for lsb in (False, True):
                    raw = packed(bits, lsb)
                    tag = f"packed/{ones}{zeros}/{rname}/{'lsb' if lsb else 'msb'}"
                    emit(out, tag + "/bits", bits)
                    emit(out, tag + "/latin1", raw.decode("latin1"))
                    emit(out, tag + "/hex", raw.hex())

    # Row/column symbol counts are the attachment-local analogue of the
    # puzzle's matrixsumlist, retained as decimal lists only.
    for axis, seqs in (("rows", m), ("cols", [[m[r][c] for r in range(14)] for c in range(14)])):
        for symbol in "RWK":
            vals = [sum(x == symbol for x in seq) for seq in seqs]
            emit(out, f"counts/{axis}/{symbol}/digits", "".join(map(str, vals)))
            emit(out, f"counts/{axis}/{symbol}/csv", ",".join(map(str, vals)))
    return out


def main() -> int:
    assert O.selftest()
    m = crop_grid()
    candidates = build(m)
    hits, padding, direct_target = [], [], []
    for label, candidate in candidates.items():
        lock, info = O.attempt_locks(candidate)
        door, dinfo = O.attempt_door(candidate)
        if info.get("valid_padding"):
            padding.extend({"label": label, "event": x} for x in info["valid_padding"])
        if lock or door:
            hits.append({"label": label, "candidate": candidate, "lock": info, "door": dinfo})
        for digest_name, digest in (("sha256", hashlib.sha256(candidate.encode()).digest()),):
            try:
                addrs = O.priv_to_addrs(digest)
            except Exception:
                continue
            if addrs["uncompressed"] == O.TARGET1:
                direct_target.append({"label": label, "digest": digest_name})
    report = {
        "attachment_sha256": hashlib.sha256(IMAGE.read_bytes()).hexdigest(),
        "crop": {"x": 118, "y": 118, "size": 560, "modules": 14, "module_size": 40},
        "grid": ["".join(row) for row in m],
        "symbol_counts": Counter("".join("".join(row) for row in m)),
        "candidate_count": len(candidates),
        "valid_padding_events": len(padding),
        "hits": hits,
        "direct_target_hits": direct_target,
        "interpretation": "Attachment-local direct encodings only; no canonical-grid claim.",
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("grid", "symbol_counts", "candidate_count", "valid_padding_events", "hits")}, indent=2))
    print("report:", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
