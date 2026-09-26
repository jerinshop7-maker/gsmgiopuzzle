# Dead Ends

No hypotheses have yet been conclusively tested locally.

Public claims explicitly retained for falsification rather than accepted:

- The 1327-byte Cosmic Duality plaintext claim.
- The “Half and Better Half” split-key/dusting mechanism claim.
- The small SalPhaseIon blob two-typo correction claim.
- Any valid WIF that does not independently derive the prize target.

Each claim will receive an experiment record before being marked supported, falsified, or decoy.

## Dead End #1 — Literal issue #108 small-blob correction

- Tested source: ART-004 live SalPhaseIon capture.
- Issue claim: replace Base64 positions 18=`R` with `J` and 51=`k` with `s`, concatenate the adjacent fragments, then decrypt with the five-token password.
- Observed: the captured first fragment already has `J` at index 18 and `s` at index 51, so the proposed correction changes no bytes. The concatenated Base64 decodes to 95 bytes, leaving 79 ciphertext bytes after the 16-byte OpenSSL header/salt.
- Failure: 79 is not AES-CBC block-aligned; the claimed 79-byte plaintext and `K_C1`/`K_C2`/`E_C` values were not reproduced from the literal artifact.
- Status: `UNVERIFIED`/contested, not accepted as a solution. See `discoveries.md` Discovery #9 and `evidence.md` CLM-001.

## Dead End #2 — Matrix-derived Half/Better Half as funded target keys

- Tested source: independently reproduced 1327-byte Cosmic Duality plaintext.
- Result: documented matrix/base-38 output yields candidate values labelled Half and Better Half, but their derived P2PKH addresses do not match either funded target `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` or `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`.
- Status: `FALSIFIED` as the final prize-key interpretation. The values may be intermediate outputs, but no ownership claim is accepted without exact target-address equality.

## Dead End #3 — 2023-02-23 upper-five-bit/Base32 reading

- Tested source: official hint image `2023-02-23.png`.
- Result: 161 OCR-recovered binary tokens all end in `110`; upper-five-bit extraction, Base32 trims/padding, 7x23 rearrangement, fixed XOR variants, and alternate alphabets produced no meaningful plaintext, WIF, address, or target match.
- Status: `FALSIFIED` for these interpretations. The artifact itself is not a Base32 payload; its useful interpretation is the bit-reversed author message recorded in `evidence.md` CLM-006.

## Dead End #4 — Treating the 1327-byte Cosmic output as a solved final gate

- Tested source: issue #106 correction and the locally reproduced 1327-byte intermediate.
- Result: the output has valid AES padding and a self-reported matching hash, but the hash is self-referential and the bytes are high entropy with no recognized structure. The documented matrix/base-38 values do not derive either funded target address. Issue #106's complete sweep and false-positive analysis are not locally reproduced because the reported scripts/witnesses are absent.
- Status: `FALSIFIED` as proof of a complete solution; the exact status of the underlying Cosmic blob remains `UNRESOLVED` pending an independently captured sweep.

## Dead End #5 — Posted "Phase 3 SOLVED" ownership signatures

