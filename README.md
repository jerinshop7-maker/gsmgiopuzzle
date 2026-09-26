# GSMG 5 BTC Puzzle — Autonomous Forensic Cryptanalysis

This repository is an evidence-first investigation of the GSMG.IO Bitcoin puzzle. It preserves source artifacts, records exact transformations, reproduces public claims, and maintains falsifiable hypotheses.

## Status

**The puzzle is NOT SOLVED.** No private key or prize mechanism has been independently established.

The strongest unresolved branch is the byte-for-byte interpretation of the two SalPhaseIon digit streams and their relationship to the final encrypted blobs. The official 2023 hint, when bit-reversed per byte and read in reverse token order, names `yellow blue primes matrixsumlist lastwordsbeforearchichoice yinyang` and says the password is in front of the solver's eyes. Public “Half and Better Half” and 1327-byte Cosmic Duality claims are not accepted as final proof: the derived addresses do not match either funded target, and issue #106's full sweep witnesses are not locally available.

## Evidence policy

- `raw/` contains untouched source artifacts and is immutable.
- `derived/` contains transformations and analysis outputs; every significant output must identify its parent artifact hashes.
- `scripts/` contains deterministic computational experiments.
- `experiments/` contains experiment-specific manifests and reports.
- `evidence.md` separates directly observed facts from inference and hypotheses.
- `discoveries.md` and `dead_ends.md` are append-only research logs.
- No script submits forms, signs messages, broadcasts transactions, or sends candidate secrets to external services.

A readable plaintext, valid hash, valid WIF, valid address, successful padding check, or matching length is not proof of the intended path by itself.

## Layout

- `raw/web/` — live and archived HTTP captures.
- `raw/github/` — preserved public repositories and issue material.
- `derived/transcriptions/` — byte/code-point-preserving page analysis.
- `derived/crypto/` — cryptographic transformations and controls.
- `derived/bitcoin/` — offline verification and cached read-only chain queries.
- `scripts/` — intake, hashing, analysis, and validation tools.
- `experiments/` — reproducible run records.

## Initial sources

Primary candidates:

- `https://gsmg.io/puzzle`
- `https://gsmg.io/theseedisplanted`
- `https://gsmg.io/choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself`
- `https://gsmg.io/89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32`

Secondary sources:

- `https://github.com/puzzlehunt/gsmgio-5btc-puzzle`
- `https://github.com/Naddiseo/gsmgio-5btc-puzzle`
- `https://github.com/jackdevs66/GSMG5_CDuality`
- Public issue and comment records, labeled by source and date.

## Reproduction

The intended workflow is:

```text
python3 scripts/intake_web.py --help
python3 scripts/intake_github.py --help
python3 scripts/hash_artifacts.py
python3 scripts/build_inventory.py
python3 scripts/transcribe_salphaseion.py
python3 scripts/reproduce_public_claims.py
python3 scripts/crypto_vectors.py
python3 scripts/bitcoin_verify.py --help
python3 scripts/verify_repository.py
python3 -m pytest
```

Network collection is read-only. Captures are timestamped, hashed, and never overwritten. The runtime fingerprint and exact commands belong in experiment reports.

## Current position

The repository began empty on 2026-09-03. Initial public-source review found a live puzzle image, live phase pages, a live SalPhaseIon/Cosmic Duality page, historical GitHub artifacts, and contradictory recent solution claims. Artifact intake and independent reproduction are required before any solution status can change.
