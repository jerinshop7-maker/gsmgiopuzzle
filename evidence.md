# Evidence Ledger

## Ledger rules

- Directly captured bytes outrank transcriptions, solver writeups, and issue claims.
- Every artifact record must include source, acquisition time, path, size, hashes, type, encoding where applicable, reliability tier, and independent-verification status.
- Raw artifacts are immutable. Corrections and alternate interpretations are separate derived artifacts.
- A hash authenticates only the exact bytes hashed; it does not prove that the interpretation is correct.

## Artifact records

### ART-001 — puzzle.png

- Source: `https://gsmg.io/puzzle`
- Date obtained: 2026-09-03T18:09:10+00:00
- File: `raw/web/live/puzzle/response.bin`
- Size: 29931 bytes
- SHA-256: `38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830`
- SHA-512: `357511c59db2b8a92db4f296398818e4cc8854f2256327798142b86a80a007fac37cd6f8f13f174a6338eff8fbb2f4cc04b25e08a9aa1c62b6280bafa0945563`
- MIME/type: image/png
- Encoding: binary
- Associated clue: starting grid
- Source reliability: Tier 1 (live primary route)
- Independent verification: pending archive comparison
- Notes: served with `Cache-Control: no-store` and `Last-Modified: Sat, 15 Aug 2026 23:16:52 GMT`.

### ART-002 — theseedisplanted

- Source: `https://gsmg.io/theseedisplanted`
- Date obtained: 2026-09-03T18:09:13+00:00
- File: `raw/web/live/theseedisplanted/response.bin`
- Size: 832 bytes
- SHA-256: `7cb766d406008a397f8ae32b3a38ca68b42724bb07b3481deb84baad5c725183`
- SHA-512: `0461d8c3e476f07adc6ea4460f1fc1bb84347794f332ec2c42404b899f15fcf53ea46c69bb8715ebc0be5dd48fe6b8e8fc982285712465109c3dc4609ba46503`
- MIME/type: text/html; charset=utf-8
- Encoding: utf-8 (gzip transfer)
- Associated clue: stage-1 images and POST form
- Source reliability: Tier 1 (live primary route)
- Independent verification: pending archive comparison
- Notes: references eight `/img/*.png` assets and a POST form action `/phase1verification`.

### ART-003 — phase2

- Source: `https://gsmg.io/choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself`
- Date obtained: 2026-09-03T18:09:15+00:00
- File: `raw/web/live/phase2/response.bin`
- Size: 9207 bytes
- SHA-256: `06fbd4461ab20d45c54a7053c7c0cfa256ba82a5ad4c73a47fac67f3f1cdf7d9`
- SHA-512: `a500c8153a2684e55b80eb30c6dd4a116a0ef8c2fbdba4950e44e73750195815276836f0539869ac3103c182a8f3ef43c9e7ffd182274a30b75d1487a206532f`
- MIME/type: text/html; charset=utf-8
- Encoding: utf-8 (gzip transfer)
- Associated clue: Phase 2 and Phase 3 encrypted textareas
- Source reliability: Tier 1 (live primary route)
- Independent verification: pending archive comparison

### ART-004 — salphaseion

- Source: `https://gsmg.io/89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32`
- Date obtained: 2026-09-03T18:09:18+00:00
- File: `raw/web/live/salphaseion/response.bin`
- Size: 4536 bytes
- SHA-256: `a83d3de7810f26b19b4965339b76d403e44f6b6877e5d7de2555480ca1779d77`
- SHA-512: `f6234d8b99577d6b5f20b9492fca4178b7fa3f5716c7df8d5dcdd5237cd251527e220277236fd0113d7c426193d666b2098482da9c74d3510e99863140826901`
- MIME/type: text/html; charset=utf-8
- Encoding: utf-8 (gzip transfer)
- Associated clue: SalPhaseIon and Cosmic Duality textareas
- Source reliability: Tier 1 (live primary route)
- Independent verification: pending archive comparison and repository cross-check

### ART-005 through ART-013 — stage-1 image assets

Captured from `https://gsmg.io/img/...` with the exact filenames referenced by ART-002. Stored under `raw/web/live/img_*`. Each has its own `provenance.json` and manifest record. Filenames include a space in `black_banking - war.png`.

## Current public-source facts

- The live `/puzzle` route responded with a PNG image during initial read-only review.
- The live `/theseedisplanted` route exposed image references and a password POST form.
- The long Phase 2 URL exposed Phase 2 and Phase 3 encrypted textareas.
- The hash route `89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32` exposed SalPhaseIon and Cosmic Duality textareas.
- The public `puzzlehunt/gsmgio-5btc-puzzle` repository contains a README and six image artifacts and has history beginning 2020-04-25.

These observations came from read-only web retrieval and are not yet represented by local raw files. They become ledger records only after deterministic intake and hashing.

## Claim records

### CLM-001 — Issue #108 small-blob correction

- Source: issue #108 text supplied during the investigation; related live artifact ART-004.
- Claim: change Base64 positions 18 and 51, concatenate the two small fragments, and decrypt to a 79-byte plaintext containing `K_C1`, `K_C2`, and `E_C`.
- Captured first fragment: `U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9` (63 chars).
- Captured positions: index 18 = `J`; index 51 = `s`; the claimed substitutions are already present.
- Captured second fragment: `QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ` (64 chars).
- Literal concatenation: 127 Base64 chars -> 95 bytes; after the 16-byte Salted__ header/salt, 79 ciphertext bytes remain.
- Verification: 79 is not divisible by AES-CBC's 16-byte block size; the claimed plaintext was not reproduced from the captured bytes.
- Status: `UNVERIFIED` / contested. The raw capture is unchanged; no correction was applied.

### CLM-002 — Two funded prize targets

- Sources: puzzlehunt README, author hint OCR, and read-only Blockstream API responses.
- Main address: `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`; current observed balance approximately 1.256 BTC.
- Halving address: `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`; current observed balance approximately 3.7505 BTC, fully unspent at observation time.
- Status: `STRONGLY_SUPPORTED` as on-chain state; ownership/private keys remain unproven.

### CLM-003 — Official prime/zeroing/yin-yang clues

- Sources: OCR transcriptions under `derived/hints/` from official hint images in the Naddiseo archive.
- Key text: primes `2,3,5,7`; prime number required to proceed; some characters need to be “zeroed out”; reaching a “ying yang” enables solving the puzzle the same day.
- Status: `STRONGLY_SUPPORTED` as author statements, with normal OCR character-level uncertainty.

