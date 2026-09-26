# SALFINAL report — 2026-09-04 controlled structural attack

Checkpoint: `CHECKPOINT-2026-09-04-SALFINAL.md`. Region map: `sal_regions.json`.
Engine: `sal_final_search.py` (2868 candidates). Phase-2 oracle probe:
`sal_phase2_bifid_oracle.py` (54 password families, 108 decryptions, both digests).

## 1. Exact SalPhaseIon object (byte-identical, primary)

- S0 textarea bytes sha256 `d39d10b1...3330c`, 2149 bytes, 1075 single-char
  tokens, compact sha256 `26e37652...78e6156`. Live capture == canonical
  `jackdevs66/.../SalPhaseIon.txt` byte-for-byte.
- Regions (token offsets, lengths, alphabets, deterministic decodes):
  LEAD91 [0:91] 91 a–i (unsolved digit stream) · MID104 [91:195] 104 a/b →
  `matrixsumlist` · TAIL570 [195:765] 570 a–i (unsolved) · z@765 sep ·
  R1 [766:829] 63 a–o → bigint-hex → `lastwordsbeforearchichoice` ·
  z@829 sep · R2 [830:859] 29 a–o → bigint-hex → `thispassword` · z@859 sep ·
  R3ENG [860:895] 35 → `shabef|ourfirsthintis|yourlastcommand` ·
  R3B64A [895:958] 63 base64-A · **z@958 = BLOB DATA** · R4A [959:999] 40 a/b
  → `enter` (encoded line break) · R4B [999:1063] 64 base64-B ·
  R4C [1063:1075] 12 → `shabef|anstoo`.
- Naddiseo notebook cells 3/11/12 independently document the four deterministic
  decodes re-verified here; cell 13 leaves LEAD91+TAIL570 undecoded — the live
  bottleneck.

## 2. Small-blob assembly (CORRECTED, supersedes Dead End #1 framing)

- WRONG: A+B (63+64=127 chars) → padding error / 79-byte non-aligned reading.
- RIGHT: **A+z+B (63+1+64=128 chars → 96 bytes: `Salted__` + salt
  `3ab585348552415d` + 80 ct, ct%16==0)**. The 40-char `enter` is the page's
  64-column line-break between the two 64-char lines. Ranked VALID_CIPHERTEXT
  (SALFINAL-02859). Matches floflo777 `BLOB_B64` byte-for-byte.
- B alone decodes (48 bytes) but has no `Salted__` header — mid-blob chunk.
- Phase 3.2.2 second lock (same shape): `U2FsdGVkX1+0...46z` +
  `gKlIi8...0NAv4` = 128 chars → 96 bytes, salt `b45a5e3d827593ca`, 80 ct.
  Both locks must be tested for every password family (done in phase-2 probe
  for the small blob; p32 lock queued for the next sweep).
- Large Cosmic/Dualite blob (live textarea_1): 1792 chars → 1344 bytes,
  `Salted__` header. NOT used as input (checkpoint exclusion).

## 3. Prime / zeroing enumeration (finite, both mappings)

- Mappings: legacy a1 (a=1..i=9) for control + bifid9 from issue #106 square
  rows (d=0,b=1,i=2,f=3,h=4,c=5,e=6,g=7,a=8).
- LEAD91 bifid9: 33/91 prime-valued digits {2,3,5,7}; TAIL570: 291/570.
- Enumerated: streams {LEAD91,TAIL570,LEAD_TAIL661,FULL765,MID104,R4A40,R1,R2}
  × orientations {normal,reversed} × definitions {P2357,Pfull} × indexings
  {idx0,idx1} × rules {keepPrime,zeroPrime} (+ prime-VALUE keep/zero in phase2).
  Result: no EXACT_MATCH; probes recorded with factors/triangular flags and
  legibility probes. Full JDNL in `sal_final_report.jsonl`.

## 4. matrixsumlist as instruction + dimensions

- N table: 91=[1×91,7×13] triangular T13=13 ✓ · 570=[1×570,2×285,3×190,5×114,
  6×95,10×57,15×38,19×30] · 661 prime · 765=[1×765,3×255,5×153,9×85,15×51,
  17×45] · 104=[1×104,2×52,4×26,8×13] · 40=[1×40,2×20,4×10,5×8] ·
  63=[1×63,3×21,7×9] · 29 prime · 128/96/80 block shapes.
- Triangular property tested independently (LEAD91=91=T13); old 91-symbol dbbi
  theory NOT resurrected.
- Matrix candidates enumerated: every factor shape (capped for large N) ×
  {id,hmirror,vmirror,rot180,complement,+transpose/antitranspose if square} ×
  bitmodes {mod2,primeval,nonprimeval,direct} × sums {rows,cols} × yin/yang
  pair ops {none,rowpair_sum/diff,colpair_sum/diff}. Prime-valued sum masks
  (Rpm/Cpm/XOR/XNOR) computed throughout. 1231 PARTIAL_STRUCTURAL_MATCH
  (pair-sum constancy, prime-count thresholds) retained as leads, none promoted.