- Tested source: 2026-02-20 claim post (Half/Better Half keys, two Bitcoin compact signatures, prize-step request) plus the reproducible-derivation note.
- Byte chain: XOR key, 1327-byte decrypt, 103×103 +7-offset secondary string, base-38 Half/Better/trail hex, and all four quoted addresses reproduce EXACTLY from primary bytes.
- Failure 1: prize equality False — neither key derives either funded target (confirms Dead End #2 for the new post).
- Failure 2: both compact signatures INVALID under offline recovery (self-tested implementation; stated message plus 5 variants; recovered addresses match neither compressed nor uncompressed forms). No ownership proven.
- Failure 3: chain shows dust only (Half 103 txs / ~0.0176 BTC swept; Better 103 txs / ~0.0179 BTC swept), consistent with public key exposure, not prize flows.
- Addendum: the repo's `validate_uniqueness.py` does not run as shipped (wrong blob path → `FileNotFoundError`); path-corrected rerun gives exactly 1/210 successes, but P(exactly 1 | chance) = 36% and P(≥1) = 56% at the 1/256 padding rate with a circular hash check — the README's "constrained search + validation" documents fitting, not derivation.
- Addendum 2: re-encrypt round-trip is a tautology (AES reversibility; adds nothing); 210 RANDOM token sets validate 2× through the same KDF/decrypt, killing the uniqueness claim empirically. XOR-key vs small/p32 locks: one chance-rate 79-byte padding, all 8 addresses miss. 1327 is prime; 23×57+16 numerology unpromoted (no mechanism/test).
- Status: `FALSIFIED` as a solution/ownership claim. See `experiments/sal_final_search/phase3_claim_verification.md`.

## Dead End #6 — Bifid onward-use from TAIL570 (head CORRECTED 2026-09-04)

- Correction first: an earlier entry (FULL_SUMMARY falsified list) called the BTCSEED head unreproducible. That was an implementation error (encode run instead of decode). Retracted for the head.
- Verified: true Bifid DECODE, 5×5 square (key DBIFHCEGA from LEAD91 first-occurrence order + alphabetical remainder), period 570 → head `BTCSEED…`, single Z (@97), odd positions exactly {B,C,D,E} across all 285.
- Verified negative: no other creator tokens in full output or even stream; SHA-256 as key/password/door material misses; token-block combine via the 13/38 length coincidences yields structured noise with no lock hit.
- Status: head reproduction `SUPPORTED` as a mechanical fact; the 285→256 reduction untested here; prize-use `FALSIFIED` for all tested readings. LEAD91 gains a verified FUNCTION (key source) while the onward path stays open. See `discoveries.md` Discovery #20.
- Addendum (variation sweep): a published "BTCSEED not reproducible" sweep is void — its headline "decrypt" output is byte-identical to the ENCODE direction (direction labels flipped). 96-config check (4 keys × RC/CR × dec/enc × 6 periods): ONLY (first_occ, RC, dec, 570) hits any token (BTCSEED); token-derived key MATRIXSUL (9 unique letters) negative at 8 periods. The result is specific to the single most-principled configuration — consistent with design or a lucky point; downstream stays dead either way.

## Dead End #7 — 15-char char-value selector indexing (7 selectors, sum + operand + EC)

- Tested source: Chain-4 1151B plaintext (byte-exact repro, discovery #23/#25) + sieved `8k+7` 24-char extraction (`begbbebebabbbbabbbfccfgg` verified) + URL-LSB mask (`111101110011110110010010`).
- Claim: 15 kept chars as a-i→0-8 indices into the 7 `0x77` selector blocks `[0,2,3,8,9,12,26]`, sum 15 with repetition + 30B operand, EC `x2`/`/2`/`+-1`/`+-2` vs `X=f4d1bbd9...` / `a955...` / `4bc468...` / door `eb862e...`.
- Correction first: published `begbebebbbbbcgg` is a transcription error (double-flip 10<->23); correct mask output is `begbebebbbbbbcg` (`[1,4,6,1,4,1,4,1,1,1,1,1,1,2,6]`). Both variants tested.
- Observed: ~10,000 candidates (claimed+corrected+off2+all-8-offsets+ext24+dropped9 x sel7/pay28/all35 x direct/mod x sum/xor/wsum x 8 operand variants incl. half/better x 7 EC ops + hash/multiply/zeroing/5 orderings/position-based kept15/dropped9/all24/kept±dropped; exact offline oracle, comp+uncomp) -> 0 hits, best X-prefix 3 (chance).
- Status: `FALSIFIED` for all reasonable readings. The all-<7 observation survives as alphabet fact but carries no routing power in tested space. The surviving structural signal is the h,i-avoidance anomaly itself (discovery #25), not its selector use. See `discoveries.md` Discovery #25 and `evidence.md` CLM-010.

## Dead End #8 — S2/S7 pre-registered hashing + 7x5/mod-35 routing bundle

- Tested source: S2/S7 24-char streams (Discovery #26) + Chain-4 1151B/35 scalars/operand + clue text (`phase3.2.ipynb:359`).
- Claim bundle: Tier 1 (4 direct SHA256 vs all materials), Tier 2 (decimal-digit BE/LE + sha), Tier 3 (`SHA256(S2)^SHA256(S7)` x 8 EC variants), one-marker-per-group, group-sum routing (45), mod-35 routing (60).
- Observed: Tier 1: 0 exact hits (best overlap 10/64, P~0.13 over 140 comparisons — chance, not promoted). Tier 2: 0 hits (24-digit values ~80 bits, size-mismatched). Tier 3: 0/8. Group distribution 3/2/1/0/0/1/0 kills one-per-group; routing batteries 0/45 and 0/60.
- Status: `FALSIFIED` for every specified variant (discovery #27). Surviving: dimensional correspondence as structure (not mechanism) + two open bridges (24x3x16 addressing needs a function; marker-operation semantics beyond sums untested).

## Dead End #9 — S2/S7 pair-coordinate addressing (diagnostics-first family)

- Tested source: pair object P[i]=(S2[i],S7[i]) i=0..23 (streams per #26); Chain-4 blob layers.
- Claim: 24 ordered pairs form a finite control alphabet / symmetric structure / permutation of 24 groups. Tested with NO hashing and NO integer conversion, per spec: census, symmetry, Delta, shuffle controls, distinct-address check.
- Observed: 16 unique/24 ((a,b)x5 top, 13 singletons); symmetry 5/12/7 (sign p~0.18); mean|d|=1.917 with shuffle nulls P~0.20 (tracking), P~0.54 (equality), P~0.33 ((a,b)), P~0.78 (uniqueness) — all null-consistent. 24-unique required for distinct addressing, observed 16: strong form FALSIFIED with zero invented constants.
- Status: `FALSIFIED` in distinct-address form (discovery #28). General form (repetition-tolerant addressing, pair encodings) deliberately untested — any 81->24 map is arbitrary without an artifact function. 23->24 reinsertion BLOCKED (only 23-object is 161 columns, values untranscribed; Z@97 failed before; drop-1-of-24 unfishable).

## Dead End #10 — 16-pairs->7x5 coordinate mapping via (x%7,y%5)

- Tested source: 16 unique S2/S7 pairs (#28) + 7x5 marker matrix (cross-checked identical: rows `10110/00011/00100/00000/00000/01000/00000`).
- Claim: mapping pairs to matrix coordinates yields 4 marker hits, proving pairs route through marker coordinates.
- Observed: 4/16 reproduced exactly at (0,0),(0,2),(1,4),(5,1) — then killed by its own control: 20k-shuffle null gives P(>=4) ~ 0.49 (expected ~3.2; orientation granted, mapping choices unpenalized). The companion "perfect surjection" claim is definitional (pairs come FROM the 24 positions), weight zero.
- Status: `FALSIFIED` as evidence (discovery #29). Lesson recorded: coordinate-mapping hits require a shuffle null BEFORE promotion; tautological restatements are not discoveries.

## Dead End #13 — operand 23+7 split + modular 24->35 projection + mod-5 position null (bundle)

- Tested source: Chain-4 operand `2dca9ebc...0537` (30B, 0x77 at sub-offset 5 = global 6) + ten in-block 0x77 intra-offsets recomputed byte-exact this round.
- Ground-truth correction: intra-block offsets are [0,2,13,9,28,4,10,31,14,9] (sorted [0,2,4,9,9,10,13,14,28,31], sum 120) — the reported list (11,29 instead of 13,28; doubled 10 instead of 9) is wrong at three positions. Kill computation redone on truth: mod-5 counts {0:2,1:1,2:1,3:2,4:4}, chi2 = 3.0, df = 4, p ~ 0.56 (their 5.0/0.29 ran on wrong data; kill stands, stronger).
- Sum-120: verified TRUE on ground truth — but parse-insensitive (their wrong list also sums 120 via compensating +1/-2/+1 errors), so the checksum cannot confirm any parse; plus post-hoc frame ambiguity. Graded coincidence, do NOT promote (agrees with their 🟡-at-best, for a further reason).
- Operand split (their ★-priority test, run exactly as specified — natural ranges only, no invented mod): A[0:23] has 1/23 bytes <23 (null P~0.89); B[23:30]=`638f45b3e70537` has 1/7 bytes <7 (null P~0.18). Both chance-consistent. The 0x77-in-operand control-symbol observation is confirmed as fact (value 119, out of selector range) but is not a mechanism. Vague rescue transforms (open-ended zeroing/prime-filtering/reversal) deliberately NOT applied — unstated which-bytes/how = guaranteed fit = fishing.
- Modular projection (their §8 family, clue parameters only): slot=(a*i+b)%35, a in {2,3,5,7} x b in {0,1} (8 maps; cycles 35/35/7/5 — note a=5 yields 7 distinct slots, a=7 yields 5), x {sum,xor} x {plain,+op} x EC(5) = 160 checks -> 0 hits.
- Status: `FALSIFIED` for split-as-selectors, projection family, and mod-5 selector (no discovery entry — threshold unmet). Surviving facts: arithmetic identities (16+7=23, 23+7=30, 23+1=24, 7x5=35) verified but mechanism-free; prime->meaning assignment (2->half/double CONFIRMED ops, 3->AESx3 fact, 7->markers fact, 5->states hypothesis) stays interpretive — labels permute freely, and leg 5's op order is artifact-unstated (#11).

## Dead End #11 — 7-way interleave × 5 elliptic states (layouts + chains)

- Tested source: 35 Chain-4 scalars + 7 marked blocks + author EC-op vocabulary {I,+G,-G,x2,/2} (#24).
- Claim: de-interleaved seven 5-element streams under layouts A (contiguous 7x5), B (5x7 stride-7), C (reversed B), D (marker-segmented runs) with marker-position->op assignment, per-stream + layout-sum + sequential-chain candidates vs oracle.
- Observed: B-stream marker positions s0:[0],s1:[1],s2:[0,1],s3:[0],s4:[],s5:[1,3],s6:[] (no clean 1-per-stream structure in any layout; A gives 3/2/1/0/0/1/0). Rules applied uniformly (first-marker wins, empty->I; op orders O1 as-proposed + reverse). 420 point-checks (per-stream/layout/chain x EC) -> 0 hits. Op assignments swing wildly between O1/O2 (e.g. B: [I,+G,I,I,I,+G,I] vs [/2,x2,/2,/2,I,x2,I]) — position->op order comes from no artifact, so the mechanism is underdetermined on top of negative.
- Theory note: "scalar-first vs point-first" test orders coincide by group law (scalar accumulator is exact for {+1,-1,x2,/2}), so they were correctly run once, not doubled.
- Status: `FALSIFIED` for all pre-registered variants (no discovery entry — nothing met promotion threshold).

## Dead End #12 — 96-symbol 3-bit packing to 36 bytes (32+4 split)

- Tested source: 96 prime-offset symbols (#26) + 3-bit/36B/32+4 proposal.
- Claim: 96 symbols x 3 bits = 288 bits = 36B = 32B material + 4B control, over 16 packing variants (concat orders x value base x bit/symbol order).
- Observed: premise ILL-FORMED on the real object — max symbol value is 8 (single `i` in off5/chunk1 = sieved pos 13); 3-bit cells cap at 7. The neat packing assumed the purity #26 already killed (94/96). Post-hoc 4-bit fallback (fwd/rev -> 48B -> first/last-32 exact + EC): 36 checks -> 0 hits. 4B control words were never produced (no valid 36B packing exists).
- Status: `FALSIFIED` as premise (structural, no oracle needed) + fallback negative. Same lone outlier blocks two branches now (strict confinement #26 and this packing) — recorded as shared single-point failure, not independent evidence.

## Dead End #14 — Round-9 audit bundle (operand rescue paths + factor/modular batteries)

- Tested source: operand `2dca9ebc...0537` + ground-truth intra-block offsets [0,2,13,9,28,4,10,31,14,9] + clue-prime set {2,3,5,7,23}.
- Data corrections first: reported position list wrong x3 (11/10/29 vs true 13/9/28) — the cited chi2=5.0/p~0.29 recomputes on truth as chi2=3.0/p~0.56 (kill stands, stronger). Reported "0 of 23 qualify" wrong — A[8]=10<23 gives 1/23 (null P~0.89; conclusion unchanged). P3-as-specified ("sum of positions in 1120") is a false-positive machine — correct frame is intra-block offsets: exact P(sum=120)=0.0068 confirmed, but two-sided P(|dev|>=35)~0.24; plus parse-insensitivity (wrong list also sums 120). "3-bit packing 🟡" status is stale — #12 killed it as ill-formed.
- P1 zeroing (pre-registered concrete forms): zero A-positions {2,3,5,7} -> validity False; zero B-mod-23-indicated {0,1,5,7,9,18} -> validity False. Dead as specified, no oracle runnable. Open-ended rescue transforms declined (unstated which-bytes/how = fishing).
- P2 seed: SHA256(operand)=`c72db6c4...` mod35 first-7-distinct [24,10,7,21,31,2,1] vs marked {0,2,3,8,9,12,26} — 1/7 overlap (expected ~1.4). Dead.
- Factorization battery (clue primes {2,3,5,7,23} x 2 parts, Bonferroni 0.005): min single p 0.285 (B div23) — all dead. Post-hoc 11-clustering in B (4/7, p~0.0021) killed by multiplicity (11 not clue-motivated; ~10+ scannable primes). B-all-odd (0.0078 x10 = 0.078) dead. Modular chi-squares: Amod7 7.13/0.309, Amod5 3.30/0.509, Bmod7 2.00/0.920, Bmod5 3.71/0.447 — all dead.
- Independence caveat recorded: "five constants from five sources" overstated — 16 is AES-external, 7+23 share one sentence, 35/1152/30 share one object (~2-3 independent origins). Network stays 🟡-structure (H-DIM-003), weight unchanged.
- Status: `FALSIFIED` for every specified variant (no discovery entry — threshold unmet).

## Dead End #15 — 36x32 bridge (slip proof + row battery + cross-layer + (u,v) maps)

- Tested source: 1152B padded pt (36x32 rows R[0..35]) vs 35 Chain-4 scalars K[0..34]; 24-group (u,v) coords vs 7x5 (r,c) slots.
- Slip proof (deterministic, by parse geometry — construction, not discovery): R[0]=H+K[0][:1], R[j]=K[j-1][1:]+K[j][:1] (j=1..34), R[35]=K[34][1:]+0x01 verified byte-exact. Consequence: dropping ANY single row cannot yield the K array (slip-misaligned by construction) — the "36 rows minus control row = 35 scalars" reading is REFUTED structurally, and R[35]'s only exceptionality is the trailing pad byte. Corollaries: 1152-1120=32 reduces to header(31)+pad(1)=32 (parse geometry, not an operation); max position-aligned R-K shared bytes is 3 (chance).
- Row battery: exact R==K 0/1260 pairs; SHA256(R)==K 0; direct/offset alignments, reverse, rotate-1, all 36 single-row removals — all miss; 36 unique rows; no second exceptional row (min-entropy dip at R[34] routine for n=32).
- Cross-layer: 36 rows as scalars (36/36 valid, P~1, weight zero) vs X/targets/Half/Better/author point -> 0 hits.
- (u,v)->(r,c) family (row-major + col-major 8x3 x 3 r-rules x 3 c-rules, prime-motivated coefficients only): 21 distinct slots each; x {sum,xor} x {plain,+op} x EC(5) = 360 checks -> 0 hits. The 24x35=840 Cartesian framing leaves the missing function missing.
- Status: `FALSIFIED` for the bridge as a row operation and for the stated mapping family (no discovery entry — threshold unmet). Lattice identities (24=2^3x3, 30=2x3x5, 35=5x7, 1120=2^5x5x7, 1152=2^7x3^2) verified as arithmetic, mechanism-free.

## Dead End #16 — 0x77 intra-block position as 5-bit selector into 28 payload blocks

- Tested source: Chain-4 1151B plaintext (sha `e4269ed5...`, `/tmp/opencode/chain4_pt.bin`); exact oracle `X=f4d1bbd9...` + `a955...`/`4bc468...`/door (coincurve, comp+uncomp).
- Claim: the byte offset of `0x77` inside each 32-byte control block is a natural 5-bit selector (0..31) addressing the 28 payload blocks — structurally superior to scalar-mod-28 because the block size motivates the selector space; 7 control blocks -> 7 selectors -> 7 payload scalars summed with the 30B operand (`+` header) mod n.
- Observed ground truth: 7 marked blocks `[0,2,3,8,9,12,26]` hold TEN `0x77` occurrences (block0:{0,2}, block3:{9,28}, block9:{10,31}; others single). So "the position" is undefined without an extra free choice (first/last/all tried). Positions 28,31 overflow a 0..27 space (raw-indexing invalid for last7/all10 readings; mod-wrap tried).
- Battery: first/last/all-10 occurrence lists x {raw, mod28, -1, +1, 31-p} x {fwd, rev} payload order x {sum, xor, per-single} x {op-int, op-rpad, op-sha, none} x {S,2S,S/2,+1,-1,+2,-2} plus direct-position-into-35 and neighbor/first/last-byte Route-B variants: ~3.5k candidates -> 0 hits, best X-prefix 4 (chance-consistent at this trial count).
- Status: `FALSIFIED` for all natural readings (discovery #30). Lesson: a "natural" framing that needs multiplicity resolution + overflow wrap is fitted, not designed — count the free choices before promoting.

## Dead End #17 — LEAD91 triangle (T13) row-sums as `matrixsumlist` checksum (H-TRI-001)

- Tested source: LEAD91 (91 chars = 1+2+...+13 exactly, zero remainder).
- Claim: left-aligned 13-row triangle -> 13 row sums -> 13 letters == `matrixsumlist` (design checksum linking LEAD91 to MID104).
- Observed: row sums (a1/a0) x {raw,+7} x {mod26,mod9} + column sums + reversed order = 10 readings -> none spells `matrixsumlist` (e.g. a1 rows mod26 = `eerqzxrjwupgk`). Clean miss on a sharp prediction.
- Status: `FALSIFIED` as checksum (discovery #31). Row-sums-as-scalar-material not pursued (no artifact motivation; would be fitted).

## Dead End #18 — even256 as 16x16 prime-zeroed matrix-sum scalar

- Tested source: even256 (256 chars = 16x16 exact); clue primes {2,3,5,7} + "zero out" + `matrixsumlist` (sums); exact oracle `X=f4d1...`/h160s/door.
- Claim: the most clue-faithful even256 reading — 16x16 matrix, zero (or keep) prime-indexed rows/cols, 32 sums mod256 -> 32B scalar.
- Observed: {row,col} layouts x {1-based,0-based} prime indices x {zero,keep} x {rows+cols,cols+rows} x {S,2S,S/2,+-1,+-2} = 112 candidates -> 0 hits, best X-prefix 1 (chance).
- Status: `FALSIFIED` for all stated variants (discovery #31).

## Dead End #19 — row-bit stream / base-23 / base-4 direct scalars

- Tested source: TAIL570 row-bits under the DBIFHCEGA square (570b, the last unexamined principled object per the #31 recoding theorem); even256 as base-23 number; odd285 as base-4 number.
- Claim: rows carry 1 bit/char of independent ciphertext information; direct (CHAIN1-convention) or hashed conversion yields the key.
- Observed: 71B row objects (3 remainder handlings) + 11B LEAD rows x {int-mod-n, sha256} + base-23/base-4 direct x 7 EC ops = 70 candidates -> 0 hits, best prefix 1.
- Status: `FALSIFIED` for stated readings (discovery #31). Direct digit-stream->key readings are now exhausted for stated mappings.

## Dead End #20 — H-COLOR-MUX (B/Y multiplexing S2/S7 into a 7-state stream)

- Tested source: S2/S7 recomputed from scratch (match ledger); B/Y mask `111101110011110110010010`; oracle `X=f4d1...`/h160s/door.
- Claim: the B/Y frame multiplexes S2/S7 into a 24-symbol stream over exactly a..g (0..6), naturally realizing "seven intertwined passwords" without invented moduli.
- Observed: BOTH parents are independently 24/24 pure a..g, so all 2^24 choice-strings (both orientations) are trivially pure with P=1 regardless of mask — the alphabet argument is VACUOUS; the mask is explanatorily idle. Mux strings A/B verified as distinct chimeras (dist 7/12, 12/7), but scalar battery (S2/S7/A/B x base-7/SHA256/concat-decimal x 7 EC ops = 84) -> 0 hits, best prefix 1.
- Status: `FALSIFIED` as argued (discovery #32). Any future mask-involving theory must demonstrate the SPECIFIC mux strings succeeding where S2/S7 fail. Lesson: check parent purity before promoting a "collapse" — a selector that cannot fail to produce the advertised alphabet proves nothing.

## Dead End #21 — prime-extraction (35-byte) op-schedule / weights / offsets vs Chain-4

- Tested source: Bifid odd285 -> 2-bit coords -> groups of 8 -> positions {2,3,5,7} -> 35 bytes (repro exact, discovery #33) + Chain-4 35 scalars/operand + author EC family {P,P+G,P-G,2P,P/2}.
- Claim: bytes mod 5 schedule per-block EC operations (stated assignment), summed vs `X=f4d1...`; alternates: scalar offsets, linear weights.
- Observed: index base {1,0} x order {fwd,rev} x bit order {rc,cr} x byte order {MSB,LSB} x {sched plain/+op, offsets plain/+op, weights} = 80 candidates -> 0 hits, best prefix 1 (chance). Op-permutation sweep (119) declined as fishing; grouping-from-end twin untested (no stated reason).
- Status: `FALSIFIED` in all stated variants (discovery #33). Object itself stays CONFIRMED as waypoint. Lesson: dimensional alignment (35<->35) conditional on an unstated grouping choice is resonance, not routing — count which choices the match depends on.

## Dead End #22 — 35-byte matrix sums (570/1152) as designed artifact coordinates

- Tested source: 35-byte object in 7x5; artifact dimensions 570 (TAIL) / 1152 (Chain-4 layer); full 16-extraction pipeline family.
- Claim: literal `matrix -> sum -> list` on the confirmed object lands on real dimensions (row1=570, col2=1152), so the 12 sums are an artifact-addressing layer (direct offsets / mod-103 indices / 7x5 coordinates).
- Observed: sums and mod-103 indices arithmetically exact — but shuffle null P(either hit)=0.0208 combined with pipeline multiplicity (16 extractions = 4 distinct objects; 570-in-rows recurs in 2/4; near-mean effect) plus target-mapping freedom puts the coincidence at ~15-30%: resonance. Offsets/mod-103 oracle batteries declined (missing readout function x failed premise = fishing); revival needs an artifact-stated readout.
- Status: `FALSIFIED` as designed layer (discovery #34). Lesson: "no invented modulus" is not the same as "no free choices" — the pipeline that built the object already spent them; audit choices before the readout, not just within it.

## Dead End #23 — 7x5 token-x-EC lattice (T1-T4 + token-hash masks)

- Tested source: Chain-4 35 scalars (row-major 7x5) + fixed EC columns (P,P+G,P-G,2P,P/2) + canonical 7 tokens (duplicate H1==H5) + E1 bytes (T3/T4 selectors); exact oracle.
- Claim: lattice rows = tokens, columns = author EC ops; Bifid bytes route (mod7 rows / mod35 cells); token SHA256s mask rows.
- Observed: T1/T5 totals (identical sums — regrouping, run once) plain/+op; T3 diagonal filter keeps 3/35 cells (chance-sparse); T4 distinct-24 + weighted; T2 per-cell/per-row x canonical/user-list — 18 candidates -> 0 hits, best prefix 1. Fill/column/row permutations untested (unstated).
- Status: `FALSIFIED` in all stated variants (discovery #35). Lesson: independent semantic grounding on BOTH axes still fails without the wiring artifact — two grounded halves do not make a grounded bridge.

## Dead End #24 — sum-all-35 Chain-4 scalars as "second answer"

- Tested source: Chain-4 35 scalars in canonical order; exact oracle X/h160s (comp+uncomp).
- Claim: second `matrixsumlist` = unfiltered scalar sum mod N -> private key (pre-registered, no selection).
- Observed: sum -> x=`7e68e84b663c584033f45b444a98a9bf93fc6d73e076c8f0050c6a3ba3e513e2`; h160s `45524005...`/`388e0f8d...` — all miss both targets. Consistent with #23 sums-family negatives.
- Status: `FALSIFIED` (discovery #36).

## Dead End #25 — C(23,16)=245157 letter-selection sweep on even256

- Tested source: even256 (16×16 over 23-letter alphabet A–Z minus I,O,J; sha `1740b55b…`); exact oracle `X=f4d1bbd9…` + `a955…`/`4bc468…` (coincurve, comp+uncomp).
- Claim: the author clue "select from over twentythree ciphers sixteen encryptions … bruteforcing might be required" means brute-forcing all C(23,16)=245,157 ways to choose 16 letters from the 23-letter alphabet, each selection yielding a private-key candidate.
- Observed (brute23.py, completed): 245,157 selections × 5 derivations — SHA256(16 values), values+zeros, zeros+values, base-23 mod N, SHA256(sum) — = 1,225,785 candidates → 0 hits (411s). Second battery (brute23b.py, frequency/string derivations: SHA256(freq16), SHA256(selected-str), SHA256(remaining-str), freq16+zeros, freq7×5, SHA256(xor16)) ABORTED mid-run — no completion verdict, not counted.
- Status: `FALSIFIED` for the 5 stated derivations; the frequency/string variants remain UNTESTED (aborted, may be re-run). The structural even256 frame (#38) is unaffected — only this specific selection→key mapping is killed.

## Dead End #26 — Coincidence audit bundle (sum-35 / 0x77-selection / h-split / marker-clustering)

- Tested source: Chain-4 1151B plaintext (`e4269ed5...`); sieved S7 24-char parent + 15/9 mask split; TAIL570 halves; 35 block positions; exact oracle `X=f4d1...`/h160s/door.
- Claim bundle: (a) kept15 index-sum 35 == 35 blocks is designed; (b) `0x77` byte excess (11/1151) proves marker design; (c) TAIL second-half h-enrichment (19 vs 39) is designed drift; (d) 6/7 markers in first 13 positions is designed clustering.
- Observed: (a) kept15 sum 35 has exact-DP P=0.087 over C(24,15)=1307504 subsets (mean 35.0 — IS the expected value; dropped 21 likewise). (b) `0x77` body count 10 / full 11 ties the observed max (`0x7b`/`0x17` also 11); 25 byte-values hit >=7 blocks, `0x77` is one of fourteen at exactly 7 — post-hoc selection, not unique. (c) h-split one-sided p~0.004 fails replication on LEAD91 (7 vs 1, opposite direction) — chance with inconsistent sign. (d) 6/7-in-first-13 p~0.0059 is a post-hoc cutoff; pre-registered halves give p~0.052 (6/7 in 0-17), quarters/ thirds 0.03-0.59 — fishing the boundary.
- Status: `FALSIFIED` for all four as designed signals (discoveries #40/#41 round). Lesson: exact equalities to salient numbers (35), byte-maxima, halves extrema, and boundary-tuned clustering need an exact null + replication BEFORE promotion — all four fail one of those.

## Dead End #27 — Token-length / operand-alone / even-substring selector battery

- Tested source: 7 token lengths `[13,5,26,12,13,15,12]` (incl. duplicate 13 + interpretive 12); Chain-4 operand 30B `2dca9ebc...0537`; even256 256 chars; exact oracle (comp+uncomp).
- Claim: token lengths directly index the 35 blocks (all <35, no mod needed); or the operand alone / even ASCII substrings / early-late halves hash to the key.
- Observed: direct/minus1/plus1 index sets x {sum, +op, -op} (9) + unique-5 sum variants + xor variants + EC `2S,/2,+-1` extensions (32 total) -> 0 hits, best X-prefix 0. Operand direct/SHA256/`2S`/`/2`/`+-1` + SHA256(pt) -> 0 hits. even256 32B ASCII substrings (225, all valid scalars since 0x41-0x5A < 0xFF) -> 0 hits, best prefix 0 (P(all-miss-first-byte)~0.42 — chance-consistent). even256 early/late (128/128) x {SHA256, base-23} + concat orders (6) -> 0 hits.
- Status: `FALSIFIED` for all stated variants (discoveries #40/#41 round). Note: lengths bundle the duplicate matrixsumlist + interpretive secondanswer, so even a hit would have needed a provenance audit; none arose.

## Dead End #28 — VIC Phase-3.2-key reuse on TAIL570/LEAD91

- Tested source: TAIL570 (570 a-i digits 1-9) + LEAD91; authenticated VIC from `phase3.2.ipynb:16` (row ids 1 and 4 from "one for one, four for one"; alphabet `fubcdora/lethingkymvpszjqwx.` = 8+10+10; implementation validates byte-exact on the 149-digit string -> `incaseyoumanagetocrackthistheprivatekeysbelongtohalfandbetterhalfandtheyalsoneed...`).
- Claim: the same VIC decodes the SalPhaseIon digit streams (same digit alphabet 1-9, same puzzle family).
- Observed: TAIL -> 482 chars, LEAD -> 84 chars, both lowercase gibberish (`diwoccqbuvurr...` / `puaudurbbucoua...`); zero creator tokens (MATRIXSUMLIST/ENTER/HALF/BETTER/BTCSEED/PRIVATE/PASSWORD) in either case; 4 password forms (raw/upper) x 2 locks (small salt `3ab58534...`, p32 salt `b45a5e3d...`) x 2 KDFs (MD5/SHA256) = 16 decrypts -> 0 valid paddings.
- Status: `FALSIFIED` for this reuse (discoveries #40/#41 round). A SalPhaseIon-native VIC alphabet/key, if any, is unstated — declined as fishing. Revival needs an artifact-stated SalPhaseIon checkerboard, not a transplant.

## Dead End #29 — The 29 dropped I/O letters as their own message (floflo lead 6, tested locally)

- Tested source: even285 stream (Bifid even positions, 285 chars); dropped set = I x13 + O x16 = 29 chars in stream order `OOIIOOOIIOOIOIIOIOOOOIOIIOIOI` (positions `[4,18,21,22,...,283]`); exact oracle `X=f4d1...`/h160s/door (comp+uncomp); both 80-byte locks (small salt `3ab58534...`, p32 salt `b45a5e3d827593ca`) x both KDFs.
- Claim (external open lead, previously untested on both sides): the 29 letters dropped in the 285->256 reduction, read in their own right, match or open something.
- Observed: extraction order == position order here (single removal pass), so the "two orders" coincide — one 29-char object plus its reversal. Oracle battery (SHA256 fwd/rev, raw ASCII zero-padded left/right to 32B, I/O-as-bits both polarities MSB-first + reversed = 8 candidates) -> 0 hits, best X-prefix 0. Lock battery (raw fwd/rev, SHA256-hex, SHA256-raw x 2 locks x MD5/SHA256 = 16 decrypts) -> 0 valid paddings. Legibility: 2-letter alphabet admits no English fragment by construction.
- Status: `FALSIFIED` for all reasonable readings (2026-09-11, option-1 execution). Note: distinct from Dead End #6's raw-stream I/O drops (TAIL->495/75 etc.) — this is the even-stream 29. The external lead is now closed on both sides (it was open in `leads.md`).
- Overlap audit (no-repeat rule): Dead End #27's even256 32B-ASCII-substring leg (225 cands) overlaps floflo `tested.md` row 3 (32-ASCII windows, 34k cands, 0 match, witnessed) — counted here as CORROBORATION of that row's even256 leg, not as novel ground. Novel in #27 remain token-lengths, operand-alone, and halves SHA/base-23. Rows 1-7 + 15-19 (335.7M + 62.6M, all witnessed negatives) are recorded as SECONDARY corroborating boundaries and will not be re-swept (see CLM-013).

## Dead End #30 — Prime-sieve length identity mistaken for stream identity

- Tested source: primary SalPhaseIon stream `LEAD91 + MID104 + TAIL570`,
  length 765; prime positions through 570 under both 0-based and 1-based
  conventions.
- Claim: removing the 104 positions yields the canonical `LEAD91 + TAIL570`
  stream of length 661.
- Observed: both outputs have length 661 but differ from the canonical stream
  immediately (first mismatch at output position 3 under 0-based indexing and
  position 1 under 1-based indexing). The equality was inferred from lengths,
  not verified bytes.
- Status: `FALSIFIED` as a content claim; retain only the arithmetic identity.
  Revival requires an artifact-stated insertion order or source stream.

## Dead End #31 — First order/Genesis route battery

- Tested source: canonical `even256` and exact 69-byte Genesis source literal
  arranged as a 3x23 rectangle.
- Battery: adjacent/second/absolute differences, run lengths, transition
  matrices, 16x16 route permutations, and bounded 3x23 row/column/snake/spiral,
  row-permutation, cyclic-column, Caesar, casing/reversal/hash families.
- Result: 820 unique candidates, 21 chance-valid padding events, 0 target
  matches and 0 third-door matches. Lag analysis found no privileged 16/23/7
  period after correcting for 64 tested lags.
- Status: `FALSIFIED` for these key readings. The order-drift observation and
  3x23 geometry remain structural leads; revival requires an author-stated
  sequential/cipher rule rather than more route permutations.

## Dead End #32 — even256 frequency/string family

- Tested source: canonical `even256`, reconstructed byte-for-byte from TAIL570.
- Battery: count vectors, frequency-ranked alphabets, rank streams, count-boundary
  selections and complements, modular/XOR streams, decimal/hex/byte forms,
  reversal, SHA-256, and MD5 controls.
- Result: 604 unique candidates, 8 chance-valid padding events, 0 target
  matches, 0 third-door matches; oracle selftest passed.
- Status: `FALSIFIED` for the bounded frequency family. The object must be
  treated as ordered rather than as a bag of letters.

## Dead End #33 — Invalid copied-grid discrepancy report (retracted)

- Tested source: the canonical `puzzle.png`, the public README matrix, and a new
  image battery. The five-cell discrepancy was in the temporary comparison
  literal, not in the README; center sampling separately contaminated one cell.
- Corrected finding: dominant exact-fill extraction matches the README at all 196
  positions and gives K86/W86/B15/Y9 plus leftover `0000`.
- Corrected battery: 797 candidates, 22 chance-valid paddings, 0 target/door
  matches. See Discovery #52 and CLM-020.
- Status: `RETRACTED` as a ground-truth claim; the image branch remains negative
  only for the tested explicit readings.

## Dead End #34 — Genesis 3×23 direct matrix-sum readings

- Tested source: exact Genesis source literal as a 3×23 byte matrix, with
  ASCII/A1Z26 sums, prime-column zeroing/reinsertion, bounded B/Y selectors,
  and the reported `490/497` pair.
- Result: 4,210 candidates, 114 chance-valid paddings, 0 target matches, and 0
  third-door matches.
- Status: `FALSIFIED` for direct numeric/list encodings. The 3×23 geometry is
  still a structural clue, but it needs a specified semantic operation rather
  than another sum representation.
## Dead End #35 — Bifid → prime/zero → matrix-sum direct continuation

- Tested source: canonical full-period `DBIFHCEGA` Bifid output, `LEAD91`, `TAIL570`, natural 7×13/19×30 shapes, and the 20+49=69 composite.
- Result: 640 candidates, 18 chance-valid paddings, 0 target matches, and 0 third-door matches.
- Status: `FALSIFIED` for the tested direct encodings. The Bifid waypoint remains confirmed.

## Dead End #36 — 16×16 even256 prime/matrix readings

- Tested source: canonical even256, rank-0/rank-1 values, no mask, prime-value, full-prime-value, and prime-position zeroing; row/column/paired/difference and reverse forms.
- Result: 4,608 candidates, 146 chance-valid paddings, 0 target matches, and 0 third-door matches.
- Status: `FALSIFIED` for this clue-faithful family. The ordered 16×16 object remains a structural waypoint only.

## Dead End #37 — Aligned yin/yang selector readings

- Tested source: 256 retained positions after the 29 I/O drops, with corresponding B/C/D/E symbols from the other half as selector.
- Result: 304 bounded routes/encodings, 6 chance-valid paddings, 0 target matches, and 0 third-door matches.
- Status: `FALSIFIED` for these selector constructions. Revival requires an author-stated yin/yang operation.

## Dead End #38 — B/C/D/E mapped to prime basics

- Tested source: the 256 retained yin/yang positions, all 24 permutations of
  `B/C/D/E -> 2,3,5,7`, and both rank bases of the even256 payload.
- Battery: aligned add/subtract/multiply/XOR, squared/cubed combinations,
  raw/mod-23/mod-256 and reverse forms, letter/byte/hex/decimal/CSV/SHA-256
  encodings, 16×16 matrix summaries, and prime-only controls.
- Result: 24,432 unique candidates, 745 chance-valid paddings, 0 target
  matches, and 0 third-door matches.
- Status: `FALSIFIED` for this explicit numeric prime-basics family. The
  alignment is retained only as a structural waypoint; revival requires a
  specified operation or new primary evidence.

## Dead End #39 — 6+5 southeast B/Y chain direct readings

- Tested source: pixel-grounded canonical grid; contiguous chain strings
  `BYYBYB` and `YYYYB`.
- Battery: both chain orders and B/Y polarities, forward/reverse, separate and
  concatenated bit/color strings, decimal/hex/ASCII/SHA-256 forms, plus the
  corresponding URL characters selected by the proven frame relation.
- Result: 202 unique candidates, 5 chance-valid paddings, 0 target matches,
  and 0 third-door matches.
- Status: `FALSIFIED` for direct chain encodings. The chain geometry remains
  confirmed image structure; revival requires a specified downstream role.

## Dead End #40 — Latest 546/864 target transaction as a new author signal

- Tested source: refreshed target history through block 964501.
- The newest target spend `a751...` has 864 sats to the target and 546 sats to
  `17ucy1K9...`, but no OP_RETURN. Its input lineage is a solver 600-sat
  fan-out wallet, and its change is later redistributed to the same cluster.
- Status: `FALSIFIED` as a new creator message or numeric key hint. The exact
  amounts and lineage remain `CONFIRMED`; the older OP_RETURN witness branch
  remains secondary only.
