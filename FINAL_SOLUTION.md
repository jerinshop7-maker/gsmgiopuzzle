# GSMG Puzzle — Verified Solution

## Executive Summary

**The puzzle is NOT SOLVED.** The public “Cosmic Duality → Half/Better Half” chain is reproducible as a byte transformation, but it is not proof of the intended final gate: the output is high entropy, its advertised hash is self-referential, and its derived addresses do not control either funded target.

The main prize address `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` still holds approximately 1.256 BTC, and the halving address `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` holds approximately 3.7505 BTC fully unspent at the recorded observation. Issue #106 identifies the two final-page digit streams and the “yellow blue primes matrixsumlist lastwordsbeforearchichoice yinyang” message as the strongest remaining public lead. The issue #108 small-blob correction is not reproducible from the captured bytes.

## Puzzle Artifacts

Primary captures (read-only, hashed, immutable):

- `raw/web/live/puzzle/response.bin` — puzzle.png, SHA-256 `38125bbd...`
- `raw/web/live/theseedisplanted/response.bin` — stage-1 HTML + images
- `raw/web/live/phase2/response.bin` — Phase 2/3 encrypted text
- `raw/web/live/salphaseion/response.bin` — SalPhaseIon/Cosmic Duality textareas, SHA-256 `a83d3de7...`
- Nine stage-1 image assets under `raw/web/live/img_*`
- Cloned repositories: `puzzlehunt/gsmgio-5btc-puzzle`, `Naddiseo/gsmgio-5btc-puzzle`, `jackdevs66/GSMG5_CDuality` (full commit history)

## Evidence Chain

### Phase 1 — VERIFIED

