# GSMG 5 BTC Puzzle — Forensic Cryptanalysis Plan

## Objective

Build a reproducible, evidence-first investigation workspace for the GSMG.IO puzzle. Recover the intended path only if every transformation from a primary artifact to the prize mechanism is independently reproducible and cryptographically verified. Until then, `FINAL_SOLUTION.md` must state that the puzzle is not solved.

The repository is currently empty apart from an empty taste file, so this plan establishes the research infrastructure from scratch.

## Current evidence position

- Live `https://gsmg.io/puzzle` serves the puzzle PNG; the live response and bytes must be captured and hashed.
- `/theseedisplanted` exposes the image fragments and a POST form.
- The long Phase 2 URL exposes Phase 2 and Phase 3 encrypted text.
- The hash URL `89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32` exposes SalPhaseIon and Cosmic Duality textareas.
- The `puzzlehunt/gsmgio-5btc-puzzle` repository contains six images, README claims, and history beginning 2020-04-25; SalPhaseIon was added 2021-05-07.
- The Naddiseo fork contains notebooks and additional asset directories that must be treated as secondary until their underlying provenance is established.
- Recent public issues disagree about the 1327-byte Cosmic decrypt, the small-blob typo claim, and “Half and Better Half” private-key/dusting claims. These remain hypotheses, not evidence.
- Highest-information unresolved branch: byte-for-byte interpretation of all SalPhaseIon regions, especially the two digit streams and their relationship to the blobs.

## Repository structure

Create and maintain:

```text
README.md
evidence.md
artifact_inventory.md
timeline.md
discoveries.md
dead_ends.md
hypothesis_tree.md
FINAL_SOLUTION.md
raw/
  README.md
  web/{live,archive,manifests}/
  github/{puzzlehunt-gsmgio-5btc-puzzle,naddiseo-fork,manifests}/
  screenshots/
derived/
  normalized/
  crops/
  transcriptions/
  crypto/
  bitcoin/
  reports/
  manifests/
  logs/
scripts/
experiments/
  README.md
  001-live-intake/
  002-github-history/
  003-salphaseion/
  004-cosmic/
  005-crypto-controls/
  006-bitcoin-verification/
```

Raw files are immutable. Derived files must reference parent artifact IDs. Logs and discovery/dead-end entries are append-only; corrections are new entries rather than silent edits.

## Implementation phases

### 1. Reproducible foundation

- Add a Python 3.11+ analysis environment with pinned versions for HTTP retrieval, HTML parsing, Pillow, NumPy, cryptography, notebook inspection, Bitcoin serialization, and pytest.
- Document commands and environment fingerprints in `README.md`.
- Keep network collection read-only; never submit forms, broadcast transactions, sign messages, or transmit candidate secrets.
- Add repository verification tests before analysis scripts depend on them.

### 2. Primary and historical intake

Implement `scripts/intake_web.py` to capture exact request URL, final URL, UTC time, status, headers, body bytes, declared media type/encoding, referenced resources, form metadata, and optional screenshot. Store each acquisition in a timestamped or content-addressed directory under `raw/web/`; never overwrite an earlier capture.

Capture the known live routes and all referenced image/style/script resources. Capture Wayback replay URLs separately under `raw/web/archive/`, recording archive timestamp and replay metadata. Archive completeness must be marked explicitly; an archive request alone is not proof that a page existed with content.

Implement `scripts/intake_github.py` to preserve full Git history and raw assets for:

- `puzzlehunt/gsmgio-5btc-puzzle`
- `Naddiseo/gsmgio-5btc-puzzle`
- `jackdevs66/GSMG5_CDuality`
- other repositories only when discovered and recorded as secondary sources

Capture commits, branches/tags, issue and comment JSON, README revisions, notebooks, and asset bytes. Record commit hashes and remote URLs. Do not treat a README, notebook output, issue, or fork as primary puzzle evidence without provenance.

### 3. Inventory and evidence ledger

Implement `scripts/hash_artifacts.py` and `scripts/build_inventory.py` to calculate SHA-256, SHA-512, byte length, MIME/type, and stable artifact ID for every raw file. Emit machine-readable JSONL manifests and a human-readable `artifact_inventory.md`.

