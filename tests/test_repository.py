from __future__ import annotations

import json
from pathlib import Path

from scripts.paths import MANIFESTS, RAW
from scripts.provenance import sha256_of


def test_manifest_hashes_match_files() -> None:
    manifest = MANIFESTS / "raw_manifest.jsonl"
    if not manifest.exists():
        return
    with manifest.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            path = Path(record["path"])
            assert path.exists(), f"missing {path}"
            assert sha256_of(path) == record["sha256"], f"hash mismatch {path}"


def test_raw_directory_contains_artifacts() -> None:
    files = [p for p in RAW.rglob("*") if p.is_file()]
    assert files, "no raw artifacts captured"
