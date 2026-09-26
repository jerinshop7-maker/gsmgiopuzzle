# Live Hypothesis Tree

Status vocabulary: `UNTESTED`, `TESTING`, `SUPPORTED`, `STRONGLY_SUPPORTED`, `FALSIFIED`, `DECOY`, `PROVEN`.

## H0 — GSMG 5 BTC puzzle

Status: `TESTING`

The objective is to reconstruct the intended path from primary artifacts to the mechanism controlling the prize target.

### H-PROV-001 — Captured live route is a primary artifact

Status: `UNTESTED`

Supporting evidence: none locally yet.

Contradicting evidence: live content may have changed since publication.

Required test: capture exact bytes, response metadata, timestamp, and compare with dated archives and independent captures.

### H-P1-001 — Puzzle grid uses a down-first counterclockwise spiral

Status: `PROVEN`

Required test: reconstruct from the original image bytes and verify output, cell count, color classification, and leftover data without relying on copied matrices.

Supporting: PROVEN from primary bytes (discoveries #42/#52, CLM-005/020): 75px-pitch lattice at origin (0,0) in ART-001 (live re-fetch byte-identical) classifies all 196 cells by dominant canonical fill as K86/W86/B15/Y9; the README matrix matches all 196 positions; spiral reproduces `gsmg.io/theseedisplanted` byte-exact with `0000` leftover and the B/Y frame byte-exact vs URL LSBs. The same pixels give row-major yellow mask `0x41D464`. `scripts/extract_grid.py` VERIFY PASS on both canonical copies. The former K/W 87/85 and `0100` result was center-sampling contamination from bunny line-art and a bad comparison fixture, and is superseded.

### H-SAL-001 — SalPhaseIon computational regions encode deterministic data

Status: `TESTING`

Required test: preserve raw textarea bytes/code points, segment every region, test clue-justified transformations, and verify against independently sourced copies.

Supporting: five regions decode cleanly on the exact captured bytes (`matrixsumlist`, `enter`, the readable sentence, both bigint-hex tokens). LEAD91's function is now verified (first-occurrence order → Bifid square → reproduced `BTCSEED` head with exact odd-position lock; discovery #20). Contradicting: LEAD91/TAIL570 onward use stays negative across matrix-sum, cipher, prime, forensic, ordered-pipeline, and key-stream readings; the literal span sizes diverge from public writeups. Bottleneck: digit-stream onward mechanism and target-key derivation.

### H-COS-001 — A specified Cosmic Duality ciphertext/password/KDF decrypts to an intended intermediate

Status: `UNRESOLVED`

Required test: reproduce exact bytes, KDF, mode, padding, output length, structure, and independent confirmation. A padding-valid or self-hash-matching result is insufficient.

Supporting: the public 1327-byte result and matrix/base-38 outputs are reproducible from the canonical secondary repository.
Contradicting: issue #106 retracts the interpretation because PKCS#7 has a false-positive rate, the output is high entropy with no recognized format, the target hash is self-referential, and the derived values do not control either funded target. The issue's full sweep/witness set is not locally available, so the sweep conclusion itself remains secondary.

### H-BTC-001 — A candidate WIF controls the prize target

Status: `TESTING`

Required test: decode WIF, derive compressed and uncompressed public keys and HASH160 addresses, and compare exactly with the actual target address.

Supporting: targets are now precisely known: `1GSMG1JC...` (hash160 `a9553269...`, ~1.256 BTC) and `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` (hash160 `4bc46844...`, ~3.7505 BTC, fully unspent). Half/better/combos do not match either.

### H-MECH-001 — “Half and Better Half” is the actual prize mechanism

Status: `FALSIFIED` for the documented matrix-derived keys

Required test: find primary clue support and a complete cryptographic relation to the funded prize address. On-chain funding or dust activity alone is not proof.

Supporting: VIC decode literally states "THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE"; the 2020-05-11 hint states half the prize moved to `17ucy1K9...`.
Contradicting: the matrix-derived half/better keys derive only to incidental dust addresses, not to `17ucy1K9...` or `1GSMG1JC...`. So either the "half"/"better half" naming refers to the split of the prize between the two live addresses (key not yet found), or the documented matrix decode is a decoy.

### H-PRIME-001 — Primes 2,3,5,7 and "zeroing out" define the final matrix step

Status: `TESTING`

Required test: identify the specific operation (prime-indexed zeroing of rows/cols/characters) on a documented matrix/stream that yields a key controlling `1GSMG1JC...` or `17ucy1K9...`.

Supporting: author (2021-03-01) "just say which primes 2,3,5,7 we need use"; author (2021-12-25) "some characters need to be zeroed out"; author (2023-08-06) "Once you hit a 'ying yang', you'll be able to solve it the same day"; author (2023-01-09) "prime number is very important to get any further".
Contradicting: zeroing prime-indexed rows/columns of the 103x103 matrix did not produce a match in this session; too many combinations remain.

### H-GRID-001 — The 2023-02-23 binary grid encodes a final clue

Status: `SUPPORTED`

Required test: reproduce the exact image transcription and the reversible transform; then use the recovered clue to derive a target key.

Supporting: all 161 tokens have low-3-bits `110`; reversing bit order per token and reversing token order recovers a near-exact compact author message naming `yellow blue primes matrixsumlist lastwordsbeforearchichoice yinyang` and stating that the password is in front of the solver's eyes and the last step is a giveaway. The exact local transcription contains a character discrepancy (`choise`/`choice`), so character-perfect reproduction from the image remains pending.
Contradicting: upper-five-bit/Base32 interpretations were negative; the recovered message has no direct key yet.

### H-SMALL-001 — The small SalPhaseIon blob decrypts after a two-typo fix ("CADEIA" chain)

Status: `UNVERIFIED`/contested

Supporting: issue #108 claims typos at Base64 positions 18 and 51; claims K_C1 matches a WIF from issue #68 and E_C matches a chain-4 AES password.
Contradicting: positions 18/51 in the captured blob are already J/s (no-op); concatenating the two literal fragments produces 79 ciphertext bytes, not an AES-CBC block-aligned input; Naddiseo disputes the entire "CADEIA" chain; requiring modification of near-random Base64 contradicts the author's stated puzzle design. See `evidence.md` CLM-001 and `dead_ends.md` Dead End #1.

### H-OTHER-001 — A separate route (not the cosmic matrix) leads to the prize key

Status: `UNTESTED`

Required test: identify which documented stream (the 161-token grid, the second AES blob `U2FsdGVkX1+0Wl49...`, the 79-byte blob, `cosmic_A.bin`, phase 3.2.1 blob) yields the key.
Community blockers (issue #104): `cosmic_A.bin` never publicly distributed; XOR-triangle row definitions unknown; oracle hash `e2590f15...2cbd` never reproduced.

### H-OTHER-001 — A separate route (not the cosmic matrix) leads to the prize key

Status: `UNTESTED`

Required test: identify which documented stream (the 161-token grid, the second AES blob `U2FsdGVkX1+0Wl49...`, the 79-byte blob, `cosmic_A.bin`, phase 3.2.1 blob) yields the key.
Community blockers (issue #104): `cosmic_A.bin` never publicly distributed; XOR-triangle row definitions unknown; oracle hash `e2590f15...2cbd` never reproduced.

### H-SEL-001 — 15-char char-value selector indexing yields the prize key

Status: `FALSIFIED`

Required test was: map the 15 kept chars (a-i→0-8) to indices 0-6 into the 7 `0x77` selector blocks, sum 15 with repetition + 30B operand, apply author EC ops (`x2`, `/2`, `+-1`), exact oracle hit on `X=f4d1...` / `a955...` / `4bc468...` / door.
Contradicting: ~10,000 candidates across claimed+corrected+off2+all-8-offsets+ext24+dropped9 x sel7/pay28/all35 x direct/mod x sum/xor/wsum x operand/half/better x 7 EC ops + hash/multiply/zeroing/orderings/position-based (discovery #25) -> 0 hits, best prefix 3 (chance). See Dead End #7, CLM-010.

### H-ANOM-001 — Sieved h,i-avoidance is designed (selector-compatible alphabet)

Status: `TESTING` (narrowed to depletion; strict form dead — see H-PRIME-002)

Supporting: 4x24 prime plane 94/96 <=6 (binomial tail vs background p~3.6e-7); pre-registered prime-vs-nonprime control wins (94/2 vs 86/10, Fisher two-sided p~0.033); twin-24/24 rate P(>=2/8)~0.001 (discoveries #25/#26, CLM-010).
Contradicting: strict 96/96 confinement FALSE (misses in prime offsets 3,5); both halves still span all 9 symbols (prime h,i = 1+1) — depletion, not a 7-symbol alphabet; onward EC use negative (580 + 240 candidates).
Required test: replicate depletion on an independent object (161-token values are BLOCKED — no local transcription); deferred hashing/interleave step for the two pure streams (off2/off7).

### H-PRIME-002 — 4x24 prime plane is fully confined to 0..6

Status: `FALSIFIED`

Required test was: every symbol of offsets 2,3,5,7 (96 total) lies in 0..6.
Contradicting: actual 94/96 — off3 has 1x h@chunk0 (sieved pos 3), off5 has 1x i@chunk1 (sieved pos 13). Full 8-offset table: 0:23, 1:19, 2:24, 3:23, 4:22, 5:23, 6:22, 7:24 (discovery #26). The (7/24)^24 ~1e-13 figure is withdrawn (wrong denominator — alphabet is 9, correct naive p~(7/9)^24~0.0024). Surviving signal continues under H-ANOM-001 as depletion.

### H-DIM-003 — 23/16/7 dimensional correspondence frames the final mechanism

Status: `SUPPORTED` as structure, `OPEN` as mechanism

Supporting: clue wording authenticated in-capture (`phase3.2.ipynb:359`: "reinserting the prime basics ... select from over twentythree ciphers sixteen encryptions and or seven intertwined passwords ... bruteforcing might be required"); four independently authenticated dimensional correspondences — 161-token count (#5/#8) = 7x23, the decoded Genesis source literal is exactly 69B = 3x23 (#46), 1152B ciphertext = 72x16 = 24x3x16 = 48x24, and 35 scalars = 7x5 with 7 marker blocks (discovery #27).
Contradicting: every mechanism tried on it misses — Tier 1/2/3 hashing, one-marker-per-group (distribution 3/2/1/0/0/1/0), group-sum routing (0/45), mod-35 routing (0/60); Dead End #8.
Required test (exactly two open bridges, no fishing): (a) 24x3x16 addressing — needs a stated addressing function from an artifact; (b) 7x5 marker-operation matrix — selection reading dead, operation/group reading beyond sums untested.

### H-PAIR-004 — S2/S7 ordered pairs address the 24 groups

Status: `FALSIFIED` in distinct-address form, `BLOCKED` in general form

Required test was (diagnostics first, no hashes): pair census, symmetry, Delta + shuffle controls, distinct-address check (24 unique required).
Contradicting: 16 unique/24 (top (a,b)x5); symmetry 5/12/7 (p~0.18); all four shuffle nulls pass as chance (0.20/0.54/0.33/0.78); distinct form dead with zero invented constants (discovery #28, Dead End #9).
Blocked remainder: repetition-tolerant addressing and pair encodings need an 81->24 function no artifact states; 23->24 reinsertion needs a 23-symbol target whose only candidate (161 columns) is values-BLOCKED. H-DIM-003 bridge (a) is now layer-pinned: 24x3x16 addressing, IF it exists, operates at the 1152-byte CT/padded-pt layer (1152/48 exact there; 1151/48 inexact on the parse).

### H-COORD-005 — 16 unique pairs map to 7x5 marker coordinates via (x%7,y%5)

Status: `FALSIFIED`

Required test was: mapped unique-pair coordinates coincide with marker coordinates beyond chance.
Contradicting: 4/16 reproduced exactly — then nullified by pre-registered shuffle control: P(>=4) ~ 0.49 over 20k shuffles (expected ~3.2; discovery #29, Dead End #10). Mapping choices (letter encoding, mod folding) unpenalized and still chance-level. Companion surjection claim audited as tautology (pairs derive FROM the addressed positions; no pair->byte-group function ever stated).

### H-OPSPLIT-008 — 30-byte operand splits 23+7 into cipher/password selectors

Status: `FALSIFIED` as specified (natural ranges only)

Required test was: operand[0:23] bytes <23 select ciphers, operand[23:30] bytes <7 select passwords/streams, no invented mod.
Contradicting: 1/23 in range (null P~0.89), 1/7 in range (null P~0.18) — both chance-consistent; 0x77 at sub-offset 5 (value 119) out of every selector range. Rescue transforms (open zeroing/filtering/reversal) declined as unfishable. Dead End #13.

### H-MODPROJ-009 — slot=(a*i+b)%35 with a in {2,3,5,7}, b in {0,1} routes 24->35

Status: `FALSIFIED`

Required test was: 8 clue-parameterized maps x sum/xor x plain/+op x EC(5) = 160 checks vs oracle.
Contradicting: 0 hits (Dead End #13). Noted structure: a=5 cycles to 7 distinct slots, a=7 to 5 — resonance without oracle consequence.

### H-MOD5-010 — in-block 0x77 position mod 5 selects operation state

Status: `FALSIFIED` (computational correction included)

Required test was: mod-5 distribution of the ten intra-block positions vs uniform.
Contradicting: ground-truth recompute gives positions [0,2,13,9,28,4,10,31,14,9] (reported list wrong at three spots) -> counts {0:2,1:1,2:1,3:2,4:4}, chi2=3.0, p~0.56 — kill confirmed on correct data, stronger than reported. Sum-120 verified but parse-insensitive (wrong list also sums 120) + post-hoc: coincidence grade kept. Dead End #13.

### H-BRIDGE-011 — 36x32 padded layer minus one control row = 35 Chain-4 scalars

Status: `FALSIFIED` structurally (slip proof) + empirically (batteries)

Required test was: Steps A-E (36-row exact/SHA/alignment/removal/rotation), cross-layer point checks, prime-coefficient (u,v)->(r,c) family.
Contradicting: slip relations verified byte-exact (R[0]=H+K[0][:1], R[j]=K[j-1][1:]+K[j][:1], R[35]=K[34][1:]+pad) — row-dropping CANNOT yield K by construction; exact/SHA/alignments/reverse/rotate/all-36-removals miss; cross-layer 36 rows 0 hits (validity P~1); 18 mapping variants (360 checks) 0 hits. 1152-1120=32 reduces to 31+1 (header+pad). Dead End #15.

### H-OPS-006 — de-interleaved seven 5-streams x {I,+G,-G,x2,/2} yield the key

Status: `FALSIFIED`

Required test was: layouts A/B/C/D with uniform first-marker-wins rules, per-stream + layout-sum + sequential-chain candidates (scalar-accumulator exact; 420 point-checks) vs oracle.
Contradicting: 0 hits; no layout gives clean 1-marker-per-stream (A: 3/2/1/0/0/1/0, B: 1/1/2/1/0/2/0); op-order O1-vs-O2 assignments diverge wildly (position->op order is artifact-unstated, mechanism underdetermined). Dead End #11 (no discovery entry — threshold unmet).

### H-PACK-007 — 96 symbols pack as 3-bit x 96 = 36B = 32+4

Status: `FALSIFIED` as premise (ill-formed)

Required test was: 16 packing variants -> 36B -> [32][4]/[4][32] exact + EC tests.
Contradicting: max symbol 8 exceeds 3-bit cells (lone off5 `i`); premise assumed purity #26 killed (94/96). Post-hoc 4-bit fallback 0/36. Dead End #12.

### H-DRIFT-012 — even256/TAIL carry sequential drift (order-level structure)

Status: `SUPPORTED` as structure, `OPEN` as mechanism

Supporting: even256 16x16 row-homogeneity chi2 415.0 df330 p~0.001 with 2000-shuffle null P>=obs 0.0005; early128 vs late128 halves chi2 40.6 df22 p~0.009; TAIL early-j (284) vs late-j (286) chi2 18.4 df8 p~0.018 with Bifid-column mechanism check (early a/g excess -> even S excess; late b/i excess -> even B excess); counts control null-consistent (19.6 df24 p~0.72), so structure is ORDER not bag-of-letters; no outlier row (max-row shuffle P~0.20) — drift is gradual (discovery #40, CLM-011).
Contradicting: halves-key battery (early/late SHA256/base-23 x concats = 6) -> 0 hits.
Required test: a TAIL sequential decoder with a STATED key (Phase-3.2 VIC-key reuse falsified — 482/84-char gibberish, 0/16 lock hits, Dead End #28, not fished); replication on an independent object is unavailable (LEAD91 too short for 16x16; 161 values exhausted as message per #32).
2026-09-11 update (option-1 execution): external lead 6 (29 dropped I/O letters as their own message) CLOSED locally — `OOIIOOOIIOOIOIIOIOOOOIOIIOIOI`, 8 oracle + 16 lock attempts, 0 hits (Dead End #29; extraction == position order, single pass). Contemporary primary-community note (`salphaseion.ipynb` cell 13: "the dbbib and faed strings haven't been decoded") confirms no stated LEAD/TAIL decoder existed in the 2021 community material either. External witnessed boundary recorded (CLM-013: 335.7M + 62.6M negatives, secondary, not re-swept); open external directions are dynamic-script replay, single-tool menu identification (name in private research), esrever remainder, and the 256-right-object question — none executed here.

### H-ONCHAIN-013 — On-chain author-vs-solver separation bounds all chain work

Status: `SUPPORTED` as guardrail; routing-as-author reading `FALSIFIED`

Supporting: 2026 Half/Better bursts (blocks 938165/944096) every token/quote OP_RETURN spends a public key (e.g. `3f0f28b973b1ee22` Half->17ucy+bc1, `a4355923...` Better->17ucy+hereismysecret, `0a756d0b9a...` Better->1GSMG+Matrix quote); embedded `bc1qks8zrshwmu3m8vgqdzwl2u8jjfgnvgjlezwqcd` decodes to solver P2WPKH `b40e21c2...` (14/13 fund/spend, 546-sat balance); author objects (P-escrow #24, planted-2020 via `3GSMG24...` P2SH redeem `OP_0 <P2WPKH 2780438f...>`, initial splits `2aa9a4a90be819d5`/`88cdb3cdca12b471`) carry no token OP_RETURNs (discovery #41, CLM-012).
Contradicting (routing-as-author): no author txid; all cited Half->Target2 flows post-date public-key exposure by years; author funding shows no such pattern. E5 stays UNVERIFIED for author routing.
Required test: none — exclusion rule. Solver messages (`abacus`, `hereismysecret`, `leavethematrix`, bc1 test wallet) must not seed key hypotheses.

## Current bottleneck

No candidate key controls either funded target (`1GSMG1JC...` ~1.256 BTC or `17ucy1K9...` ~3.7505 BTC). The documented matrix->base-38 chain is reproducible but its outputs are not target keys, and issue #106 now treats the underlying Cosmic interpretation as a likely padding accident. Chains 1–3 decrypts verify byte-exact with WIF link and three-way AES-key rebuild, but all 8 chain keys miss both targets. Chain-4 decrypt reproduces byte-exact (1151B `e4269ed5...`, `+-`, `31+35x32`, tail `9f06936a...`, discoveries #23/#25) but stays `UNVERIFIED` as author design (free-mask header, random-plaintext statistics); Chain-4 interpretation stays OPEN from public artifacts only (7x0x77 markers label-only, ~27k + ~10k (H-SEL-001) sweeps 0 hits, `X=f4d1...` oracle resolved; `cosmic_A`/`K_I1`/`row1-4` are secondary folklore, not author facts). The small blob's correct A+z+B assembly is block-aligned (discovery #12); the literal issue #108 correction stays unverified. Prime-removal `765-pi(570)=661` is length-only (content 249/661). The 15-char string is corrected to `begbebebbbbbbcg` (CLM-010) and its selector use is falsified (Dead End #7). Strict 4x24 prime-plane confinement is falsified (94/96, H-PRIME-002, discovery #26); S2/S7 pre-registered hashing + group/mod routing falsified as specified (Dead End #8, discovery #27); pair-coordinate distinct addressing falsified with null-consistent controls (Dead End #9, H-PAIR-004, discovery #28); coordinate-mapping falsified by its own null (p~0.49) with surjection exposed as tautology (Dead End #10, H-COORD-005, discovery #29); 5-state op layouts+chains falsified 0/420 with underdetermined op order (Dead End #11, H-OPS-006); 3-bit 36B packing ill-formed on lone value-8 outlier + fallback 0/36 (Dead End #12, H-PACK-007); operand 23+7 split falsified by own range criterion (1/23 p~0.89, 1/7 p~0.18), modular 24->35 projection 0/160, mod-5 position null confirmed on corrected ground truth (chi2=3.0, p~0.56; Dead End #13, H-OPSPLIT-008/H-MODPROJ-009/H-MOD5-010); Round-9 audit re-verified all three on truth and closed the rescue paths (P1 zeroing validity False/False, P2 seed 1/7~chance, P3 frame corrected with exact P(sum=120)=0.0068 but two-sided ~0.24, clue-prime factorization battery min p 0.285 with Bonferroni, modular chi-squares 0.31-0.92; Dead End #14); 36x32 bridge refuted by slip proof (row-drop cannot yield K by construction) with row/cross-layer/(u,v)-mapping batteries all miss (Dead End #15, H-BRIDGE-011). 2026-09-11 round: coincidence bundle dead — kept15 sum-35 P=0.087 (expected value), 0x77-selection (25 values >=7 blocks, max tied), h-split fails LEAD replication, marker 6/7-in-13 post-hoc (Dead End #26); token-length/operand-alone/even-substring battery 0 hits incl. 225 ASCII substrings (Dead End #27, best prefix 0); Phase-3.2 VIC-key reuse on TAIL/LEAD gives 482/84-char gibberish + 0/16 lock hits (Dead End #28). Strongest live leads now: the 23/16/7 dimensional frame as pure structure (H-DIM-003 — all mechanism proposals on it dead) + prime-half depletion (H-ANOM-001, Fisher p~0.033) + NEW even256/TAIL sequential drift (H-DRIFT-012: rows p~0.001/shuffle 0.0005, halves p~0.009, TAIL early-j p~0.018; halves-key 0/6) + on-chain author-vs-solver guardrail (H-ONCHAIN-013: 2026 Half/Better token dust = solver with public keys, EXCLUDED; routing-as-author FALSIFIED) + author EC-op family (discovery #24), plus the third door. Puzzle is NOT near-solved on the key: all mechanism batteries negative. 2026-09-11 grid breakthrough (discoveries #42/#43): 14x14 matrix pixel-grounded from ART-001 (75px lattice, VERIFY PASS; H-P1-001 PROVEN; BLOCKED leg withdrawn) — image branches B1-B4 testable again; prize-address QR decoded (provenance only, no mechanism weight).

## Update rule

Every status change must cite artifact IDs and experiment IDs. Do not delete prior claims; append corrections and falsification results.