Use records containing at least:

```json
{
  "artifact_id": "sha256:<digest>",
  "path": "raw/web/live/puzzle/response.bin",
  "source_url": "https://gsmg.io/puzzle",
  "source_type": "live-web",
  "acquired_at": "<UTC ISO-8601>",
  "byte_length": 0,
  "sha256": "",
  "sha512": "",
  "media_type": "",
  "parent_artifact": null,
  "tool": "scripts/intake_web.py",
  "tool_version": "<git commit>"
}
```

Populate `evidence.md` with one entry per significant artifact: source, URL, acquisition date, filename, size, hashes, raw-content location, encoding, associated clue, reliability tier, independent verification, and anomalies. Keep direct facts separate from inference and hypothesis.

### 4. Timeline and baseline reproduction

Build `timeline.md` from source dates and investigation events: original site/archive observations, repository commits, issue/comment dates, artifact acquisitions, experiments, and corrections.

Implement `scripts/reproduce_public_claims.py` in isolated experiment directories. Reproduce known claims from raw inputs, including:

- 14x14 puzzle traversal and URL extraction.
- Phase 2/3 AES-256-CBC paths, SHA-256 password derivations, exact OpenSSL-compatible KDF parameters, and plaintext hashes.
- Phase 3.2 Beaufort/VIC/EBCDIC claims where inputs are available.
- SalPhaseIon token extractions.
- Claimed 1327-byte Cosmic decrypt and all published password/KDF variants.
- Private-key/WIF/dusting claims and the retracted self-referential Cosmic hash argument.

Every report must include input artifact hashes, exact source span, command/parameters, dependency versions, output length/hash, expected result, observed result, and differences. A failed reproduction becomes a dead-end entry rather than an error to hide.

### 5. SalPhaseIon forensic analysis — priority branch

Implement `scripts/transcribe_salphaseion.py` to extract the live textarea as raw bytes and Unicode code points while preserving whitespace, line endings, HTML entities, visual ordering, offsets, separators, and non-ASCII symbols. Produce:

- `source_bytes.hex`
- `html_text.json`
- `rendered_text.txt`
- `visual_transcription.tsv`
- `candidate_streams.json`
- a byte/code-point comparison report against every repository copy

Segment every region independently. Do not merge visually similar streams. Represent alleged corrections, including the two small-blob character changes, as separate candidates with original offsets and parent hashes; never patch the source artifact.

For the two digit streams and every other computational region, test and record only justified transformations first: exact grouping, ASCII/byte interpretations, endian variants, base conversions indicated by clues, concatenation/interleaving, and source-order alternatives. Record length, entropy/frequency/periodicity, run lengths, modular/difference patterns, factorization/divisors, matrix dimensions, and leftover data. A readable output alone is not validation.

### 6. Standards-based cryptographic verification

Implement `scripts/crypto_vectors.py` with known-answer tests for SHA-256, MD5, EVP_BytesToKey, PBKDF2, AES-128/192/256 modes, Base64, Base58Check, and relevant padding. Include controls that prove the implementation reproduces known solved stages before candidate testing.

Implement `scripts/crypto_candidates.py` to test clue-derived candidates under explicit records of algorithm, KDF, digest, mode, key size, IV/salt, padding, encoding, and input hash. Test EVP-MD5 and EVP-SHA256 separately where public reports disagree. Reject malformed input and do not treat PKCS#7 padding, printable output, matching length, or a self-reported output hash as proof.

No arbitrary constants, massive unconstrained brute force, post-hoc parameter selection, or discarded bytes are permitted. Record every anomaly and bounded negative result.

### 7. Bitcoin and blockchain verification

Implement `scripts/bitcoin_verify.py` for offline Base58Check, WIF, compressed/uncompressed public-key derivation, HASH160, P2PKH, Bech32/Bech32m, and checksum validation. Use standard known-answer vectors first. For each candidate, derive the address independently and compare it to the actual target; a valid WIF that derives to another address is a decoy/intermediate, not a solution.

