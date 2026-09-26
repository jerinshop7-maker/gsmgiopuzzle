from __future__ import annotations

import getpass
import hashlib
import json
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOL_VERSION = "git:workspace-bootstrap"


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fingerprint() -> dict:
    return {
        "hostname": socket.gethostname(),
        "user": getpass.getuser(),
        "python": sys.version.split()[0],
        "tool_version": TOOL_VERSION,
    }


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha512_of(path: Path) -> str:
    digest = hashlib.sha512()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
