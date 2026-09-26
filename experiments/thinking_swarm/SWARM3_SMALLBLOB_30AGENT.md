# Thinking Swarm 3 — 30-agent small-blob analysis (2026-09-09)

Date: 2026-09-09. Mode: thinking-only, ≤20 hand-picked candidates per agent, no sweeps, offline.
Target: small blob A+z+B (128 b64 → 96B, `Salted__`, salt `3ab585348552415d`, 80 ct)
+ p32 twin where noted (salt `b45a5e3d827593ca`). Pipeline per candidate:
`password=sha256(X).hexdigest()` → EVP_BytesToKey {sha256,md5} → AES-256-CBC → PKCS#7 gate.
Address check vs `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` ONLY on valid padding (exact or nothing).
Status: **PUZZLE NOT SOLVED. Zero EXACT hits across all 30 branches.**

## Results

| # | Branch | Cands | Decrypts | Valid | Hits |
|---|---|---|---|---|---|
| 1 | Roses poem + first-piece + Y9/B15 | 20 | 40 | 0 | none |
| 2 | 2023-02-23 bitrev pipeline tail phrases | 16 | 32 | 2 (chance) | none |
| 3 | Layout-as-program (z/enter spine joins) | 20 | 40 | 0 | none |
| 4 | shabef digest-label + anstoo expansions | 20 | 40 | 1 MD5 (chance) | none |
| 5 | last-command = reverse-applied-last | 20 | 40 | 0 | none |
| 6 | lastwords acrostic (phase3.2 tail) | 14 | 56 (both locks) | 1 MD5 `ra` (chance) | none |
| 7 | Architect riddle clause parse (VIC) | 16 | 32 | 0 | none |
| 8 | Width-14 TAIL570 ragged bifid9 | 16 | 32 | 0 | none |
| 9 | Prime-value keep + zeroing (shape-preserved) | 12 | 24 | 0 | none |
| 10 | 24-bit color frame + prime ranks | 20 | 40 | 1 MD5 (chance) | none |
| 11 | Yinyang checksum joined-halves | 20 | 40 | 1 MD5 C17 (chance) | none |
| 12 | R1_63 grids (7×9/3×21, a1o15) | 20 | 160 (both locks, dual form) | 0 | none |
| 13 | LEAD91 key-as-password + square | 20 | 40 | 0 | none |
| 14 | Z@97-anchored TAIL windows | 20 | 40 | 0 | none |
| 15 | 29 dropped letters (R2-mask + run-lengths) | 16 | 64 | 0 | none |
| 16 | esrever bit/nibble/byte forms | 20 | 40 | 0 | none |
| 17 | Known material vs NULY (address compare) | 12 | 0 (24 addrs) | — | none |
| 18 | Chain-key combos as passwords | 20 | 80 (both locks) | 1 = WIF control | none new |
| 19 | Twin-lock password relations + salts | 18 | 72 (both locks) | 0 | none |
| 20 | EC half/double reconciliation (12 pt-ops) | — | 0 | — | none (falsified) |
| 21 | SHA256d 7th construction vs NULY/prize | 20 | 0 (20 addrs) | — | none |
| 22 | Audio full analysis (no 2nd message) | 0 | 0 | — | none |
| 23 | Grid B2/B3 aggregates, color-free | 20 | 80 (dual form) | 0 | none |
| 24 | `beleive` misspelling family | 16 | 32 | 0 | none |
| 25 | 7-token two-round program joins | 20 | 80 (both locks) | 0 | none |
| 26 | Enter CR/command/z×CR hybrids | 20 | 160 (dual form, both locks) | 0 | none |
| 27 | Halving-split adjudication (+4 known vs 17ucy) | 4 | 0 | — | none |
| 28 | Late hints 2024-2026 transcription + tokens | 20 | 40 | 0 | none |
| 29 | #108 residue raw/composed (E_C/WIF/CADEIA) | 20 | 160 (dual form, both locks) | 1 (`CADEIA`, chance) | none |
| 30 | Gate-number singletons (91/104/40/…) | 18 | 36 | 0 | none |

Totals: ~500 candidates, ~1500 decrypts, 8 valid paddings (6 chance-rate single-`0x01` +
1 WIF control + 1 `CADEIA` chance), **0 EXACT address hits**.

## Verified side-facts (keep)

- Agent 2: 2023-02-23 bitrev message byte-exact, `choice` not `choise` (single-bit OCR error).
- Agent 20: matrix half/better are NOT EC halves/doubles of each other, chain keys, trail, or prize P — VIC ≠ EC ≠ amount-split (confirms dead_ends #2/#5).
- Agent 22: audio has no second message (199 valid MP3 frames, white mid, hum + 3 known S-bursts = HASHTHETEXT channel; no SSTV/morse/hidden text).
- Agent 24: `choise/SalPhaselon/Dualite` = noise; only `beleive` (on-chain OP_RETURN) was signal-grade — now exhausted (0/32).
- Agent 27: 1GSMG remains sole gate; 17ucy = operational change, no payout path.
- Agent 28: six late-hint transcriptions (`1357 blocks`, three-item prize list, `tiny hint <3`, friends-vs-skills, `tiny fraction`); minimal password surface, 0/40.
- Agent 29: full K_S1/K_S2 recovered (`b06fa6f2…09c4b` / `b11d211c…ea597`); WIF link + E_C bytes genuine but prizeless.

## Open (unchanged)

CHAIN4 spec, 2019-original grid bbox, creator square confirmation. No further CPU sweeps
without new primary. Chance-rate paddings (≈1/256, single-`0x01`, high-entropy heads,
MD5-leaning) are not signal — acceptance remains EXACT P2PKH equality + verifying signature.