Cache read-only blockchain responses under `derived/bitcoin/<network>/<query-id>/` with request, response, provider, block height, query time, and response hash. Prefer two independent public providers. Record balances, transactions, outputs, address relationships, OP_RETURN data, and timing as current chain facts only; do not infer a puzzle mechanism from funding or dust activity without an explicit cryptographic link.

### 8. Hypothesis, discovery, and falsification management

Maintain stable IDs in `hypothesis_tree.md`, for example:

- `H-PROV-001`: a captured route is a primary artifact.
- `H-P1-001`: the puzzle grid traversal is down-first counterclockwise.
- `H-SAL-001`: SalPhaseIon streams encode deterministic data.
- `H-COS-001`: a specific Cosmic ciphertext/password/KDF is genuine.
- `H-BTC-001`: a candidate WIF controls the prize target.
- `H-MECH-001`: “Half and Better Half” describes the actual prize mechanism.

Each record includes statement, supporting/contradicting evidence IDs, required assumptions, transformations, expected/actual output, independent confirmation, coincidence risk, complexity, status, and last experiment. Use statuses `UNTESTED`, `TESTING`, `SUPPORTED`, `STRONGLY_SUPPORTED`, `FALSIFIED`, `DECOY`, and `PROVEN`; reserve `PROVEN` for a complete artifact-backed chain.

Implement `scripts/score_hypotheses.py` with an explicit rubric for provenance, exact reproducibility, independent confirmation, clue fit, anomaly handling, predictive power, and competing explanations. Missing provenance cannot be offset by readable plaintext or a valid cryptographic object.

Append genuinely new observations to `discoveries.md` and rejected branches to `dead_ends.md`, each with UTC date, artifact/experiment IDs, exact result, why it matters, possible next branches, confidence, and reproducible script.

### 9. Repository verification and final reporting

Implement `scripts/verify_repository.py` and pytest checks to ensure:

1. Every raw file has a matching manifest and recomputed hash.
2. Raw files are never overwritten by analysis scripts.
3. Every derived file references existing parent artifact IDs.
4. HTTP captures include URL, timestamp, status, headers, and response hash.
5. GitHub artifacts include repository/commit provenance.
6. Transcription offsets map back to source bytes/code points.
7. Cryptographic and Bitcoin known-answer vectors pass.
8. No script signs, broadcasts, submits forms, or sends candidate secrets.
9. Experiment reports include parameters, versions, and output hashes.
10. `FINAL_SOLUTION.md` cannot claim a verified solution without a complete machine-checkable evidence chain.

Start `FINAL_SOLUTION.md` with the explicit status: **The puzzle is NOT SOLVED.** Update it only after the complete chain is independently reproduced. Its final structure should be Executive Summary, Puzzle Artifacts, Evidence Chain, Phases 1–4, SalPhaseIon, Previously Incorrect Theories, Newly Discovered Structures, Final Cryptographic Construction, Bitcoin Verification, Complete Reproduction Procedure, Independent Verification, Remaining Uncertainties, Confidence Assessment, Scripts, and Artifact Hashes.

## Verification and acceptance criteria

The investigation may declare success only when it can provide exact source bytes, deterministic transformations, clue-supported operations, independently reproduced intermediate outputs, complete Bitcoin serialization/public-key/address verification, and a final mechanism that demonstrably controls the prize target. A hash match authenticates only the exact hashed bytes; it does not authenticate the interpretation. If the key or mechanism remains unavailable, report the strongest unresolved bottleneck and keep the solution status unresolved.

## Initial ranked experiments

1. Capture and hash all live routes and referenced resources, then compare with dated archive captures.
2. Preserve and diff all SalPhaseIon versions, including raw HTML, textarea bytes, repository text, and alleged blob variants.
3. Reproduce the clean Phase 1–3 chain with independent controls to establish trusted implementations and exact source spans.
4. Decode and structurally analyze every SalPhaseIon region, prioritizing the two digit streams and unexplained leftovers.
5. Run bounded, standards-based Cosmic/small-blob candidate tests with known-good KDF controls.
6. Verify all claimed WIFs/addresses and current on-chain relationships offline and through cached read-only queries.
7. Only after those results, test combined hypotheses that explain the prize mechanism and predict the target address.
