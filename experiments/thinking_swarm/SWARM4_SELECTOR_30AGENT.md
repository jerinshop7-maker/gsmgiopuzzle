# Thinking Swarm 4 — 30-agent selector-mechanism attack (2026-09-09)

Prompt: color-count → matrix geometry → SalPhaseIon indexing, especially 15×13.
Rule: no promotion on padding/counts alone; claims need ≥2 independent structural clues.
Focus: selector/permutation mechanism (clue → structure → selector → password), not passwords.
Status: **PUZZLE NOT SOLVED. Zero EXACT hits. Several branches KILLED with rescue conditions.**

Branches: 8× 15×13 (A) · 6× 24-cell selectors (B) · 5× yin-yang mask (C) ·
4× 29-selector (D) · 3× Z@97 (E) · 2× index-list (F) · 2× designer (G).

## Wave 1 — 15×13 (A1–A8)

| # | Test | Result |
|---|---|---|
| A1 | 15×13 row-major sums → TAIL indices | garbage (`igihhhacggacdgc`), not forced (map/orientation/index all free) |
| A2 | Stacked 7×13+8×13: MID rows as bytes; 15 sums → 15-row select | both byte readings gibberish; LEAD sums out of range, MID pops collide (8/15 distinct) — KILL stacked semantics |
| A3 | Dimension assignment audit | **13 FORCED** (4 independent: 91=7×13, 104=8×13, decode len 13, R1 len 26=2×13). **15 NOT forced** (only 2 families) — privileged convention only |
| A4 | YELLOW=9 operator (best: prime-row filter → 9 of 15 rows) | most-forced sense, output random (295/287 unround) — not promoted |
| A5 | 28 sums → TAIL indices (bifid9) | garbage + collisions (62×5, 55×5; ≥6 free choices) — not forced |
| A6 | 15×13 vs 13×15 orientation | **15×13 FORCED over 13×15**: MID starts at clean row boundary (91=7×13+0) vs ragged mid-row; 7+8=15 composition; MID-subgrid flatness — 4 clues |
| A7 | Prime-keep-zero geography on 15×13 | block split forced (MID all-zero BY CONSTRUCTION: {a,b}→{8,1} non-prime; p≈2.7e-13) but within-block scatter random — structure is alphabet artifact |
| A8 | Falsification: factor census + 15 audit + neighbor sums | **KILL as designed**: 30/66 region pairs share factors (norm); 15 derivable ~23 ways (non-unique); MID+TAIL=674 ugly, LEAD+TAIL=661 prime; R4A+R4B=104=8×13 (another 13-sum). Rescue: no-tuning geometric payoff. CORRECTION: LEAD+MID+TAIL=**765=15×51**, not 761 |

