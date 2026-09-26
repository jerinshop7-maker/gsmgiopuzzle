"""Read-only web capture for GSMG puzzle primary and archived sources.

Network collection is strictly read-only: no form submission, no signing,
no transactions, no candidate secrets transmitted. Each capture is hashed
and stored alongside provenance metadata that records the exact request and
response.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

import requests

from .paths import RAW, ensure_dirs
from .provenance import fingerprint, now_utc_iso, sha256_of, sha512_of, write_json

DEFAULT_TIMEOUT = 30
DEFAULT_HEADERS = {"User-Agent": "gsmg-forensic-capture/0.1 (read-only research)"}


def content_address_store(target: Path, data: bytes) -> str:
    digest = sha256_of(target) if target.exists() else None
    target.write_bytes(data)
    return digest or sha256_of(target)


def capture(url: str, store_root: Path, label: str | None = None) -> dict:
    ensure_dirs()
    parsed = urlparse(url)
    base_label = label or f"{parsed.netloc}{parsed.path}".replace("/", "_").strip("_") or "root"
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    response = session.get(url, timeout=DEFAULT_TIMEOUT, allow_redirects=True)
    response.raise_for_status()

    capture_dir = store_root / base_label
    capture_dir.mkdir(parents=True, exist_ok=True)
    body_path = capture_dir / "response.bin"
    body_path.write_bytes(response.content)
    body_sha = sha256_of(body_path)

    provenance = {
        "url": url,
        "final_url": response.url,
        "label": base_label,
        "acquired_at_utc": now_utc_iso(),
        "status_code": response.status_code,
        "elapsed_seconds": response.total_seconds if hasattr(response, "total_seconds") else None,
        "headers": dict(response.headers),
        "declared_content_type": response.headers.get("content-type"),
        "declared_encoding": response.encoding,
        "body_sha256": body_sha,
        "body_sha512": sha512_of(body_path),
        "body_length": len(response.content),
        "history_status_codes": [resp.status_code for resp in response.history],
        "fingerprint": fingerprint(),
    }
    write_json(capture_dir / "provenance.json", provenance)
    print(json.dumps(provenance, indent=2))
    return provenance


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Read-only URL to capture.")
    parser.add_argument("--label", help="Stable label used in the storage directory name.")
    parser.add_argument("--out", type=Path, default=RAW / "web/live", help="Root storage directory.")
    args = parser.parse_args(argv)
    capture(args.url, args.out, args.label)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
