"""Bounded order-preserving and Genesis-3x23 candidate battery.

This deliberately tests only transformations motivated by the surviving clues:
the 16x16/23-symbol even stream and the exact 3x23 Genesis source rectangle.
Acceptance is delegated to the existing dual-lock/third-door oracle.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "sal_final_search"))
import dual_oracle as O  # noqa: E402
from sal_bifid import bifid_decode, build_square, first_occurrence_key, load_lead, load_tail  # noqa: E402


ALPHA = "ABCDEFGHKLMNPQRSTUVWXYZ"  # A-Z minus I/J/O, exactly 23 symbols
GENESIS_HEX = (
    "736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E616843"
    "20393030322F6E614A2F33302073656D695420656854"
)


def put(out: dict[str, str], label: str, value: str) -> None:
    if value and len(value) <= 10000:
        out.setdefault(label, value)


def encode_nums(nums: list[int], mode: str) -> str:
    if mode == "letters":
        return "".join(ALPHA[n % 23] for n in nums)
    if mode == "lower":
        return "".join(ALPHA[n % 23].lower() for n in nums)
    if mode == "decimal":
        return ",".join(str(n) for n in nums)
    if mode == "decimal-tight":
        return "".join(str(n) for n in nums)
    if mode == "hex":
        return bytes(n % 256 for n in nums).hex()
    raise ValueError(mode)


def spiral_coords(rows: int, cols: int, clockwise: bool = True) -> list[tuple[int, int]]:
    top, left, bottom, right = 0, 0, rows - 1, cols - 1
    out: list[tuple[int, int]] = []
    while top <= bottom and left <= right:
        if clockwise:
            out += [(top, c) for c in range(left, right + 1)]
            out += [(r, right) for r in range(top + 1, bottom + 1)]
            if top < bottom:
                out += [(bottom, c) for c in range(right - 1, left - 1, -1)]
            if left < right:
                out += [(r, left) for r in range(bottom - 1, top, -1)]
        else:
            out += [(r, left) for r in range(top, bottom + 1)]
            out += [(bottom, c) for c in range(left + 1, right + 1)]
            if top < bottom:
                out += [(r, right) for r in range(bottom - 1, top - 1, -1)]
            if left < right:
                out += [(top, c) for c in range(right - 1, left, -1)]
        top, left, bottom, right = top + 1, left + 1, bottom - 1, right - 1
    return out


def grid_candidates(even: str) -> dict[str, str]:
    out: dict[str, str] = {}
    nums = [ALPHA.index(c) for c in even]
    put(out, "even/raw", even)
    put(out, "even/reverse", even[::-1])
    put(out, "even/lower", even.lower())

    # Adjacent and second-order differences preserve sequence but change symbols.
    for name, seq in (
        ("d1", [(b - a) % 23 for a, b in zip(nums, nums[1:])]),
        ("d2", [(c - 2 * b + a) % 23 for a, b, c in zip(nums, nums[1:], nums[2:])]),
        ("abs-d1", [abs(b - a) for a, b in zip(nums, nums[1:])]),
    ):
        for mode in ("letters", "lower", "decimal", "decimal-tight", "hex"):
            put(out, f"even/{name}/{mode}", encode_nums(seq, mode))

    # 16x16 route changes: row/column, snake, dihedral row-major, spiral.
    def at(coords: list[tuple[int, int]]) -> str:
        return "".join(even[r * 16 + c] for r, c in coords)

    row = [(r, c) for r in range(16) for c in range(16)]
    col = [(r, c) for c in range(16) for r in range(16)]
    snake_r = [(r, c if r % 2 == 0 else 15 - c) for r in range(16) for c in range(16)]
    snake_c = [(r if c % 2 == 0 else 15 - r, c) for c in range(16) for r in range(16)]
    routes = {"row": row, "col": col, "snake-row": snake_r, "snake-col": snake_c}
    routes["spiral-row"] = spiral_coords(16, 16, True)
    routes["spiral-col"] = spiral_coords(16, 16, False)
    for name, coords in routes.items():
        put(out, f"grid/{name}", at(coords))
        put(out, f"grid/{name}/reverse", at(coords)[::-1])
    for flip_r, flip_c, transpose in itertools.product((False, True), repeat=3):
        coords = []
        for r in range(16):
            for c in range(16):
                rr, cc = (c, r) if transpose else (r, c)
                if flip_r:
                    rr = 15 - rr
                if flip_c:
                    cc = 15 - cc
                coords.append((rr, cc))
        put(out, f"grid/dihedral/{int(flip_r)}{int(flip_c)}{int(transpose)}", at(coords))

    # Run lengths and 23x23 transition counts are order-derived, not bag counts.
    runs: list[str] = []
    i = 0
    while i < len(even):
        j = i + 1
        while j < len(even) and even[j] == even[i]:
            j += 1
        runs.append(f"{even[i]}{j - i}")
        i = j
    put(out, "even/runs", "".join(runs))
    put(out, "even/runs-delimited", ",".join(runs))
    trans = [[0] * 23 for _ in range(23)]
    for a, b in zip(nums, nums[1:]):
        trans[a][b] += 1
    flat = [x for row_ in trans for x in row_]
    for mode in ("letters", "decimal", "decimal-tight", "hex"):
        put(out, f"even/transitions/row/{mode}", encode_nums(flat, mode))
        put(out, f"even/transitions/row-reverse/{mode}", encode_nums(flat[::-1], mode))
        transposed = [trans[r][c] for c in range(23) for r in range(23)]
        put(out, f"even/transitions/col/{mode}", encode_nums(transposed, mode))
    return out


def genesis_candidates() -> dict[str, str]:
    source = bytes.fromhex(GENESIS_HEX).decode()[::-1]
    assert len(source.encode()) == 69
    rect = [list(source[r * 23:(r + 1) * 23]) for r in range(3)]
    out: dict[str, str] = {}

    def emit(label: str, value: str) -> None:
        variants = {
            "raw": value,
            "compact": "".join(value.split()),
            "lower": value.lower(),
            "upper": value.upper(),
        }
        for suffix, v in variants.items():
            put(out, f"genesis/{label}/{suffix}", v)
            put(out, f"genesis/{label}/{suffix}/reverse", v[::-1])
            put(out, f"genesis/{label}/{suffix}/sha256", hashlib.sha256(v.encode()).hexdigest())

    def route(coords: list[tuple[int, int]]) -> str:
        return "".join(rect[r][c] for r, c in coords)

    row = [(r, c) for r in range(3) for c in range(23)]
    col = [(r, c) for c in range(23) for r in range(3)]
    snake_r = [(r, c if r % 2 == 0 else 22 - c) for r in range(3) for c in range(23)]
    snake_c = [(r if c % 2 == 0 else 2 - r, c) for c in range(23) for r in range(3)]
    emit("row", route(row)); emit("col", route(col)); emit("snake-row", route(snake_r)); emit("snake-col", route(snake_c))
    emit("spiral", route(spiral_coords(3, 23, True)))
    emit("spiral-ccw", route(spiral_coords(3, 23, False)))
    for rows in itertools.permutations(range(3)):
        for rev in (False, True):
            coords = [(r, 22 - c if rev else c) for r in rows for c in range(23)]
            emit(f"rows-{''.join(map(str, rows))}-rev{int(rev)}", route(coords))
    # Evidence-grounded 23-column cyclic routes; no arbitrary full permutation search.
    for shift in range(23):
        coords = [(r, (c + shift) % 23) for r in range(3) for c in range(23)]
        emit(f"column-shift-{shift}", route(coords))
    # Caesar family over letters, preserving spaces and punctuation.
    compact = "".join(source.split())
    for k in range(23):
        shifted = "".join(chr((ord(c.upper()) - 65 + k) % 26 + 65) if c.isalpha() else c for c in compact)
        emit(f"caesar-{k}", shifted)
    return out


def main() -> int:
    assert O.selftest()
    lead, tail = load_lead(), load_tail()
    bifid = bifid_decode(tail, build_square(first_occurrence_key(lead)), len(tail))
    even = "".join(c for c in bifid[1::2] if c not in "IO")
    candidates = grid_candidates(even)
    candidates.update(genesis_candidates())
    hits: list[dict[str, object]] = []
    valid_padding = 0
    for label, candidate in candidates.items():
        ok_lock, lock_info = O.attempt_locks(candidate)
        ok_door, door_info = O.attempt_door(candidate)
        valid_padding += len(lock_info.get("valid_padding", []))
        if ok_lock or ok_door:
            hits.append({"label": label, "candidate": candidate, "lock": lock_info, "door": door_info})
    report = {
        "candidate_count": len(candidates),
        "valid_padding_events": valid_padding,
        "hits": hits,
        "even256_sha256": hashlib.sha256(even.encode()).hexdigest(),
        "genesis_source": bytes.fromhex(GENESIS_HEX).decode()[::-1],
    }
    out = HERE / "order_genesis_battery_report.json"
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"candidate_count": len(candidates), "valid_padding_events": valid_padding, "hits": hits}, indent=2))
    print("report:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