Net wave 1: 15×13 survives ONLY as working convention (A6 orientation + A3's 13). The
BLUE=15→rows inference is circular (A8). Do not cite 15×13 as evidence; use as layout only.

## Wave 2 — 24-cell selectors (B1–B6) + 29-selector (D1–D4)

| # | Test | Result |
|---|---|---|
| B1 | 24-mask × LEAD head-24 (exact order from unverified/phase0 file + URL-bit identity) | negative both polarities |
| B2 | Prime/non-prime rank 15/9 split on TAIL first-24 | most-forced split, outputs random — no promotion |
| B3 | Prime-rank partition of exact B/Y color order | **BLOCKED: exact per-position B/Y order ABSENT from repo** (counts+positions only). Proxy on LEAD/TAIL first-24 = noise. UNBLOCK TASK: pixel-extract 24-char B/Y order from canonical puzzle.png |
| B4 | Spiral positions as indices (mod table) | **MID104 eliminated** (13/24 distinct, collides). TAIL-direct 24-string `ehfbgghifagagcadghea` = negative control. In-range fit non-unique (661/765/1075 tie) |
| B5 | 24-bit S as permutation on LEAD head | null (runs 22→21, no English) |
| B6 | NULL TEST (real vs 3 random 24-subsets, pre-registered metrics) | **KILL**: real indistinguishable (distinct 8=tie, maxrun 2<3, ge4 hit inside null scatter; ~60% chance of ≥1 hit over 8 tries). Rescue: pre-registered positional structure |
| D1 | R2_29 × 29 I/O correspondence | **CORRECTION: 29 I/O live in ODD stream r[1::2], not even.** No correspondence (all n.s.; best p≈0.051 dies ×9 symbols). Coincidence |
| D2 | I/O positions as indices (×2 mapping forced) | mapping forced (2 clues), content garbage — no promotion |
| D3 | Period-29 Bifid re-decode | **FALSIFIED**: destroys BTCSEED head, single-Z, 4-letter odd-set; windows ciphertext-like |
| D4 | 29 base-rate audit | **KILL**: P(27–31\|matched p)=0.3755 exact / 0.378 MC; 29 one of many small numbers; R2 is a label (`thispassword`), not a mask |

## Wave 3 — yin-yang (C), Z@97 (E), index-list (F), designer (G)

| # | Test | Result |
|---|---|---|
| C1 | ODD-as-2bit-mask XOR even256 | random (27/71 printable) — closed |
| C2 | ODD quads → positions into EVEN256 | noise (`PGDBICLDGBINHXR`) — dead |
| C3 | ODD-key Vigenere on even256 | entropy/IoC move WRONG way — dead |
| C4 | Why interleaved? split comparison + fractionation analysis | **MECHANISM PROOF: odd/even = ROW-coordinate vs COLUMN-coordinate streams** (even n=570 → output[2k]=sq[row,row], [2k+1]=sq[col,col]). Odd-lock forced by a–i input × top-two-rows key × even period (3 lines of proof). Contiguous halves both diverse. **Designed split KILLED; design lives upstream (why {A..I}? why full-length period?)** |
| C5 | Null: random a–i through same square/period | **KILL**: every trial reproduces odd-lock {B,C,D,E} + even diversity exactly. Rescue: within-half content only |
| E1 | Z@97 as split ([0:97] + [98:]) | not forced (mid-row in ALL factor grids; parity lock straddles cut; B-head unstructured) |
| E2 | Z@97 echoes (2×97, moduli, offsets; pre-registered z/Z/English/boundary criterion) | all chance (0/~13 probes) |
| E3 | Adjudication | ranking: marker 1 > offset 1(weak) > rest 0. (d) = category error (selection positional, Z content; 0/1-index flips inclusion). (f) killed (570 ∤ 96/98/100). Probe proposed: gate-length windows at offset 97 |
| F1 | TAIL 19×30 self-index (rows → TAIL) | garbage + window clustering (sums ∈ [95,158]) — self-reference unjustified, negative |
| F2 | Pipeline end-to-end (15×13 → SEL28 → word-find) | **DIVERGES to noise** (hop-1 resampled head slice; hop-2 longest word `giga`/len-3 chance) — publishable kill |
| G1 | Designer profile + whiteboard shortlist (≤10) | **shortlist exhausted** (every ≥2-clue singleton already negative with witnesses); mechanism missing, not items |
| G2 | Naive rereading (master + page only) | **COLLAPSES** into closed families (§9/§15/A3/A4/A5/A10/A26); 3 truly-untested borderline re-tested live: 0/6 valid |

## Corrections to the record (apply everywhere)

1. LEAD+MID+TAIL = **765 = 15×51**, not 761 (A8). The triple also hits ×15 (without ×13).
2. 29 I/O live in **ODD stream r[1::2]** (D1). Prior "even-stream I/O" phrasing is wrong.
3. Exact B/Y per-position color order is **absent** (B3). Counts + spiral positions only.
4. π(570) = **104**, not ~103 (E3). 1-indexed prime-select includes Z@97; 0-indexed excludes.
5. `choise` = single-bit OCR error, not variant (swarm-3 A2, reconfirmed). `Dualite` = secondary nickname (zero DOM hits).

## What survives (ranked)

1. **C4 mechanism proof** (strongest): odd/even = row/col coordinate streams; all split-level
   "design" is upstream (shared {A..I} alphabet + key-at-head + even period). Route effort to
   the alphabet-identity audit (why a–i? checkerboard escapes 1,4?) — the one open upstream question.
2. **A6 orientation** (15×13 over 13×15) + **A3's 13** (4 attestations): use as layout convention,
   never as evidence (A8).
3. **B3 unblock task**: pixel-extract the 24-char B/Y order from canonical puzzle.png
   (sha `38125bbd…`); then ONE pre-registered prime-rank test vs B6's null table.
4. **E3 probe**: gate-length windows {91,104,40,63,29,64,80} anchored at offset 97 (14 checks).
5. **A8 rescue condition** for 15×13: no-tuning geometric payoff only (legible bitmap/text/
   columnar decode, zero dropped cells beyond a pre-stated rule).
6. **KILLED, do not revisit without rescue**: 15×13-as-designed, color→stream indexing (B6 null),
   29-selector (D4 p≈0.38), odd/even-as-payload-split (C4/C5), Z@97 split/seed/dims (E1–E3),
   15×13→TAIL pipeline (F2 diverge), whiteboard singletons (G1), naive literals (G2).

## Open (unchanged)

CHAIN4 spec, 2019-original grid bbox, creator square/convention confirmation.
Acceptance stays EXACT P2PKH equality + verifying signature. Chance-rate paddings
(≈1/256, single-`0x01`, high-entropy, MD5-leaning) are never signal.