14x14 grid, down-first counterclockwise spiral -> `gsmg.io/theseedisplanted`. Reproduced from the public grid matrix and pixel-grounded from ART-001 itself (75px lattice, dominant-fill classification, `scripts/extract_grid.py` VERIFY PASS; discoveries #42/#52). The stable pixel counts are `K=86/W=86/B=15/Y=9`, with unused nibble `0000`; a temporary center-sample/comparison-fixture branch claiming `K=87/W=85` / `0100` is withdrawn. Row-major yellow cells independently give `0x41D464`; the corrected 797-candidate lock/door battery produced no exact hit.

### Phase 2 — VERIFIED

OpenSSL AES-256-CBC, password `eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf` (`sha256(“causality”)` hex), `-md sha256`. Decrypts to readable English. Reproduced from the live capture.

### SalPhaseIon tokens — VERIFIED

From the live textarea (byte-identical to the canonical repo copy):

1. `matrixsumlist` (104-char abba span -> binary ASCII)
2. `enter` (40-char abba span -> binary ASCII)
3. `lastwordsbeforearchichoice` (a-i/o -> 1-9/0 -> hex -> ASCII)
4. `thispassword` (a-i/o -> 1-9/0 -> hex -> ASCII)
5. `matrixsumlist`
6. `yourlastcommand`
7. `secondanswer`

### Cosmic Duality decrypt — UNRESOLVED

The public transformation is reproducible from the canonical secondary repository: XOR of seven SHA-256 digests -> 32-byte value `a795de11...`; EVP_BytesToKey MD5 -> AES-256-CBC; 1327-byte output with advertised SHA-256 `4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081`. However, issue #106 correctly identifies that valid PKCS#7 padding and a self-reported output hash do not establish intended decryption. The output is high entropy and the matrix-derived values do not control either funded target.

### Prize mechanism — UNRESOLVED

The 1327-byte payload is 103x103 bits + 7 padding. The documented matrix + base-38 transform yields two valid secp256k1 scalars:

- half `0423d911...` -> address `1JG648ya...`
- better `48cc46e6...` -> address `145ZQ9si...`

**Neither matches either funded target:** `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` or `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`. The derived addresses show only incidental dust activity, not the puzzle's prize funds. The main target retains approximately 1.256 BTC and the halving target retains approximately 3.7505 BTC at the recorded observation.

Issue #108's claimed two-typo correction is not reproduced: captured Base64 positions 18 and 51 are already `J` and `s`, and the literal concatenation leaves 79 ciphertext bytes, which is not divisible by AES-CBC's 16-byte block size.

## Previously Incorrect Theories

- **”Half and Better Half” split-key mechanism**: the documented matrix-derived values do not control either funded target. FALSIFIED as the final-key claim.
- **1327-byte decrypt as proof of solution**: matching the hash only proves you reached the same public bytes as everyone else. FALSIFIED as a complete solution.
- **Small-blob two-typo fix (issue #108)**: the claimed substitutions are already present in ART-004, and the literal combined ciphertext is not block-aligned. UNVERIFIED/CONTESTED.
- **Any valid WIF treated as the prize key without address equality**: rejected as a solution criterion.

## Newly Discovered Structures

- The live SalPhaseIon textarea is byte-identical to the canonical `jackdevs66` repo copy (capture verified against secondary source).
- The documented solver passes the key as **raw bytes** to EVP_BytesToKey, not the hex string — a subtle but critical detail.
- The public region-size claims (91/103/570) do not match the literal captured bytes; the actual structure is 104/40/63/29.
- The official hint corpus explicitly names primes `2,3,5,7`, says some characters must be “zeroed out,” and says reaching a “ying yang” enables solving the puzzle the same day.
- The 2023-02-23 binary hint, when bit-reversed per byte and read in reverse token order, gives a near-exact message naming `yellow blue primes matrixsumlist lastwordsbeforearchichoice yinyang` and saying the password is in front of the solver's eyes.
- The puzzle has two funded target addresses: the original `1GSMG1JC...` and the post-halving `17ucy1K9...`; both must be treated as target candidates.
- The adjacent second SalPhaseIon Base64 fragment is 64 characters, but its literal concatenation with the first fragment leaves 79 ciphertext bytes and cannot be standard AES-CBC input.
- The #106 report says its full sweeps found no target match, but the scripts and witnesses are not yet present in this workspace; that coverage remains secondary.

## Final Cryptographic Construction

Partially resolved (discovery #23). Chains 1–3 plus Chain-4 decrypt reproduce byte-exact from primary bytes (1151B, sha `e4269ed5...`, `+-`, `31+35x32`, tail `9f06936a...`); the 35-block selector to `X=f4d1bbd9...` remains OPEN from public artifacts. `cosmic_A.bin` / `K_I1` / `row1-4` are secondary solver folklore (no author source, no bytes), not proven requirements. The strongest remaining lead is the combination logic itself (`+`, operand, `0x77` markers, half/better). The exact final reduction remains unverified.

## Bitcoin Verification

`scripts/derive_address.py` derives P2PKH addresses from candidate keys and compares to the targets. The documented matrix-derived candidates fail against both `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` and `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`. Read-only chain data confirms both targets remain funded at the recorded observation; no solver ownership proof exists.

## Complete Reproduction Procedure

```text
python3 -m scripts.transcribe_salphaseion
python3 -m scripts.reproduce_public_claims
python3 -m scripts.analyze_salphaseion
python3 -m scripts.crypto_vectors
python3 -m scripts.derive_address --hexkey <HEX> --target 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
python3 -m scripts.verify_repository
python3 -m pytest
```

## Independent Verification

All cryptographic steps were independently reimplemented (not copied) from the documented descriptions and verified against the captured primary bytes.

## Remaining Uncertainties

- The actual intended interpretation of the 1327-byte payload (if any) that leads to the prize.
- Whether the prize is controlled by a key derived through a different path entirely.
- Whether the puzzle is solvable from public information or requires a private clue.

## Confidence Assessment

- Evidence-first repository and reproduction pipeline: STRONGLY SUPPORTED.
- Published prize mechanism (Half/Better Half): FALSIFIED.
- Complete puzzle solution: **NOT SOLVED.**

## Scripts

`intake_web.py`, `intake_github.py`, `hash_artifacts.py`, `build_inventory.py`, `transcribe_salphaseion.py`, `reproduce_public_claims.py`, `analyze_salphaseion.py`, `crypto_vectors.py`, `derive_address.py`, `bitcoin_verify.py`, `verify_repository.py`.

## Artifact Hashes

See `artifact_inventory.md` and `raw/manifests/raw_manifest.jsonl`.
