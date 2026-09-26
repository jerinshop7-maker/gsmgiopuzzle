"""Byte-preserving transcription of the SalPhaseIon textarea.

The live page places the SalPhaseIon and Cosmic Duality payloads inside HTML
<textarea> elements. This tool extracts the raw bytes and Unicode code points,
preserves whitespace/line endings/separators, records offsets into the
source document, and compares the live transcription against any repository
copy. It does not repair, normalize, or patch the source.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from .paths import DERIVED, RAW, ensure_dirs
from .provenance import now_utc_iso, write_json

TEXTAREA_RE = re.compile(r"<textarea[^>]*>(.*?)</textarea>", re.S)


def extract_textareas(html: bytes) -> list[dict]:
    text = html.decode("utf-8", "replace")
    textareas: list[dict] = []
    cursor = 0
    for match in TEXTAREA_RE.finditer(text):
        start = match.start(1)
        end = match.end(1)
        body = match.group(1)
        textareas.append({
            "source_byte_offset": start,
            "source_byte_end": end,
            "char_count": len(body),
            "line_count": body.count("\n") + 1,
            "ends_with_newline": body.endswith("\n"),
            "carriage_return_count": body.count("\r"),
            "tab_count": body.count("\t"),
            "non_ascii_count": sum(1 for ch in body if ord(ch) > 127),
            "body": body,
        })
    return textareas


def render_streams(body: str) -> dict:
    compact = "".join(ch for ch in body if not ch.isspace())
    tokens = re.findall(r"\S+", body)
    return {
        "compact_char_count": len(compact),
        "compact_sample": compact[:240],
        "token_count": len(tokens),
        "unique_chars": sorted(set(body)),
    }


def compare(live_body: str, repo_body: str) -> dict:
    if live_body == repo_body:
        return {"identical": True, "live_len": len(live_body), "repo_len": len(repo_body), "diffs": []}
    diffs: list[dict] = []
    for idx, (left, right) in enumerate(zip(live_body, repo_body)):
        if left != right:
            diffs.append({"offset": idx, "live": repr(left), "repo": repr(right)})
        if len(diffs) >= 20:
            break
    return {
        "identical": False,
        "live_len": len(live_body),
        "repo_len": len(repo_body),
        "diffs": diffs,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", type=Path, help="Raw HTML capture to transcribe.")
    parser.add_argument("--repo", type=Path, help="Optional repository copy to compare.")
    args = parser.parse_args(argv)
    ensure_dirs()

    html = (args.html or RAW / "web/live/salphaseion/response.bin").read_bytes()
    textareas = extract_textareas(html)
    out_dir = DERIVED / "transcriptions/salphaseion"
    out_dir.mkdir(parents=True, exist_ok=True)

    write_json(out_dir / "textareas.json", {
        "source": str(args.html) if args.html else "raw/web/live/salphaseion/response.bin",
        "acquired_at_utc": now_utc_iso(),
        "count": len(textareas),
        "textareas": [
            {key: value for key, value in ta.items() if key != "body"} for ta in textareas
        ],
    })

    for idx, ta in enumerate(textareas):
        body = ta["body"]
        (out_dir / f"textarea_{idx}.txt").write_text(body, encoding="utf-8")
        (out_dir / f"textarea_{idx}.hex").write_text(body.encode("utf-8").hex(), encoding="utf-8")
        write_json(out_dir / f"textarea_{idx}.json", {
            "index": idx,
            "source_byte_offset": ta["source_byte_offset"],
            "char_count": ta["char_count"],
            "line_count": ta["line_count"],
            "carriage_return_count": ta["carriage_return_count"],
            "tab_count": ta["tab_count"],
            "non_ascii_count": ta["non_ascii_count"],
            "streams": render_streams(body),
        })

    if args.repo:
        repo_body = args.repo.read_text(encoding="utf-8")
        live_body = textareas[0]["body"] if textareas else ""
        write_json(out_dir / "comparison.json", compare(live_body, repo_body))

    print(f"Transcribed {len(textareas)} textarea(s) to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
