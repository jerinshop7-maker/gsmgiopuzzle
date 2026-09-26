"""Pixel-grounded 14x14 grid extraction from the live puzzle capture (ART-001).

Method (no copied matrices):
  1. Grid geometry discovered from pixels: 75px-pitch lattice, origin (0,0),
     top-justified (rows y=0..1050 of the 1048x1556 capture; photo/QR below).
     Blue/yellow calibration quads (75x75, contour-detected) sit exactly on it.
  2. Each cell is classified by the dominant exact canonical fill in its
     75x75 cell crop.  The black bunny line-art overlays some cell centers,
     so center sampling can falsely turn a white background cell into black.
     Canonical fills are W=(255,255,255), K=(0,0,0), B=(63,72,204), and
     Y=(255,242,0).
  3. Down-first counterclockwise inward spiral from (0,0), K/B=1, W/Y=0.

Verified output (2026-09-11, sha 38125bbd... bytes):
  counts K=86/W=86/B=15/Y=9, spiral -> 'gsmg.io/theseedisplanted' + '0000'
  leftover, B/Y frame at spiral idx 7,15,...,191 == URL LSBs exactly.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None  # type: ignore

import numpy as np

GRID_N = 14
PITCH_Y = 75.0

EXPECTED_URL = "gsmg.io/theseedisplanted"
EXPECTED_FRAME = "111101110011110110010010"
EXPECTED_COUNTS = {"K": 86, "W": 86, "B": 15, "Y": 9}
EXPECTED_ROW_YELLOW_MASK = "010000011101010001100100"  # 0x41D464


def load_pixels(path: str | Path) -> np.ndarray:
    assert Image is not None, "Pillow required"
    return np.asarray(Image.open(path).convert("RGB")).astype(int)


CANONICAL = {
    (255, 255, 255): "W",
    (0, 0, 0): "K",
    (63, 72, 204): "B",
    (255, 242, 0): "Y",
}


def classify(cell: np.ndarray) -> str:
    counts = Counter(map(tuple, cell.reshape(-1, 3)))
    available = {rgb: counts[rgb] for rgb in CANONICAL}
    return CANONICAL[max(available, key=available.get)]


def extract_matrix(px: np.ndarray) -> list[list[str]]:
    h, w, _ = px.shape
    pitch_x = w / GRID_N
    grid: list[list[str]] = []
    for j in range(GRID_N):
        row: list[str] = []
        for i in range(GRID_N):
            x0, x1 = round(i * pitch_x), round((i + 1) * pitch_x)
            y0, y1 = round(j * PITCH_Y), round((j + 1) * PITCH_Y)
            row.append(classify(px[y0:y1, x0:x1]))
        grid.append(row)
    return grid


def spiral_read(grid: list[list[str]]) -> list[str]:
    n = len(grid)
    seen = [[False] * n for _ in range(n)]
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # down-first CCW
    x, y, d = 0, 0, 0
    out: list[str] = []
    for _ in range(n * n):
        out.append(grid[y][x])
        seen[y][x] = True
        nx, ny = x + dirs[d][0], y + dirs[d][1]
        if not (0 <= nx < n and 0 <= ny < n and not seen[ny][nx]):
            d = (d + 1) % 4
            nx, ny = x + dirs[d][0], y + dirs[d][1]
        x, y = nx, ny
    return out


def decode(cells: list[str]) -> tuple[str, str, str]:
    bits = "".join("1" if c in "KB" else "0" for c in cells)
    text = "".join(
        chr(int(bits[i : i + 8], 2)) for i in range(0, 192, 8)
    )
    frame = "".join(
        "1" if cells[k] == "B" else "0"
        for k in range(7, 196, 8)
    )
    return text, bits[192:], frame


def row_yellow_mask(grid: list[list[str]]) -> str:
    return "".join(
        "1" if cell == "Y" else "0"
        for row in grid
        for cell in row
        if cell in "BY"
    )


def main(path: str) -> int:
    px = load_pixels(path)
    grid = extract_matrix(px)
    flat = [c for row in grid for c in row]
    assert "?" not in flat, "unclassified cells present"
    text, leftover, frame = decode(spiral_read(grid))
    counts = {c: flat.count(c) for c in "KWBY"}
    yellow_mask = row_yellow_mask(grid)
    print("counts:", counts)
    print("url:", repr(text), "leftover:", leftover)
    print("frame:", frame)
    print("row-major yellow mask:", yellow_mask, "(0x%06x)" % int(yellow_mask, 2))
    ok = (
        counts == EXPECTED_COUNTS
        and text == EXPECTED_URL
        and leftover == "0000"
        and frame == EXPECTED_FRAME
        and yellow_mask == EXPECTED_ROW_YELLOW_MASK
    )
    print("VERIFY:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "raw/web/live/puzzle/response.bin"))
