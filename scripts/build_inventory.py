"""Generate a human-readable artifact inventory from the manifests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .paths import INVENTORY, MANIFESTS, ensure_dirs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args(argv)
    ensure_dirs()

    manifest = MANIFESTS / "raw_manifest.jsonl"
    lines: list[str] = ["# Artifact Inventory", ""]
    if not manifest.exists():
        lines.append("No raw artifact manifest found yet.")
        INVENTORY.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("Inventory generated (empty).")
        return 0

    with manifest.open(encoding="utf-8") as handle:
        rows = [json.loads(line) for line in handle if line.strip()]

    lines.append(f"Total raw artifacts: {len(rows)}")
    lines.append("")
    for row in rows:
        lines.append(f"- `{row['path']}`")
        lines.append(f"  - sha256: `{row['sha256']}`")
        lines.append(f"  - size: {row['size_bytes']} bytes")
    INVENTORY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Inventory written to {INVENTORY}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
