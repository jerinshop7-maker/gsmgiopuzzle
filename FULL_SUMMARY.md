# GSMG 5 BTC Puzzle — Full Root Markdown Summary

## Scope

This summary consolidates only these eight root Markdown files:

- `README.md`
- `FINAL_SOLUTION.md`
- `evidence.md`
- `discoveries.md`
- `dead_ends.md`
- `hypothesis_tree.md`
- `timeline.md`
- `artifact_inventory.md`

Nested Markdown files under `raw/`, `experiments/`, `.commandcode/`, and other directories are intentionally excluded.

## Executive Status

**The puzzle is NOT SOLVED.** No private key or prize mechanism has been independently established for either funded target address.

The investigation is an evidence-first forensic analysis of the GSMG.IO Bitcoin puzzle. It preserves raw captures, records provenance and hashes, reproduces public transformations, tests competing hypotheses, and refuses to treat readable text, valid hashes, valid WIFs, successful padding, or matching lengths as proof of the intended solution.

The strongest remaining lead is the complete interpretation of the two SalPhaseIon digit streams. An official 2023 hint, decoded by reversing bits within each byte and reversing token order, names:

```text
yellow blue primes matrixsumlist lastwordsbeforearchichoice yinyang
we wont give away the password its in front of your eyes but youre not seeing it
very last step is a true giveaway promised
```

The local transcription is near-exact but has an OCR-level character discrepancy around `choice`/`choise`; the compact reconstruction omits spaces by design.

On 2026-09-04 the investigation froze `CHECKPOINT-2026-09-04-SALFINAL` (`experiments/sal_final_search/`): the live SalPhaseIon textarea is byte-identical to the canonical repository copy (2149 bytes, 1075 tokens), the small-blob assembly was corrected to A+z+B (128 Base64 chars → 96 bytes, salt `3ab585348552415d`, block-aligned), and Half/Better Half, the 103×103 reading, the 1327-byte plaintext, the Issue #108 correction, and all claimed keys were excluded as inputs. A self-tested dual-lock + third-door harness plus ~3,700 structural candidates and ~6,300 offline decrypts have produced zero prize hits since (see `REPORT.md`, discoveries #12–#21).

## Investigation Principles

The root documentation establishes these rules:

- Raw artifacts are immutable and must be preserved byte-for-byte.
- Direct captures outrank transcriptions, solver writeups, and issue claims.
- Derived transformations belong under `derived/` or `experiments/`.
- Every important transformation should identify its input, parameters, outputs, hashes, and tool information.
- Observed facts must be separated from inferences, hypotheses, speculation, and public claims.
- Hypotheses must have explicit statuses and falsification criteria.
- Corrections must be appended rather than silently replacing earlier claims.
- External investigation is read-only: no forms, transactions, signatures, or candidate secrets are submitted or broadcast.
- A successful decryption or valid cryptographic object is not enough; the result must connect reproducibly to the actual target mechanism or address.

## Repository Layout and Tooling

The project is organized into:

- `raw/web/` — live and archived HTTP captures.
- `raw/github/` — preserved repositories and issue material.
- `derived/transcriptions/` — byte- and code-point-preserving analysis.
- `derived/crypto/` — cryptographic outputs and controls.
- `derived/bitcoin/` — offline Bitcoin verification and cached public chain data.
- `scripts/` — deterministic intake, hashing, transcription, reproduction, cryptographic, Bitcoin, and integrity tools.
- `experiments/` — experiment-specific reports and outputs.

The documented workflow includes web/GitHub intake, artifact hashing, inventory generation, SalPhaseIon transcription, public-claim reproduction, cryptographic controls, Bitcoin verification, repository integrity checks, and pytest.

## Evidence Inventory

The evidence ledger records four primary web artifacts:

1. `ART-001` — `https://gsmg.io/puzzle`
   - Stored as `raw/web/live/puzzle/response.bin`.
   - PNG, 29,931 bytes.
   - SHA-256: `38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830`.
   - Contains the starting image/grid and prize address.

2. `ART-002` — `https://gsmg.io/theseedisplanted`
   - Stored as `raw/web/live/theseedisplanted/response.bin`.
   - HTML, 832 bytes.
   - SHA-256: `7cb766d406008a397f8ae32b3a38ca68b42724bb07b3481deb84baad5c725183`.
   - References the image assets and hidden password form.