## 5. Yin/yang + prime-valued sums (prompt R/C preserved)

- R14 prime mask `00010010001010`, C14 `00000110110000`,
  XOR `00010100111010` (five 1s), XNOR `11101011000101`; R-C and R-revC vectors
  reproduced exactly as given. Mod 2/3/5/7 and diff-from-7/8/9 recorded
  (SALFINAL-02829..02854). No decoded key; retained as threshold leads for the
  matrix-sum Prime test, not solutions.

## 6. lastwordsbeforeForcearchichoice context

- R1/R2 directives read together as "the last words before the Architect Choice
  are this blob's password" (floflo lead 9). Literal reading (every ≤20-word
  window of every text incl. Architect scene + 3 films, 7 forms × 2 KDFs × both
  locks ≈ 405k candidates / 24.8M decryptions) is externally reported CLOSED
  (0 match) — recorded SECONDARY until rerun here; NOT re-swept literally.
- Local chronological extraction: phase2 live page last-words region (Genesis/
  anarchist-digital-answer passage); phase3.2.txt order = Architect monologue →
  149-digit string → checkerboard riddle ("Raising the stakes ... as wide as
  the first one seen.") → p32 blob. So the riddle sentence is the last-words
  candidate before the p32 lock; the SalPhaseIon R3ENG sentence is the last
  words before the small blob. Non-literal readings (initials, hashes,
  prime-rank chars) queued; prime-rank structural probes already in engine.

## 7. Seven-token sequence

- concat_order / reverse / odd1357 / even246 / lengths / firsts / lasts /
  sha_each / repeat_equal recorded (SALFINAL-02860..02868). Repetition
  matrixsumlist@1,5 preserved as complementary-structure lead (odd/even split).
  No hashing-as-solution performed (checkpoint: Cosmic XOR excluded).

## 8. Strict acceptance

- Targets: `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` (primary) and
  `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` (recorded separately; no payout link).
- Phase-2 probe: 54 families → 108 offline decryptions (SHA-256 + MD5) → 0
  valid paddings (chance expectation ~0.4; 0 observed, consistent), 0 matches.
- Engine: 2868 candidates → 0 EXACT_MATCH, 1 VALID_CIPHERTEXT (A+z+B),
  4 KNOWN_TOKEN (trivial token concatenations), 1231 PARTIAL, 1632 NO_MATCH.
- **Puzzle remains NOT SOLVED. No new SOLUTION CANDIDATE.**

## 9. Queued branches — executed 2026-09-04 (`dual_oracle.py`, `sal_queued_runner.py`)

- Harness certified (SELFTEST OK): phase-2 blob opens under SHA-256/`sha256(causality)`
  hexdigest (MD5 fails); `causality` re-derives planted `1Jqq37...`; both lock
  shapes verified (small salt `3ab585348552415d`, p32 salt `b45a5e3d827593ca`).
  Per candidate X: both locks × {hexdigest,direct} × {sha256,md5} + third-door
  6 constructions × {compressed,uncompressed} vs 9 planted addresses.
- Last-words non-literal (monologue/149-digit/riddle/phase2pt/R3ENG/R4C ×
  last-N/initials/nospace/sha/prime-rank/nonprime-rank/reversed): all NO_MATCH
  on locks and open door. Literal-window sweep remains externally-reported
  CLOSED (secondary).
- Bifid 3×3 period-570, squares {DBG-keyed-A-last, DBG-alpha=alphabetical,
  alpha-ai, rev-ai}: all decode cleanly, NONE contains BTCSEED. Floflo
  byte-exact BTCSEED claim stays UNVERIFIED (different square/convention
  required). Bifid outputs fed to harness: NO_MATCH.
- Dropped I/O: TAIL570→kept 495/dropped 75; LEAD91→86/5; R1→56/7; R2→19/10.
  No 256-length object emerges from raw streams — the 285→256 reduction is a
  downstream (unverified Bifid) product, not a raw-stream property. Dropped
  strings fed to harness: NO_MATCH.
- esrever: 108 harness attempts → sole EXACT_MATCH is the KNOWN control
  (reversed URL → `13HGhjkmKUkP8sk9k63BLmhkxRjy7uK4Rp` bits-reversed "Good job,
  Neo!"), validating the harness; NOT a prize hit. Two valid paddings
  (arch-monologue-last3/md5, reversed-R1/sha256) with no address match =
  chance-rate padding accidents, consistent with ~1/256 expectation.
- Totals this phase: 108 attempts, 0 prize/third-door-open hits.
  Full log: `sal_queued_report.json`.

## 10. Deep phase — 2026-09-04 (`sal_matrix_sweep.py`, cipher/Bifid probes)

- Matrix-sum sweep (matrixsumlist taken literally on LEAD91/TAIL570):
  bifid9+a1 × {plain,keepPval,zeroPval,Pfull-keep/zero,P2357-keep/zero} × every
  factor shape × fwd/rev × rows/cols/diag × {raw,mod10,csv,chr}: **765 password
  candidates → 6120 decrypts (both locks × 2 forms × 2 digests) → 17 valid
  paddings (≈1/360, chance-rate) → 0 address matches**; door spot-checks on all
  17 vpads → 0 hits. No family concentration (paddings spread across shapes,
  maps, digests) — the signature of chance, not signal. Log:
  `sal_matrix_sweep_report.json`.
- Classical ciphers: Beaufort/Vigenere (9-letter a–i) with keys
  thematrixhasyou/causality/matrixsumlist/enter/architect → max a/b run 5
  (vs 104/40 needed), 0 lock/door hits. EBCDIC (cp1140/037/500) on digit bytes
  → control chars, meaningless (phase-3.2 EBCDIC applied to high-byte cipher,
  not 0–9 digits). Negative.
- Bifid (≈120 combos): 3×3 keyed/alpha/rev, 5×5 keyed DBIFHCEG/SALPHASEION/
  MATRIX/GSMG (+transpose), 6×6 A–Z0–9 keyed, periods {full,7,13,19,30},
  fwd/rev, encode/decode — **no BTCSEED, no 285→29-drop→256** (observed kept:
  228–280, never 256). The byte-exact BTCSEED/256 claim is not reproducible
  from TAIL570 under any standard convention tried; it needs an unstated
  segment/square/fractionation or is wrong. Digit streams stay undecoded,
  agreeing with issue #106 (mechanism = last unexplained step, likely what
  matrixsumlist instructs).

## 11. Forensic layer — 2026-09-04 (`sal_final_structure.py`, `sal_structure_report.json`)

DOM forensics (all three live pages): no comments/scripts/hidden inputs on the
SalPhaseIon page (bare tags, two identically-styled textareas, titles
`SalPhaseIon` / `Cosmic Duality`); flavor-only "bunny hunter" comments on the
other two pages. **No `Dualite` string exists anywhere in the capture** — the
"titled Dualite in markup" claim is factually wrong; the h1 reads
`Cosmic Duality`. Wrapping forensics confirm the blob design: large blob is
28 lines × 64 cols; small blob is 64 (A+z) + token-encoded `enter` break + 64
(B) — one consistent 64-column convention, not two coincidences.

Natural-matrix diagnostics (bifid9+a1, all factor shapes, rows/cols/diags,
pair partitions, complements, mods, constancy-scored): prompt R/C vectors
verified True/True against the public grid. Sharpest anomalies, chance-calibrated:

- TAIL570 bifid9 ≥4 → first-24 split 15/9, mirroring the 15-blue/9-yellow
  signature — but 1 hit in 8 op/stream tries at ~8% each is expected ~48% of
  the time. Weak; recorded, not promoted.
- TAIL570 a1 10×57 row parities [0,0,0,0,0,0,0,1,0,0] (lone odd row 321, H=0.469)
  — p≈1% per sequence, ≈27% across the tested set. Weak.
- LEAD91 a1 7×13 top/bottom pair sums [117,128,117] (palindromic) — weak.
- No constant-sum/XOR/mod partition anywhere outside chance bounds.

Architect positional extraction (exact phase-3.2 head): 4 sentences; last words
[you, human, not, irrelevant]; second-last [for, irrevocably, will, also];
riddle tail [first, one, seen]. Pure extraction; non-literal harness already
negative on these families.

Lock comparison: salts differ (xor `8eefdb090727d297`), zero repeated blocks
either side, byte entropy 5.97/5.93 (proper ciphertext), ct-xor recorded — no
shared-plaintext structure. Third door: version 0, checksum valid, hash160
`eb862e…` fresh vs sampled planted hashes; `NULY` is a base58 vanity-pattern
accident-or-grind, indistinguishable either way — defused as a clue.

Pipeline verdict: **no single deterministic string emerges** — every anomaly
sits inside chance bounds, so per the pipeline rule nothing new is fed to the
locks beyond the already-swept sum-list families. Log: `sal_structure_report.json`.

## 12. Next (remaining open)

1. Dynamic-candidate replay (98/213 filtered scripts) — hours-to-days, queued.
2. C/GPU-scale door pass (rockyou-class) — needs speed this workspace lacks.
3. Pre-2023 Telegram archive / original ArchitectChoice contents (never archived).
4. Author confirmation of the digit-stream segment/square convention.
