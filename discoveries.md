# Discoveries

## Discovery #1

Date: 2026-09-03

Artifact: Public-source review; local repository state.

Observation: The local repository contained no puzzle artifacts, reports, scripts, tests, or prior analysis. Public sources expose multiple live puzzle stages and a large SalPhaseIon/Cosmic Duality page, while recent public claims disagree about the final decrypt and prize mechanism.

Experiment: Read-only repository inspection and public-source retrieval.

Result: A new evidence-first workspace is required. The unresolved SalPhaseIon streams are the highest-information initial branch.

Why it matters: It prevents inherited solver claims from being mistaken for primary evidence and establishes a reproducible starting point.

Possible next branches: immutable live/archive intake; GitHub history preservation; exact SalPhaseIon transcription; known-answer crypto controls.

Confidence: STRONGLY_SUPPORTED

Reproducible script: Initial intake tooling pending.

## Discovery #2

Date: 2026-09-03

Artifact: `raw/web/live/salphaseion/response.bin` (ART-004), SHA-256 `a83d3de7...`

Observation: The live SalPhaseIon textarea decodes cleanly for several public claims but diverges on region sizes.

Experiment: Compact the textarea, map uniform spans, and apply the documented transformations (`a=0,b=1 -> 8-bit ASCII`; `a..i -> 1..9, o=0 -> hex/ASCII`) on the exact captured bytes.

Result:
- The 104-char span at offset 91 -> `matrixsumlist` (correct).
- The 40-char trailing span -> `enter` (correct).
- The readable sentence `shabef...ourlastcommand` is present and contiguous.
- Divergence: public writeups quote "91 symbols", "103 symbols", "570 symbols". The actual compact textarea structure is different: leading 91 single-char tokens are digits (not a binary abba span), the first binary span is 104 chars, the second is 40 chars, and the remaining digit spans are 62 and 29 chars. The leading 91-digit span does not decode to `lastwordsbeforearchichoice` under pair-hex, 3-digit, or bigint-hex transforms tested so far.
- Also captured: the cloned history of the three key repositories (commit-level primary provenance), while the anonymous GitHub issue API remained rate-limited.

Why it matters: Reproducing the live bytes independently confirms parts of the public chain and, more importantly, identifies where the public chain is unsupported by the actual captured bytes. The digit stream remains the bottleneck.

Possible next branches: alternative groupings for the digit stream; whitespace/line-length interpretation (lines appear to be formatted to specific widths); cross-check against the cloned repository copy; decode the small base64 (OpenSSL blob) in region 3.

Confidence: STRONGLY_SUPPORTED

Reproducible script: `scripts/analyze_salphaseion.py`, `scripts/transcribe_salphaseion.py`.

## Discovery #3

Date: 2026-09-03

Artifact: `experiments/004-cosmic/cosmic_decrypted.bin` + blockchain state.

Observation: The entire public "solution" chain (SalPhaseIon tokens -> XOR key -> 1327-byte decrypt -> 103x103 matrix -> base-38 -> Half/Better Half keys) is reproducible and verified up to the final step. Then it fails the only test that matters.

Experiment: Independently reimplemented the documented decrypt (XOR of 7 SHA-256 digests -> EVP_BytesToKey MD5 -> AES-256-CBC). Confirmed output is exactly 103x103+7 bits. Applied the documented matrix + base-38 transform to derive two candidate 256-bit private keys. Derived Bitcoin addresses (compressed and uncompressed) for both and compared against the prize target.

Result:
- Decrypt reproduces exactly: 1327 bytes, SHA-256 `4f7a1e4e...`.
- Two valid secp256k1 scalars derived: half=`0423d911...`, better=`48cc46e6...`.
- Addresses: half -> `1JG648ya...`; better -> `145ZQ9si...`. Neither matches the prize address `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` (not even a near miss).
- On-chain: prize address still holds ~1.256 BTC. The "Half" and "Better Half" addresses are fully swept (every output spent).

Why it matters: Matching the hash `4f7a1e4e...` only proves you decrypted to the same public bytes as everyone else. It does NOT prove the resulting bytes control the funded address. The published prize mechanism is unverified and almost certainly wrong.

Confidence: STRONGLY_SUPPORTED (independent reimplementation + direct address derivation + chain confirmation).

Reproducible script: inline derivation; address-derivation logic pending promotion to `scripts/`.

## Discovery #4

Date: 2026-09-03

Artifact: raw capture integrity; `raw/manifests/raw_manifest.jsonl`.

Observation: Repository verification failed because (a) a prior session had patched `raw/github/jackdevs66-GSMG5_CDuality/working/solver_salphasion_cosmic.py` (changing the hardcoded `cosmic_file` path), violating raw immutability, and (b) the manifest included 186 volatile `.git` internals (`.git/index`, pack temp files) that churn on any git operation.

Experiment: Restored the solver file byte-for-byte via `git checkout`; excluded `.git` internals from manifest classification in `scripts/hash_artifacts.py`; rebuilt the manifest to latest-state records.

Result: Manifest now has 106 stable non-git records; `verify_repository` and pytest pass clean.

Why it matters: Raw artifacts must stay immutable and manifests must hash stable content only, or integrity checks produce false failures.

Confidence: STRONGLY_SUPPORTED

## Discovery #5

Date: 2026-09-03

Artifact: OCR of official Telegram hint images under `raw/github/Naddiseo-gsmgio-5btc-puzzle/working/hints/` (primary author words). Transcriptions stored in `derived/hints/`.

Observation: Tesseract OCR recovered previously-unread author statements that constrain the final step.

Result (verbatim, OCR-level):
- `2021-03-01-primes.png`: "just say which primes 2,3,5,7 we need use and will be fine"; "there are too many combinations"; Jrk: "You are at the prime part already???"
- `2021-12-25-hint.png`: "We've seen prime numbers being mentioned; well, that is definitely an aspect which is required to proceed. Furthermore, along the way, some characters need to be 'zeroed out'."
- `2023-08-06-3.png`: "Probably the last hint: Once you hit a 'ying yang', you'll be able to solve it the same day."
- `2023-08-03-2.png`: "the hardest part is done."
- `2021-03-14.png`: creator confirms they don't check website logs / don't monitor progress; "When people progress in salphation it might be cracked pretty soon."
- `2021-05-06-salph instructions.png`: `SHA-256(GSMGIOSBTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe)` — the documented route into the SalPhaseIon page (hash = 89727c59..., ART-004 route).
- `2020-05-11.png` + README: after the 2020 halving "Half of the prize was moved to 17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa"; a "second door" is referenced repeatedly.
- `2023-02-23.png`: a grid of 161 eight-bit tokens; EVERY token has low 3 bits = `110` (`0b??????110`).

Why it matters: "primes 2,3,5,7", "some characters need to be zeroed out", and "ying yang" are the author's own constraints on the final step; the 161-token binary grid is a concrete unexplored artifact.

Confidence: STRONGLY_SUPPORTED (OCR text is primary author content; individual OCR characters carry small error risk).

## Discovery #6

Date: 2026-09-03

Artifact: Blockstream API state for the two documented prize addresses.

Observation: The puzzle has TWO live target addresses, both funded.

Result (on-chain, sats):
- `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`: funded 875,988,872 / spent 750,353,498 / 126 txs -> balance ~125,635,374 (~1.256 BTC).
- `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`: funded 375,055,856 / spent 0 / 45 txs -> balance 375,055,856 (~3.7505 BTC), fully unspent. Hash160 `4bc468447fe1b048ad030a2f9a125478eabc4ed6`.