3. `ART-003` — the long Phase 2 route
   - Stored as `raw/web/live/phase2/response.bin`.
   - HTML, 9,207 bytes.
   - SHA-256: `06fbd4461ab20d45c54a7053c7c0cfa256ba82a5ad4c73a47fac67f3f1cdf7d9`.
   - Contains Phase 2 and Phase 3 encrypted materials.

4. `ART-004` — the SalPhaseIon hash route
   - Stored as `raw/web/live/salphaseion/response.bin`.
   - HTML, 4,536 bytes.
   - SHA-256: `a83d3de7810f26b19b4965339b76d403e44f6b6877e5d7de2555480ca1779d77`.
   - Contains the SalPhaseIon and Cosmic Duality textareas.

The artifact inventory reports **115 stable raw artifacts** (106 originals plus 9 hashed files from the 09-04 floflo777 snapshot; docs/metadata unhashed by design). It includes captured images, notebooks, text files, encrypted blobs, cloned repository contents, and live web responses. The inventory records SHA-256 hashes and sizes for each artifact. The raw capture policy prohibits editing, normalizing, repairing, transcoding, or renaming captured content in place.

On 2026-09-04 a machine-readable region map (`experiments/sal_final_search/sal_regions.json`) fixed the exact SalPhaseIon segmentation (LEAD91, MID104, TAIL570, R1_63, R2_29, R3ENG35, R3B64A_63, blob-`z`, R4A40, R4B64B_64, R4C12; see SalPhaseIon Findings). Two same-shape locks are now tracked: the SalPhaseIon small blob (salt `3ab585348552415d`) and the phase-3.2 tail blob (salt `b45a5e3d827593ca`), each 128 Base64 chars → 96 bytes → 80 ciphertext bytes. The creator's planted-address set (8 verified preimages plus the open third door `1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9`) was imported from the independent floflo777 research as corroboration-only material; its sweep counts remain secondary until rerun here.

## Reconstructed Puzzle Path

### Phase 0 — Starting Bunny Image

The puzzle image is a 14×14 binary/color grid. The documented mapping is:

- Black and blue squares = `1`.
- White and yellow squares = `0`.
- Read from the upper-left square using a down-first, counterclockwise inward spiral.
- Group bits into eight-bit ASCII characters.

The result is:

```text
gsmg.io/theseedisplanted
```

The local color-frame check independently reproduces this output from the image. Exact dominant-color counts are:

- Black: 86
- White: 86
- Blue: 15
- Yellow: 9

The 24 colored squares occur at zero-based spiral positions 7, 15, 23, through 191. These are the final bit positions of the first 24 decoded bytes. Blue/yellow values reproduce the low-bit pattern of the decoded URL, showing that the colored cells form an intentional frame around the binary reading convention.

### Phase 1 — The Warning

The image fragments on `theseedisplanted` refer to Logic's song “The Warning.” Rearranging the image names produces “war” + “ning” and “LO” + “crypto” + “gic,” pointing to the song and to the following lyric:

```text
The flower blossoms through what seems to be a concrete surface
```

The password is the lowercase, spaceless form:

```text
theflowerblossomsthroughwhatseemstobeaconcretesurface
```

Submitting that password reaches the long Phase 2 route.

### Phase 2 — Mr. Robot / Matrix

The Phase 2 page references *The Matrix Reloaded*. The central password clue is “causality.” The SHA-256 digest is:

```text
eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf
```

The documented decryption is OpenSSL AES-256-CBC using the Base64 blob and that digest as password input. The local reproduction obtains readable plaintext beginning with the “ironic name of the keymakers” text and multiple riddles.

The seven Phase 2 answer components are documented as:

1. `causality`
2. `Safenet`
3. `Luna`
4. `HSM`
5. `11110`
6. A Genesis Block/source-code hexadecimal string beginning `0x736B6E...`
7. A chess-position string ending in `b - - 0 1`

The exact case and whitespace rules are part of the construction. The concatenated seven-part answer hashes to:

```text
1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5
```

That digest opens the next Phase 3 material.

### Phase 3 — Free Will

The Phase 3 riddles identify:

- Jacque Fresco and The Venus Project.
- Alice in Wonderland's “How long is forever?” — answered by “just one second.”
- The Heisenberg Uncertainty Principle.

The documented answer string is:

```text
jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple
```

Its SHA-256 digest is used for the next AES-256-CBC decryption.

### Phase 3.2 — EBCDIC, Beaufort, and VIC

