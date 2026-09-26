"""Render the live hypothesis tree with explicit status and evidence links."""

from __future__ import annotations

import argparse

from .paths import ROOT, ensure_dirs
from .provenance import now_utc_iso


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args(argv)
    ensure_dirs()
    tree = ROOT / "hypothesis_tree.md"
    if not tree.exists():
        print("hypothesis_tree.md not found")
        return 1
    content = tree.read_text(encoding="utf-8")
    print(f"# Hypothesis snapshot — {now_utc_iso()}")
    print()
    print(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