Why it matters: Naddiseo (issue #108/#55) states a real solution must yield the private key to `1GSMG1JC...` and/or `17ucy1K9...`. The 17ucy address — where "half the prize was moved" at the 2020 halving — holds the larger unspent balance and is the primary unclaimed target.

Confidence: STRONGLY_SUPPORTED (direct blockstream.info API).

## Discovery #7

Date: 2026-09-03

Artifact: `raw/github/puzzlehunt-gsmgio-5btc-puzzle/issues/104/comments.jsonl` and issue #108 text.

Observation: The community's documented final-step derivation is reproducible, and the dispute about the "small blob" is resolved in favor of skepticism.

Result:
- The documented 103x103 matrix -> row/col sums offset +7 -> 103-char secondary `Vmfgiel[rfc\h]iodi\engckhbucp`cjjbP\nnrga`]qjicil^_ihd\gppek_lq_cYie^iddgafb^j`]ilkda_q^^ZifZg]__g\]]a`` -> base-38 -> 68 bytes reproduces EXACTLY the community Half/Better Half keys: half `0423d9115a1dc756d5d08d2de880ab508bd4745fc97709f4fcb513f2cb8fcc35`, better `48cc46e66bdd36b09ae344552f606a761f9d90681f20dfefe2b43db18b623971`, trail `fc0c1b02`. Independently confirmed in this session.
- Derived addresses: half-comp `1JG648yaB7Wp2dpUfcZoRSD4q35oq47vCu`, better-comp `145ZQ9siLrsXBKf465wjdyQYAP5dRwhRhQ`. On-chain both show only incidental dust (5000-sat self-outputs, occasional ~119k-sat flows to segwit addresses) — NOT the prize "funds to live" flows.
- Neither half, better, nor trail controls either funded target (hash160s: half-comp `567e30de...`, better-comp `acb8a9a3...` vs target `a9553269...` / `4bc46844...`). XOR/add/sub/doubling/sha combos all miss.
- Issue #108 ("CADEIA chain", two-typo small-blob fix) is publicly disputed: Naddiseo calls the chain "nonsense an LLM made up", notes bad puzzle design in requiring modification of near-random base64, and restates the acceptance criterion (key to `1GSMG1JC...` and/or `17ucy1K9...`).
- Community blockers (issue #104): `cosmic_A.bin` never publicly distributed; exact row1-row4 XOR-triangle definition unknown; oracle hash `e2590f15...2cbd` never reproduced.

Why it matters: Confirms the matrix -> base-38 step is a real documented intermediate whose keys do NOT match the funded targets, so the remaining step (or a different route entirely) is still unknown. The small-blob two-typo theory is retained but contested.

Confidence: STRONGLY_SUPPORTED (cryptographic reproduction + on-chain check); FALSIFIED for the claim that half/better control the funded targets.

## Discovery #8

Date: 2026-09-03

Artifact: `raw/github/Naddiseo-gsmgio-5btc-puzzle/working/hints/2023-02-23.png` (161-token binary grid).

Observation: Every token has the form `0b??????110` (low 3 bits always 6). Reading the upper 5 bits as a base32 (RFC 4648) stream gives a valid-charset string of length 161.

Experiment: Decoded the 5-bit stream as base32 with all valid trims/paddings; also 7x23 re-arrangement, xor with 0x66/0x06, and alternate 32-symbol alphabets.

Result: All decodes yield binary garbage (~50-55% printable) — no plaintext, address, or WIF emerges. Recorded as a dead end rather than the key path.

Confidence: SUPPORTED as a negative result (many interpretations tested, none meaningful).

Reproducible script: inline OCR/pixel analysis in this session.

## Discovery #9

Date: 2026-09-03

Artifact: issue #108 text supplied in the investigation context; `raw/web/live/salphaseion/response.bin` (ART-004).

Observation: Issue #108 claims that two Base64 characters in the SalPhaseIon small blob should be changed, and that concatenating two adjacent strings produces a 79-byte plaintext containing `K_C1`, `K_C2`, and `E_C`.

Experiment: Compared the claimed positions and exact strings against the immutable live capture. The first captured segment is `U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9`, length 63; positions 18 and 51 are already `J` and `s`. The adjacent second segment is `QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ`, length 64. Concatenation is 127 Base64 characters, decodes to 95 bytes: 16-byte OpenSSL header/salt plus 79 ciphertext bytes.

Result: The claimed substitutions are a no-op on the captured data. The claimed concatenated blob has 79 ciphertext bytes, which is not divisible by AES-CBC's 16-byte block size. No decrypt can be accepted from this literal concatenation under standard AES-CBC. The issue's downstream values (`K_C1`, `K_C2`, `E_C`) remain unverified claims, not recovered plaintext.

Why it matters: This precisely separates a public assertion from the captured artifact. The issue #108 chain may refer to another source or an omitted transformation, but it is not reproduced by the literal live bytes and claimed correction.

Confidence: STRONGLY_SUPPORTED for the byte/length findings; UNVERIFIED for the claimed downstream chain.

## Discovery #10

Date: 2026-09-03

Artifact: `raw/web/live/salphaseion/response.bin` and `raw/github/jackdevs66-GSMG5_CDuality/working/cosmic_duality.txt`.

Observation: The SalPhaseIon page contains a second Base64-looking string after the first small blob. The exact adjacent strings are independently present in the canonical repository's documented SalPhaseIon material and were previously treated as separate fragments.

Result: Captured compact textarea layout around the boundary is:

```text
... U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9 z
... abba ... QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ shabefanstoo
```

The second fragment is 64 Base64 characters and decodes to 48 bytes by itself, but lacks the `Salted__` header. Concatenating it to the first fragment creates a non-block-aligned 79-byte ciphertext, so it cannot be treated as a conventional single AES-CBC ciphertext without additional evidence.

Confidence: STRONGLY_SUPPORTED for exact capture and lengths; UNKNOWN for intended assembly.

## Discovery #11

Date: 2026-09-03

Artifact: issue #106 research report; local `puzzle.png`; official hint image `2023-02-23.png`; captured issue corpus.

Observation: The new report distinguishes the actual final gate from the previously promoted Cosmic Duality interpretation. Its strongest claims are locally testable and substantially reproduce.

Verified locally:
- The 14x14 grid has counts K=86, W=86, B=15, Y=9 when each square is classified by exact dominant color. Down-first counterclockwise spiral with K/B=1 and W/Y=0 decodes to `gsmg.io/theseedisplanted`.
- The 24 colored squares occur at spiral positions 7,15,...,191 (zero-based), exactly the last bit of each of the first 24 decoded bytes. This verifies the color-frame/URL relationship and the reading convention.
- The 2023-02-23 binary tokens all have low three bits `110`. Reversing bits within each byte and reversing token order produces a near-exact no-space message containing `yellow blue primes matrixsumlist lastwordsbeforearchichoice yinyang ... very last step is a true giveaway promised`; the local OCR/transcription has at least one character-level discrepancy (`...choise...` versus `...choice...`) and omits spaces by construction.
- The captured issue corpus contains the #106 report, #104 retraction, #108 disputed correction, and #80/#91 Half/Better-Half claims. These are secondary claims, not primary proof.

New constraints from #106:
- The unresolved objects are the two final-page digit streams and the password/key reduction, not a proven post-hash URL.
- The report identifies `cosmic_A.bin`, an XOR-triangle formula, and an oracle hash as missing public operands; none is present in this workspace.
- It reports large sweeps over KDFs, modes, password candidates, and direct reductions, but those scripts and full witnesses are not locally captured, so the numerical coverage is recorded as reported rather than independently verified.
- It reclassifies the 1327-byte Cosmic result as a PKCS#7 false positive. This is a credible correction because the output is high entropy and the hash target is self-referential, but the exact sweep and probability experiment remain secondary until imported and rerun here.

Why it matters: The correct working model is now: the public intermediate decrypt and matrix outputs are not sufficient; the final password/key mechanism remains unresolved. The color frame and bit-reversed author message provide concrete constraints for that mechanism, while the billion-scale negative claims require artifact-level reproduction before acceptance.

Confidence: STRONGLY_SUPPORTED for local color-frame and bit-reversal facts; SUPPORTED/SECONDARY for the #106 sweep conclusions; UNKNOWN for the final key.

## Discovery #12

Date: 2026-09-04

Artifact: `experiments/sal_final_search/` (CHECKPOINT-2026-09-04-SALFINAL, `sal_regions.json`, `sal_final_search.py` 2868 candidates, `sal_phase2_bifid_oracle.py` 54 families, `REPORT.md`); `raw/web/live/salphaseion/response.bin` (ART-004); floflo777/open-crypto-puzzles `tools/oracle.py` + `analysis/tested.md` + `analysis/leads.md` + `data/planted-addresses.csv` (fetched 2026-09-04, corroboration only).

Observation: Byte-identical SalPhaseIon recovery (live == canonical `SalPhaseIon.txt`, 2149 bytes / 1075 tokens) forces a corrected region map and blob assembly: LEAD91 (unsolved) + MID104 (`matrixsumlist`) + TAIL570 (unsolved) + R1 (`lastwordsbeforearchichoice`) + R2 (`thispassword`) + R3ENG (`shabef|ourfirsthintis|yourlastcommand`) + R3B64A (63) + z@958 (blob data, not separator) + R4A (`enter` line-break) + R4B (64) + R4C (`shabef|anstoo`). A+z+B (128 chars → 96 bytes, salt `3ab585348552415d`, 80 ct) is the only block-aligned assembly (VALID_CIPHERTEXT); A+B (127 chars) is the wrong assembly behind the old 79-byte dead end. Phase 3.2.2 second lock has the same shape (salt `b45a5e3d827593ca`). Issue #106 square rows give a new digit convention (d=0,b=1,i=2,f=3,h=4,c=5,e=6,g=7,a=8) tested alongside legacy a=1 mapping across prime-position/prime-value × zeroing × matrix-shape/transform × sum × yin/yang enumeration.

Experiment: Deterministic finite engine over structurally justified interpretations only (Half/Better Half/103×103/1327-byte/Issue #108/private-key excluded as inputs); every password-like output tried offline against the small-blob oracle under both digests; strict EXACT-address acceptance.

Result: 2868 candidates → 0 EXACT_MATCH, 1 VALID_CIPHERTEXT (A+z+B), 4 trivial KNOWN_TOKEN, 1231 PARTIAL_STRUCTURAL_MATCH, 1632 NO_MATCH; 54 phase-2 families → 108 decryptions → 0 valid paddings, 0 matches. Puzzle remains NOT SOLVED; no new SOLUTION CANDIDATE.

Why it matters: Freezes the exact search object, kills the A+B assembly, imports (without blindly trusting) the dual-lock + planted-address + Bifid-square context, and replaces clever guessing with an exhaustive structural baseline all future branches must beat.

Confidence: STRONGLY_SUPPORTED for region/blob facts and negative counts; SECONDARY for imported sweep/lead claims until rerun here.

Reproducible script: `experiments/sal_final_search/sal_final_search.py`, `experiments/sal_final_search/sal_phase2_bifid_oracle.py`.

## Discovery #13

Date: 2026-09-04

Artifact: `experiments/sal_final_search/dual_oracle.py` (SELFTEST OK), `sal_queued_runner.py`, `sal_queued_report.json` (108 harness attempts).

Observation: Dual-lock (small salt `3ab585348552415d` + p32 salt `b45a5e3d827593ca`) × {hexdigest,direct} × {sha256,md5} + third-door 6-construction harness executed four queued branches: non-literal last-words, Bifid 3×3 period-570 under four keyed squares, dropped-I/O readings, esrever readings.

Experiment: Every password-like output tried offline; strict EXACT-address acceptance.

Result: Sole EXACT_MATCH is the KNOWN bits-reversed-URL control (`13HGhjkmKUkP8sk9k63BLmhkxRjy7uK4Rp`), validating the harness — not a prize hit. Bifid outputs contain no BTCSEED under tested squares (claim UNVERIFIED). Dropped-I/O gives 495/75, 86/5, 56/7, 19/10 — no 256 object from raw streams. Two valid paddings without address match = chance-rate accidents. 0 prize/third-door-open hits. Puzzle remains NOT SOLVED.

Confidence: STRONGLY_SUPPORTED (self-tested harness + exact counts).

Reproducible script: `experiments/sal_final_search/dual_oracle.py`, `experiments/sal_final_search/sal_queued_runner.py`.

## Discovery #14

Date: 2026-09-04

Artifact: `experiments/sal_final_search/sal_matrix_sweep.py` + `sal_matrix_sweep_report.json` (765 candidates / 6120 decrypts); inline Beaufort/Vigenere/EBCDIC/Bifid probes (~140 combos).

Observation: Literal matrixsumlist sweep (bifid9+a1 × prime masks × factor shapes × sum axes × string forms) vs both locks gives 17 valid paddings at chance rate with zero address matches and no family concentration — chance, not signal. Classical ciphers give no binary runs and no hits; EBCDIC on 0–9 digits is meaningless. Bifid under 3×3/5×5/6×6 squares, five keywords, five periods, both directions never yields BTCSEED or the 285→256 reduction (kept 228–280).

Experiment: Offline dual-lock oracle + door spot-checks; strict EXACT acceptance.

Result: 0 prize/third-door-open hits. The BTCSEED/256-object claim is not reproducible from TAIL570 in the tested space; digit streams remain undecoded. Puzzle remains NOT SOLVED.

Confidence: STRONGLY_SUPPORTED (deterministic counts; C-backed AES; self-tested harness).

Reproducible script: `experiments/sal_final_search/sal_matrix_sweep.py`.

## Discovery #15

Date: 2026-09-04

Artifact: `experiments/sal_final_search/sal_final_structure.py` + `sal_structure_report.json`; live HTML of all three pages.

Observation: Full DOM forensics finds no hidden channels (no comments/scripts/inputs on the SalPhaseIon page) and no `Dualite` string anywhere — the h1 reads `Cosmic Duality`, and both blobs follow one 64-column wrapping convention (large: 28×64 literal; small: 64 + token-`enter` + 64). Natural-matrix diagnostics verify prompt R/C against the public grid (True/True); the three sharpest anomalies (TAIL570 ≥4 first-24 15/9 split; 10×57 lone-odd parity; LEAD91 palindromic pair sums) all sit inside chance bounds when calibrated against the number of tries. Locks show no shared structure (entropy 5.97/5.93, no repeated blocks); third door is a fresh valid v0 address (`NULY` defused). Architect positional extraction recorded verbatim.

Experiment: Constancy-scored invariant ranking; pipeline rule admits a lock attempt only for a uniquely-privileged string.

Result: No string qualifies — 0 new lock attempts, 0 hits. Forensics exhausted at the structural level. Puzzle remains NOT SOLVED.

Confidence: STRONGLY_SUPPORTED.

Reproducible script: `experiments/sal_final_search/sal_final_structure.py`.

## Discovery #16

Date: 2026-09-04

Artifact: posted 2026-02-20 "Phase 3 SOLVED" claim (keys, two compact signatures) + derivation note; live Cosmic blob; `experiments/sal_final_search/verify_sig.py`.

Observation: Entire byte chain (XOR key, 1327-byte decrypt, secondary string, base-38 keys, all four addresses) reproduces EXACTLY, but prize equality is False, both ownership signatures are INVALID under self-tested offline recovery (5 message variants), and chain shows dust-only activity (~0.018 BTC swept each, 103 txs).

Experiment: Independent reimplementation + offline signature recovery + read-only chain queries.

Result: New post adds nothing prize-relevant; ownership unproven, prize untouched by this chain. FALSIFIED as solution (Dead End #5).

Confidence: STRONGLY_SUPPORTED.

Reproducible script: `experiments/sal_final_search/verify_sig.py`, `experiments/sal_final_search/phase3_claim_verification.md`.

## Discovery #17

Date: 2026-09-04

Artifact: Portuguese post with exact chain values; live blobs; `experiments/sal_final_search/chains_verification.md`.

Observation: Three chained decrypts verify byte-exact — CHAIN 1 (5-token direct+MD5 → K_C1/K_C2/E_C, WIF link), CHAIN 2 (WIF+MD5 → K_S1/K_S2/E_S), CHAIN 3 (1327 field parse, E_B[:2] completes AES key `38d4f4c90…59cc` three-way). All 8 chain keys miss both targets (16 addresses). CHAIN 4 underspecified (8 readings fail); final pubkey-X step open as admitted; decoy checksum invalid but absent from live OCR; image-count/B2/B3 claims untested.

Experiment: Deterministic re-derivation per posted spec; full oracle on all chain keys.

Result: First verified multi-step decrypts beyond Cosmic; structured, cross-validated, prizeless. Puzzle still NOT SOLVED.

Confidence: STRONGLY_SUPPORTED for chains 1–3; UNVERIFIED for chain 4/image branches.

Reproducible script: inline derivations in `chains_verification.md`.

## Discovery #18

Date: 2026-09-04

Artifact: Indonesian 23-stage walkthrough; live chain data; `experiments/sal_final_search/walkthrough_verification.md`.

Observation: Token hashes (6/6), 14×14 spiral (third transcription), and slice-0 address derivation all MATCH; both donation OP_RETURNs confirmed on-chain ("for ying yang thank you!", "it myself 140 investment", May 2025 third-party). The "5 hidden BMP files" reproduce mechanically but a full scan shows they are ALL 0x0F-adjacent offsets in the file (5 vs ~5.2 expected) — a 1/256 selection effect, falsifying TAHAP 14–21 as designed content. 40B object misses prize + door.

Experiment: Re-derivation, exhaustive offset scan, oracle/door checks, read-only chain queries.

Result: Corroboration where checkable; one more chance-artifact family falsified. Puzzle NOT SOLVED.

Confidence: STRONGLY_SUPPORTED.

Reproducible script: `experiments/sal_final_search/walkthrough_verification.md`.

## Discovery #20

Date: 2026-09-04

Artifact: posted LEAD91/TAIL570 analysis; canonical SalPhaseIon bytes; `sal_regions.json`.

Observation: Every checkable statistic reproduces exactly (strings, IoC 0.1509/0.1181, distributions, no n-grams ≥6, first-occurrence DBIFHCEGA, lengths 13/38). True Bifid DECODE (5×5, DBIFHCEGA + alpha remainder, period 570) yields head `BTCSEED…`, single Z @97, odd positions exactly {B,C,D,E} — overturning the earlier unreproducible verdict (encode/decode mixup, retracted). No other creator tokens in full/even streams; SHA/oracle/door all miss; token-block combine (13/38 as key streams) is structured noise.

Experiment: Independent reimplementation + full-output scan + oracle/door battery + key-stream combine.

Result: Strongest verified structural fact on the digit streams to date — and it terminates: head + constraints, no onward content. LEAD91's FUNCTION (key source) is the genuinely new information. Puzzle NOT SOLVED.

Confidence: STRONGLY_SUPPORTED.

Reproducible script: inline derivations (this session).

## Discovery #22

Date: 2026-09-04

Artifact: LEAD91/TAIL570 bytes; 2023 bit-reversed hint method; XOR-variant 79B.

Observation: Bit-reversal battery (a1/bifid9 × raw/bitrev/bytereversed, locks+door): all garbage, bit-reversal strictly reduces printability (0.6–0.8 → 0.3–0.4), zero hits — the 2023 bit-reversal was transport encoding, not instructed method. XOR-variant 79B door probes miss. No principled untested transform remains in the local battery.

Experiment: Method-from-artifact transforms with oracle/door battery.

Result: Negative throughout. Puzzle NOT SOLVED; local transform space exhausted — only missing-input branches remain (Chain-4 spec, grid crop, new archives, creator confirmation).

Confidence: STRONGLY_SUPPORTED.

Reproducible script: inline battery (this session).

## Discovery #21

Date: 2026-09-04

Artifact: verified Bifid output (`sal_bifid.py`); floflo777 285→256→23-letter claim.

Observation: The verified odd stream (285 chars) contains ZERO I/O letters (locked to {B,C,D,E} by construction), so the documented "drop I/O → 256 symbols over 23 letters" step is IMPOSSIBLE under the verified settings — nothing drops, output stays 285 over 4 letters. The public Bifid→256 chain is internally inconsistent: its head-reproduction settings cannot yield its downstream object. Z-segment battery (before/after/around/head/64-window × hex/raw × locks/door): all miss.

Experiment: Alphabet audit of odd stream; I/O-drop accounting; Z-segment oracle battery.

Result: The 256-object's provenance from the documented Bifid is refuted (whatever was swept at 335M scale, it was not produced by these steps). Puzzle NOT SOLVED.

Confidence: STRONGLY_SUPPORTED (mechanical necessity, not statistics).

Reproducible script: `experiments/sal_final_search/sal_bifid.py` + inline audit.

## Discovery #19

Date: 2026-09-04

Artifact: live puzzle.png; chain material; `experiments/sal_final_search/open_solutions.md`.

Observation: Four OPEN items attacked one-by-one with artifact-derived parameters only — Chain-4 slice forensics (24 slices, no sha/marker), grid count-objective + template match (best err 144, max corr 44/196 ≈ chance; grid not in live capture at scales 8–40), 9 chain strings vs door (0 hits), ordered 6×91+24 pipeline (0/91 correspondence, remainder 8/24 not 15/9).

Experiment: Single deterministic chains per the five-step rule, falsification tests pre-registered.

Result: 3 negative, 1 deepened-blocked. Nothing promoted. Puzzle NOT SOLVED.

Confidence: STRONGLY_SUPPORTED.

Reproducible script: `experiments/sal_final_search/open_solutions.md`.

## Discovery #23

Date: 2026-09-09

Artifact: `raw/github/jackdevs66-GSMG5_CDuality/working/cosmic_duality.txt` (salt `2d3f6fe06dc950e6`); `experiments/sal_final_search/sal_regions.json` BLOB128 (salt `3ab585348552415d`); `raw/github/Naddiseo-gsmgio-5btc-puzzle/working/phase3-assets/phase3.2.txt` p32 blob (salt `b45a5e3d827593ca`); `experiments/004-cosmic/cosmic_decrypted.bin` (1327B, sha `4f7a1e4e...`).

Observation: The OPEN CHAIN-4 spec (`route_tree.md` CHAIN 4, `experiments/sal_final_search/chains_verification.md` 8-reading failure) fails only because prior readings tried raw ECB/CBC0. The mystery payload carries a second OpenSSL blob after XOR-unmasking.

Experiment: Deterministic re-derivation from primary bytes only, no brute force: (1) CHAIN 1 small blob A+z+B with 5-token direct+MD5 -> 79B `K_C1/K_C2/E_C`, `E_C=38d4f4c90cb45fdfc8cff50d0ed1c5`, WIF `5K2by...pz8AT` link verified; (2) CHAIN 2 p32 blob with WIF direct+MD5 -> 79B `K_S1/K_S2/E_S`, `E_S=740a25de4b8e946d0a5ae2667a23a2`; (3) CHAIN 3 cosmic XOR-7 `a795de11...` (raw bytes)+MD5 -> 1327B sha `4f7a1e4e...`, field parse `158+1169`, `E_B[:2]=59cc`, full key `38d4f4c90...259cc` three-way; (4) `mystery[:-1]` XOR repeating `b657264f2f6e6921` -> `Salted__` salt `5bbd88ac32481bca` +1152ct (drop-first gives no header; ascii-mask gives no header); (5) that blob with raw32 `E_C||E_S||E_B[:2]` as EVP-MD5 password -> 1152B pad 1 valid -> 1151B sha `e4269ed5fbb202a81e5e1aa6b5190fdd1ea126b2c8547ea7cdbdf45387ea135b`, marker `+-` (`2b2d`), `tail[246:1151]` sha `9f06936a...`. Hex-ascii password and SHA256-KDF variants give invalid padding.

Result:
- CHAIN-4 decrypt PROMOTED to SUPPORTED (was OPEN). Header is 31B (`+-` + 29B operand context), blocks `up[31:]` = 35x32B, all valid secp256k1 scalars, exactly 7 contain `0x77` at indices `[0,2,3,8,9,12,26]`, 22/35 valid X-coordinates.
- FALSIFIED: `1168=16 IV+1152 raw-CBC` split (actual is Salted__ EVP); `E_S=begbebebbbbbcgg` mask claim (actual `740a25...`); GreatResearch final `idx%9->BR9 + operand + half + better` rule (tested in 264-candidate battery, 0 hits).
- Final-key sweep: ~962 singles/pairs/pyramid + ~13k triples/selector-subsets/BR-subsets (coincurve, exact X `f4d1bbd9...` + h160 `a955...`/`4bc468...`/door `eb862e...`) + ~12k point-addition pairs/triples on 22 valid-X blocks -> 0 hits. Target `X` resolves to uncompressed `04f4d1bbd9...9c73d25f...` (odd Y) -> `a955...`, giving an exact offline oracle.
- Puzzle remains NOT SOLVED at the selector stage. Correction (2026-09-09): `cosmic_A.bin cd3fea3d...`, `K_I1`, `row1-4` are secondary solver folklore from issues #87/#88/#92/#104 with no author source and no bytes produced — NOT author facts, NOT proven blockers. Final routing is OPEN from public artifacts only; 2026-09-09 addendum tested operand-as-multiplier, selector-as-weights (full + byte), and 0x77-parity point-sum (+half+better): 0 hits. Note: point-add of priv-derived pubs == scalar sum `(a+b)*G`, so no new ground there; X-parity rule was the only non-redundant EC test.
- 2026-09-09 addendum 2: 19 scalar families (sums/diffs/mult/XOR/token-sums/byte-sum/sha-concat + half/better/operand): 0 hits. 12 XOR families (xor-all/77/no + half/better/operand/^operand): 0 hits. 10 hash families (operand||concat, concat||operand, pt4, stream||pt4, LEAD/TAIL||pt4, operand/stream/sieved shas): 0 hits, sieve LEAD/TAIL != documented. 5x7 rows sel0064 `3,3,0,1,0`, 7x5 cols `1,1,2,1,0,2,0` (not one-per-group); X-mod35 n∩sel `0,9` only; reverse `0/35`, XOR-pairs `0/595`, SHA-single `0/35` vs 22-X set; half/better not in blocks.
- 2026-09-09 addendum 3 (attempt): 5x7/selector REJECTED as route; 31->32 reconstructions x16, adj-XOR x34, all-pair XOR x595, SHA-chain x68, byte add/sub x68, pairwise diffs x595 vs `X f4d1...` + 3 targets: 0 hits. Hamming mean 128.4, shared-prefix>=4B 0 (random). Frozen rule: promotion requires oracle hit; #23/CLM-009 stay authoritative boundary.

## Discovery #24

Date: 2026-09-09

Artifact: mempool tx `a82052a216cad8f57dee2a039c3b5cef9b5fcb2bc1c3bffa94d713cee0b30e2b` (2021-07-18, escrow `3GSMG24TujqfMJG1kQoBX18DzJHQLeJYMK`); escrow OP_RETURN set 2020-03-24; recovered escrow pubkey `04f4d1bbd9...33559` (oracle.py selftest, tx `88cdb3cdca12...`).

Observation: OP_RETURN `GSMG.io neighbors, half and double` + 4x5000-sat P2PKH outputs (`a4ae210a...`, `3de34fca...`, `c889dfbf...`, `f8fca692...`); OP_RETURN `You are here because 227 chars were correct`.

Experiment: Recompute from the escrow pubkey offline (coincurve/ecdsa): `2P` (double), `P/2` (x inv2 mod N), `P+G`, `P-G`; Hash160 uncompressed; compare. Length-audit the 7-part Phase2->3 concat.

Result:
- `2P` -> `c889dfbf698413209b6131895250b869f68560e0` MATCH output 3. `P/2` -> `3de34fca1bd6b7607243b0316a8102b7598cc9dc` MATCH output 2. `P+G` -> `f8fca692...` MATCH output 4. `P-G` -> `a4ae210a...` MATCH output 1. All 4 byte-exact. PROMISING DISCOVERY: first independent proof the creator demonstrates EC group ops (neighbors +-G, half, double) on the prize key.
- 7-part concat length exactly 227 chars -> `SHA256 1a57c572...`, binding the `227 chars` message to the Phase2->3 password. SUPPORTED as provenance anchor.
- Follow-up neighbor-offset sweep (8 base sums x +-1/+-2 + 35 blocks x +-1 = 102 candidates vs `X f4d1...` + 3 targets): 0 hits.

Why it matters: Certifies `P` independently of the puzzle files; proves author thinks in `+-G`/`2P`/`P/2` terms, so final combination hypotheses should include small offsets and halving/doubling (now tested negative for the obvious set). Does NOT yield the privkey (outputs are hashes of derived points).

Confidence: STRONGLY_SUPPORTED (exact hash equality on 4/4 + length equality).

Reproducible script: inline derivations (this session; coincurve point ops + mempool read-only tx fetch).

Addendum (relation graph): 35/35 distinct scalars; neighbor pairs (±1) 0, double pairs 0, 6 composed half/double-neighbor forms 0, 6 triple forms (sums/diffs/halved, O(35^3)) 0, ordered quadruple A+B=C+C=4D+B-A=±2 0. Graph has no edges — 35 scalars show zero author-relation structure. Branch killed cleanly per frozen rule; no oracle needed.
Addendum (0x77 positional audit): 11 total in 1151B (header abs 6 + 10 body bytes in 7 blocks); intra-block offsets [0,2,4,9,9,10,13,14,28,31], gaps irregular, prev/next bytes all distinct, marked-block X-validity mixed (4 valid/3 invalid). No spacing/periodicity/context pattern; block hit-count 7 vs ~4.1 expected is chance-level. Marker-routing theory killed; 0x77 stays a descriptive label only.

Why it matters: Closes the highest-value OPEN (exact CHAIN-4 wiring) without new primary material, replaces two fitted claims with byte-exact anchors, and bounds the remainder to a missing-operand problem rather than an open-ended decrypt.

Confidence: STRONGLY_SUPPORTED for decrypt/parse/falsifications and negative counts; UNVERIFIED for any final selector rule.

Reproducible script: inline derivations (this session; EVP-MD5 + AES-256-CBC + coincurve checks against `e4269ed5...`, `9f06936a...`, `f4d1bbd9...`).

## Discovery #25

Date: 2026-09-09

Artifact: `experiments/004-cosmic/cosmic_decrypted.bin` (1327B, sha `4f7a1e4e...`); `experiments/sal_final_search/sal_regions.json` (LEAD91/MID104/TAIL570); full prize pubkey `04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4649c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559` (floflo777 README + oracle selftest); Chain-4 1151B plaintext (discovery #23).

Observation: The proposed "15-char selector indexing" final route (15-char Yin-Yang mask as indices 0-6 into the 7 `0x77` selector blocks, sum 15 + operand, EC x2//2/+-1) is directly testable from primary bytes, but the published 15-char string carries a 1-char transcription error, and the full battery misses throughout.

Experiment: Independent reimplementation this session (EVP-MD5 + AES-256-CBC + coincurve, exact offline oracle `X=f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464` + h160 `a9553269572a317e39f0f518cb87c1a0ee1dbae4` / `4bc468447fe1b048ad030a2f9a125478eabc4ed6` / door `eb862e37998c1d077a6c0b46330bccb5f73427`, comp+uncomp): (1) Chain-4 repro byte-exact (1151B `e4269ed5...`, tail `9f06936a...`, `+-`, operand `2dca9ebc...0537`, 35 valid scalars, 7x`0x77` at `[0,2,3,8,9,12,26]`); (2) on-chain 4/4 recompute byte-exact (`2P`->`c889...`, `P/2`->`3de3...`, `P+G`->`f8fc...`, `P-G`->`a4ae...`); (3) sieve repro (raw765 1-indexed primes<=570, pi=104 -> 661B; `8k+7` -> `begbbebebabbbbabbbfccfgg` byte-exact; URL LSBs `111101110011110110010010`, 15 ones); (4) mask audit -> correct kept string is `begbebebbbbbbcg` (not `begbebebbbbbcgg`; double-flip 10<->23; corrected idx `[1,4,6,1,4,1,4,1,1,1,1,1,1,2,6]`); (5) ~10k-candidate battery (claimed+corrected+off2+all-8-offsets+ext24+dropped9 x sel7/pay28/all35 x direct/mod x sum/xor/wsum x 8 operand variants incl. half/better x `S,2S,S/2,+-1,+-2` + hash/multiply/zeroing/5 orderings/position-based kept15/dropped9/all24/kept+-dropped): 0 hits, best X-prefix 3 (chance); (6) E_B 2B-slice sweep (1326 offsets): 11 valid vs 5.2 expected (p~0.01), `+-` unique to `59cc` (duplicate occ @64+524, P(repeat)~2% — weak support, no replacement key).

Result:
- CORRECTION: published `begbebebbbbbcgg` FALSIFIED as transcription; correct `begbebebbbbbbcg` PROMOTED (byte-exact mask output). The all-<7 observation survives either way.
- FALSIFIED: 15-char char-value selector-indexing as the final route for all reasonable readings (~10k, 0 hits). Recorded as Dead End #7.
- PROMISING DISCOVERY (new): sieved offsets `8k+7` AND `8k+2` BOTH avoid `h,i` (values 7,8) over all 24 chars (max idx 6); kept/dropped splits also all a-g. P(single offset avoids h,i)~0.81^24~0.006; P(>=2/8 offsets)~0.0007 — 40x enrichment, the only significant alphabet constraint in the digit<->selector intersection. Yields selector-compatible index strings by construction. Twin `+2` offset is unexplained and is the new lead. Onward EC use of both offsets tested negative (580 candidates), so the signal is structural, not yet routing.
- Chain-4 design status DOWNGRADED to SUPPORTED-reproduction/UNVERIFIED-design: mask `b657264f...` has no author source (GalloClaudio64 #68 secondary only); 8B mask freely forces 8B `Salted__`; plaintext entropy 7.83 / chi2 253 uniform with zero internal relations — consistent with wrong-key chance-valid padding as well as design.

Why it matters: Closes the latest proposed final route with a counted negative, fixes the 15-char string for all downstream work, and replaces it with a counted structural anomaly (h,i-avoidance) plus the author-certified EC-op family as the bounded search space.

Confidence: STRONGLY_SUPPORTED for repro/correction/negative counts and 4/4 on-chain recompute; SUPPORTED (p~0.0007, needs independent-offset replication) for the h,i-avoidance anomaly; UNVERIFIED for any selector rule.

Reproducible script: inline derivations (this session; EVP-MD5 + AES-256-CBC + coincurve + sieve/mask recompute vs `e4269ed5...`, `a955...`, `f4d1bbd9...`).

## Discovery #26

Date: 2026-09-09

Artifact: `experiments/sal_final_search/sal_regions.json` (LEAD91/MID104/TAIL570 -> raw765 -> 1-indexed primes<=570 removal -> 661B sieved); Chain-4 1151B plaintext (`/tmp/opencode/chain4_pt.bin`, re-derived byte-exact this session: sha `e4269ed5...`, tail `9f06936a...`, selectors `[0,2,3,8,9,12,26]`, operand `2dca9ebc...0537`).

Observation: The proposed "four prime byte positions" test (offsets 2,3,5,7 of 8-byte chunks all confined to seven-symbol alphabet 0..6) is directly runnable — and its strict form FAILS, while a narrower depletion signal SURVIVES with a passing control.

Experiment (all pre-registered before oracle contact; exact offline oracle `X=f4d1...` + `a955...`/`4bc468...`/door, comp+uncomp):
1. Full 8-offset confinement table (24 chars each, values a-i->0-8, C_o = count <=6): off0 23/24 (1x i@chunk1), off1 19/24, off2 24/24, off3 23/24 (1x h@chunk0), off4 22/24, off5 23/24 (1x i@chunk1), off6 22/24, off7 24/24. Prime set {2,3,5,7} -> 24,23,23,24. Strict "all four 24/24" prediction FALSIFIED (off3/off5 miss once each).
2. Probability correction: alphabet is 9 letters (a-i), NOT 24. Naive single-offset p = (7/9)^24 ~0.0024 uniform / 0.808^24 ~0.0060 empirical (the reported (7/24)^24 ~1.4e-13 uses the wrong denominator — position count mistaken for alphabet size). The 8 offset streams are DISJOINT samples (partition of 192 sieved positions), so Bonferroni x8 is valid: twin-24/24 rate P(>=2/8) ~0.0010 emp / ~0.0002 uniform — borderline alone.
3. Joint 4x24 prime plane (offsets 2,3,5,7 chunk-interleaved = 96 symbols): 94/96 <=6. Binomial tail vs background p=0.808: p~3.6e-7 (uniform: ~1.3e-8). Non-prime plane (0,1,4,6): 86/96, tail p~0.015. Fisher exact prime-vs-nonprime (94/2 vs 86/10): two-sided p~0.033 — the pre-registered control PASSES at 5%: prime positions are depleted in h,i beyond background. Both halves still span all 9 symbols (prime h,i = 1+1; nonprime = 6+4), so "control alphabet" framing is DOWNGRADED to depletion, not confinement.
4. Routing battery, natural mappings ONLY (identity 0..6->selectors `[0,2,3,8,9,12,26]`, reverse 6..0; NO hashing per deferral): streams A=off2, B=off3, C=off5, D=off7, P96 chunk-interleave, R96 row-concat x sum/XOR x {plain,+operand} x {S,2S,S/2,+-1} = 240 candidates -> 0 hits. (Sums are order-free, so transpose needs no separate test.) 7-password-ID mapping DEFERRED (requires the postponed hashing step; password list itself disputed).
5. Reinsertion halves: prime-retained (zero 0,1,4,6) vs nonprime-retained 4-byte streams compared by distribution (see #3) — no separate key object; reconstruction = original (tautology, not tested as oracle).

Result:
- FALSIFIED: strict "24x4 every symbol in 0..6" (actual 94/96; the 2 misses sit inside prime offsets 3,5).
- SUPPORTED (promising, narrowed): prime-half h,i depletion — 94/96 joint (p~3.6e-7 vs background) + control win vs non-prime half (Fisher p~0.033). Best structural lead remaining, below "major", above "dead".
- FALSIFIED for routing: 240 natural-mapping selector-routing candidates, 0 hits. Order-sensitive natural space within routing-only scope is now EXHAUSTED (EC accumulation is commutative); next needs either the deferred hashing/interleave step or a new constraint.
- BLOCKED: the 161-token grid leg of the proposal has no local token-value transcription (only counts/Base32-garbage + bit-reversed message in workspace), so the 7x23/8-byte framing on THAT object is untestable here — all numbers above are the sieved-661 object. Do not conflate the two.

Why it matters: Replaces an overstated claim (wrong-denominator 1e-13, untested "all four 24/24") with counted facts: strict confinement dead, depletion alive with control, routing battery negative. Draws the exact boundary of what order-preserving tests can still do.

Confidence: STRONGLY_SUPPORTED for the table/counts/negative battery (mechanical); SUPPORTED for depletion (pre-registered set + passing control, needs replication on an independent object); FALSIFIED for strict 96/96 and for natural-mapping routing.

Reproducible script: inline derivations (this session; sieve/offset recompute + coincurve oracle vs `X=f4d1...`, counts above).

## Discovery #27

Date: 2026-09-09

Artifact: S2=`fbeebcefeaaaabbbaabgacga` + S7=`begbbebebabbbbabbbfccfgg` (sieved-661 8k+2/8k+7, Discovery #26); Chain-4 1151B/1152B ciphertext; clue wording in captured `raw/github/Naddiseo-gsmgio-5btc-puzzle/working/phase3.2.ipynb:359` ("reinserting the prime basics ... select from over twentythree ciphers sixteen encryptions and or seven intertwined passwords ... bruteforcing might be required").

Observation: The "23/16/7" clue dimensions have exact arithmetic counterparts in authenticated artifacts — but every pre-registered mechanism built on them misses, while the dimensional correspondence itself promotes to a supported structural hypothesis with two concrete open bridges.

Experiment (pre-registered tiers; exact oracle `X=f4d1...` + `a955...`/`4bc468...`/door, comp+uncomp):
- Tier 1 (direct textual SHA256: S2, S7, S2+S7, S7+S2 vs operand/E_C/E_S/E_B/35 scalars/TX/h160): 0 exact hits. Best hex overlap 10/64 (SHA256(S7) vs one block) assessed chance — P(max>=10 over 4x35 comparisons)~0.13 — explicitly NOT promoted, with reasoning recorded.
- Tier 2 (a-i/o->1-9/0 decimal digits, canonical BE+LE only, plus SHA256 of digit-bytes): 0 hits. Note: 24-digit values are only ~80 bits (10B) — size-mismatched to 30/32B targets, recorded as structural fact.
- Tier 3 (SHA256(S2) XOR SHA256(S7)=`0ae8b658...1c5a3e` x {S,2S,S/2,+-1,+half,+better}): 0 hits (8 EC checks).
- 7x5 matrix: sequential grouping gives markers-per-group 3/2/1/0/0/1/0 with rows `10110/00011/00100/00000/00000/01000/00000` — one-marker-per-group FALSIFIED by distribution. Group-sum routing (per-group marked/signed/all sums, 7 group values x {plain,+op,+half+better} x EC = 45) -> 0 hits. 24->35 mod-35 routing (S2/S7/S2S7/S7S2 x sum/xor x {plain,+op} = 60) -> 0 hits.
- Dimensions verified this session: 1152=72x16=24x3x16=48x24 exact; 35=7x5 exact; 7 marker blocks exact; 161-token count per prior #5/#8 (161=7x23 arithmetic; token VALUES still untranscribed locally — 7x23 leg on that object stays BLOCKED).
- "SOLVED"-issue critique AGREED: no priv scalar + no target equality = not solved (already Dead Ends #2/#5: Half/Better message confirmed, dusting mechanism falsified with dust-only flows; no new test needed).

Result:
- FALSIFIED: Tier 1, Tier 2, Tier 3 (as specified bounded sets); one-marker-per-group; 7x5 group-sum routing; 24->35 mod-35 routing. Recorded as Dead End #8 (bundle).
- PROMOTED to SUPPORTED structural hypothesis: the 23/16/7 dimensional correspondence — clue wording authenticated in-capture + three independently authenticated numbers (161 count, 1152 length, 7 markers) + exact arithmetic counterparts verified. Two concrete falsifiable bridges stay OPEN: (a) 24 positions x 3 AES blocks addressing the 1152B ciphertext (needs an addressing function — none proposed/tested, NOT fished); (b) 7x5 marker-operation matrix (selection reading dead; operation/group reading untested beyond sums).
- "11=7+4" recorded as idea only (no operation stated, untested).

Why it matters: Converts numerology into an authenticated structural frame with counted negatives on every mechanism tried, leaving exactly two pre-defined open bridges instead of another open-ended sweep. Per the clue's own "bruteforcing might be required", remaining search stays bounded to stated operations only.

Confidence: STRONGLY_SUPPORTED for Tier negatives/dimensions/matrix distribution (mechanical); SUPPORTED for the dimensional-correspondence hypothesis (authenticated text + numbers, mechanism open); FALSIFIED for all mechanism variants listed.

Reproducible script: inline derivations (this session; SHA256/decimal/XOR/group batteries + coincurve oracle).

## Discovery #28

Date: 2026-09-09

Artifact: S2/S7 pair object P[i]=(S2[i],S7[i]) i=0..23 (streams per #26); Chain-4 blob re-derived byte-exact this session (1168 = 16 + 1152CT; padded pt 1152 pad 1; parsed 1151 = 31+35x32).

Observation: The pair-coordinate addressing proposal is testable in its strong form without any invented mapping — and it FAILS there; its general form is BLOCKED on a missing addressing function. The same session pins the 24-group partition to an exact byte layer, which is the round's surviving structural constraint.

Experiment (no hashing, no integer-key conversion; diagnostics first as specified):
1. Pair census: 16 unique / 24. Top (a,b)x5, (e,b)x3, (b,b)x3, 13 singletons — no small-alphabet collapse.
2. Symmetry: == 5, < 12, > 7. Sign test on 19 non-ties P(>=12|0.5)~0.18 — chance.
3. Delta (a=0..i=8): {0:x5, -1:x5, -2:x3, +3:x3, +4:x2, -3:x2, +1:x2, -4:x1, -6:x1}; mean|d|=1.917.
4. Shuffle controls (20k, seed 20260909, same marginals): P(mean|d|<=obs)~0.20, P(eq>=5)~0.54, P((a,b)>=5)~0.33, P(unique<=16)~0.78 — ALL null-consistent. Streams track each other only via shared marginals.
5. Distinct-address test (no mapping assumed): 24 distinct pairs required to address 24 groups — observed 16. FALSIFIED in strong form with zero invented constants. General form (addresses with repetition, mod-maps, pair->scalar encodings) NOT tested by design: any mapping from 81 cells to 0..23 is arbitrary without an artifact function, and mod-routing already died (#27).
6. Layer pinning (byte-exact): 1152/48 = 24.0 on CT (72 AES blocks) AND padded pt (72 blocks); 1151/48 ~ 23.98 on parsed plaintext — the 24-group partition is exact ONLY at the 1152-byte layer. Any addressing mechanism must therefore operate at CT/padded-pt level, not on the 31+35x32 parse.
7. 23->24 reinsertion: no runnable non-fishing test exists. Only 23-object is 161-grid columns (values BLOCKED); Z@97 variants already failed (prior); drop-1-of-24 = 24 variants with no specified target = fishing. Recorded BLOCKED/underdetermined, not tested.

Result:
- FALSIFIED: pair-coordinate addressing in distinct-address form; pair small-alphabet/symmetry/tracking structure (all shuffle-null). Recorded as Dead End #9 (pair family).
- BLOCKED (not falsified): general pair->group addressing (function missing); 23->24 reinsertion (target missing).
- SUPPORTED (new constraint): 24-group address hierarchy, if it exists, lives at the 1152-byte layer — narrows all future addressing proposals to CT/padded-pt, excluding the parsed-plaintext layer.

Why it matters: Closes the pair-coordinate proposal exactly where specified (diagnostics, no hashes) with controls, refuses the fishable remainder, and converts the 24x3x16 bridge from free-floating numerology into a layer-pinned constraint: H-DIM-003 bridge (a) now reads "24x3x16 addressing AT the 1152-byte layer, function still missing".

Confidence: STRONGLY_SUPPORTED for census/nulls/layer arithmetic (mechanical + controlled); FALSIFIED for distinct-addressing; BLOCKED (honest) for the remainder.

Reproducible script: inline derivations (this session; pair census + 20k-shuffle controls + blob layer recompute).

## Discovery #29

Date: 2026-09-09

Artifact: pair object P[i]=(S2[i],S7[i]) (#28); 7x5 marker matrix `10110/00011/00100/00000/00000/01000/00000` (markers at (0,0),(0,2),(0,3),(1,3),(1,4),(2,2),(5,1); matrix rows cross-checked against the reported version — identical).

Observation: The "routing matrix" report's four CONFIRMED claims reduce on independent re-derivation to one tautology, one chance-level hit with an invented mapping, one agreement, and one untested assertion. The round's value is guardrail, not solution: "99% solved" is unjustified — no candidate from any battery stands within a bounded operation of target.

Experiment (exact oracle `X=f4d1...` + `a955...`/`4bc468...`/door, comp+uncomp):
1. Surjection audit: "all 16 unique pairs appear at least once across the 24 groups" is DEFINITIONAL — the pairs are derived FROM those 24 positions, so each trivially occurs at its own positions. No pair->ciphertext-group mapping was ever specified (the 24 x 48B groups have no stated addressing function). Evidential weight: zero. Reclassified as tautology, not discovery.
2. Coordinate mapping reproduced EXACTLY as stated (letter->0-8, (x%7,y%5)): matches at (0,0),(0,2),(1,4),(5,1) = 4/16. Null control (20k shuffles, seed 20260909, same marginals, orientation granted): mean unique 15.6, P(matches>=4) ~ 0.49 — expected value ~3.2. The mapping itself is invented (letter encoding + mod folding chosen to fit 7x5; unpenalized). Verdict: chance-level hit, FALSIFIED as evidence.
3. Prime row/col sums independently confirmed negative: 0-based rows {2,3,5} + 1-based {1,2,4,6}, cols {2,3}/{1,2}, x {plain,+op} x {S,2S,S/2,+-1} = 40 candidates -> 0 hits. (Prior marker-arithmetic negatives already Dead Ends #2/#5/#7.)
4. 23->24 "reinserted coordinate": no operation specified or tested in the report — interpretive assertion only. Stays BLOCKED per #28 (only 23-object is 161 columns, values untranscribed).

Result:
- DOWNGRADED to tautology: "perfect surjection onto sixteen encryptions" (claim 1).
- FALSIFIED as evidence: 16-pairs->7x5 coordinate mapping (claim 3; p~0.49). Recorded as Dead End #10.
- AGREED: marker matrix + falsified list (claims 2-minus-interpretation and the negative list check out against workspace state).
- UNTESTED (not confirmed): 23->24 reinsertion mechanics (claim 4); "markers as operation selectors" for EC ops P+-G/P/2/2P beyond sums (priority plan step 2-3: no operands/keys/IVs/modes were ever specified, so nothing runnable exists there yet).
- Puzzle is NOT 99% solved: every mechanism battery to date is negative; the final private key is not "a bounded operation away" under any stated operation.

Why it matters: Prevents a chance hit (p~0.5) and a tautology from redirecting the search into invented-mapping space — the exact failure mode the workspace's frozen rule exists to block. Surviving search space is now sharply bounded: H-DIM-003 bridge (a) needs an artifact-stated function at the 1152B layer; bridge (b) needs marker-operation semantics beyond sums; depletion needs 161 values.

Confidence: STRONGLY_SUPPORTED for reproduction/null/negatives (mechanical + controlled); FALSIFIED for the mapping-as-evidence and surjection-as-discovery readings.

Reproducible script: inline derivations (this session; mapping repro + 20k-shuffle null + 40-candidate prime sums + tautology audit).

## Discovery #30

Date: 2026-09-10

Artifact: `experiments/004-cosmic/cosmic_decrypted.bin` (1327B, sha `4f7a1e4e...`); Chain-4 1151B plaintext (`/tmp/opencode/chain4_pt.bin`, sha `e4269ed5...`); exact offline oracle `X=f4d1bbd9...55633559` + `a955...`/`4bc468...`/door (coincurve, comp+uncomp).

Observation: Three verification tasks and one uniqueness control, all executed (not thinking-only):

1. B/Y frame re-verified from the copied 14x14 matrix: counts K=86/W=86/B=15/Y=9; down-first CCW spiral decodes to `gsmg.io/theseedisplanted`; colored spiral positions 7,15,...,191; spiral-order B/Y sequence `BBBBYBBBYYBBBBYBBYYBYYBY` == URL LSBs `111101110011110110010010` (bytes `F7 3D 92`) exactly. Structural checksum reading CONFIRMED (agrees with CLM-005/#11); independent-secret reading stays DEAD. Pixel-level grid localization in the live capture NOT re-attempted beyond layout inspection — the "75px overturn" claim has no local artifact support; grid-from-pixels stays BLOCKED, grid-from-matrix stays SOLVED.
2. Bifid "impossibility proof" (GreatResearch errata claim that rows-0/1-restricted ciphertext cannot decode to `BTCSEED` with T/S in row 3) is FALSE as stated — it misdescribes Bifid decode, which concatenates row-coords then col-coords and re-splits, so output rows for the second half come from input COLUMNS (span 0-4). True decode (5x5 DBIFHCEGA+alpha, RC, period 570) reproduces head `BTCSEED`, single Z@97, odd set {B,C,D,E} byte-exact (`sal_bifid.py`). Discovery #20 RESTORED; the errata falsification is itself falsified. Even-stream correction STANDS: odd285 has 0 I/O (drop impossible), even285 has I=13+O=16=29 -> even256 over 23 letters, head `TSEDMKAH...`, sha256 `1740b55b...` verified byte-exact.
3. Chain-4 parse re-verified: 1151B = `+-` + 30B operand `2dca9ebc...0537` + 35x32B; all 35 are valid secp256k1 scalars; exactly 7 blocks contain `0x77` at indices `[0,2,3,8,9,12,26]` — BUT with multiplicity: intra-block offsets are block0:{0,2}, block2:{13}, block3:{9,28}, block8:{4}, block9:{10,31}, block12:{14}, block26:{9} (10 occurrences over 7 blocks).
4. PROMISING (new, positive): drop-dimension uniqueness of the Chain-4 wiring. Holding mask `b657264f...` + key `E_C||E_S||E_B[:2]` fixed: all 1169 single-byte drops tested; 1161 preserve the `Salted__` header trivially (any drop at position >=8 leaves bytes 0:8 untouched — header carries zero drop evidence, as previously noted); of those 1161, EXACTLY ONE (drop-last, index 1168) decrypts (EVP-MD5) to valid PKCS#7 padding AND 1151B AND `+` marker, yielding sha `e4269ed5...` byte-identical to the reference. Valid-padding(any) count is 1 vs ~4.5 expected at 1/256; joint padding+`+` expected ~0.02. The wiring's drop parameter is therefore a unique fixed point, not a fitted accident within this family.

Result:
- CORRECTION: Bifid impossibility claim FALSIFIED (mechanics + byte-exact repro). 75px grid-relocalization claim UNVERIFIED (no artifact).
- FALSIFIED (new, Dead End #16): 0x77-intra-block-position as 5-bit selector into 28 payload blocks for all natural readings (~3.5k candidates: first/last/all-occurrence positions x raw/mod28/-1/+1/mirrored x fwd/rev payload order x sum/xor/single x operand/int/rpad/sha/none x S/2S/S/2/+1/-1/+2/-2, plus direct-into-35 and neighbor-byte Route-B variants) -> 0 hits, best X-prefix 4 (chance-consistent). Two structural defects found by execution: (a) multiplicity — 3/7 control blocks hold TWO 0x77 each, so "the position" needs an extra free choice; (b) overflow — positions 28,31 exceed a 0..27 payload space, forcing ad-hoc wrap (direct-into-35 variant also misses).
- PROMOTED to SUPPORTED-design (was UNVERIFIED): Chain-4 (drop-last, mask, raw32-key) decrypt, on drop-dimension uniqueness. Mask provenance (secondary-only #68) and E_B-slice fitting remain the honest caveats — the test fixes those dimensions, it does not bless them.

Why it matters: Kills two false redirections (fake impossibility proof, unverified grid claim), closes the newest selector proposal with counted negatives plus executed structural defects, and gives the first positive specificity evidence for the Chain-4 wiring itself — the search object for any future selector work is now a uniqueness-certified plaintext, not a possibly-chance blob.

Confidence: STRONGLY_SUPPORTED for repro/negatives/uniqueness counts (mechanical); SUPPORTED-design for the Chain-4 wiring (one dimension certified, two fitted dimensions disclosed).

Reproducible script: `/tmp/opencode/test_selector_pos2.py`, `/tmp/opencode/test_selector_pos3.py`, `/tmp/opencode/test_selector_pos4.py`, `/tmp/opencode/test_chain4_dropuniq.py`, `/tmp/opencode/test_chain4_calib.py` (this session; coincurve oracle + EVP-MD5 + AES-256-CBC).

## Discovery #31

Date: 2026-09-10

Artifact: LEAD91/TAIL570 (`sal_regions.json`); `sal_bifid.py` (5x5 DBIFHCEGA+alpha, RC DECODE, period 570); exact oracle `X=f4d1bbd9...` + `a955...`/`4bc468...`/door (coincurve, comp+uncomp).

Observation: Baseline re-verified byte-exact (keyword `DBIFHCEGA`, square rows DBIFH/CEGAK/LMNOP/QRSTU/VWXYZ, head `BTCSEED`, single Z@97, all 285 odd positions in {B,C,D,E} — stronger than the reported "first 285"). Then the round's structural result:

1. THEOREM (proven by construction + verified prediction): full-period Bifid decode is a PURE RECODING with zero diffusion. Coords `[r0,c0,r1,c1,...]` split into halves; output[j] uses one coord from each half. Odd output positions (0-indexed even j) pair two INPUT ROW-bits -> alphabet mechanically locked to {B,C,D,E} = exactly the {0,1}x{0,1} square cells (repro script predicts all 285 odd chars from input rows alone: EXACT match). Even positions pair two input COLUMN-values -> 25-letter alphabet (I,O present). Consequences: (a) the "odd lock" is a mechanical necessity given ciphertext in square rows 0-1, not an independent clue — the odd/even yin/yang mystique is demoted to a consequence of period=full-length; (b) ALL ciphertext information resides in 570 row-bits + 570 column-values(0-4); (c) BTCSEED-head significance estimated ~1/4M under the single principled config (~1/41k Bonferroni over the 96-config family, uniformity caveat on columns) — consistent with a DESIGNED confirmation header (author tuned first input chars), remainder carrying the payload.
2. NEGATIVES (bounded, stated mappings only): H-TRI-001 (LEAD91=91=T13 triangle -> 13 row/col sums -> `matrixsumlist` checksum; rows/cols/reversed x a1/a0 x raw/+7 x mod26/mod9 = 10 readings) -> 0 hits, KILLED as checksum. even256-as-16x16 (256=16^2 exact) with prime-{2,3,5,7} zero/keep rows/cols (1-based + 0-based) -> 32 sums mod256 -> scalar x {S,2S,S/2,+-1,+-2} (112 candidates) -> 0 hits, best prefix 1. Row-bit stream (570b->71B, 3 remainder handlings; LEAD 88b->11B; int-mod-n + sha256 forms x 7 EC ops) + base-23 even256 + base-4 odd285 direct scalars (70 candidates) -> 0 hits, best prefix 1. The row-bit stream was the last unexamined principled object from this family.

Result:
- PROMOTED to THEOREM: full-period Bifid = row/column recoding; odd-lock mechanical (demotes H-ANOM-adjacent mystique, constrains all future Bifid theories to operate on COLUMNS — rows are 1-bit and fully extracted).
- FALSIFIED: H-TRI-001 checksum (Dead End #17); even256-16x16-primezero-matrix-sum scalar route (Dead End #18); row-bit/base-23/base-4 direct-scalar readings (Dead End #19).
- SUPPORTED (estimate, needs no further action): BTCSEED as designed confirmation header.

Why it matters: Reframes the entire digit-stream frontier — kills three of the last untested principled branches with counted negatives AND replaces superstition (yin/yang split, odd-lock-as-clue) with mechanism. Direct digit-stream->key readings are now EXHAUSTED for stated mappings; remaining frontier is Chain-4 selector semantics on the uniqueness-certified (#30) plaintext, plus provenance (mask attestation, 161 values).

Confidence: STRONGLY_SUPPORTED for theorem/repro/negatives (mechanical proof + exact prediction + counted batteries).

Reproducible script: `/tmp/opencode/test_triangle.py`, `/tmp/opencode/test_even16.py`, `/tmp/opencode/test_rowbits.py` (this session).

## Discovery #32

Date: 2026-09-10

Artifact: `hints/2023-02-23.png` (551x760 Telegram screenshot); sieved-661 offsets S2/S7 (#26); B/Y mask `111101110011110110010010` (CLM-005); cosmic mystery `cosmic[158:1327]`; oracle `X=f4d1...`/h160s/door.

Observation: Four results on the proposed COLOR-MUX / trailer / 161 program:

1. VACUITY REFUTATION (mechanical): S2 AND S7 recomputed from scratch (raw765, 1-indexed primes<=570 removal, first 24 chunks) match ledger strings exactly — and EACH is independently 24/24 pure a..g (max value 6, zero h/i). Therefore EVERY one of the 2^24 possible choice-strings (both mux orientations included) is automatically a..g with probability 1 REGARDLESS of mask. The B/Y frame does NO work in the alphabet collapse; H-COLOR-MUX's central "naturally produces seven values" argument carries zero evidential weight as stated. Mux strings verified distinct chimeras (A=M(S2,S7) dist 7/12 from S2/S7; B=M(S7,S2) dist 12/7) — specific objects, but their purity is inherited, not produced.
2. MUX SCALAR BATTERY (84 candidates: S2/S7/A/B x {base-7 int mod n, SHA256-ascii, concatenated-decimal mod n} x {S,2S,S/2,+-1,+-2} vs oracle) -> 0 hits, best prefix 1. Mux-as-selector-index readings additionally collapse to vacuity per (1): any index use must justify the mask independently.
3. TRAILER FACT BASE (H-DROP-001): mystery == cosmic[158:] exactly, so trailer = cosmic[1326] = last byte of the whole Cosmic plaintext. Value 58 = 0x3A = ASCII ':'. a-i mod9 -> 'e'(4); mod7/mod28 = 2; mod35 = 23; mod24 = 10; non-prime; hi-bit 0. Trailer-as-index readings (2->payload-2, 23->block-23, 10->block-10, 2->token-2) collapse to already-tested singles (all miss per #23); recorded as facts, no new battery warranted.
4. PROMISING (new, positive): 161-TOKEN TRANSCRIPTION RECOVERED AND VALIDATED. Tesseract on cropped grid (every-5th-column tokens lost trailing '10' to column-edge clipping — repaired deterministically) yields 160 tokens, all ending 110; bit-reverse + reverse order reproduces the known author message EXACTLY minus its first char ('ellowblue...promised'). The missing 161st token (screenshot bottom cut off) reconstructs as `10011110` (bitrev of 'y'=0x79, ends 110 consistent). A 160-byte OCR output coherently decoding to English under the stated transform is self-validating (chance ~0). CONSEQUENCE: values = message bytes + constant low-3-bits — NO independent numeric operand exists for depletion replication or the 7x23 mechanism. 7x23/23x7 acrostics (`yucifni`, `ylextrrcievhonfeuevtavr`) are garbage. The 161 leg goes BLOCKED -> RESOLVED (content = message only, exhausted).

Result:
- FALSIFIED as argued: H-COLOR-MUX alphabet-collapse claim (vacuous; Dead End #20); mux strings as scalars (same).
- PROMOTED to RESOLVED: 161-token values (transcribed, validated, content-exhausted — closes the highest-value missing artifact per prior prioritization, negatively for key material).
- RECORDED: trailer byte facts (no promotion, collapse noted).

Why it matters: Removes the round's most attractive false lead with a one-line mechanical fact (parents already pure), closes the longest-standing BLOCKED leg with a validated transcription, and leaves the honest remainder: prime depletion (#26, still unreplicated) and Chain-4 selector semantics on certified plaintext (#30) with no new prized battery.

Confidence: STRONGLY_SUPPORTED throughout (recomputation, counted battery, self-validating transcription).

Reproducible script: `/tmp/opencode/test_muxscalar.py`, `/tmp/opencode/grid161.png` + Tesseract `--psm 6` pipeline (this session).

## Discovery #33

Date: 2026-09-10

Artifact: Bifid odd stream (285 chars, #20/#31); Chain-4 1151B plaintext + 30B operand (`/tmp/opencode/chain4_pt.bin`); oracle `X=f4d1...`/h160s/door (coincurve, comp+uncomp).

Observation: The proposed prime-extraction object is REAL — reproduced byte-exact under stated conventions (odd=r[0::2]; 35 groups of 8 from start; 1-indexed positions {2,3,5,7}; D=00/B=01/C=10/E=11 row||col; MSB-first): 35 bytes `be64aa42...b7a0804b` match the claimed hex exactly; leftover `DDDCE` (0000001011) confirmed; E1 mod-5 7x5 matrix matches the claimed matrix exactly. The object is therefore PROMOTED to CONFIRMED OBJECT (reproducible, dimension-exact: 285 = 35x8+5, 35 = Chain-4 block count).

Oracle battery (exact X/h160/door, scalar-linear EC so sums are exact, NO point-op approximations): index base {1,0} x prime order {fwd,rev} x bit order {row||col, col||row} x byte order {MSB,LSB} = 16 extractions x {op-schedule sum (stated assignment 0->P,1->P+G,2->P-G,3->2P,4->P/2) plain/+operand, scalar offsets plain/+operand, linear weights} = 80 candidates -> 0 hits, best X-prefix 1 throughout (chance level).

Degrees-of-freedom audit (forced vs chosen): FORCED — square/coords mapping (only swap twin, tested), primes {2,3,5,7}, odd stream, 35-block target. CHOSEN — groups-of-8 (byte unit; groups of 4/2 untested, would break the 35-match), grouping from start (leftover-last; from-end twin untested), op assignment (1 of 120 permutations tested — the stated one; the other 119 deliberately NOT swept: fishing), combination = sum/weights/offsets (tested), mod-5 (op reading assumed). The "35<->35" alignment is therefore conditional on the byte-grouping choice: natural, not forced.

Result:
- PROMOTED: 35-byte extraction to CONFIRMED OBJECT (waypoint, reproducible).
- FALSIFIED (Dead End #21): op-schedule / weights / offsets readings of it vs the exact oracle in all 80 stated variants. "byte mod 5 = operation" remains the unjustified link, exactly as flagged pre-test.
- Rule applied: op-permutation sweep (119) declined as fishing; grouping-from-end twin left UNTESTED (single binary choice, may be run if a new stated reason appears — currently none).

Why it matters: Closes the round's top-ranked structural lead the honest way — object confirmed, mechanism dead in stated form, rescues named-but-declined with reasons. The pattern across #30/#31/#32/#33 is now unmistakable: every artifact-faithful construction reproduces beautifully and misses the oracle uniformly, which itself is evidence about the problem (see forward tree).

Confidence: STRONGLY_SUPPORTED for repro + negatives (mechanical, exact oracle).

Reproducible script: `/tmp/opencode/test_opsched.py`, `/tmp/opencode/test_opsched2.py`, `/tmp/opencode/test_opsched3.py` (this session).

## Discovery #34

Date: 2026-09-10

Artifact: 35-byte object (#33); Chain-4 layers (1327/1152/1151); 16-extraction pipeline family (#33).

Observation: The matrix-sum claim is arithmetically TRUE and evidentially DEAD. 7x5 row sums `[570,897,495,899,452,660,732]` and column sums `[1048,1152,760,797,948]` verified exact; mod-103 indices `[55,73,83,75,40,42,11,18,19,39,76,21]` verified exact. Specificity controls kill the designedness inference:

1. Shuffle null (50k, seed 20260910, fixed byte multiset, pre-registered targets row==570 / col==1152): P=0.0147 / 0.0062, P(either)=0.0208. Passes 5% in isolation — but isolation is the wrong frame.
2. Pipeline multiplicity (the killer): all 16 pipeline extractions (#33 family) collapse to 4 DISTINCT byte-strings (complement symmetries). Row-sum 570 recurs in 2 of 4 distinct objects (near-mean resonance: 5-byte sums mode sits ~570-640); 1152 in 1 of 4. Combined with target-mapping freedom (which sums pair to which of ~14 artifact dimensions), the coincidence sits at ~15-30% — square resonance, not routing. The sums were examined only on the favored E1 object; E1 is not special among the four.
3. Consequence: direct-offset and mod-103 batteries DECLINED (not run): both need an unstated readout function (offsets → bytes → ??? → X; 12 selected values → ??? → key material) stacked on a premise that just failed its control. Running them would be fishing. Revival condition stated: an artifact-given readout function.

Result:
- CONFIRMED as arithmetic: 12 sums, mod-103 indices (Dead End #22 records the designedness kill).
- FALSIFIED as designed addressing layer: 570/1152 coincidence (resonance grade).
- Pattern note (4th round): artifact-faithful constructions reproduce exactly and miss uniformly — the workspace now treats uniform-miss under exact oracles as evidence that the key is not a stated function of public stream material (missing operand, non-public trapdoor, or unstated relation class).

Confidence: STRONGLY_SUPPORTED (exact arithmetic + controlled nulls + enumerated pipeline family).

Reproducible script: inline derivations (this session; 50k-shuffle null + 16-extraction census).

## Discovery #35

Date: 2026-09-10

Artifact: canonical solver `jackdevs66/.../solver_salphasion_cosmic.py` (7 passwords incl. p1==p5 duplicate); Chain-4 1151B/operand; E1 35-byte object (#33); oracle `X=f4d1...`/h160s/door (coincurve, scalar-exact sums).

Observation: CORRECTION first — the canonical 7-token XOR set is [matrixsumlist, enter, lastwordsbeforearchichoice, thispassword, matrixsumlist, yourlastcommand, secondanswer] (p1==p5 duplicate, the documented XOR-cancel). The proposed row list (yourlastcommand@5, secondanswer@6, sha256@7) is NON-canonical: 'sha256' as a 7th token has no primary support (it is the KDF-family name / R3ENG wordplay, interpretive). Claimed H-prefixes check out as prefixes but for the non-canonical order. Both sets tested anyway (user set labeled secondary).

Lattice battery (row-major 7x5, canonical order blocks 0..34; fixed columns P,P+G,P-G,2P,P/2 as scalar maps d,d+1,d-1,2d,d/2; rows 1..7 <-> canonical tokens incl. H1==H5 duplicate mask): T1 fixed-column total plain/+op (T5 paired-cancellation regrouping is the IDENTICAL sum — run once, not twice); T3 mod-7 diagonal-match filter (selects only 3/35 cells: 5,27,32 — sparsity chance-consistent vs 5 expected) with/without col ops x plain/+op; T4 mod-35 distinct-set (24 cells) + multiplicity-weighted sums with col ops x plain/+op; T2 token-hash masks per-cell and per-row x canonical/user-list x plain/+op. Total 18 candidates -> 0 hits, best prefix 1 (chance). Untested by design: lattice fill permutations, column permutations (120), row-token reassignments — no artifact states them.

Result:
- CORRECTED: 7-token set (canonical restored; duplicate H1==H5 noted — rows 0,4 share any token mask).
- FALSIFIED (Dead End #23): 7x5 token-x-EC lattice readings T1-T4 + bounded T2 in all 18 stated variants.
- SECONDARY/UNVERIFIED: "16 yin-yang permutations dead by oracle" (no local reproduction); Issue #69 SOLVED-report claims (issue absent from local corpus; #84 present).

Why it matters: Closes the last structured Chain-4 interpretation with independent semantic grounding (author EC family x documented token set) — the last bridge between the two halves of the puzzle in stated form. Remaining: provenance and unstated-relation classes only.

Confidence: STRONGLY_SUPPORTED for correction + negatives (primary artifact + exact oracle).

Reproducible script: `/tmp/opencode/test_lattice.py` (this session).

## Discovery #36

Date: 2026-09-10

Artifact: canonical solver (7-token XOR consumes ALL tokens before any matrix op); `phase3_claim_verification.md:13` (secondary[i]=row[i]+col[(i+7)%103] — canonical readout already uses BOTH); Chain-4 35 scalars; oracle X/h160s.

Observation: FRAMING CORRECTION — the "first matrixsumlist -> Half/Better, second -> secondanswer" narrative misattributes the pipeline: the Cosmic decrypt XORs all 7 tokens (incl. both matrixsumlists AND secondanswer) BEFORE the matrix/base-38 step. The p1==p5 duplicate is byte-real but its known role is XOR self-cancel, not a staged double application. 'Second matrixsumlist' as sequential re-application is interpretive, not artifact-stated. Dispositions of Branches A-E:

- A (sum all 35 mod N, no selection): EXECUTED this session -> x=`7e68e84b...`, both h160s miss (comp+uncomp). DEAD (consistent with #23 sums family; recorded Dead End #24 under new framing).
- B (column-sums-only -> base-38): COVERED-DEAD — canonical construction already consumes row+col jointly; columns-only is an invented subset with no stated basis.
- C (14x14 sums -> indices -> key): DECLINED — readout incomplete (indices -> ??? -> key unstated) + transplant analogical + 103-list not locally derivable from cosmic bits without new free choices (bit order x layout x 7-bit trim). Revival: artifact-stated readout.
- D (16x16 sums): DEAD (#18 + reporter's own 104-construction negative). Declined re-run.
- E (7x5 marker sums as selectors): COVERED-DEAD (#27 group-sum routing 0/45). Declined re-run.

Result: The artifact-stated readout audit is valuable framing, but every executable branch under it is dead/covered/declined. No new prized battery remains in this program.

Confidence: STRONGLY_SUPPORTED (primary artifacts + citations + executed Branch A).

Reproducible script: inline sum-35 derivation (this session).

## Discovery #37

Date: 2026-09-10

Artifact: `raw/web/live/salphaseion/response.bin` textarea_1 vs canonical `cosmic_duality.txt`; `chain4_pt.bin` (1151B `e4269ed5...`); `sal_regions.json` (LEAD91/TAIL570); Bifid output (`sal_bifid.py`); exact oracle `X=f4d1bbd9...` + `a955...`/`4bc468...` (coincurve, comp+uncomp).

Observation: The "large second blob" nicknamed "Dualite" in route-tree side-routes is BYTE-IDENTICAL to the canonical Cosmic Duality blob. textarea_1 (live capture) == `cosmic_duality.txt` (sha256 `b18950551a4dd0cb8a9378f0906ba18c03a15f0ee83eb98c6bc90165c5f79805`, 1344B, salt `2d3f6fe06dc950e6`, 1328B CT). Both decrypt under the documented 7-token XOR→EVP-MD5 pipeline to the SAME 1327 bytes (`4f7a1e4e...`). The route-tree "second blob never opened" entry is a misconception — there is no independent second blob; "Dualite" == "Cosmic Duality". The 1327B parse is exactly 103×103 matrix bits + 7-bit trail `0111010` = 58 = 0x3A = ASCII ':' (matrix density 0.4895, non-symmetric p≈0.5, diagonal 49/103 ones).

Result:
- CONFIRMED: textarea_1 == cosmic_duality.txt byte-for-byte; both open to `4f7a1e4e...`; 7-bit trail = `:`.
- FALSIFIED as a separate unexplored route: the "Dualite / second blob OPEN" side-route (it is the same, already-analyzed Cosmic blob).

Confidence: STRONGLY_SUPPORTED (byte equality + decrypt repro + bit parse).

Reproducible script: `/tmp/dualite` reconstruction + `sal_bifid.py`.

## Discovery #38

Date: 2026-09-10

Artifact: even256 object (Bifid even stream minus I/O); 7-token set; Chain-4 35 blocks; author clue `phase3.2.ipynb:359`.

Observation: The even256 object structurally instantiates the author's final clue word-for-word. Bifid decode of TAIL570 (5×5 DBIFHCEGA+alpha, RC DECODE, period 570) yields 570 chars head `BTCSEED`; even positions (285) have I=13 + O=16 = 29; dropping I/O gives EXACTLY 256 chars over a 23-letter alphabet (A–Z minus I,O,J), sha256 `1740b55ba5d224e86f61054bacd7caf90a8cf2c4418535c67d092903c4509f35`. The clue "select from over twentythree ciphers sixteen encryptions and or seven intertwined passwords" maps exactly: 23 letters = "twentythree ciphers"; 256 = 16×16 = "sixteen encryptions" (16 rows × 16 columns); 7 tokens (matrixsumlist, enter, lastwordsbeforearchichoice, thispassword, matrixsumlist, yourlastcommand, secondanswer) = "seven intertwined passwords" (intertwined = XORed to `a795de11...`); and 16+7=23. The even256 is also a valid Base58 string (all chars in Base58; decodes to 188 bytes, checksum-invalid).

Result:
- PROMOTED to SUPPORTED structural frame: even256 = the "23 ciphers / 16 encryptions / 7 passwords" object (arithmetic + wording + alphabet all match, no invented constants).
- OPEN (key derivation): every direct/sum/XOR/base-N/Base58/hash reading tested this session vs `X=f4d1bbd9...` + `a955...`/`4bc468...` missed (row/col sums, 16×16 submatrix of the 103×103 matrix, base-23/25/58, XOR-with-7-token-key families).

Confidence: SUPPORTED for the structural frame; OPEN for the key function.

Reproducible script: `/tmp/xortri` reconstruction + `sal_bifid.py` + inline oracle batteries.

## Discovery #39

Date: 2026-09-10

Artifact: XOR-triangle (Lucas theorem) applied to 24 CT groups, 28 unmarked Chain-4 blocks, and 103 matrix rows; GalloClaudio64 issue #68 hint "triangular … XOR triangle".

Observation: The "XOR triangle" hint yields exactly SIXTEEN survivors from every natural object, matching "sixteen encryptions". A repeated adjacent-XOR reduction of N elements collapses to the XOR of elements at indices where C(N−1,i) is odd (Lucas). (a) 1152B CT = 24 groups × 48B: 23 = 0b10111 (popcount 4) → 16 survivors `[0,1,2,3,4,5,6,7,16,17,18,19,20,21,22,23]`. (b) 28 unmarked Chain-4 blocks (28 = T7, the "triangular" hint): 27 = 0b11011 (popcount 4) → 16 survivors. (c) 103 matrix rows: 102 = 0b1100110 (popcount 4) → 16 survivors `[0,2,4,6,32,34,36,38,64,66,68,70,96,98,100,102]`. All three independently land on 16, and 16+7=23 matches the clue arithmetic.

Result:
- CONFIRMED arithmetic: XOR-triangle → 16 survivors on 24/28/103 (Lucas theorem; the 24→16 and 28→16 matches are exact, not fitted).
- OPEN: the 16 survivors' combine function with the 7 passwords. All tested XOR/sum/hash/EC readings of the 16×16 submatrix and the 16-group XOR vs the oracle missed this session (0 hits).

Confidence: STRONGLY_SUPPORTED for the arithmetic alignment; OPEN for the final combine.

Reproducible script: `/tmp/xortri` XOR-triangle batteries.

## Discovery #42

Date: 2026-09-11

Artifact: `raw/web/live/puzzle/response.bin` (ART-001, sha `38125bbd...`, 1048x1556 RGBA — live re-fetch this session byte-identical, `Last-Modified: Sat, 15 Aug 2026 23:16:52 GMT`, `Cache-Control: no-store`); new tool `scripts/extract_grid.py`.

Observation: The 14x14 grid is IN the live capture and decodes from RAW PIXELS. The initial center-patch census in this entry was contaminated by bunny line-art; Discovery #52 replaces it with dominant exact-fill classification: K=86/W=86/B=15/Y=9 and leftover `0000`. The README matrix matches all 196 bits. The URL and B/Y frame remain byte-exact.

Experiment: `scripts/extract_grid.py` run on both live bytes and committed capture -> VERIFY PASS on both (counts/decode/frame all match).

Result:
- PROMOTED to PROVEN-from-pixels: grid location (origin, pitch, extent), reading convention, URL decode, and color frame. The BLOCKED leg (discovery #19 / open_solutions.md OPEN-2: "grid unlocatable", count err 144, template corr ~chance) is overturned — caused by searching the photo two-thirds and template-matching the bit pattern instead of contour-detecting the 75px color quads. The "75px overturn" previously flagged as artifact-less (#30) is now pixel-grounded.
- Caveat (superseded by #52): the center-sample K/W 87/85 and leftover `0100` were method artifacts. Dominant-fill extraction and the README agree at all 196 positions.
- OPENED: image branches B1-B4 (0x41D464, sums, merlons, off-white cell) are testable again with a grounded matrix — first time since the freeze.

Why it matters: Removes the longest-standing BLOCKED input (grid matrix) and replaces three agreeing secondary transcriptions with a primary-byte derivation. H-P1-001's required test (reconstruct from original image bytes without copied matrices) is now satisfied.

Confidence: STRONGLY_SUPPORTED (byte-identical live capture + deterministic pixel script + self-validating English decode + exact frame).

Reproducible script: `scripts/extract_grid.py /tmp/puzzle_live.bin` (also passes on the committed capture).

## Discovery #43

Date: 2026-09-11

Artifact: ART-001 bottom-left square, pixels (0,1289)-(231,1527) (~231x238px B/W only, zero blue/yellow).

Observation: The square is a QR code encoding `https://www.blockchain.com/btc/address/1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` (prize-address explorer link). OpenCV `detectAndDecode` returns '' on the tight crop (no quiet zone) — the cause of the 2026-09-04 "no decodable QR" verdict — and decodes byte-exact after a 30px white border (plus ECI warning, both scales agree; inverted variant negative as expected).

Result: CORRECTION of the 2026-09-04 forensic claim (timeline): a decodable QR DOES exist in puzzle.png; its payload is a public explorer link, not key material. No puzzle consequence beyond provenance hygiene.

Confidence: STRONGLY_SUPPORTED (two-scale agreement + expected negative control).

## Discovery #40

Date: 2026-09-11

Artifact: even256 object (Bifid even stream minus I/O, 256 chars over 23 letters, sha `1740b55b...`); TAIL570 (`sal_regions.json`); Chain-4 1151B plaintext (`/tmp/opencode/chain4_pt.bin`, sha `e4269ed5...`); exact offline oracle `X=f4d1bbd9...` + `a955...`/`4bc468...`/door (coincurve, comp+uncomp).

Observation: The even256 stream carries real sequential drift — early vs late halves differ beyond chance under two independent nulls — while its letter COUNTS match the TAIL-halves marginals exactly (no extra count structure). Row-homogeneity over the 16x16 layout: chi2 = 415.0 on df 330 (p~0.001 chi2-approx); 2000-permutation shuffle null gives P(>=obs) = 0.0005 (mean null 331.4, sd 23.0). Early (first 128) vs late (last 128) halves: chi2 = 40.6 on df 22, p~0.009 (S 21vs5, B 2vs10, D 11vs4, M 5vs13). TAIL early-j (first-half early + second-half early, 284 chars) vs late-j (286 chars): chi2 = 18.4 on df 8, p~0.018 (a 34vs20, b 16vs33, i 29vs46, h 35vs23). Mechanism check: early TAIL excess in a (col 3) + g (col 2) predicts early even excess in S = sq[3][2] (21vs5); late TAIL excess in b (col 1) predicts late even excess in B = sq[0][1] (10vs2) — drift propagates through the verified Bifid recoding (#31), so the even drift is inherited from TAIL order, not added by the cipher. Counts control: even letter counts vs halves-empirical expectation give chi2 = 19.6 on df 24, p~0.72 (null-consistent) — the structure is in ORDER, not in the bag-of-letters. No single outlier row (max-row shuffle null P~0.20 over 2000 perms) — drift is gradual halves-level, not a selector row.

Experiment (pre-registered splits only — 16x16 rows/cols, early/late halves, early-j/late-j; exact oracle for the prized battery): early/late halves x {SHA256, base-23} + early+late/late+early SHA256 = 6 candidates vs `X=f4d1...` + 3 targets -> 0 hits, best prefix 0.

Result:
- PROMOTED to SUPPORTED structural lead (new, positive): even256/TAIL sequential drift — the first order-level signal in the digit-stream family to survive its own shuffle null at p~0.0005 with a convergent halves split (p~0.009) and a TAIL-side source split (p~0.018).
- FALSIFIED for key use in tested form: early/late-half SHA/base-23 readings (6 candidates, 0 hits).
- BLOCKED forward: drift needs a TAIL sequential decoder with a STATED key (Phase-3.2 VIC-key reuse tested negative this round — see Dead End #28, not fished further); replication on an independent object is unavailable (LEAD91 too short for 16x16; 161 values exhausted as message per #32).

Why it matters: Reframes the digit-stream frontier from counts (exhausted: #26-#29, Dead Ends #7-#10) to ORDER. Every artifact-faithful count construction reproduces and misses uniformly; drift is the first order construction to beat chance with controls, and it names its source (TAIL early-j vs late-j in a/b/g/i/h). It does not yield the key — it bounds where a future stated sequential decoder must operate.

Confidence: STRONGLY_SUPPORTED for drift counts/nulls (mechanical + 2000-shuffle controls); SUPPORTED as structural lead (convergent splits, mechanism-checked); FALSIFIED for the 6-candidate halves-key battery.

Reproducible script: inline derivations (this session; chi2 + 2000-shuffle nulls + halves/early-j splits + 6-candidate coincurve oracle vs `X=f4d1...`).

## Discovery #41

Date: 2026-09-11

Artifact: on-chain funding/spending for `1GSMG1JC...` (126 txs) and `17ucy1K9...` (45 txs) via read-only Blockstream API; planted-address ledger `raw/github/floflo777-open-crypto-puzzles/1-big-prizes/gsmg-io-5btc-puzzle/data/planted-addresses.csv`; escrow tx `a82052a216cad8f57dee2a039c3b5cef9b5fcb2bc1c3bffa94d713cee0b30e2b` (discovery #24); Half `1JG648ya...` / Better `145ZQ9si...` (public privkeys from the Cosmic matrix step).

Observation: The 2026 Half/Better -> prize dust with puzzle-token OP_RETURNs is SOLVER timestamping with public keys, NOT author routing. Bursts at blocks 938165 (2026-02) and 944096 (2026-04): every token-bearing tx spends a public-privkey input — e.g. `3f0f28b973b1ee22` (Half 8124 sats -> 546 to `17ucy...` + OP_RETURN `bc1qks8zrshwmu3m8vgqdzwl2u8jjfgnvgjlezwqcd` + change), `a4355923d003bd70` (Better 7373 -> 546 to `17ucy...` + `hereismysecret`), `8fc3318401e9c728` (Half -> `ourfirsthintisyourlastcommand`), plus `matrixsumlistenterlastwordsbeforearchichoicethispassword` (56 chars = 4-token concat without the duplicate), `yourlastcommandsecondanswer`, `isolveditwithanabacus`, `leavethematrix`, and Matrix quotes on `1GSMG1JC...` (`here is no spoon`, `the answer is women`, `THEMATRIXHASYOU`, `SalPhaseIon`, all from Half/Better 546-sat dust, e.g. `0a756d0b9a...`, `a53663a6...`). The embedded `bc1qks8zrshwmu3m8vgqdzwl2u8jjfgnvgjlezwqcd` is a solver P2WPKH test wallet (witness program `b40e21c2...`, 14 fundings / 13 spends / 546-sat balance, same token-dust pattern at block 944090) — not a prize target. Known-privkey planted controls (`13HGhjkm...`, `148XH2...`) also dust `17ucy...` (2500 sats, block 946416). Author objects are cleanly separated: P-escrow neighbors (secret priv, #24), planted-2020 funding from vanity `3GSMG24...` P2SH (redeem `OP_0 <P2WPKH 2780438f...>`, e.g. `bd1b5d81b3...` block 622767 with `GSMG.io: are you sure?`), and the initial 5 BTC split (`2aa9a4a90be819d5` block 630001: 249815966 to `1GSMG1JC...` + 250000000 to `17ucy...`; `88cdb3cdca12b471` block 840725) — none carries token/quote OP_RETURNs.

Result:
- CONFIRMED with txids: 2026 token/quote dust = solver activity with public Half/Better/planted keys (secondary, EXCLUDED as puzzle inputs — same grade as `cosmic_A` folklore).
- FALSIFIED as author design: GreatResearch "Half sends dust to Target 2 as designed living-router infrastructure" (no author txid; all cited flows post-date public-key exposure by years; author funding shows no such pattern). E5 stays UNVERIFIED for author routing.
- PROMOTED to SUPPORTED guardrail: author-vs-solver on-chain separation — future on-chain work is bounded to author objects only (P-escrow, planted-2020, initial split). Solver messages (`abacus`, `hereismysecret`, `leavethematrix`, bc1 test wallet) must not seed key hypotheses.

Why it matters: Stops the search from fishing into solver-generated messages (which mimic puzzle vocabulary by construction) and certifies the only on-chain author vocabulary that survives (#24 EC ops + planted phase gates). It does not yield the key.

Confidence: STRONGLY_SUPPORTED (read-only tx/block/amount/input-address/OP_RETURN evidence, byte-exact witness-program decode, secret-vs-public privkey separation).

## Discovery #44

Date: 2026-09-14

Artifact: canonical `raw/github/puzzlehunt-gsmgio-5btc-puzzle/working/puzzle.png`
and the byte-identical Naddiseo copy; extractor `scripts/extract_grid.py`.

Observation: the first pixel extractor sampled each cell center. The bunny
line-art crosses the center of cell `(row 7, column 6)`, so that method called
one white background cell black. Reclassifying each 75x75 cell by the dominant
exact canonical fill (`K=(0,0,0)`, `W=(255,255,255)`,
`B=(63,72,204)`, `Y=(255,242,0)`) produces the stable matrix counts
`K=86, W=86, B=15, Y=9` on both canonical files. The down-first
counter-clockwise spiral still decodes byte-exactly to
`gsmg.io/theseedisplanted`, with the unused four bits `0000`; the 24-cell
spiral color frame remains `111101110011110110010010`.

The same pixels independently recover the image-branch B2 object in a second
ordering: row-major yellow cells are
`010000011101010001100100 = 0x41D464`; row-major blue cells are its bitwise
complement `0xBE2B9B`, so their XOR is exactly `0xFFFFFF`. This promotes the
previously secondary B2 claim to a primary-pixel fact. A bounded battery of
40 direct representations (raw/hex/decimal/bit strings and SHA/MD5 controls),
plus the finite prime-rank/color-mask extraction family (960 candidates), was
run against both 80-byte AES locks and the planted-address oracle: **0 exact
target or planted-address hits**. The B2 object is therefore confirmed as an
image invariant, but not yet a key.

Result:

- `PROVEN-from-pixels`: corrected cell classification, counts, URL, leftover,
  spiral color frame, and row-major `0x41D464` mask.
- `FALSIFIED`: the prior center-sample K/W count and `0100` leftover as image
  ground truth; they were a sampling artifact.
- `OPEN`: B3 (`490/497`) and B4 (merlon/indexed-string) semantics; neither has
  a reproducible key relation yet.
- `NO_MATCH`: all bounded B2/prime-mask candidates against both locks/door.

Reproducibility: both canonical PNG copies pass `scripts/extract_grid.py`;
the repository pytest collection still has the pre-existing unrelated import
failure in `tests/test_codex_accounts.py` (`scripts.codex_accounts` missing).

## Discovery #45

Date: 2026-09-14

Artifact: canonical SalPhaseIon region map `experiments/sal_final_search/sal_regions.json`,
the authenticated 765-character `LEAD91 + MID104 + TAIL570` stream, and the
primary pixel-derived grid from `scripts/extract_grid.py`.

Observation: the repeated “prime sieve” claim was checked as a content
transformation, not merely as a length coincidence. Removing prime-indexed
positions through 570 removes 104 characters and leaves 661 characters, but
neither 0-based nor 1-based indexing produces the canonical `LEAD91 +
TAIL570` bytes. The first mismatch is at output position 3 (0-based) and
position 1 (1-based). Thus `765 - pi(570) = 661` is real arithmetic, but the
claimed stream identity is false.

A second primary-artifact test treated `matrixsumlist` literally on the
corrected 14x14 grid: row/column binary sums, blue/yellow row/column sums,
prime-row/column zeroing, the frame `111101110011110110010010`, and the
row-major yellow mask `010000011101010001100100` (185 unique representations,
including reversals and SHA controls). The lock/door oracle produced 25
valid-padding events but zero target or planted-address matches, consistent
with padding chance; the direct matrix-sum family is not the final key.

Finally, clue-faithful interleavings of the seven visible tokens (canonical,
reverse, odd/even order, column/row reversals, and prime-position zeroing)
produced 48 unique objects. Both locks and the planted-door oracle yielded
zero exact matches. “Intertwined” is not supported as a simple character
weave or XOR substitute by this test.

Result:

- `CONFIRMED`: `765 - pi(570) = 661` is arithmetic only.
- `FALSIFIED`: the stronger claim that this sieve reconstructs the canonical
  661-character stream.
- `FALSIFIED`: direct grid matrix-sum / color-mask readings tested here as
  lock or door keys.
- `FALSIFIED`: bounded seven-token character-weave readings.
- `OPEN`: the author’s actual “reinserting the prime basics” operation; it
  needs a stated source/ordering rule rather than another free prime mask.

This is a useful boundary because issue #87 explicitly warns that prior LLM
analysis was “poisoned” by plausible but unverified claims. The prime-sieve
length coincidence must not be promoted to a route without byte-level
agreement.

## Discovery #46

Date: 2026-09-14

Artifact: the Bitcoin Genesis source-code literal embedded in the primary Phase-2
README (`0x736B6E...`), decoded exactly as the reversed Genesis coinbase headline.

Observation: the decoded source string is exactly 69 bytes and therefore an exact
`3 x 23` byte rectangle:

```text
The Times 03/Jan/2009 C
hancellor on brink of s
econd bailout for banks
```

This is an artifact-level dimensional match to the authenticated “over
twenty-three ciphers” wording, and is stronger than a bare length coincidence:
the source-code object itself, rather than a derived ciphertext, supplies the
23 columns. The prime-column projections were then tested at both 0- and
1-based conventions, both row/column orders, both orientations, and with the
prime columns kept or zeroed. Column XOR/sum/difference projections were also
included. Direct bytes, SHA-256, MD5-expanded values, and the resulting strings
were checked against both AES locks and the planted-address/target oracle.

Result:

- `CONFIRMED`: the source-code literal is byte-exactly 69 bytes = `3 x 23`.
- `SUPPORTED structural lead`: the 23-column geometry is compatible with the
  final clue and is now an explicit route node.
- `FALSIFIED as a key reading`: the bounded prime-column/row/column/hash battery
  produced 0 target-address and 0 planted-door hits (three chance-valid paddings;
  no address match).
- `OPEN`: what “reinserting the prime basics” does to this rectangle. No
  insertion order or cipher choice is assumed from the geometry alone.

Confidence: SUPPORTED for the byte/geometry fact; OPEN for mechanism.

Reproducible test: bounded inline source-rectangle battery run 2026-09-14;
oracle `experiments/sal_final_search/dual_oracle.py`.

## Discovery #47

Date: 2026-09-14

Artifact: newly captured May-2026 transactions linked from the prize address.

The target address history contains an unsaved witness transaction in block
949664: `973646bb3204b9e67e0fcb58efabe951aaf3714020c277f77092ae59bc1a1bd6`,
whose OP_RETURN says `GSMG WITNESS BLK 949653 TX 808f812f`. The referenced block
contains two unsaved 71-byte OP_RETURN payloads, labelled `GSMGJH` and `GSMGBH`.
Each payload is exactly a one-byte compact-ECDSA header (`0x20` or `0x1f`) plus
64 bytes with valid ECDSA `r` and `s` ranges. This is a substantially more
specific structural match than treating the bytes as arbitrary ciphertext.

The branch is not promoted to author evidence. Both records are chained through
the vanity wallet `1GSMG9VDLTU6jyuG7bkNMdmnHBLtbbM51M`, which was funded from a
burn-looking-address sweep and carries solver-style phrase OP_RETURNs. Candidate
message hashes tested so far do not recover either the target public key or the
vanity-wallet public key. The live question is what exact message/preimage the
two compact signatures sign, and whether `JH`/`BH` means a solver's “just
half/better half” proof attempt.

Result:

- `CONFIRMED`: the missing target witness and both referenced transactions are
  now saved with raw response hashes and provenance.
- `CONFIRMED`: the two binary payloads have compact-signature serialization.
- `SECONDARY`: the wallet lineage and phrase records identify solver activity.
- Negative check: 118,701 repository-text candidates plus transaction-field/raw-hex
  candidates were tested under raw/SHA-256/double-SHA-256/Bitcoin-Signed-Message
  hashing; none recovered the target, Half, Better, or vanity-wallet public key.
- `OPEN/PROMISING`: recover the signed-message convention and test whether the
  recovered keys encode a useful intermediate (not yet the prize key).

## Discovery #48

Date: 2026-09-14

Artifact: target-address OP_RETURN/output-value census.

The number 546 is genuinely dominant in the solver traffic: 81 target-address
transactions have OP_RETURN, 77 target outputs are 546 sats, and 70 transactions
have both. The exact `hereismysecret` records at the target all use 546 sats, and
the new witness transaction does too.

The provenance test changes the interpretation. Of the 70 OP_RETURN+546 pairs,
32 spend from the known Better wallet, 32 from the known Half wallet, 1 from the
new `1GSMG9...` solver wallet, and only five are isolated older test wallets.
Earlier non-burst records use many other amounts, including the original 2020
`Halving` output of 700 sats. Bitcoin Core documents 546 sats as the default
P2PKH dust threshold, so 546 is a natural repeated solver-token amount.

Result:

- `CONFIRMED`: 546 is the dominant amount in the later OP_RETURN dust protocol.
- `CONFIRMED`: `hereismysecret` is repeated with that protocol.
- `SUPPORTED`: solvers intentionally used 546 as a recognizable timestamp/token
  amount.
- `WEAK/OPEN`: 546 may echo a creator hint, but the amount is not author-specific
  and cannot yet be used as a numeric key without an independent bridge.

## Discovery #49

Date: 2026-09-14

Artifact: canonical TAIL570-derived `even256` plus the Genesis source-code
rectangle.

The surviving order branch was tested with a bounded, reproducible battery rather
than another direct frequency reduction. It covered adjacent/second differences,
run lengths, transition matrices, 16x16 routes, and a 3x23 Genesis route family
including row/column/snake/spiral paths, row permutations, cyclic column shifts,
Caesar variants, casing, reversal, and hashes.

Result:

- `CONFIRMED`: oracle selftest passed.
- `FALSIFIED` for the tested key readings: 820 unique candidates, 21
  chance-valid padding events, 0 target matches, 0 third-door matches.
- `NOT FOUND`: a privileged 16/23/7 sequence period. The strongest lag result
  (58) has shuffle p≈0.044 before the 64-lag multiplicity correction.
- `SUPPORTED`: the earlier halves/order drift remains a structural observation;
  it is not explained by a simple periodic or route transform here.
- `OPEN`: a sequential decoder still requires a stated key or cipher rule. The
  exact Genesis 3x23 geometry remains a clue, but the direct route family is now
  bounded and negative.

## Discovery #50

Date: 2026-09-14

Artifact: canonical `even256` (SHA-256
`1740b55ba5d224e86f61054bacd7caf90a8cf2c4418535c67d092903c4509f35`).

The previously unfinished frequency/string branch was independently rebuilt and
run through the self-testing dual-lock and third-door oracle. It included count
vectors in decimal/hex/byte forms, frequency-ranked alphabets, stable tie rules,
rank streams, every observed count-boundary selection/complement, count-modular
and XOR streams, reversals, and SHA-256/MD5 forms.

Result: 604 unique candidates, 8 chance-valid padding events, 0 target matches,
and 0 third-door matches. The branch is now `FALSIFIED` for these stated
frequency constructions. This reinforces Discovery #40: the surviving signal is
order-level, not a frequency-derived key.

## Discovery #51 — RETRACTED (bad comparison fixture)

Date: 2026-09-14

Artifact: canonical `puzzle.png` (SHA-256 `38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830c`).

The five-cell discrepancy was caused by a bad temporary comparison literal in the
new battery, not by the README or the canonical image. Center sampling also
misclassified one bunny-overlaid cell. The result is superseded and must not be
used as evidence.

## Discovery #52

Date: 2026-09-14

Artifact: canonical `puzzle.png`, its README matrix, and the corrected
`experiments/next_stage/grid_instruction_battery.py`.

Dominant exact-fill extraction matches the README matrix at all 196 positions.
The stable primary result is `K=86/W=86/B=15/Y=9`, leftover `0000`, URL
`gsmg.io/theseedisplanted`, and B/Y frame
`111101110011110110010010`. The rerun of the explicit image instruction family
covered 797 deduplicated candidates and produced 22 chance-valid paddings, zero
target matches, and zero third-door matches.

This restores the K/W balance as confirmed structural evidence, while closing the
five-cell/87-85/0100 route as an analysis-fixture error. The image branch remains
negative for the tested direct matrix-sum/prime-zero/yin-yang readings.

## Discovery #53

Date: 2026-09-14

Artifact: Genesis source literal, exact 3×23 arrangement, B/Y frame, and
`experiments/next_stage/genesis_matrixsum_battery.py`.

The clue-faithful `matrixsumlist` continuation was tested on the Genesis object:
ASCII and A1Z26 row/column sums, prime-column zeroing, all 24 repeated
permutations of `{2,3,5,7}` at the 1-based prime columns, eight repeated B/Y
mask offsets, and the secondary reported `490/497` pair in both orders. The
pair also occurs naturally in one prime-basic ASCII column-pair-sum reading,
but that does not make it a key.

Result: 4,210 candidates, 114 chance-valid paddings, zero target matches, and
zero third-door matches. The direct Genesis matrix-sum family is closed; the
remaining live branch is the semantic interpretation of `enter`, `thispassword`,
`yourlastcommand`, and `secondanswer`.
## Discovery #54

Date: 2026-09-14

Artifact: canonical `TAIL570`, `LEAD91`, and the reproducible full-period 5×5
`DBIFHCEGA` Bifid decode.

The Bifid decode is a genuine waypoint: it begins `BTCSEED`, has one `Z` at
position 97, and produces the canonical 285/285 split. The focused continuation
that follows the stated clue order—prime/zero, then `matrixsumlist` on the
natural 7×13 and 19×30 matrices—was tested including the untested 20+49=69
composite form.

Result: 640 candidates, 18 padding-only events, zero target matches, zero
third-door matches. The direct continuation is closed, but `BTCSEED`, the Bifid
decode, and the 69=3×23 geometry remain confirmed structural facts.

## Discovery #55

Date: 2026-09-14

Artifact: canonical `even256` and its aligned B/C/D/E yin half.

After dropping the 29 I/O symbols from the diverse 285 stream, the same
positions in the locked half form a 256-symbol four-state selector. This gives
a reproducible yin/yang alignment and explains why the 256 object should be
kept as ordered data rather than frequency data.

The complete bounded selector family tested 304 stable routes/encodings: six
chance-valid paddings, zero target matches, zero third-door matches. The
alignment is `CONFIRMED` as structure; its tested key readings are `FALSIFIED`.

## Discovery #56

Date: 2026-09-14

Artifact: the 256-position aligned B/C/D/E selector and canonical even256
payload, with the exact dual-lock and third-door oracle.

The suggested prime-basics interpretation was tested directly: all 24 mappings
of B/C/D/E to 2,3,5,7 were combined with rank-0/rank-1 payloads, six natural
arithmetic operations, modular/raw forms, reversals, transparent encodings,
16×16 summaries, and a prime-only control stream.

Result: 24,432 unique candidates, 745 padding-only events, zero target
matches, and zero third-door matches. This closes the numeric B/C/D/E →
2/3/5/7 interpretation tested here. The 256 alignment remains a confirmed
structural waypoint, not a recovered key rule.

## Discovery #57

Date: 2026-09-14

Artifact: canonical `puzzle.png`, extracted by `scripts/extract_grid.py`.

The previously noted image pattern resolves to two contiguous southeast
components of lengths 6 and 5, not to the incomplete full diagonal lines:
`BYYBYB` and `YYYYB`. This is a cleaner reproduction of the surviving P2-08
image lead.

The direct color/bit interpretation was tested in both orders and polarities,
with forward/reverse, separate/concatenated, decimal/hex/ASCII and SHA-256
forms. The natural frame follow-up—selecting the corresponding URL characters
for those cells—was tested too. The exact oracle battery covered 202 unique
candidates: five padding-only events, zero target matches, and zero third-door
matches.

Thus the 6+5 geometry is confirmed, but it does not yet identify the prize
key. Its direct readings are closed pending a new operation clue.

## Discovery #58

Date: 2026-09-14

The refreshed target-address capture contains a newer confirmed transaction:
`a751791bf7125e2ba94fd451900391a1cd3a50f01e09ec461450ac0de1d1945e` at block
964501. It pays 864 sats to the prize address and 546 sats to the halving
split-off, but contains no OP_RETURN. Its input is a solver fan-out wallet
funded by a 600-sat distribution; the change is later redistributed into the
same test cluster. This separates the new amount pair from creator evidence.

The saved OP_RETURN frontier remains the previously recorded
`GSMG WITNESS BLK 949653 TX 808f812f` at block 949664. No newer target-address
OP_RETURN was found.

## Discovery #59

Date: 2026-09-15

Artifact: the two original public image attachments from Issue #67, preserved
under `raw/github/puzzlehunt-gsmgio-5btc-puzzle/issues/67/attachments/`.

The previously referenced “merlon in QR code” material was missing from the
local evidence set. The issue's attachment URLs were recovered and saved with
provenance. The colour rendering contains a deterministic 560×560 crop at
`(118,118)`, exactly fourteen 40px modules per side. Dominant-fill extraction
gives a 14×14 `R/W/K` object with counts `R=72`, `W=60`, `K=64`; the central K
region is an 8×8 chamber.

Result: this is a new, byte-hashed secondary research object, not a replacement
for the canonical `puzzle.png` grid. Direct symbol routes, masks, ternary
assignments, perimeter readings, row/column counts, and packed-bit forms were
run through the self-tested dual-lock/third-door oracle: 300 candidates, 30
padding-only events, zero exact target matches, zero third-door matches, and
zero direct SHA-256-to-target matches.

Status: attachment and crop `CONFIRMED`; direct merlon encodings `FALSIFIED` as
key/door readings; full QR payload `BLOCKED` because the original screenshot is
clipped at its lower edge.

## Discovery #60

Date: 2026-09-15

Artifact: decoded 2026-01-01 and 2026-07-12 hint wording plus the visible
SalPhaseIon tokens.

The bounded semantic branch tested 3,724 exact phrase normalizations and
explicitly motivated context combinations. It produced 105 valid-padding
accidents, zero AES-lock hits, zero third-door hits, and zero direct target
hits when each candidate was hashed with SHA-256 as a private-key candidate.

Status: this explicit phrase family is `FALSIFIED`; the broader “friend-context”
interpretation remains an unspecific hypothesis rather than a candidate.

## Discovery #61

Date: 2026-09-15

Artifact: the independently reproduced community 68-byte branch interpreted
as four 16-byte GF(256) interpolation values plus four x-coordinates.

The finite extension was run at the natural triangle level 3, where the
seven-point XOR triangle becomes a 4×16 byte matrix. It covered all 30
irreducible degree-8 fields for the reported order, all 2,520 AES-field
orders, eight row/column serializations, reversals, row/column XOR and
byte-sum list constructions, and SHA-256/double-SHA-256 finalization.

Total: 224,312 exact hash/address checks. There were zero target matches and
zero planted-door matches. Two candidates shared two leading hash160 bytes
with the target: the already reported AES/raw/double-SHA result
`a955a042…`, and a separate matrix-sum result `a955bfa2…`; neither extends
to a third byte.

Status: the natural 4×16 matrix family is `FALSIFIED` as a key derivation.
The near-match is reproducible but not author-confirmed and is not promoted
to a discovery of the puzzle mechanism. The exact finite boundary is saved
in `experiments/next_stage/gf256_matrix_probe_report.json`.

## Discovery #62

Date: 2026-09-15

Artifact: `raw/github/Naddiseo-gsmgio-5btc-puzzle/working/hints/2023-02-23.png`,
the author's 161-token binary hint image.

All 161 eight-bit tokens were recovered directly from the image. The bytes
have SHA-256 `ca3d8ab58d893c9a3b955adbdb4f6bf812dd86941401f2d583729e1c1e16c5f5`
and every byte ends in `110`. Bit-reversal within each byte followed by
reverse token order reproduces the complete author message, including the
`yellow blue primes matrixsumlist lastwordsbeforearchichoice yinyang` lead.

The upper five bits now make the previously blocked `7×23` numerical object
explicit. A finite test of its row/column routes, prime-row/column zeroing,
`{2,3,5,7}` reinsertion permutations, matrix-sum lists, and transparent
encodings produced 2,337 candidates / 4,674 target checks, with no exact
target match.

Status: source bytes and 7×23 geometry `CONFIRMED`; tested direct reductions
`FALSIFIED`; the 23/16/7 operation remains the strongest structured lead.

## Discovery #63

Date: 2026-09-15

Artifact: the Phase-3 notebook's explicit instruction to put `giveit` in front
of an answer, together with the exact visible text and final hint phrases in
the canonical puzzle image/page.

The historical convention has a known-answer witness: the saved Phase-3
answer `jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple`
re-derives planted address `1K23RS1y2fnuZRkhw5nUpFr5Jk5WN11Zeq` under
SHA-256. I therefore tested the same prefix operation, with only exact,
lowercase, compact, and spaced forms, on 21 literal final objects and both
`giveit` / `give it` prefix spellings.

The probe covered 252 deduplicated candidates. It produced twelve valid-padding
accidents, zero AES-lock hits, zero third-door hits, and zero direct SHA-256
target-address hits.

Status: the `giveit` prefix rule is `CONFIRMED` as a historical author
convention, but this direct transfer to visible final objects is `FALSIFIED`.
It remains a useful grammar clue, not the final key.

## Discovery #64

Date: 2026-09-15

Artifact: the confirmed `esrever` convention, applied to the Bifid-derived
objects rather than to the already-solved URL witness.

Method: whole-bitstream reversal, per-byte bit reversal, identity/duplicate
controls, and 32-byte aligned windows were applied to the full 570-symbol
Bifid output, the 285-symbol halves, and the 256-symbol I/O-filtered object.
Raw bytes, SHA-256, hexadecimal, Base64, and digest encodings were checked
against both AES locks and the planted third-door oracle.

Result: 180 exact records, zero lock hits, zero third-door hits. The known
`esrever` operation remains confirmed for the URL witness, but its direct
transfer to these objects is falsified.

Report: `experiments/next_stage/esrever_binary_probe_report.json`; runner:
`experiments/next_stage/esrever_binary_probe.py`.

## Discovery #65

Date: 2026-09-15

Artifact: the source-order 16-item / seven-token interpretation of the final
instruction. The Genesis item was tested as the literal hex, the exact decoded
published bytes (including `CHancellor`), and the conventional headline
spelling.

Method: concatenation, spacing, character/item reversal, odd/even item
selection, SHA-256 forms, and XOR-of-digest forms were sent through the exact
two-lock and third-door oracles.

Result: 115 candidates, zero lock hits, zero third-door hits. This bounded
“intertwined password” synthesis is falsified; the seven-token chain already
verified for earlier locks is not evidence that the same forms produce the
prize key.

Report: `experiments/next_stage/full_password_synthesis_probe_report.json`; runner:
`experiments/next_stage/full_password_synthesis_probe.py`.

## Discovery #66

Date: 2026-09-15

Artifact: the literal `reinsert the prime basics` reading applied to the
69-byte Genesis source at 1-based positions 2, 3, 5, and 7.

Method: all 24 permutations of `2357` were tested as replacements and as
before/after insertions. Direct, reversed, MD5, and SHA-256-rendered forms
were checked against both locks and the planted door.

Result: 864 candidates, zero lock hits, zero third-door hits. This exact
source-position interpretation is falsified; the wording still lacks a
confirmed operation.

Report: `experiments/next_stage/prime_basic_position_probe_report.json`; runner:
`experiments/next_stage/prime_basic_position_probe.py`.

## Discovery #67

Date: 2026-09-15

Artifact: `LEAD91`, whose length is exactly the triangular number
`1+2+...+13=91`.

Method: the stream was arranged as a 13-row triangular matrix, left- and
right-aligned in a 13×13 zero-padded square, under both published digit maps.
Both orientations, prime-value and prime-position zeroing, row/column sums,
reversals, transparent encodings, and SHA-256 forms were checked.

Result: 2,880 exact candidates, zero lock hits, zero third-door hits. The
triangular geometry is confirmed, but this literal matrix-sum family is
falsified as the final key route.

Report: `experiments/next_stage/lead_triangle_matrix_probe_report.json`; runner:
`experiments/next_stage/lead_triangle_matrix_probe.py`.

## Discovery #68

Date: 2026-09-15

Artifact: the triangular `LEAD91` object and the confirmed `LEAD`/`TAIL`
ordering of the SalPhaseIon streams.

Method: triangular row and column sums under both digit maps, orientation and
prime-zero variants were used as direct 0- or 1-based selectors into raw
`TAIL570`, the complete Bifid output, and the confirmed `even256` object.
Non-cumulative and cumulative modulo-index forms were checked, with direct,
reversed, and SHA-256 candidate renderings.

Result: 1,728 candidates, zero lock hits, zero third-door hits. The natural
triangular `LEAD -> TAIL` selector rescue is falsified; the stream ordering
remains confirmed, but its author-specific operation is still unknown.

Report: `experiments/next_stage/lead_triangle_tail_selector_probe_report.json`;
runner: `experiments/next_stage/lead_triangle_tail_selector_probe.py`.
