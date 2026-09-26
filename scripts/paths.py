from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
DERIVED = ROOT / "derived"
SCRIPTS = ROOT / "scripts"
MANIFESTS = RAW / "manifests"
DERIVED_MANIFESTS = DERIVED / "manifests"
DERIVED_REPORTS = ROOT / "evidence.md"
INVENTORY = ROOT / "artifact_inventory.md"


def ensure_dirs() -> None:
    for directory in (RAW, DERIVED, MANIFESTS, DERIVED_MANIFESTS):
        directory.mkdir(parents=True, exist_ok=True)
