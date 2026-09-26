"""Repository integrity checks for the forensic workspace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .paths import MANIFESTS, RAW, ensure_dirs
from .provenance import sha256_of


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args(argv)
    ensure_dirs()
    manifest = MANIFESTS / "raw_manifest.jsonl"
    if not manifest.exists():
        print("no manifest present")
        return 0

    failures: list[str] = []
    with manifest.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            path = Path(record["path"])
            if not path.exists():
                failures.append(f"missing: {path}")
                continue
            if sha256_of(path) != record["sha256"]:
                failures.append(f"hash mismatch: {path}")
            if path.stat().st_size != record["size_bytes"]:
                failures.append(f"size mismatch: {path}")

    if failures:
        print("FAILURES:")
        for failure in failures:
            print(f"  - {failure}")
        return 2
    print("Repository integrity OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