The first Phase 3.2 blob is interpreted using IBM EBCDIC 1141, suggested by “One for one, four for one.” The resulting text is processed with the Beaufort cipher, suggested by “beautiful strategic position.” The key is:

```text
thematrixhasyou
```

The plaintext contains a long Architect monologue, a 149-digit string, a chessboard-style clue, and another encrypted blob.

The 149-digit string is solved with a VIC/straddling-checkerboard approach. The phrase “one for one, four for one” supplies the numerical clues 1 and 4. The alphabet is derived from the unusual phrase involving `fubcd`, `oracle`, `thingky`, and `mvps`, with a punctuation replacement and missing alphabet characters added.

The result is a message whose essential content is:

```text
IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE
```

The root files treat this as an important clue, but not as proof of a specific private-key derivation.

### Decentraland and the SalPhaseIon Route

The Decentraland hint at coordinates `-41,-17` leads to an audio file. The documented audio operation is:

1. Split the stereo channels.
2. Invert one channel.
3. Mix the channels back together.
4. Downmix to mono and inspect the spectrogram.

The recovered message is:

```text
HASHTHETEXT
```

This directs the solver back to the original image. Hashing the image's textual content, including the prize address, gives:

```text
SHA256(GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe)
= 89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32
```

That digest forms the SalPhaseIon route.

## SalPhaseIon Findings

The exact live textarea is byte-identical to the canonical `jackdevs66` repository copy (2149 bytes, SHA-256 `d39d10b1...3330c`; 1075 single-char tokens, compact SHA-256 `26e37652...78e6156`). The frozen 2026-09-04 region map gives:

| Region | Tokens | Len | Alphabet | Decode |
|---|---|---|---|---|
| LEAD91 | 0:91 | 91 | a–i | unsolved digit stream |
| MID104 | 91:195 | 104 | a/b | `matrixsumlist` |
| TAIL570 | 195:765 | 570 | a–i | unsolved digit stream |
| z@765 | sep | 1 | z | separator |
| R1_63 | 766:829 | 63 | a–o | bigint-hex → `lastwordsbeforearchichoice` |
| z@829 | sep | 1 | z | separator |
| R2_29 | 830:859 | 29 | a–o | bigint-hex → `thispassword` |
| z@859 | sep | 1 | z | separator |
| R3ENG35 | 860:895 | 35 | English | `shabef\|ourfirsthintis\|yourlastcommand` |
| R3B64A_63 | 895:958 | 63 | Base64 | fragment A |
| z@958 | data | 1 | z | **blob data, not a separator** |
| R4A40 | 959:999 | 40 | a/b | `enter` (encoded line break) |
| R4B64B_64 | 999:1063 | 64 | Base64 | fragment B |
| R4C12 | 1063:1075 | 12 | English | `shabef\|anstoo` |

Notes:

