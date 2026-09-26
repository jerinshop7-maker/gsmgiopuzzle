"""Hash every raw artifact and write append-only manifest records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .paths import MANIFESTS, RAW, ensure_dirs
from .provenance import sha256_of, sha512_of

IGNORED_SUFFIXES = {".json", ".jsonl", ".md"}


def classify(path: Path) -> str | None:
    if path.name == "provenance.json":
        return None
    if path.suffix.lower() in IGNORED_SUFFIXES:
        return None
    if ".git" in path.parts:
        return None
    return "raw" if RAW in path.parents else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args(argv)
    ensure_dirs()
    manifest = MANIFESTS / "raw_manifest.jsonl"
    with manifest.open("a", encoding="utf-8") as handle:
        for path in sorted(RAW.rglob("*")):
            if not path.is_file():
                continue
            kind = classify(path)
            if kind is None:
                continue
            record = {
                "path": str(path),
                "sha256": sha256_of(path),
                "sha512": sha512_of(path),
                "size_bytes": path.stat().st_size,
            }
            handle.write(json.dumps(record, sort_keys=True) + "\n")
    print(f"Manifest updated: {manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
