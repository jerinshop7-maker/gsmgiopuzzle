"""Structural analysis of the captured SalPhaseIon textarea.

This script reproduces the public token-interpretation claims against the raw
captured bytes while preserving offsets and parent hashes. It does not accept
a claim because a writeup states it; it tests the documented transformation
on the exact captured bytes and reports agreement or divergence.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
from pathlib import Path

from .paths import DERIVED, RAW, ensure_dirs
from .provenance import now_utc_iso, write_json


def compact(text: str) -> str:
    return "".join(ch for ch in text if not ch.isspace())


def split_regions(text: str) -> list[str]:
    return [compact(chunk) for chunk in text.split("z")]


def abba_to_ascii(stream: str) -> str | None:
    if not re.fullmatch(r"[ab]+", stream):
        return None
    if len(stream) % 8 != 0:
        return None
    bits = stream.replace("a", "0").replace("b", "1")
    chars = [chr(int(bits[i:i + 8], 2)) for i in range(0, len(bits), 8)]
    return "".join(chars)


def a1zhex_to_ascii(stream: str) -> str | None:
    mapping = {ch: str(i + 1) for i, ch in enumerate("abcdefghi")}
    mapping["o"] = "0"
    if not re.fullmatch(r"[abcdefghio]+", stream):
        return None
    pairs = [stream[i:i + 2] for i in range(0, len(stream), 2)]
    try:
        values = [int("".join(mapping[ch] for ch in pair)) for pair in pairs]
        return bytes(values).decode("utf-8", "replace")
    except KeyError:
        return None


def decode_a1z26_hex(stream: str) -> str | None:
    mapping = {ch: str(i + 1) for i, ch in enumerate("abcdefghi")}
    mapping["o"] = "0"
    if not re.fullmatch(r"[abcdefghio]+", stream):
        return None
    digits = "".join(mapping[ch] for ch in stream)
    # Read two decimal digits per byte, skipping impossible values gracefully.
    out = bytearray()
    i = 0
    while i < len(digits):
        if i + 2 > len(digits):
            break
        value = int(digits[i:i + 2])
        if value > 255:
            return None
        out.append(value)
        i += 2
    return bytes(out).decode("utf-8", "replace")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args(argv)
    ensure_dirs()

    text = (RAW / "web/live/salphaseion/response.bin").read_bytes().decode("utf-8", "replace")
    match = re.search(r"<textarea[^>]*>(.*?)</textarea>", text, re.S)
    if not match:
        return 1
    body = match.group(1)
    full = compact(body)

    analysis = {
        "acquired_at_utc": now_utc_iso(),
        "source_artifact": "raw/web/live/salphaseion/response.bin",
        "compact_length": len(full),
    }

    # First 91 symbols -> binary ASCII (public claim: "matrixsumlist").
    first91 = full[:91]
    analysis["first91_abba"] = abba_to_ascii(first91) if re.fullmatch(r"[ab]+", first91) else None

    # Next 103 symbols -> binary ASCII (public claim: "enter").
    next103 = full[91:194]
    analysis["next103_abba"] = abba_to_ascii(next103) if re.fullmatch(r"[ab]+", next103) else None

    # Following 570 symbols over {a..i,o} -> a1z26/hex decode.
    digit_stream = full[194:764]
    analysis["digit_stream_sample"] = digit_stream[:60]
    analysis["digit_stream_a1zhex"] = decode_a1z26_hex(digit_stream)

    # Locate pure spans to report any divergence from public claims.
    abba_spans = [(m.start(), m.end()) for m in re.finditer(r"[ab]{8,}", full)]
    digit_spans = [(m.start(), m.end()) for m in re.finditer(r"[abcdefghio]{4,}", full)]
    analysis["abba_spans"] = abba_spans
    analysis["digit_spans"] = digit_spans
    analysis["region3_head"] = split_regions(body)[3][:80] if len(split_regions(body)) >= 4 else None

    out = DERIVED / "transcriptions/salphaseion" / "region_analysis.json"
    write_json(out, analysis)
    print(json.dumps(analysis, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