- The compact text length and region boundaries differ from several public claims; the old "91/103/570" framing is superseded by the table above.
- `shabef` is interpreted as a SHA-256-convention clue (`sha bef…`, restating password = SHA-256 of the answer); the seventh public token `secondanswer` is interpretive (from `shabefanstoo`'s `ans too`), not a direct byte decode — five tokens decode deterministically, with `matrixsumlist` occurring twice (positions 1 and 5).
- LEAD91 is triangular (91 = T13 = 7×13); TAIL570 factors include 19×30, 15×38, 10×57; issue #106 supplies a second digit convention for these streams via Bifid square rows (d=0,b=1,i=2,f=3,h=4,c=5,e=6,g=7,a=8), tested alongside legacy a=1 in the 09-04 sweeps.

The seven public token values are therefore:

```text
matrixsumlist
enter
lastwordsbeforearchichoice
thispassword
matrixsumlist
yourlastcommand
secondanswer
```

The page carries two Base64 fragments: fragment A (63 chars, `U2FsdGVkX18…`, OpenSSL `Salted__` header) and fragment B (64 chars, `QvX0t8v3…`, mid-blob chunk with no header). **The correct assembly is A+z+B** (63+1+64 = 128 chars → 96 bytes: `Salted__` + salt `3ab585348552415d` + 80 ciphertext bytes, block-aligned; the 40-char `enter` is the page's 64-column line break between the two 64-char lines). The old A+B concatenation (127 chars → padding error / 79 non-aligned bytes) is the wrong assembly and must not be used.

## Cosmic Duality Status

The canonical secondary repository documents this chain:

1. SHA-256 each of seven SalPhaseIon tokens.
2. XOR the seven 32-byte digests.
3. Use the resulting raw 32-byte value as an EVP_BytesToKey/MD5 password for AES-256-CBC.
4. Obtain a 1327-byte output.
5. Interpret 10,609 bits as a 103×103 matrix with seven remaining bits.
6. Compute row/column-derived values and decode a base-38 number.

The locally reproduced output has the advertised SHA-256:

```text
4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081
```

The matrix/base-38 interpretation yields values labelled `Half`, `Better Half`, and a four-byte trailing value. The reported candidate values include:

```text
Half:        0423d9115a1dc756d5d08d2de880ab508bd4745fc97709f4fcb513f2cb8fcc35
Better Half: 48cc46e66bdd36b09ae344552f606a761f9d90681f20dfefe2b43db18b623971
Trail:       fc0c1b02
```

However, the root evidence does not accept this as the intended final solution. The derived P2PKH addresses do not equal either funded target address. The output is high entropy, and the advertised hash is self-referential: it proves only that the same bytes were obtained, not that the bytes are the intended plaintext or prize key. Issue #106 retracts the final-key interpretation and reports that broader sweeps found no target match, but the full sweep scripts and witnesses are not locally present.

Therefore the status is:

- Public byte transformation: reproducible.
- Intended Cosmic plaintext: unresolved.
- Matrix-derived Half/Better Half as prize keys: falsified.
- Complete puzzle solution: not solved.

Per `CHECKPOINT-2026-09-04-SALFINAL` the Cosmic chain is excluded as an input to new branches (two of its seven tokens are interpretive rather than decoded, and its KDF convention is foreign to the puzzle's stated SHA-256 convention). Independent analysis further argues the 1327-byte output is a ~1/256 PKCS#7 padding accident (local spot-checks reproduce chance-rate valid paddings with no address match); that analysis is recorded as corroboration, not as a locally proven sweep. The large second-blob object itself (live textarea_1: 1792 chars → 1344 bytes, `Salted__` header, h1 `Cosmic Duality`) remains a closed, unopened object. Note: no `Dualite` string exists anywhere in the captured markup, so "Dualite" is used here only as a nickname for that second blob, not as a page-given title.

## Bitcoin Targets and Verification

The investigation treats two addresses as relevant targets:

### Original prize address

```text
1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
```

Recorded chain state:

- Funded total: 875,988,872 satoshis.
- Spent total: 750,353,498 satoshis.
- Remaining: approximately 125,635,374 satoshis, or 1.256 BTC.
- Hash160: `a9553269572a317e39f0f518cb87c1a0ee1dbae4`.

### Halving destination

```text
17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa
```

Recorded chain state:

- Funded total: 375,055,856 satoshis.
- Spent total: 0.
- Remaining: approximately 3.7505 BTC.
- Hash160: `4bc468447fe1b048ad030a2f9a125478eabc4ed6`.

The second address received the halving transfers. No published evidence proves that it is a solver payout address, but it remains a target candidate because the puzzle's initial funds were split between the two addresses.

The offline Bitcoin verifier derives compressed and uncompressed public keys, HASH160 values, Base58Check addresses, and WIF data. A candidate is accepted only if its derived address exactly equals a target address. Valid secp256k1 scalars, readable outputs, successful padding, or similar addresses are insufficient.

The documented matrix-derived candidates produce addresses such as:

```text
Half:        1JG648yaB7Wp2dpUfcZoRSD4q35oq47vCu
Better Half: 145ZQ9siLrsXBKf465wjdyQYAP5dRwhRhQ
```

They do not equal either funded target.

## Disputed Small-Blob Correction

Issue #108 claims that two characters in the small SalPhaseIon blob should be changed:

- Position 18: `R` → `J`.
- Position 51: `k` → `s`.

The root evidence ledger directly compares this claim with the captured data and finds:

- The first captured fragment already has `J` at index 18.
- The first captured fragment already has `s` at index 51.
- The proposed changes are therefore a no-op on the captured artifact.

The 2026-09-04 correction supersedes the old block-alignment framing: the A+B concatenation (127 Base64 chars → padding error / 79 non-aligned bytes) is the **wrong assembly**. The correct assembly is **A+z+B** (the `z` at token 958 is blob data): 128 chars → 96 bytes (`Salted__` + salt `3ab585348552415d` + 80 ciphertext bytes), AES-CBC block-aligned and ranked VALID_CIPHERTEXT locally. The blob is therefore a well-formed unopened lock, not a malformed one — but it remains unopened: 09-04 sweeps (matrix-sum families, last-words non-literals, prime-masked digit strings; both locks × 2 password forms × 2 KDFs) yield chance-rate paddings only, with zero address matches.

The claimed 79-byte plaintext containing `K_C1`, `K_C2`, and `E_C` has not been reproduced from the captured bytes under either assembly. The raw artifact was not changed. The issue claim is recorded as unverified and contested.

## Official Hint Constraints

The root discovery and evidence ledgers record these official or author-attributed constraints:

- Primes `2,3,5,7` are important.
- Some characters must be “zeroed out.”
- The solver is at the “prime part.”
- Reaching a “ying yang” supposedly allows the puzzle to be solved the same day.
- The password is “in front of your eyes” in the 2023 bit-reversed message.
- The 2020 halving moved half of the prize to `17ucy1K9...`.
- A second door is repeatedly mentioned.

These clues point toward an unresolved operation involving the SalPhaseIon streams, prime selection, zeroing, and some form of yin-yang or complementary structure.

2026-09-04 testing status for each clue:

- **Primes/zeroing**: finite enumeration (P2357/Pfull × idx0/idx1 × normal/reversed × keep/zero) over all eight SalPhaseIon streams plus prime-VALUE filtering (digit ∈ {2,3,5,7}) under both bifid9 and a1 mappings — no prize hit; R/C prime masks (`Rpm=00010010001010`, `Cpm=00000110110000`, XOR/XNOR) preserved as threshold leads.
- **matrixsumlist**: literal sweep (765 sum-list passwords → 6120 decrypts → 17 chance-rate paddings → 0 matches); 14×14 grid sums externally reported swept (secondary).
- **yinyang**: complementary transforms (mirrors, rot180, transpose, complement) + pair-sum constancy + prime-mask XOR/XNOR enumerated (1231 partial-structural leads, none promoted).
- **lastwordsbeforearchichoice**: literal word-window reading externally reported closed (secondary); local non-literal family (initials, hashes, prime-rank, reversals) vs both locks + third door — 0 hits. Chronology fixed: Architect monologue → 149-digit string → checkerboard riddle → p32 blob.
- **Bifid digit mechanism**: ~120 combos (3×3/5×5/6×6 squares, five keywords, five periods, both directions) never yield BTCSEED or the 285→256 reduction (kept 228–280) — the byte-exact claim is unreproducible in the tested space.

## Hypothesis Tree Summary

The root hypothesis tree uses explicit statuses:

- `H0 — GSMG 5 BTC puzzle`: `TESTING`.
- `H-PROV-001 — Captured live route is primary`: `UNTESTED`; exact captures exist, but historical-change comparison remains incomplete.
- `H-P1-001 — Down-first counterclockwise spiral`: `STRONGLY_SUPPORTED`.
- `H-SAL-001 — SalPhaseIon regions encode deterministic data`: `TESTING`; five tokens decode deterministically (discoveries #2, #12), LEAD91/TAIL570 remain unresolved after the 09-04 matrix-sum, cipher, and Bifid sweeps.
- `H-COS-001 — Cosmic Duality decrypt is intended`: `UNRESOLVED`; excluded as an input by the 09-04 checkpoint (interpretive tokens, foreign KDF convention); large blob unopened.
- `H-BTC-001 — Candidate WIF controls a target`: `TESTING`; no candidate has passed exact address equality (local: ~3,700 structural candidates, ~280 oracle families, ~6,300+ decrypts, 0 hits).
- `H-MECH-001 — Matrix-derived Half/Better Half is the prize mechanism`: `FALSIFIED` for the documented candidates.
- `H-PRIME-001 — Prime and zeroing clues define the final step`: `TESTING`; finite prime/zeroing/yinyang enumeration complete with no hit (discoveries #12–#21).
- `H-GRID-001 — 2023 binary grid encodes a final clue`: `SUPPORTED`; the bit-reversed author message is recovered, though the exact OCR transcription needs refinement.
- `H-SMALL-001 — Small blob is a valid unopened lock`: assembly corrected (A+z+B, VALID_CIPHERTEXT); a 5-token direct+MD5 password now decrypts it to structured K_C1/K_C2/E_C with a verified WIF link (discovery #17) — decrypt SUPPORTED, prize key still UNRESOLVED; Issue #108 correction remains `UNVERIFIED`/contested.
- `H-OTHER-001 — A separate route leads to the prize`: `TESTING`; p32 lock (salt `b45a5e3d827593ca`) and third door (`1NULY7Dhu…`, 6 constructions, self-tested harness) added 09-04, both negative so far.

The active bottleneck is the exact interpretation of the two final-page digit streams and their relation to the final encrypted material. `cosmic_A.bin`, the XOR-triangle formula, and the exact final password reduction are not locally available or proven.

## Dead Ends and Falsifications

The root dead-end log records:

1. **Literal issue #108 small-blob correction** — not reproduced; proposed substitutions are already present. (Superseded framing: the old A+B concatenation is the wrong assembly; the correct A+z+B assembly is block-aligned but unopened.)
2. **Matrix-derived Half/Better Half as funded target keys** — candidate addresses do not match either funded target.
3. **Upper-five-bit/Base32 interpretation of the 2023 hint** — binary garbage; superseded by the bit-reversed message interpretation.
4. **Treating the 1327-byte Cosmic output as a solved final gate** — valid padding and a self-reported hash are insufficient, and the final address proof fails.
5. **Posted "Phase 3 SOLVED" ownership signatures (09-04)** — byte chain reproduces, but prize equality is False, both compact signatures are INVALID under offline recovery, and chain shows dust-only sweeps; falsified as solution/ownership (discovery #16).
6. **Literal matrixsumlist sweep on LEAD91/TAIL570 (09-04)** — 765 sum-list passwords → 6120 decrypts → chance-rate paddings only, 0 matches; falsified for the tested mapping/shape/form space.
7. **Beaufort/Vigenère/EBCDIC spot checks on digit streams (09-04)** — no binary runs, no hits, EBCDIC-on-digits meaningless; falsified for the tested keys.
8. **Bifid 256-object onward use (09-04)** — head `BTCSEED…` reproduces via true decode (earlier "unreproducible" verdict retracted as encode/decode mixup); prize-use falsified (no further tokens, sha/oracle/door miss).
9. **"BTCSEED not reproducible" sweep (09-04)** — void: its headline output equals the encode direction byte-exact (labels flipped); 96-config check leaves the principled config unique.
10. **Token OP_RETURN-origin + creator-disavowal claims (09-04)** — rejected: no support in captured OP_RETURN corpus; `yourlastcommand` is primary page text.
11. **Documented 285→256 Bifid reduction (09-04)** — mechanically impossible under verified settings (odd stream locked {B,C,D,E}, zero I/O); public chain internally inconsistent (discovery #21).
12. **Wikipedia-derived yinyang mechanisms (09-04)** — dots/containment, 180° rotational antisymmetry, I Ching 6/7/8/9 lines all negative.

The investigation deliberately does not erase or silently rewrite earlier claims. Each negative result remains tied to the artifact, method, and limitation that produced it.

## Timeline Summary

The documented timeline contains these major events:

- 2019-04-22 — Wayback has an archived `www.gsmg.io/` capture.
- 2020-04-25 — The public puzzlehunt repository begins.
- 2021-05-07 and 2021-05-20 — SalPhaseIon material is added to the repository.
- 2020–2024 — Official hints mention the second door, SalPhaseIon, primes, zeroing, and subsequent prize halvings.
- 2025–2026 — Public solution claims, retractions, fake-solution disputes, and forensic audits appear.
- 2026-09-03 — The local evidence-first workspace is initialized; live routes, stage assets, repositories, and issue data are captured.
- 2026-09-03 — Phase 1 and Phase 2 reproductions pass.
- 2026-09-03 — Raw integrity is repaired by restoring a modified cloned solver and excluding volatile `.git` internals from the manifest.
- 2026-09-03 — Official hint images are OCR-transcribed.
- 2026-09-03 — Both funded target addresses are checked.
- 2026-09-03 — Matrix-derived candidate keys fail target-address verification.
- 2026-09-03 — Issue #108 is checked against the immutable small-blob capture and remains unverified.
- 2026-09-03 — The 2023 binary hint is reinterpreted as a bit-reversed author message.
- 2026-09-04 — `CHECKPOINT-2026-09-04-SALFINAL` frozen; byte-identical region map fixed; small-blob assembly corrected to A+z+B (block-aligned, salt `3ab585348552415d`); Cosmic/Half/Issue #108 inputs excluded.
- 2026-09-04 — Dual-lock + third-door harness self-tested (phase-2 blob, `causality` re-derivation); 2,868-candidate prime/zeroing/matrix/yinyang enumeration + 54 bifid/oracle families + 108 queued attempts (sole EXACT hit: known esrever control) — 0 prize hits.
- 2026-09-04 — Matrix-sum sweep (765 passwords → 6120 decrypts → chance-rate paddings → 0 matches); Beaufort/Vigenère/EBCDIC spot checks negative; Bifid 256-object onward use negative (head reproduction corrected separately below).
- 2026-09-04 — Forensic layer: full DOM pass (no hidden channels; no `Dualite` string — h1 reads `Cosmic Duality`; single 64-column wrapping convention across both blobs); constancy-scored diagnostics (R/C verified True/True; three weak chance-bounded anomalies); lock comparison (no shared structure); third-door forensics (fresh valid v0; `NULY` defused); pipeline verdict 0 new lock attempts (discovery #15).
- 2026-09-04 — Phase-3 claim falsified (byte chain reproduces; prize False; signatures INVALID; dust-only); debate adjudicated (round-trip tautological; random tokens validate 2/210); chains 1–3 verified byte-exact with WIF link and three-way AES-key rebuild, all 8 chain keys miss (discovery #17); walkthrough checkables confirmed, "hidden BMPs" debunked, both OP_RETURNs on-chain (discovery #18).
- 2026-09-04 — OPENs solved one-by-one: Chain-4 slice forensics negative; grid unlocatable in live capture; chain strings miss door; ordered 6×91+24 pipeline fails all sub-tests (discovery #19).
- 2026-09-04 — Bifid BTCSEED head reproduced (true-decode correction; odds {B,C,D,E}, single Z); onward use negative, 13/38 key-stream combine is noise; LEAD91's key-source function verified (discovery #20, dead end #6 corrected).
- 2026-09-04 — Discovery #21: verified odd stream has zero I/O, so the documented 285→256 reduction is impossible — public Bifid→256 chain internally inconsistent; Z-segment battery all miss. Yinyang mechanisms (dots, rotation, I Ching lines) all negative.
- 2026-09-04 — Voided a "BTCSEED not reproducible" sweep (headline output == encode direction byte-exact); 96-config check leaves (first_occ, RC, dec, 570) unique; token-key MATRIXSUL negative; LEAD91 status writeup verified line-by-line with its Bifid row corrected.
- 2026-09-04 — Reviewed "exact wiring" writeup (corroborated salt/ct/KDF/XOR/chance; rejected OP_RETURN-origin + disavowal claims; flagged four-ingredient testing as vacuous); snapshotted floflo777 subdir (13 files @4b7d48a, zero new content; manifest deduped 221→115).

## Current Position

### Proven or strongly supported

- The raw-artifact preservation workflow exists.
- The primary web routes and many secondary repository artifacts are captured and hashed.
- The 14×14 image spiral decodes to `gsmg.io/theseedisplanted`.
- The image color counts and colored-cell frame are independently reproduced.
- Phase 2 AES reproduction yields readable plaintext.
- SalPhaseIon byte-identity (live == canonical copy) and the exact 15-region map.
- Five SalPhaseIon tokens decode exactly (`matrixsumlist`, `enter`, `lastwordsbeforearchichoice`, `thispassword`, `yourlastcommand`); `secondanswer` is interpretive.
- LEAD91's key-source function (first-occurrence order → Bifid square → verified `BTCSEED` head, odds exactly {B,C,D,E}, single Z); onward use negative; documented 285→256 reduction mechanically impossible under verified settings (odd stream has zero I/O — discovery #21).
- The small-blob correct assembly (A+z+B, salt `3ab585348552415d`) and the same-shape p32 lock (salt `b45a5e3d827593ca`).
- The self-tested dual-lock + third-door harness (phase-2 known-blob + `causality` re-derivation; esrever control re-find).
- Full DOM forensics: no hidden channels on the SalPhaseIon page; one 64-column wrapping convention across both blobs; prompt R/C vectors verified True/True against the public grid.
- Lock comparison (no shared structure; entropy 5.97/5.93) and third-door forensics (fresh valid v0; `NULY` defused); pipeline verdict of 0 new lock attempts with chance-calibrated anomaly bounds.
- Chains 1–3 decrypts verified byte-exact (5-token direct+MD5 → K_C1/K_C2/E_C with WIF link; WIF direct+MD5 → K_S1/K_S2/E_S; 1327 field parse completing AES key `38d4f4c90…59cc` three-way); all 8 chain keys miss both targets.
- Both donation-address OP_RETURNs confirmed on-chain ("for ying yang thank you!", "it myself 140 investment", May 2025 third-party).
- The 2023 binary hint contains a bit-reversed message naming the final ingredients.
- Both Bitcoin target addresses and their recorded balances are known.

### Unresolved

- The complete SalPhaseIon digit-stream method (LEAD91/TAIL570 survive matrix-sum, cipher, Bifid, and ordered-pipeline sweeps).
- The Chain-4 wiring spec (bytes/mask-order/mode/IV) and the pubkey-X derivation (all 8 chain keys miss; poster admits families negative).
- Grid ground truth: the 14×14 pattern is unlocatable in the live capture (count err 144, template corr ≈ chance), so all image branches stay untestable.
- The final password for either same-shape lock, or a direct 32-byte reduction.
- The role of primes 2, 3, 5, and 7 beyond the enumerated (negative) structural space.
- The exact meaning of “zeroed out” and “ying yang” beyond the enumerated (negative) space.
- The intended plaintext (if any) of the large second blob (nicknamed "Dualite" in secondary literature; page title reads `Cosmic Duality`).
- The preimage of the third door (`1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9`).
- The role of `cosmic_A.bin`, the XOR triangle, and other missing operands.
- Whether the small blob belongs to the intended path.

### Falsified

- The documented matrix-derived Half/Better Half candidates as keys to either funded target.
- The literal issue #108 correction as a reproduced AES-CBC decryption (plus its A+B assembly framing).
- Base32/upper-five-bit decoding of the 2023 hint.
- Treating the public 1327-byte hash match as proof of a complete solution.
- Literal matrix-sum passwords from digit streams (tested mapping/shape/form space).
- Bifid onward-use from TAIL570 (tested square/period/direction space): head `BTCSEED…` REPRODUCES via true decode (5×5, DBIFHCEGA key + alpha remainder, period 570; odds exactly {B,C,D,E}, single Z) — earlier "unreproducible" verdict retracted as an encode/decode mixup; prize-use stays falsified (no further tokens, sha/oracle/door miss, 13/38 key-stream combine is noise).
- Beaufort/Vigenère/EBCDIC readings of digit streams (tested keys/encodings).
- Posted "Phase 3 SOLVED" ownership signatures (INVALID offline; dust-only chain).
- "Hidden BMP file" extraction from the 1327 bytes (complete 0x0F-offset enumeration, 5 vs ~5.2 expected).
- Ordered 6×91+24 pipeline correspondence (0/91 sums match; remainder 8/24, not 15/9).

## Reproduction Commands

The root files document these primary commands:

```text
python3 -m scripts.transcribe_salphaseion
python3 -m scripts.reproduce_public_claims
python3 -m scripts.analyze_salphaseion
python3 -m scripts.crypto_vectors
python3 -m scripts.derive_address --hexkey <HEX> --target 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
python3 -m scripts.verify_repository
python3 -m pytest
```

New 09-04 experiment programs (all offline; never submit secrets or broadcast):

```text
python3 experiments/sal_final_search/sal_final_search.py
python3 experiments/sal_final_search/sal_phase2_bifid_oracle.py
python3 experiments/sal_final_search/sal_matrix_sweep.py
python3 -c "import sys; sys.path.insert(0,'experiments/sal_final_search'); import dual_oracle as o; o.selftest()"
python3 experiments/sal_final_search/sal_queued_runner.py
python3 experiments/sal_final_search/sal_final_structure.py
```

The workflow is read-only with respect to external services. Candidate secrets must not be transmitted, and no transaction or signature should be broadcast as part of verification.

## Final Assessment

The investigation has reproduced substantial portions of the GSMG puzzle and has falsified several popular solution claims. Local 09-04 work adds a frozen byte-exact SalPhaseIon map, a corrected block-aligned small-blob assembly, a self-tested dual-lock + third-door harness, and ~3,700 structural candidates plus ~6,300 offline decrypts with zero prize hits — including falsification of the literal matrix-sum, classical-cipher, signature-ownership, hidden-BMP, and ordered-pipeline readings, correction (not falsification) of the Bifid-BTCSEED head to reproduced-mechanical-fact with negative onward use — plus the first verified multi-step decrypts beyond Cosmic (chains 1–3 with WIF link and three-way AES-key rebuild, prizeless). It has **not** recovered or proven the private key for the funded prize address or the halving destination.

**The puzzle is NOT SOLVED.**
