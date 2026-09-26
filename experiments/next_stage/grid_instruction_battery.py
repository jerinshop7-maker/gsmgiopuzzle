"""Evidence-bounded test of the literal final-page instruction on puzzle.png.

This is deliberately small: the canonical 14x14 image object is converted to
the already-proven black/blue=1, white/yellow=0 matrix, then only explicit
matrix-sum, prime-position, zeroing, colour-frame, and yin/yang operations are
serialized.  It uses the existing exact dual-lock and third-door oracle.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
IMAGE = ROOT / "raw/github/puzzlehunt-gsmgio-5btc-puzzle/working/puzzle.png"
OUT = Path(__file__).with_name("grid_instruction_battery_report.json")
sys.path.insert(0, str(ROOT / "experiments/sal_final_search"))
import dual_oracle as O  # noqa: E402


def primes(n: int) -> set[int]:
    p = set(range(2, n + 1))
    for x in range(2, int(n**0.5) + 1):
        if x in p:
            p.difference_update(range(x * x, n + 1, x))
    return p


def image_matrix() -> tuple[list[list[int]], list[list[str]]]:
    im = Image.open(IMAGE).convert("RGB")
    # The canonical image's grid occupies the top 14*75 rows.  Classify each
    # cell by its dominant exact canonical fill; center sampling is unsafe
    # because the bunny line-art crosses at least one cell center.
    fills = {
        (255, 255, 255): "W",
        (0, 0, 0): "K",
        (63, 72, 204): "B",
        (255, 242, 0): "Y",
    }
    M: list[list[int]] = []
    C: list[list[str]] = []
    for r in range(14):
        mr, cr = [], []
        for c in range(14):
            x0, x1 = round(c * im.width / 14), round((c + 1) * im.width / 14)
            y0, y1 = r * 75, (r + 1) * 75
            cell = list(im.crop((x0, y0, x1, y1)).getdata())
            counts = Counter(cell)
            fill = fills[max(fills, key=lambda rgb: counts[rgb])]
            cr.append(fill)
            mr.append(1 if fill in "KB" else 0)
        M.append(mr)
        C.append(cr)
    return M, C


def flat(M: list[list[int]]) -> list[int]:
    return [x for row in M for x in row]


def spiral(n: int) -> list[tuple[int, int]]:
    """The proven down-first counterclockwise route used by puzzle.png."""
    out: list[tuple[int, int]] = []
    top, bottom, left, right = 0, n - 1, 0, n - 1
    while left <= right and top <= bottom:
        for r in range(top, bottom + 1):
            out.append((r, left))
        left += 1
        for c in range(left, right + 1):
            out.append((bottom, c))
        bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                out.append((r, right))
            right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                out.append((top, c))
            top += 1
    return out


def serialize(name: str, values: list[int]) -> dict[str, str]:
    # All forms are transparent encodings of the same small integer list.
    raw = "".join(map(str, values))
    delim = ",".join(map(str, values))
    forms = {
        f"{name}:digits": raw,
        f"{name}:csv": delim,
        f"{name}:hex": bytes(v & 0xff for v in values).hex(),
        f"{name}:ascii+48": bytes((v + 48) & 0xff for v in values).decode("latin1"),
        f"{name}:ascii+80": bytes((v + 80) & 0xff for v in values).decode("latin1"),
    }
    return forms


def add_matrix_forms(dst: dict[str, str], name: str, M: list[list[int]]) -> None:
    rows = [sum(row) for row in M]
    cols = [sum(M[r][c] for r in range(14)) for c in range(14)]
    pairs = {
        "rows": rows,
        "cols": cols,
        "rows-cols": [a - b for a, b in zip(rows, cols)],
        "cols-rows": [b - a for a, b in zip(rows, cols)],
        "rows+cols": rows + cols,
        "cols+rows": cols + rows,
        "row-col-pair-sum": [a + b for a, b in zip(rows, cols)],
        "row-col-pair-diff": [a - b for a, b in zip(rows, cols)],
        "row-col-pair-xor": [a ^ b for a, b in zip(rows, cols)],
    }
    for suffix, values in pairs.items():
        dst.update(serialize(f"{name}/{suffix}", values))


def main() -> int:
    M, C = image_matrix()
    known = [
        [int(x) for x in row]
        for row in [
            "00110100101100", "11110011101011", "11011101001001",
            "01101000011101", "01100011000110", "10011000100011",
            "10011100010000", "11100000001000", "00011101111101",
            "11111100110001", "11010000011011", "11110010101100",
            "01011101000110", "01101101101011",
        ]
    ]
    report: dict = {"image_sha256": hashlib.sha256(IMAGE.read_bytes()).hexdigest(),
                    "grid_match_published_copy": M == known,
                    "published_copy_differences_1based": [
                        i + 1 for i, (a, b) in enumerate(zip(flat(M), flat(known))) if a != b
                    ],
                    "candidates": [],
                    "matches": [], "valid_padding": []}

    vals: dict[str, str] = {}
    rows = M
    cols = [[M[r][c] for r in range(14)] for c in range(14)]
    p196 = primes(196)
    p14 = primes(14)
    arrays = {
        "rows": [sum(x) for x in rows],
        "cols": [sum(x) for x in cols],
        "rows+cols": [sum(x) for x in rows] + [sum(x) for x in cols],
        "rows-cols": [sum(rows[i]) - sum(cols[i]) for i in range(14)],
        "cols-rows": [sum(cols[i]) - sum(rows[i]) for i in range(14)],
        "flat-prime-values": [v for i, v in enumerate(flat(M), 1) if i in p196],
        "flat-nonprime-values": [v for i, v in enumerate(flat(M), 1) if i not in p196],
        "flat-prime-zero": [v if i in p196 else 0 for i, v in enumerate(flat(M), 1)],
        "flat-nonprime-zero": [v if i not in p196 else 0 for i, v in enumerate(flat(M), 1)],
        "flat-reverse": flat(M)[::-1],
    }
    order = spiral(14)
    sflat = [M[r][c] for r, c in order]
    arrays.update({
        "spiral-bits": sflat,
        "spiral-prime-zero": [v if i in p196 else 0 for i, v in enumerate(sflat, 1)],
        "spiral-nonprime-zero": [v if i not in p196 else 0 for i, v in enumerate(sflat, 1)],
    })
    for s in ("normal", "reverse"):
        for name, arr in list(arrays.items()):
            a = arr[::-1] if s == "reverse" else arr
            for k, v in serialize(f"{s}/{name}", a).items():
                vals[k] = v

    # Apply the same finite operations to the matrix *after* zeroing.  This
    # matters: “zeroed out” is an operation on the object before
    # matrixsumlist, not merely a way to print a selected substring.
    base_matrices: dict[str, list[list[int]]] = {
        "raw": M,
        "yin": [[1 - x for x in row] for row in M],
    }
    raster = flat(M)
    prime_raster = [v if i in p196 else 0 for i, v in enumerate(raster, 1)]
    nonprime_raster = [v if i not in p196 else 0 for i, v in enumerate(raster, 1)]
    prime_spiral = [v if i in p196 else 0 for i, v in enumerate(sflat, 1)]
    nonprime_spiral = [v if i not in p196 else 0 for i, v in enumerate(sflat, 1)]
    for name, bits in {
        "prime-raster-zero": prime_raster,
        "nonprime-raster-zero": nonprime_raster,
        "prime-spiral-zero": prime_spiral,
        "nonprime-spiral-zero": nonprime_spiral,
    }.items():
        base_matrices[name] = [bits[14 * r:14 * (r + 1)] for r in range(14)]
    for name, base in base_matrices.items():
        mats = {
            "id": base,
            "hflip": [row[::-1] for row in base],
            "vflip": base[::-1],
            "rot180": [row[::-1] for row in base[::-1]],
            "transpose": [[base[r][c] for r in range(14)] for c in range(14)],
        }
        for sym, mat in mats.items():
            add_matrix_forms(vals, f"matrix/{name}/{sym}", mat)

    # Yin/yang: complementary matrix, row/column sum pairs, and colour-only
    # blue/yellow frame in spiral order.  These are the direct interpretations
    # of the author-named words, not arbitrary hashes or permutations.
    comp = [[1 - x for x in row] for row in M]
    cr = [sum(x) for x in rows]
    cc = [sum(x) for x in cols]
    kr = [sum(x) for x in comp]
    kc = [sum(x) for x in zip(*comp)]
    for name, arr in {
        "yin-yang-row-sums": cr + kr,
        "yin-yang-col-sums": cc + kc,
        "yin-yang-row-diff": [a - b for a, b in zip(cr, kr)],
        "yin-yang-col-diff": [a - b for a, b in zip(cc, kc)],
        "yin-yang-row-xor": [a ^ b for a, b in zip(cr, kr)],
        "yin-yang-col-xor": [a ^ b for a, b in zip(cc, kc)],
    }.items():
        vals.update(serialize(name, arr))
    colour = [C[r][c] for r in range(14) for c in range(14)]
    vals["colors/raw"] = "".join(colour)
    vals["colors/by"] = "".join("1" if x == "B" else "0" for x in colour if x in "BY")
    scolour = [C[r][c] for r, c in order]
    vals["colors/spiral"] = "".join(scolour)
    vals["colors/spiral-by"] = "".join("1" if x == "B" else "0" for x in scolour if x in "BY")
    vals["colors/prime-ranks"] = "".join("1" if colour[i - 1] == "B" else "0"
                                            for i in sorted(p196) if colour[i - 1] in "BY")
    vals["colors/prime-ranks-zero-nonBY"] = "".join(
        "1" if i in p196 and colour[i - 1] == "B" else "0" for i in range(1, 197)
    )

    # Deduplicate exact candidate bytes while retaining provenance.
    by_value: dict[str, list[str]] = {}
    for label, value in vals.items():
        if 1 <= len(value) <= 128:
            by_value.setdefault(value, []).append(label)
    for value, labels in by_value.items():
        hit_lock, info_lock = O.attempt_locks(value)
        hit_door, info_door = O.attempt_door(value)
        rec = {"labels": labels, "candidate": value, "lock_hit": hit_lock,
               "door_hit": hit_door, "lock": info_lock, "door": info_door}
        report["candidates"].append({"labels": labels, "length": len(value),
                                     "sha256": hashlib.sha256(value.encode()).hexdigest(),
                                     "lock_hit": hit_lock, "door_hit": hit_door})
        if "valid_padding" in json.dumps(info_lock):
            report["valid_padding"].append(rec)
        if hit_lock or hit_door:
            report["matches"].append(rec)
    report["candidate_count"] = len(report["candidates"])
    OUT.write_text(json.dumps(report, indent=2))
    print("grid matches published copy:", report["grid_match_published_copy"],
          "differences:", report["published_copy_differences_1based"],
          "candidates:", report["candidate_count"],
          "valid paddings:", len(report["valid_padding"]), "matches:", len(report["matches"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