### CLM-004 — Cosmic Duality intermediate

- Source: canonical `jackdevs66/GSMG5_CDuality` repository and independent local reproduction.
- Result: 1327-byte padded plaintext; unpadded SHA-256 `4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081`.
- Further documented matrix/base-38 output: half `0423d911...`, better half `48cc46e6...`, trail `fc0c1b02`.
- Bitcoin verification: derived addresses do not equal either funded target; the matrix output is therefore an intermediate or decoy, not a proven prize key.
- Status: intermediate decrypt `SUPPORTED`; prize-key interpretation `FALSIFIED`.

### CLM-005 — Color-frame proof

- Source: `raw/github/Naddiseo-gsmgio-5btc-puzzle/working/puzzle.png`.
- Method: classify the 14x14 squares by dominant exact colors, map black/blue to 1 and white/yellow to 0, then read using the down-first counterclockwise spiral.
- Result: counts are K=86, W=86, B=15, Y=9; the spiral decodes exactly to `gsmg.io/theseedisplanted`; blue/yellow positions are zero-based 7,15,...,191, the last bit of each of the first 24 bytes.
- Status: `STRONGLY_SUPPORTED`; independently reproduced locally.
- 2026-09-11 pixel-grounding update (discovery #42, superseded by #52): the lattice is IN the live capture (ART-001, byte-identical sha `38125bbd...`), but the original center-sample census was contaminated by bunny line-art and reported the wrong leftover. Dominant exact-fill extraction gives K=86/W=86/B=15/Y=9, spiral URL + leftover `0000`, and the exact B/Y frame. The README matrix matches all 196 extracted bits. `scripts/extract_grid.py` VERIFY PASS on live and committed bytes. Status: `PROVEN` after the #52 correction.

### CLM-014 — Prize-address QR in puzzle.png (provenance only)

- Source: ART-001 pixels (0,1289)-(231,1527), B/W only.
- Method: OpenCV detectAndDecode after 30px white quiet-zone border (tight crop returns '' — the cause of the 2026-09-04 miss), two scales agree, inverted control negative.
- Result: payload `https://www.blockchain.com/btc/address/1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` (public explorer link, not key material).
- Status: `STRONGLY_SUPPORTED` as artifact fact; no puzzle-mechanism weight. Corrects the 2026-09-04 "no decodable QR" claim.

### CLM-006 — Bit-reversed 2023 author message

- Source: `raw/github/Naddiseo-gsmgio-5btc-puzzle/working/hints/2023-02-23.png`, with OCR/transcription saved under `derived/hints/`.
- Method: reverse bit order within each 8-bit token, then reverse the token order to restore message reading order.
- Result: near-exact compact message naming `yellow blue primes matrixsumlist lastwordsbeforearchichoice yinyang` and stating that the password is “in front of your eyes” and the last step is a giveaway. One local OCR token differs at the character level (`choise`/`choice`), so the character-perfect version remains an image-transcription issue.
- Status: `STRONGLY_SUPPORTED` for the transformation and semantic content; exact character transcription has minor OCR uncertainty.

### CLM-007 — #106 sweep and final-gate report

- Source: issue #106 supplied in the investigation context and captured issue record.
- Reported claims: test both EVP-MD5 and EVP-SHA256 because the puzzle appears to mix KDF conventions; large sweeps across modes, password candidates, direct reductions, and both final blobs found no target match; the 1327-byte Cosmic result is a padding accident; unresolved digit streams remain the highest-value lead.
- Local verification: color-frame and bit-reversal portions reproduce; the full sweep scripts, witnesses, and all claimed 2.5B tests are not present locally.
- Status: `SECONDARY/UNVERIFIED` for numerical sweep coverage; `SUPPORTED` as a prioritized research lead.

### CLM-008 — Prize-address scope correction

- Source: issue #106 report, puzzlehunt README, and read-only chain observations.
- Result: `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` is the live original address; `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` receives the halving transfers and remains separately funded. Neither address has a published solver payout proof.
- Status: `STRONGLY_SUPPORTED` for chain facts; ownership remains unproven.

### CLM-009 — Chain-4 decrypt (1151B e4269ed5...)

- Sources: `raw/github/jackdevs66-GSMG5_CDuality/working/cosmic_duality.txt` (salt `2d3f6fe06dc950e6`); `experiments/004-cosmic/cosmic_decrypted.bin` (1327B, sha `4f7a1e4e...`); BLOB128 (salt `3ab585348552415d`); p32 blob from `phase3.2.txt` (salt `b45a5e3d827593ca`).
- Method: CHAIN 1 small blob 5-token direct+MD5 -> `E_C=38d4f4c90cb45fdfc8cff50d0ed1c5`; CHAIN 2 p32 WIF direct+MD5 -> `E_S=740a25de4b8e946d0a5ae2667a23a2`; CHAIN 3 XOR-7 `a795de11...` raw+MD5 -> 1327B; `mystery[:-1]` XOR `b657264f2f6e6921` -> `Salted__` salt `5bbd88ac32481bca` +1152ct; raw32 `E_C||E_S||E_B[:2]`+MD5 -> 1151B sha `e4269ed5fbb202a81e5e1aa6b5190fdd1ea126b2c8547ea7cdbdf45387ea135b`, marker `+-`, `31+35x32`, tail `9f06936a...`.
- Falsified alongside: `16 IV+1152 raw-CBC` split; `E_S=begbeb...` mask; prime-removal `765-pi(570)=661` as byte-exact derivation (lengths match, content 249/661).
- Final selector: 7 blocks with `0x77` at `[0,2,3,8,9,12,26]`, 22/35 valid X; ~27k scalar/point candidates vs `X=f4d1bbd9...` / `a955...` / `4bc468...` -> 0 hits.
- Status: decrypt `STRONGLY_SUPPORTED` as reproduction / `UNVERIFIED` as author design (discovery #23, #25): mask `b657264f...` is secondary-only (GalloClaudio64 #68, no author source); free 8B mask forces 8B `Salted__`; plaintext entropy 7.83 / chi2 253 uniform with zero internal relations (consistent with chance-valid padding too). `cosmic_A.bin cd3fea...` / `K_I1` / `row1-4` are secondary folklore (issues #87/#88/#92/#104, no author source, no bytes) — not proven blockers. 2026-09-09 addenda: operand-multiplier, selector-weights, 0x77-parity point-sum (0 hits); 19 scalar + 12 XOR + 10 hash families (0 hits); 5x7/7x5 not one-per-group; reverse/XOR-pair/SHA-vs-X 0 hits. Discovery #25 addendum: E_B 2B-slice sweep (1326 offsets, 11 valid vs 5.2 expected, `+-` unique to `59cc`) — weak support, no replacement key; 15-char char-value selector-indexing FALSIFIED (~10k, 0 hits, Dead End #7).

### CLM-010 — 15-char mask correction + h,i-avoidance anomaly

- Sources: `experiments/sal_final_search/sal_regions.json` (LEAD91/MID104/TAIL570); URL `gsmg.io/theseedisplanted` LSBs `111101110011110110010010`.
- Method: raw765 1-indexed primes<=570 removal -> 661B; `8k+7` extraction -> `begbbebebabbbbabbbfccfgg` (verified); mask keep -> correct `begbebebbbbbbcg` (published `begbebebbbbbcgg` is a double-flip 10<->23 transcription error; corrected idx `[1,4,6,1,4,1,4,1,1,1,1,1,1,2,6]`).
- Anomaly: sieved offsets `8k+7` AND `8k+2` both avoid `h,i` over all 24 chars (max idx 6); kept/dropped splits also all a-g. P(single)~0.006, P(>=2/8)~0.0007.
- Status: correction `STRONGLY_SUPPORTED` (byte-exact mask recompute); anomaly `SUPPORTED` as structural signal (needs replication); onward selector-routing use `FALSIFIED` for tested sets (580 candidates, 0 hits). See discoveries #25, Dead End #7.
- Discovery #26 update: full 8-offset table 0:23, 1:19, 2:24, 3:23, 4:22, 5:23, 6:22, 7:24 — strict "all four primes 24/24" FALSIFIED (off3: 1x h; off5: 1x i). Probability figure corrected: alphabet is 9 (a-i), naive p=(7/9)^24~0.0024, NOT (7/24)^24. Joint 4x24 prime plane 94/96 (tail p~3.6e-7); non-prime plane 86/96 (p~0.015); Fisher prime-vs-nonprime p~0.033 (control passes — depletion, not confinement; both halves span all 9 symbols). Natural-mapping routing battery (A/B/C/D, P96, R96 x id/rev x sum/xor x +-op x S/2S/S/2/+-1 = 240) -> 0 hits. 161-token leg BLOCKED (no local value transcription).
- Discovery #27 update: clue wording authenticated in-capture (`phase3.2.ipynb:359`); dimensions verified (1152=72x16=24x3x16=48x24; 35=7x5; marker rows `10110/00011/00100/00000/00000/01000/00000`). Pre-registered Tier 1 (4 SHA256, best overlap 10/64 chance P~0.13 — not promoted), Tier 2 (decimal BE/LE + sha, 24-digit ~80-bit mismatch), Tier 3 (`SHA256(S2)^SHA256(S7)` x 8 EC), group-sum routing (0/45), mod-35 routing (0/60) — ALL 0 hits (Dead End #8). Dimensional correspondence PROMOTED to SUPPORTED structure (H-DIM-003) with two defined open bridges.
- Discovery #28 update: pair census 16 unique/24, symmetry 5/12/7 (p~0.18), Delta mean|d|=1.917 with 20k-shuffle nulls 0.20/0.54/0.33/0.78 (all chance) — distinct-address form FALSIFIED with no invented mapping (Dead End #9, H-PAIR-004); general form + 23->24 reinsertion BLOCKED (function/target missing). Layer pinning verified byte-exact: 24x48 exact on 1152B CT (72 AES blocks) and padded pt, inexact on 1151B parse — bridge (a) now constrained to the 1152-byte layer.
- Discovery #29 update: routing-matrix report audited claim-by-claim. Surjection claim reclassified TAUTOLOGY (pairs derive FROM the 24 positions; no pair->byte-group function stated — weight zero). Coordinate mapping reproduced exactly (4/16 at (0,0),(0,2),(1,4),(5,1)) then nullified: 20k-shuffle P(>=4) ~ 0.49 (Dead End #10, H-COORD-005). Prime row/col sums independently confirmed negative (40 candidates, 0 hits). 23->24 mechanics + marker-operation EC specifics UNTESTED (nothing runnable stated). "99% solved" rejected: all mechanism batteries negative.
- Falsification round, no discovery entry (threshold unmet): ground-truth recompute corrects intra-block offsets to [0,2,13,9,28,4,10,31,14,9] (reported list wrong x3) -> mod-5 chi2=3.0 p~0.56, kill confirmed stronger; sum-120 verified but parse-insensitive + post-hoc (coincidence grade kept). Operand 23+7 split run as specified: 1/23 <23 (P~0.89), 1/7 <7 (P~0.18) — dead by own range rule, rescues declined as fishing. Modular projection (primes x {0,1}, 160 checks) 0 hits. (Dead End #13, H-OPSPLIT-008/H-MODPROJ-009/H-MOD5-010.)
- Round-9 audit, no discovery entry: re-verified the three kills on ground truth and closed every rescue path the report left open — P1 zeroing (prime-positions + B-indicated) validity False/False; P2 SHA256(operand) mod35 1/7 overlap (~chance 1.4); P3 re-framed to intra-block offsets with EXACT DP P(sum=120)=0.0068 but two-sided ~0.24 (as-specified frame would false-positive); clue-prime factorization battery min p 0.285 (Bonferroni 0.005; post-hoc 11-cluster killed by multiplicity); modular chi-squares 0.309/0.509/0.920/0.447. Corrected three report data errors (positions x3, chi-square numbers, 0-of-23) and one spec error (P3 frame); flagged stale "3-bit packing 🟡" and overstated five-source independence (~2-3 origins). (Dead End #14.)
- 36x32-bridge round, no discovery entry: slip relations verified byte-exact (R[0]=H+K[0][:1], R[j]=K[j-1][1:]+K[j][:1], R[35]=K[34][1:]+pad) — row-dropping refuted by construction; 1152-1120=32 reduces to header(31)+pad(1). Batteries: exact/SHA/alignments/reverse/rotate/all-36-removals miss; cross-layer 36 rows 0 hits (validity P~1); 18 prime-coefficient (u,v)->(r,c) variants, 360 checks, 0 hits. Lattice identities verified, mechanism-free. (Dead End #15, H-BRIDGE-011.)
- Falsification round, no discovery entry (threshold unmet): Branch 1 (layouts A/B/C/D, uniform first-marker rules, O1+reverse orders, per-stream/layout/chain x EC = 420) 0 hits — plus underdetermination note (O1-vs-O2 assignments diverge; scalar/point orders coincide by group law, run once). Branch 2 headline 3-bit packing ILL-FORMED (max symbol 8 > 3-bit cells; same lone off5 outlier as #26); post-hoc 4-bit fallback (fwd/rev, 48B, first/last-32 exact+EC = 36) 0 hits. (Dead Ends #11/#12, H-OPS-006/H-PACK-007.)

### CLM-011 — even256/TAIL sequential drift (order-level structure)

- Sources: even256 (Bifid even minus I/O, 256 chars, sha `1740b55b...`); TAIL570 + LEAD91 (`sal_regions.json`); Chain-4 1151B (`e4269ed5...`); exact oracle `X=f4d1...`/h160s/door (coincurve, comp+uncomp).
- Method: 16x16 row-homogeneity chi2 (df 330) + 2000-shuffle null; early128 vs late128 halves (df 22); TAIL early-j (284) vs late-j (286) split (df 8); halves-empirical count control (df 24); max-row shuffle null (2000 perms); 6-candidate halves-key battery (SHA256/base-23 x early/late/concats).
- Result: rows chi2 415.0 p~0.001, shuffle P>=obs 0.0005; halves chi2 40.6 p~0.009; TAIL early-j chi2 18.4 p~0.018 (a/b/g/i/h driven, mechanism-checked through Bifid columns to even S/B excess). Counts control null-consistent (19.6, p~0.72) — structure is ORDER, not bag-of-letters. No outlier row (P~0.20). Key battery 0/6.
- Status: drift `SUPPORTED` as structural lead (needs independent-object replication — LEAD91 too short, 161 exhausted); halves-key use `FALSIFIED`. See discoveries #40, Dead Ends #26-#27.

### CLM-012 — On-chain author-vs-solver separation (solver dust excluded)

- Sources: read-only Blockstream API for `1GSMG1JC...` (126 txs) / `17ucy1K9...` (45 txs); planted ledger `planted-addresses.csv`; escrow `a82052a2...` (#24); Half/Better public privkeys.
- Method: per-tx input-address + amount + OP_RETURN + block-height audit; witness-program decode; secret-vs-public privkey separation; redeem-script inspection (`bd1b5d81b3...` -> P2SH `OP_0 <P2WPKH 2780438f...>`).
- Result: 2026 bursts (blocks 938165/944096) every token/quote OP_RETURN spends a public key — e.g. `3f0f28b973b1ee22` (Half->17ucy+bc1), `a4355923...` (Better->17ucy+hereismysecret), `0a756d0b9a...` (Better->1GSMG+Matrix quote); embedded `bc1qks8zrshwmu3m8vgqdzwl2u8jjfgnvgjlezwqcd` is a solver P2WPKH (`b40e21c2...`, 14/13 fund/spend, 546-sat balance). Author objects (P-escrow, planted-2020, `2aa9a4a90be819d5`/`88cdb3cdca12b471` splits) carry no token OP_RETURNs.
- Status: solver dust `CONFIRMED` as secondary (EXCLUDED as inputs); author-routing reading of Half/Better dust `FALSIFIED` (no author txid; E5 stays UNVERIFIED for author); guardrail `SUPPORTED` (on-chain work bounded to author objects). See discovery #41.

### CLM-013 — External witnessed sweep boundary (floflo777, secondary, not re-swept)

- Sources: `raw/github/floflo777-open-crypto-puzzles/1-big-prizes/gsmg-io-5btc-puzzle/analysis/tested.md` (rows 1-7, 9, 15-19), `analysis/leads.md`, `clues/author-posts.md`, folder `README.md` (all secondary; witnesses internal to that repo, not locally reproduced).
- Results taken as boundaries (counts/methods/dates as reported, 2026-07-28 to 2026-09-02): rows 1-7 = 335,724,615 submissions on the 256-object/direct readings (letter-to-bit masks x 21 orders 335M; 16+7 alphabet partitions 490,314; 32-ASCII windows 34k; Base58 windows 17k; Base58Check substrings 123k with zero valid checksums; large-blob direct 59k + uniform-entropy note; taijitu analytic refutation) + row 8 partial literal replay 116,043 + row 9 small-blob pipeline 1,358,577 (SHA-256 derivation) + rows 15-19: word-window passwords 400k+ cands / 24.8M decrypts, stage-answer/matrix/string battery, interleavings/hashes/digits/poem/nested layers, every-substring-vs-planted (25M+8M+3M), third-door six-construction sweep 25.5M — ALL 0 match with stated witnesses. Row 14 retracts the community Cosmic MD5 decrypt as a padding accident (93/20000 random keys valid ~ 1/256; reference plaintext uniform) and documents the creator convention from the 2020-11-12 archived Phase 2/3 page: `Ciphered with aes-256-cbc /w base64 sha-256(password)`, `parts 1..7 -> sha-256 -> dgst is the password` (SHA-256 only).
- Open external leads (not ours to execute blindly): dynamic-candidate replay of 98/213 filtered scripts (hours-days, needs the private scripts); single-tool identification (Bifid with no period parameter = full-length, short cipher menu — tool name in private research, requested not guessed); esrever remainder on lock plaintexts/Dualite; whether the 256-object is the right object (lead 7: I/O-drop Base58-validity argues for, 1e-17 all-uppercase argues against); third-door creator-rule readings + GPU pass.
- Local deltas this round: Dead End #27's even-substring leg CORROBORATES row 3 (overlap, not novel); Dead End #29 CLOSES external lead 6 (29 dropped letters) on both sides with a local battery (8 oracle + 16 lock attempts, 0 hits); KDF tension noted for CLM-009 (documented SHA-256 vs MD5-verified small-blob Chain-1 with WIF+E_C cross-checks and Cosmic repro — repro stands, design stays UNVERIFIED).
- Status: `SECONDARY` (no-repeat rule: these rows will not be re-swept here); corroborations noted where our batteries overlap (rows 3/4).

### CLM-015 — May-2026 compact-signature witness branch (secondary solver activity)

- Source: complete six-page Blockstream address history for `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`, plus the linked transaction chain, captured under `raw/web/live/chain/` on 2026-09-14.
- Newly saved target transaction: `973646bb3204b9e67e0fcb58efabe951aaf3714020c277f77092ae59bc1a1bd6`, block 949664, OP_RETURN ASCII `GSMG WITNESS BLK 949653 TX 808f812f`.
- The referenced block 949653 contains two previously unsaved binary OP_RETURNs:
  - `808f812f13a3137e48a0c95a818ae661a80fafaf409237efbb4b62b8198a4c13`, header `GSMGJH`, payload length 65, bytes `20` + `0495c689eb5aef53f7fa1ef650c56eac1a0e1b590f2a82fe6ddb7484ece385b37545eba470edae4316701263ce3abb194eca111d6107add0a30aab8bd77785f5`.
  - `22381b6013973fedbe7821eb82e60d50ef61ee6e430896bd47f209b12157614b`, header `GSMGBH`, payload length 65, bytes `1f` + `3afc610c1befe34300a07ec01e74c6b7f1e870dd3ff7e46e726363d0c9f18451650af99010f0495f43c1a332d45190631275191e429aa2dc1aae3b25ec79b35f`.
- Format test: `0x1f` and `0x20` are valid Bitcoin compact-signature headers (compressed-key recovery IDs 0 and 1); each following 64-byte body has in-range ECDSA `r` and `s`. This confirms a strong serialization match, not the signed message or the recovered key. Candidate-message recovery tests did not recover the target or sender key.
- Provenance: both binary records spend and return to vanity address `1GSMG9VDLTU6jyuG7bkNMdmnHBLtbbM51M`, whose exact history also contains `secondanswer`, `yourlastcommand`, `isolveditwithanabacus`, `leavethematrix`, and `hereismysecret`. Its first funding transaction (`0b609ab3...`, block 949573) consolidates inputs from burn-looking `11111119536NnU2vPAvoQhvkheQ8ejYJ`; the address is therefore classified as solver activity, not author material.
- Status: `CONFIRMED` chain facts and compact-signature serialization; `SECONDARY/SOLVER` provenance; `OPEN` signed-message/preimage interpretation. The target-address 546-sat output is a witness claim, not proof of the target private key.
- Capture note: `target_txs_p3_20260914/response.bin` and `target_txs_p3_bad_placeholder/response.bin` are retained as failed cursor controls (empty JSON and a repeated first page respectively); the authoritative third page is `target_txs_p3_20260914_real/response.bin`.

### CLM-016 — 546-sat / `hereismysecret` frequency test

- Source: the complete 126-transaction target-address capture in `raw/web/live/chain/`, with input-address and output-value grouping.
- Counts: 81 transactions contain OP_RETURN; 77 target-address outputs are exactly 546 sats; 70 of the 81 OP_RETURN transactions pair an OP_RETURN with a 546-sat output.
- Provenance split of those OP_RETURN+546 pairs: 32 spend from Better `145ZQ9siLrsXBKf465wjdyQYAP5dRwhRhQ`, 32 spend from Half `1JG648yaB7Wp2dpUfcZoRSD4q35oq47vCu`, and only 1 is the new solver vanity wallet `1GSMG9VD...`; the remaining 5 are isolated older solver/test wallets. This is consistent with repeated solver dust-token construction, not a unique author channel.
- `hereismysecret` appears in three target-address records, all with 546 sats: `25c037ecc5f9b59ada0f3a51618c7208dd370eda0ddccf9984004ffd96f6e6a2` (Half, block 938164), `a589629df479a801137db3ada8e60f64020848ae73851490e7e2aeae49f88351` (Half, block 944086), and `a2a702abbd3ae2edf0d67224d9a4a1c29c2bd53621437e6feb253677de2ec00a` (Better, block 944086). The new May-2026 witness also uses 546, but is from the separate solver vanity wallet.
- Control: earlier isolated OP_RETURN records use varied values, including 600, 700, 864, 1,000, 2,026, 2,680, and 10,000 sats. The original 2020 `Halving` record uses 700 sats, not 546.
- Interpretation: 546 is the standard Bitcoin Core P2PKH dust threshold at the default 3000 sat/kvB dust relay rate, so its recurrence is expected for solver timestamp/dust transactions. It may still function as a puzzle convention, but the chain alone does not support it as an author-only numeric hint. See Bitcoin Core's [`GetDustThreshold`](https://github.com/bitcoin/bitcoin/blob/master/src/policy/policy.cpp).
- Status: `CONFIRMED` as a 546-sat solver-token convention; `SUPPORTED` that `hereismysecret` is deliberately echoed by solvers; `WEAK/OPEN` as a creator hint.

### CLM-017 — Order/Genesis bounded continuation battery

- Source: canonical `TAIL570`/`LEAD91` and the Genesis hex literal in the primary Phase-2 README; exact oracle `experiments/sal_final_search/dual_oracle.py`.
- Method: reconstructed `even256`, then tested adjacent and second differences, absolute differences, run lengths, 16x16 row/column/snake/spiral/dihedral routes, 23x23 transition matrices, and a bounded Genesis 3x23 route family (row/column/snake/spiral, row permutations, cyclic column shifts, Caesar variants, casing/reversal/hash forms).
- Result: 820 unique candidates, 21 valid-padding events, 0 exact target-address matches and 0 third-door matches. Oracle selftest passed before the run. Report: `experiments/next_stage/order_genesis_battery_report.json`; runner: `experiments/next_stage/order_genesis_battery.py`.
- Order diagnostic: no distinguished period at 16, 23, or 7. The strongest lag mutual-information fluctuation was lag 58, with shuffle p≈0.044 before accounting for 64 tested lags; 16x16 row/column transitions were not exceptional. This does not falsify the previously measured halves/order drift, but it gives no stated sequential key.
- Status: tested transformations `FALSIFIED` as key/door readings; order drift remains `SUPPORTED` as a structural lead; Genesis 3x23 remains `OPEN` only for a more specifically motivated cipher operation.

### CLM-018 — Independent even256 frequency-family closure

- Source: canonical `even256` reconstructed from `TAIL570` using `sal_bifid.py`; exact oracle `dual_oracle.py`.
- Method: frequency vectors in multiple encodings, ascending/descending frequency alphabets, stable tie orders, rank streams, selected/complement alphabets at every observed count boundary, count-modular and XOR streams, reversals, SHA-256/MD5/hex forms.
- Result: 604 unique candidates, 8 valid-padding events, 0 exact target-address matches, 0 third-door matches. Oracle selftest passed. Report: `experiments/next_stage/frequency_even_battery_report.json`; runner: `experiments/next_stage/frequency_even_battery.py`.
- Status: this bounded frequency/string family is `FALSIFIED`; no further frequency-only work is justified unless new primary evidence changes the input or mapping.

### CLM-019 — Superseded image-copy comparison (self-inflicted test-fixture error)

- Source: the user-authorized canonical image `raw/github/puzzlehunt-gsmgio-5btc-puzzle/working/puzzle.png`, SHA-256 `38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830c`.
- The five-cell discrepancy came from an erroneous temporary comparison literal in the new test runner, not from the public README or the canonical PNG. Center sampling also let bunny line-art contaminate one cell.
- Status: `RETRACTED`; superseded by CLM-020 below. No raw artifact was changed.

### CLM-020 — Canonical image and README matrix agree; corrected battery rerun

- Source: canonical `raw/github/puzzlehunt-gsmgio-5btc-puzzle/working/puzzle.png`, SHA-256 `38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830c`, and the matrix printed in its README.
- Method: dominant exact-fill classification over every 75×75 cell, followed by a direct byte comparison with the 14×14 README matrix. This avoids the bunny-contaminated center sample and uses the corrected comparison fixture.
- Result: the matrix matches exactly; there are no differing cells. Counts are `K=86/W=86/B=15/Y=9`, leftover `0000`, URL `gsmg.io/theseedisplanted`, and B/Y frame `111101110011110110010010`.
- Corrected image-instruction battery: 797 deduplicated transparent candidates, 22 valid-padding events, 0 exact target matches, and 0 third-door matches. Report: `experiments/next_stage/grid_instruction_battery_report.json`; runner: `experiments/next_stage/grid_instruction_battery.py`.
- Status: `CONFIRMED` for the canonical grid, the public matrix agreement, and the corrected negative battery. The old K/W-balance claim is restored; the five-cell/87-85/0100 branch is closed as a test error.

### CLM-021 — Genesis 3×23 matrix-sum continuation

- Source: the exact 69-byte Bitcoin Genesis source literal in the primary README, arranged as 3×23, plus the proven B/Y frame and the stated prime basics `{2,3,5,7}`.
- Method: direct row/column `matrixsumlist` readings on ASCII and A1Z26 matrices; prime-column zeroing; all 24 permutations of repeated prime-basic reinsertion at 1-based prime columns; eight bounded B/Y repeated-mask offsets; and the reported secondary pair `490/497` in both orders and transparent encodings.
- Result: 4,210 unique candidates, 114 chance-valid padding events, 0 exact target-address matches, and 0 third-door matches. Report: `experiments/next_stage/genesis_matrixsum_battery_report.json`; runner: `experiments/next_stage/genesis_matrixsum_battery.py`.
- Status: `FALSIFIED` for these direct Genesis matrix-sum/prime-reinsert/BY-mask readings. The exact Genesis 3×23 object remains `CONFIRMED`; a separately specified semantic answer-selection operation remains open.

### CLM-022 — Bifid → prime/zero → matrix-sum continuation

- Source: canonical `LEAD91`/`TAIL570`, the reproducible 5×5 `DBIFHCEGA` full-period Bifid decode, and the exact dual-lock/third-door oracle.
- Confirmed upstream: the decode is byte-for-byte reproducible, begins `BTCSEED`, and yields the canonical `even256` SHA-256 `1740b55ba5d224e86f61054bacd7caf90a8cf2c4418535c67d092903c4509f35`.
- Method: the clue-faithful order Bifid → prime-valued/prime-position zeroing → 7×13 and 19×30 row/column sums, including the previously untested 20+49=69 composite and offset-0/7 forms.
- Result: 640 candidates, 18 valid-padding events, 0 exact target matches, and 0 third-door matches. Report: `experiments/next_stage/bifid_prime_matrix_battery_report.json`; runner: `experiments/next_stage/bifid_prime_matrix_battery.py`.
- Status: the tested direct continuation is `FALSIFIED`; `BTCSEED`/Bifid and the 69=3×23 geometry remain `CONFIRMED` structural facts.

### CLM-023 — 16×16 even256 prime/zero matrix battery

- Source: canonical Bifid-derived `even256`, exact `dual_oracle.py`, and its selftest.
- Method: 16×16 row/column, paired row+column, reverse, difference, and dual readings under no mask, prime-value, full-prime-value, and prime-position zeroing; both rank bases and six transparent encodings.
- Result: 4,608 candidates, 146 valid-padding events, 0 exact target matches, and 0 third-door matches. Report: `experiments/next_stage/even256_prime_matrix_battery_report.json`; runner: `experiments/next_stage/even256_prime_matrix_battery.py`.
- Status: direct 16×16 prime/matrix readings are `FALSIFIED`; the ordered even256 object remains a `SUPPORTED` structural waypoint, not a key.

### CLM-024 — Aligned yin/yang selector construction

- Source: the canonical 570-character Bifid decode split into 285/285 halves. Removing the 29 `I/O` markers from the diverse half leaves 256 positions, and the corresponding symbols in the other half form a 256-character `B/C/D/E` selector.
- Method: complete 4-way stable-bucket routes, all 24 selector orderings, 2-bit encodings, aligned add/subtract/XOR/multiply ranks, and pair byte encodings.
- Result: 304 candidates, 6 valid-padding events, 0 exact target matches, and 0 third-door matches. Report: `experiments/next_stage/yinyang_selector_battery_report.json`; runner: `experiments/next_stage/yinyang_selector_battery.py`.
- Status: the 256-aligned selector is `CONFIRMED` as a reproducible structural object; the tested selector/key readings are `FALSIFIED`. Any revival needs a specified yin/yang operation, not another bucket permutation.

### CLM-025 — Explicit B/C/D/E → `{2,3,5,7}` selector battery

- Source: the 256-position aligned yin/yang object used in CLM-024, with every `B/C/D/E` selector symbol mapped through all 24 permutations of the prime basics `{2,3,5,7}`.
- Method: aligned add/subtract/multiply/XOR and squared/cubed combinations against both rank-0 and rank-1 even256 payload values; raw/mod-23/mod-256 forms; reverse forms; letter, byte, hexadecimal, decimal, CSV, SHA-256, and 16×16 row/column matrix summaries; plus prime-selector-only streams.
- Result: 24,432 unique candidates, 745 chance-valid padding events, 0 exact target-address matches, and 0 third-door matches. Oracle selftest passed. Report: `experiments/next_stage/prime_selector_battery_report.json`; runner: `experiments/next_stage/prime_selector_battery.py`.
- Status: the explicit numeric reading of the aligned selector as `{2,3,5,7}` is `FALSIFIED` for this bounded family. The alignment itself remains a `CONFIRMED` structural object; a revival needs an author-specified operation beyond numeric substitution.

### CLM-026 — Canonical 6+5 southeast B/Y chain battery

- Source: the canonical puzzle image, classified from pixels under the AGENTS.md authority rule. The two contiguous southeast B/Y components are exactly `BYYBYB` (6 cells) and `YYYYB` (5 cells).
- Method: both chain orders, both B/Y bit polarities, forward/reverse readings, each chain and their concatenation, binary/decimal/hex/ASCII/colour strings, SHA-256 encodings, and the URL characters selected by the proven B/Y frame relation were checked against the exact dual-lock and third-door oracles.
- Result: 202 unique candidates, 5 chance-valid padding events, 0 exact target-address matches, and 0 third-door matches. Report: `experiments/next_stage/by_diagonal_chain_battery_report.json`; runner: `experiments/next_stage/by_diagonal_chain_battery.py`.
- Status: the 6+5 chain geometry and strings are `CONFIRMED` image facts; their direct key/door readings are `FALSIFIED`.

### CLM-027 — 2026-09-14 target-history refresh: latest fan-out is solver activity

- Source: `raw/web/live/chain/target_txs_p0_20260914/response.bin` and provenance, refreshed at `2026-09-14T18:52:10Z`. Latest confirmed target transaction: `a751791bf7125e2ba94fd451900391a1cd3a50f01e09ec461450ac0de1d1945e`, block `964501`, capture SHA-256 `63669d980cc283419572d6de3136325191fb1524e3a1ec9c04dd917f007c9bd5`.
- Outputs include `864` sats to the prize address and `546` sats to `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`; there is no OP_RETURN. The transaction returns `26289` sats to input address `1LuCK86cRc8sRwjbojEGPHHeHz1eJQSTjD`.
- Input-lineage check: `1LuCK...` was funded by `8fec143d...` (block `964476`), which distributes seven 600-sat outputs to solver/test addresses. It then redistributes the `a751...` outputs in `b13e0b365f3659b36322a186e9281c3e6e7ead846499f95843f5fda1808fdb53` (block `964521`). This is a chained solver fan-out, not an author OP_RETURN channel.
- The earlier OP_RETURN witness remains the separate `973646bb...` record at block `949664`; no newer target-address OP_RETURN appears in the refreshed history.
- Status: block/amount/script facts `CONFIRMED`; 546/864 as a puzzle hint `FALSIFIED for this lineage`; newest OP_RETURN discovery `NONE`.

### CLM-028 — Issue #67 merlon attachments recovered and audited

- Source: the two public image attachments embedded in GitHub Issue #67,
  preserved under `raw/github/puzzlehunt-gsmgio-5btc-puzzle/issues/67/attachments/`
  with URL, dimensions, and SHA-256 provenance.
- `merlon_original.png` is 1156×815 (`74f02405…`); it shows a partial QR-like
  object and the highlighted merlon. `merlon_colors.png` is 794×797
  (`e7c1aa34…`); its marked object has a deterministic 560×560 crop at
  `(118,118)`, divisible into 14×14 40px modules.
- The attachment-local 14×14 crop is reproducible and has exact symbol counts
  `R=72/W=60/K=64`, with the central `K` chamber occupying 8×8 cells. This is
  a newly saved research object, not the canonical `puzzle.png` grid.
- Method: symbol routes, per-symbol masks, ternary assignments, perimeter
  readings, row/column counts, and all six nonconstant packed-bit assignments
  were tested through the dual-lock/third-door oracle. Oracle selftest passed.
- Result: 300 deduplicated candidates, 30 valid-padding accidents, 0 exact
  target matches, 0 third-door matches, and 0 direct SHA-256-to-target matches.
  Report: `experiments/next_stage/issue67_merlon_battery_report.json`; runner:
  `experiments/next_stage/issue67_merlon_battery.py`.
- Status: the attachment and 14×14 crop are `CONFIRMED` as secondary source
  evidence; direct merlon encodings are `FALSIFIED` as key/door readings.
  The full QR payload remains unavailable because the original screenshot is
  clipped, so this does not close the merlon branch generally.

### CLM-029 — 2026 hint phrase family and direct target check

- Source: exact wording from the decoded 2026-01-01 binary hint and the
  2026-07-12 messages, plus the puzzle's visible final-page tokens.
- Method: 3,724 bounded phrase normalizations and explicitly motivated
  context combinations were tested against both AES locks and the planted
  third-door oracle, with the oracle selftest first. Each candidate was also
  checked as `SHA256(candidate)` for the uncompressed target address.
- Result: 105 valid-padding accidents, 0 lock hits, 0 third-door hits, and 0
  direct target hits. Report:
  `experiments/next_stage/semantic_hint_battery_report.json`; runner:
  `experiments/next_stage/semantic_hint_battery.py`.
- Status: this explicit phrase family is `FALSIFIED`; “human-context final
  answer” remains open only in the much larger, semantically unspecified
  space.

### CLM-030 — GF(256) 4×16 matrix continuation

- Source: the public exploratory 68-byte interpretation (`4×16-byte blocks +
  four x-coordinates`), independently reproduced locally, with the exact
  uncompressed target hash160 and planted-address controls.
- Method: all 30 irreducible degree-8 binary fields; the reported point order
  for each field; every 2,520 ordering in the AES field; triangle level 3 (the
  natural 4×16 row); 44 finite matrix representations consisting of
  row/column serializations, reversals, row/column XOR and byte-sum lists;
  SHA-256 and double-SHA-256 finalization.
- Result: 2,549 order/field cases and 224,312 hash/address checks. There were
  no exact target matches and no planted-door matches. Only two candidates
  reached a two-byte target-hash prefix: the known external near-miss
  `a955a042…` and one separate matrix-sum serialization `a955bfa2…`.
- Status: the tested 4×16 serialization/reduction family is `FALSIFIED` as a
  key route. The external near-miss remains a reproducible coincidence/lead,
  not a solution; its source branch is not an author-confirmed artifact.
  Report: `experiments/next_stage/gf256_matrix_probe_report.json`; runner:
  `experiments/next_stage/gf256_matrix_probe.py`.

### CLM-031 — 2023 hint bytes recovered and 7×23 matrix made concrete

- Source: canonical secondary hint image
  `raw/github/Naddiseo-gsmgio-5btc-puzzle/working/hints/2023-02-23.png`,
  SHA-256 `5dddf73995c45497facb034e3d38d2bbbe3642603b15fce22e118d34209c0197`.
- Method: OCR of the eight-bit tokens, cross-checked against the image layout;
  exactly 161 tokens were recovered. Every byte has low three bits `110`.
  Reversing each byte's bits and reversing token order yields the exact
  message beginning `yellowblueprimesmatrixsumlist` and ending
  `verylaststepisatruegiveawaypromised`.
- New concrete object: the five upper bits form a 161-value `7×23` matrix;
  token SHA-256 is
  `ca3d8ab58d893c9a3b955adbdb4f6bf812dd86941401f2d583729e1c1e16c5f5`.
- Method after recovery: row/column routes and reversals; prime-row and
  prime-column keep/zero masks; finite reinsertion permutations of `{2,3,5,7}`;
  row/column sum lists; raw, decimal, CSV, hex, Base32, and valid Base32
  decodings; SHA-256 and double-SHA-256 target checks.
- Result: 2,337 deduplicated candidates and 4,674 exact hash/address checks,
  with zero target matches. The one-byte prefixes in the ranking are
  chance-level and do not extend to a second byte.
- Status: the 161-byte source and 7×23 structure are `CONFIRMED`; this finite
  7×23 reduction family is `FALSIFIED` as the key route. The broader
  23/16/7 mechanism remains open because the author’s operation is still not
  specified.
- Report: `experiments/next_stage/hint161_matrix_probe_report.json`; runner:
  `experiments/next_stage/hint161_matrix_probe.py`.

### CLM-032 — Author-recorded `giveit` prefix transfer

- Source: `raw/github/Naddiseo-gsmgio-5btc-puzzle/working/phase3.ipynb`, where
  the author says to add `giveit` in front; the notebook's executed output
  provides a known-answer witness for the normalized prefix convention.
- Method: verify the known Phase-3 planted-address answer, then prefix `giveit`
  or `give it` to 21 literal image/final-hint objects under exact, lowercase,
  compact, and spaced normalizations.
- Result: 252 deduplicated candidates, 12 valid-padding accidents, 0 AES-lock
  hits, 0 third-door hits, and 0 direct SHA-256 target hits.
- Status: historical prefix convention `CONFIRMED`; this direct final-object
  transfer `FALSIFIED`. Report: `experiments/next_stage/front_prefix_probe_report.json`;
  runner: `experiments/next_stage/front_prefix_probe.py`.

### CLM-033 — Whole-bitstream `esrever` transfer

- Source: the confirmed bit-reversal convention and the canonical Bifid-derived full/half/256-symbol objects.
- Method: whole-bitstream reversal, per-byte reversal, aligned windows, raw/digest/hex/Base64 renderings, both locks, and the planted-door oracle.
- Result: 180 records, 0 lock hits, 0 third-door hits. Report: `experiments/next_stage/esrever_binary_probe_report.json`; runner: `experiments/next_stage/esrever_binary_probe.py`.
- Status: `esrever` itself remains `CONFIRMED` on its known witness; this transfer is `FALSIFIED`.

### CLM-034 — Full source-order synthesis

- Source: the seven-token chain and the published seven-part source corpus.
- Method: 16-item and seven-token concatenations, spacing, item/character reversal, odd/even item selections, SHA-256 forms, and XOR-of-digest forms. Genesis was tested as hex, exact decoded bytes, and conventional spelling.
- Result: 115 candidates, 0 lock hits, 0 third-door hits. Report: `experiments/next_stage/full_password_synthesis_probe_report.json`; runner: `experiments/next_stage/full_password_synthesis_probe.py`.
- Status: this bounded “intertwined password” family is `FALSIFIED`.

### CLM-035 — Genesis prime-position reinsertion

- Source: the exact 69-byte Genesis source object and the stated prime basics `2,3,5,7`.
- Method: every permutation as replacement at 1-based positions 2,3,5,7, and every before/after insertion variant, with direct/reversed/digest renderings.
- Result: 864 candidates, 0 lock hits, 0 third-door hits. Report: `experiments/next_stage/prime_basic_position_probe_report.json`; runner: `experiments/next_stage/prime_basic_position_probe.py`.
- Status: this literal positional interpretation is `FALSIFIED`.

### CLM-036 — LEAD91 triangular matrix

- Source: the canonical 91-symbol lead stream and the confirmed `matrixsumlist` instruction.
- Method: 13-row triangular placement in a 13×13 square, left/right alignment, both digit maps, reversal, prime-value/prime-position zeroing, row/column sums, and transparent/digest forms.
- Result: 2,880 candidates, 0 lock hits, 0 third-door hits. Report: `experiments/next_stage/lead_triangle_matrix_probe_report.json`; runner: `experiments/next_stage/lead_triangle_matrix_probe.py`.
- Status: triangular geometry is `CONFIRMED`; this direct matrix-sum family is `FALSIFIED` as the final key route.

### CLM-037 — Triangular LEAD-to-TAIL selector

- Source: the triangular `LEAD91` stream and the confirmed `LEAD`/`TAIL` ordering.
- Method: triangular row/column sums as direct 0- or 1-based, cumulative or non-cumulative modulo indices into raw `TAIL570`, full Bifid output, and `even256`; direct/reversed/SHA-256 forms were checked.
- Result: 1,728 candidates, 0 lock hits, 0 third-door hits. Report: `experiments/next_stage/lead_triangle_tail_selector_probe_report.json`; runner: `experiments/next_stage/lead_triangle_tail_selector_probe.py`.
- Status: the natural triangular selector rescue is `FALSIFIED`; the author-specific cross-stream operation remains `OPEN`.
