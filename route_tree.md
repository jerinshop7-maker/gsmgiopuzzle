# GSMG Puzzle — Solving Route Tree

Built 2026-09-04 from the full ledger (discoveries #1–#21, dead ends #1–#6).
Node statuses: `SOLVED` (verified on primary bytes) · `OPEN` (actionable,
with the exact next operation) · `BLOCKED` (missing input named) ·
`FROZEN` (excluded by checkpoint) · `DEAD` (falsified, kept for reference).
Acceptance for any prize claim: exact address equality with a funded target
plus, for ownership, a verifying signature. Nothing else promotes.

```text
[START] gsmg.io/puzzle ── SOLVED ── puzzle.png (ART-001, sha 38125bbd…)
  │
  ├─ 14×14 grid → down-first CCW spiral → gsmg.io/theseedisplanted ── SOLVED
  │     (canonical image rechecked; URL verified; README matrix matches all 196 cells — discovery #52)
  │     └─ color branches (counts, 0x41D464, sums, merlons) ── PARTIAL
  │           canonical pixels: K86/W86/B15/Y9; center-sample K87/W85 census withdrawn;
  │           row-major yellow mask 0x41D464;
  │           spiral B/Y frame exact; B2 direct/prime-mask lock battery = 0 hits (#44)
  │           pixel matrix: 75px lattice origin (0,0) rows y=0..1050, all 196 cells
  │           classified by dominant canonical fill, K86/W86/B15/Y9; the README
  │           bit matrix matches exactly. B1–B4 are testable with primary bytes;
  │           center-sample contamination is withdrawn. Canonical
  │           matrixsum/prime-zero/yin-yang battery: 797 candidates,
  │           0 target/door matches.
  │
  ├─ theseedisplanted (ART-002) ── SOLVED ── flower password → Phase-2 URL
  │
  ├─ Phase 2 / Phase 3 page (ART-003) ── SOLVED
  │     ├─ causality → sha256 → AES/SHA-256 → readable plaintext ── SOLVED
  │     ├─ 7 parts → digest 1a57c572… → phase-3 plaintext (4090 B) ── SOLVED
  │     └─ phase 3.2: EBCDIC → Beaufort(thematrixhasyou) → monologue ── SOLVED
  │           ├─ 149 digits → VIC checkerboard → HALF/BETTER-HALF sentence
  │           │     (phrase genuine; key binding DEAD — dead ends #2/#5)
  │           └─ p32 lock (salt b45a5e3d…) ── SOLVED (WIF+MD5 → K_S1/K_S2/E_S)
  │
  ├─ Decentraland audio → HASHTHETEXT → SalPhaseIon route ── SOLVED
  │
  └─ SalPhaseIon page (ART-004) ── SOLVED (15-region map frozen)
        ├─ MID104 → matrixsumlist ── SOLVED        ├─ R4A40 → enter ── SOLVED
        ├─ R1 → lastwordsbeforearchichoice ── SOLVED ├─ R2 → thispassword ── SOLVED
        ├─ R3ENG → yourlastcommand (+shabef) ── SOLVED
        ├─ LEAD91 (91) + TAIL570 (570) ── OPEN
        │     verified: Bifid-decode (5×5 DBIFHCEGA+alpha, p570) → BTCSEED head,
        │     odds {B,C,D,E}, single Z — LEAD91's FUNCTION is key source (#20);
        │     REFUTED: documented 285→256 reduction impossible here (odd stream
        │     has zero I/O — #21); yinyang dots/rotation/I-Ching all negative;
        │     a "not reproducible" sweep is void (its output == encode direction);
        │     96-config check leaves the principled config unique; MATRIXSUL key
        │     negative; onward use negative (no tokens, sha/oracle/door miss,
        │     13/38 key-streams are noise); matrix-sum/Bifid-wrong-dir/cipher/
        │     prime/forensic/ordered-pipeline sweeps all negative (#12–#15, #19)
        │     NOTE: may be the alternate "2nd way", not chain input
        │     NEW (#40 ausencia): even256/TAIL sequential drift SUPPORTED —
        │     rows χ²415 df330 p~0.001/shuffle 0.0005, early-late p~0.009,
        │     TAIL early-j p~0.018 (mechanism-checked); halves-key 0/6.
        │     Needs a STATED sequential decoder (Phase-3.2 VIC reuse DEAD — Dead End #28).
        │     2026-09-11 (option 1): external lead 6 (29 dropped letters) CLOSED locally
        │     (`OOIIOOO…OIOI`, 8 oracle + 16 lock, 0 hits — Dead End #29);
        │     2021 notebook confirms LEAD/TAIL undecoded then (cell 13);
        │     external 335.7M+62.6M boundary recorded SECONDARY, not re-swept (CLM-013).
        │
        ├─ CHAIN 1: small blob (salt 3ab58534…), 5-token direct+MD5
        │     → K_C1/K_C2/E_C (WIF link verified) ── SOLVED (#17)
        ├─ CHAIN 3: Cosmic blob → XOR-7 → 1327 B, field parse
        │     → K_B1/K_B2/E_B/K_H1/K_H2/E_H + mystery 1169 ── SOLVED (#17)
        │     (AES key 38d4f4c90…59cc rebuilt 3-way from C1/S/E_B)
        ├─ CHAIN 4: 1169→1168 + XOR-mask + AES → 1151 B (e4269ed5…) ── SUPPORTED (repro) / UNVERIFIED (design) / OPEN (interpretation)
        │     decrypt: mystery[:-1] XOR b657264f… → Salted__ salt 5bbd88ac… +1152ct; raw32 E_C||E_S||E_B[:2]+MD5 → 1151B, '+-', 31+35×32, tail 9f06936a… (#23, #25). Mask is secondary-only (#68); free-mask header + random-plaintext stats (ent 7.83/chi2 253) admit chance-padding.
        │     interpretation missing: 7×0x77 at [0,2,3,8,9,12,26] (11 total w/header; offsets/gaps random, label-only), 22 valid X; ~27k sweep +19 scalar/+12 XOR/+10 hash/+31→32/relations/diffs 0 hits (#23-24) + ~10k 15-char selector battery 0 hits (#25, Dead End #7) + 240 natural-mapping routing 0 hits (#26) + Tier 1/2/3 hashing, group-sum (0/45) and mod-35 (0/60) routing 0 hits (#27, Dead End #8) + pair-coordinate distinct addressing dead with null controls (#28, Dead End #9, H-PAIR-004) + coordinate-mapping dead by own null p~0.49, surjection exposed as tautology (#29, Dead End #10, H-COORD-005) + 5-state op layouts+chains 0/420, 36B packing ill-formed + fallback 0/36 (Dead Ends #11/#12, H-OPS-006/H-PACK-007, no discovery entry) + operand 23+7 split dead by own range rule (1/23, 1/7), modular projection 0/160, mod-5 null confirmed on corrected ground truth p~0.56 (Dead End #13, H-OPSPLIT-008/H-MODPROJ-009/H-MOD5-010; no discovery entry) + Round-9 audit re-verified on truth and closed rescues (P1/P2 dead, P3 frame corrected, factor/modular batteries dead; Dead End #14, no discovery entry) + 36x32 bridge refuted by slip proof with row/cross-layer/(u,v) batteries miss (Dead End #15, H-BRIDGE-011, no discovery entry); 15-char corrected to begbebebbbbbbcg (CLM-010); on-chain author ops P±G/half/double +227-char anchor CONFIRMED (#24); relation-graph/5×7/prime-sieve/#27-#29 markers all killed. Strict 4×24 prime-plane confinement FALSIFIED (94/96; H-PRIME-002, #26); SURVIVING: 23/16/7 dimensional frame (H-DIM-003; bridge (a) layer-pinned to 1152B per #28) + prime-half h,i depletion (Fisher p~0.033; H-ANOM-001). OPEN from public artifacts — cosmic_A/K_I1/row1-4 are secondary folklore, not author facts.
  └─ FINAL: privkey for uncompressed pubkey f4d1bbd9… ── OPEN
              (X oracle resolved to odd-Y a955…; all 8 chain keys + 35 blocks + ~10k selector combos + 240 routing + Tier/group/mod/pair/coord/op-layout/packing/split/proj/audit/bridge batteries miss; poster admits families negative; #23, #25-29 + falsification rounds (no discovery entries). NOT near-solved.)

  └─ NEW SECONDARY WITNESS BRANCH (Discovery #47) ── PROMISING / NOT AUTHOR INPUT
        ├─ block 949653: GSMGJH + 65B compact-signature-shaped payload
        ├─ block 949653: GSMGBH + 65B compact-signature-shaped payload
        ├─ block 949664: target 546-sat output + `GSMG WITNESS ... TX 808f812f`
        ├─ wallet lineage: 1GSMG9... ← burn-looking 111111... sweep + solver phrases
        └─ NEXT: identify exact signed message / hash convention; recover pubkeys;
                 test only against known Half/Better/target oracles, then decide
                 whether the branch yields a key fragment or remains solver-only.
```

```text
SIDE ROUTES (independent of the trunk)
  ├─ Third door 1NULY7… (no preimage) ── OPEN
  │     (6 constructions × text/dict/grid families negative — secondary;
  │     chain-derived strings also miss — discovery #19)
  ├─ Large second blob, "Dualite" nickname (h1: Cosmic Duality) ── RESOLVED (== Cosmic blob, #37)
  │     (textarea_1 == cosmic_duality.txt byte-identical sha b1895055…; NOT a separate
  │     unopened route — both decrypt to 4f7a1e4e… via canonical 7-token XOR→EVP-MD5)
   ├─ 17ucy1K9… halving split-off ── OPEN (no payout link published)
   │     (2026 Half/Better 546-sat token dust = SOLVER with public keys, EXCLUDED — #41;
   │     author funding `2aa9a4a9…`/`88cdb3cd…` carries no token OP_RETURNs;
   │     routing-as-author FALSIFIED; bc1qks8… is a solver P2WPKH test wallet)
  ├─ Cosmic 103×103/Half/Better + signatures + hidden-BMPs ── FROZEN as
  │  inputs; DEAD as prize/ownership claims (dead ends #2/#4/#5, #18)
  │  (round-trip = tautology; uniqueness = chance; BMPs = 0x0F selection)
  └─ Issue #108 two-typo correction ── DEAD (no-op + wrong A+B assembly)
```

## Priority-ordered next operations

1. `PROMISING / SECONDARY` witness branch (#47) — two compact-signature-shaped
   records plus the target-address witness. First identify the exact signed
   message/hash convention; use the compact recovery output as a key oracle only
   if it lands on a known Half/Better/target key. Do not promote solver bytes to
   puzzle input. The corpus and transaction-field tests currently give 0 known-key
   recoveries.
2. `SUPPORTED / WEAK` 546-sat convention (#48) — 70 OP_RETURN+546 pairs,
   including all three target `hereismysecret` records and the new witness, but
   overwhelmingly from solver Half/Better wallets. Treat 546 as a dust-token
   marker first; only pursue it as a numeric hint if an independent puzzle
   mapping appears.
3. `SUPPORTED` even256 structural frame (#38) — 16×16 over 23 letters == "23 ciphers /
   16 encryptions / 7 passwords" (16+7=23). The XOR-triangle (Lucas) also lands on 16
   from 24 CT-groups, 28 unmarked blocks (T7), and 103 matrix rows (#39). The MISSING
   piece is the combine function: 16 survivors × 7 tokens → key. EXECUTED and DEAD:
   C(23,16)=245,157 selection sweep × 5 derivations (1.23M candidates) → 0 hits
   (Dead End #25); frequency/string variants now closed independently (604
   candidates, 0 matches, Dead End #32).
   NEW 2026-09-11: token-length/operand-alone/even-substring battery (32 + 225 + 6 cands)
   → 0 hits (Dead End #27); coincidence bundle dead (sum-35 P=0.087, 0x77-selection,
   h-split, marker clustering — Dead End #26); VIC-reuse dead (Dead End #28).
4. `SUPPORTED` 23/16/7 frame (H-DIM-003) — structure only; mechanisms dead. The even256
   reframing (#38) now gives the "23" a concrete alphabet, superseding the abstract frame.
   NEW (#46): the decoded Bitcoin Genesis source literal is exactly 69 bytes = 3×23,
   giving a second primary-derived 23-column object. Prime-column/zeroing/hash readings
   are negative; the insertion operation remains OPEN.
   NEW: `SUPPORTED` drift frame (H-DRIFT-012, #40) — rows p~0.001/shuffle 0.0005,
   halves p~0.009, TAIL early-j p~0.018; halves-key 0/6. Needs a STATED sequential
   decoder; replication BLOCKED (LEAD too short, 161 exhausted).
   New audit (#45): the popular `765 -> 661` prime-sieve length match does not
   reproduce the canonical 661 bytes under either index convention; retain it
   as arithmetic only, not as the stream route (Dead End #30).
   New bounded continuation (#49): differences, runs, transitions, 16×16 routes,
   and Genesis 3×23 routes/column shifts/Caesar forms = 820 candidates, 0 exact
   matches; no privileged 16/23/7 period found. Revival needs a stated sequential
   decoder or cipher rule.
5. `TESTING` prime-half depletion (H-ANOM-001) — replicate on an independent object.
6. `OPEN` CHAIN 4 spec — request exact wiring (mask provenance secondary-only).
7. `OPEN` digit streams — needs new primary material (archives, square convention).
   The “reinserting the prime basics” wording remains the highest-value live
   clue, but its operation is not the rejected prime deletion mask.
8. `PROVEN`-from-pixels grid matrix (#44 correction to #42) — B2 `0x41D464`
   is now primary-pixel confirmed; its bounded lock/door battery is negative.
   B3 sums `490/497` and B4 merlons/indexed-string remain the next image branches.
9. `BLOCKED` nothing on the grid leg anymore; remaining BLOCKED: none (all legs have objects).
10. `OPEN` third door — C/GPU-scale passes only.
9. Everything `DEAD`/`FROZEN` — no further compute without new primary evidence.
   (floflo777 snapshot saved 09-04 @4b7d48a: zero new content vs 09-04 notes.)

## Continuation audit — 2026-09-14

```text
SALPHASEION
   |
   `-- TAIL570 -- 5x5 DBIFHCEGA, period 570 --> BTCSEED...       CONFIRMED
                    |
                    |-- 285 locked B/C/D/E symbols                CONFIRMED
                    |-- 285 diverse symbols; drop 29 I/O -> 256   CONFIRMED
                    |       `-- 23-letter alphabet, 16x16         CONFIRMED
                    |
                    |-- prime/zero -> 7x13 + 19x30 sums           FALSIFIED
                    |-- even256 16x16 prime/matrix readings       FALSIFIED
                    |-- aligned B/C/D/E selector routes           FALSIFIED
                    |-- B/C/D/E -> 2,3,5,7 numeric selector       FALSIFIED
                    `-- image 6+5 southeast B/Y chains           FALSIFIED (direct)
```

The live frontier is therefore not another matrix representation. The exact
Bifid decode and the aligned yin/yang pair survive as structural waypoints;
their tested key readings do not. The next route needs a specified cipher or
selector rule, or new primary author material, before expanding computation.

## Current chain refresh

```text
TARGET ADDRESS HISTORY
   |
   |-- block 964501: a751... pays 864 to target + 546 to 17ucy1K9...  CONFIRMED
   |       `-- no OP_RETURN; input 1LuCK... is a solver fan-out wallet   CONFIRMED
   |
   `-- OP_RETURN frontier remains block 949664 witness                  CONFIRMED
           GSMG WITNESS BLK 949653 TX 808f812f
           compact-signature records remain solver-origin               SECONDARY
```

The latest amounts do not promote 546 or 864 to an author-defined numeric
hint; the lineage is now explicitly marked as solver traffic.

## Continuation audit — 2026-09-15

```text
NEW PRIMARY-SOURCE RECOVERY
   |
   `-- Issue #67 original attachments --> merlon crop 14x14   CONFIRMED
                                      |
                                      |-- R/W/K counts 72/60/64   CONFIRMED
                                      |-- direct masks/routes/packed bits  FALSIFIED
                                      |-- complete QR payload                       BLOCKED

SEMANTIC FINAL-PASSWORD BRANCH
   |
   `-- exact 2026 hint phrases + context forms --> 3724 candidates
                                                  0 lock / door / target hits  FALSIFIED

TARGET HISTORY
   |
   `-- block 949664 witness --> 546-sat + solver OP_RETURN provenance  CONFIRMED
                               puzzle-input interpretation             EXCLUDED
```

The merlon attachment is the most useful new evidence, but it does not yet
yield the private key. The live tree therefore keeps the merlon branch open
only for recovery of the clipped full QR object, while direct encodings are
closed. The main live routes remain: the unspecified author decoder after
`BTCSEED`/`even256`, the missing Chain-4 operand/rule, and the unmessaged
third-door transform.

## Continuation audit — 2026-09-15 (GF(256) branch)

```text
COMMUNITY 68-BYTE BRANCH
   |
   `-- 4×16 blocks + x-coordinates -- GF(256) interpolation
                                      |
                                      |-- all fields / reported order       CLOSED
                                      |-- AES field / all 2520 orders       CLOSED
                                      |-- level-3 4×16 serializations       CLOSED
                                      |-- row/column sum and XOR lists      CLOSED
                                      `-- 224312 checks: 0 target / 0 door  CONFIRMED NEGATIVE
```

The previously reported `a955a042…` two-byte prefix is reproduced, but the
finite matrix extension produces no exact match and no stronger prefix. This
branch is now a bounded negative route. The remaining live route needs an
author-specified decoder or missing primary Chain-4 material; arbitrary
serialization expansion is not justified by this evidence.

## Continuation audit — 2026-09-15 (recovered 161-token object)

```text
2023 HINT IMAGE
   |
   `-- 161 exact bytes, low bits 110 -- reverse bits/order --> author message  CONFIRMED
                                       |
                                       `-- upper five bits --> 7×23 object  CONFIRMED
                                                        |
                                                        |-- prime rows/cols + zeroing  CLOSED
                                                        |-- {2,3,5,7} reinsertion       CLOSED
                                                        |-- matrix sums / encodings       CLOSED
                                                        `-- 4674 target checks: 0 hits   NEGATIVE
```

This is a genuine input recovery, not a solution: it validates the 7×23
dimension and removes the earlier transcription blocker. The next live
question is how the 23-object, 16-encryption object, and seven-password
object are combined under the author’s unstated operation.

## Continuation audit — 2026-09-15 (prefix grammar)

```text
AUTHOR PHASE-3 CONVENTION
   |
   `-- "add giveit in front" -- known planted-address witness  CONFIRMED
                              |
                              `-- 252 literal final-object forms
                                  0 lock / door / target hits  FALSIFIED
```

This closes the direct transfer of the historical prefix rule to visible
final-page objects. The broader “in front of your eyes” instruction remains
semantic and underspecified; it does not justify expanding to arbitrary
insertions or wordlists.

## Continuation audit — 2026-09-15 (digit-stream and source-position probes)

```text
UNRESOLVED FINAL DECODER
   |
   |-- confirmed esrever convention --> Bifid objects: 180 checks, 0 hits     CLOSED
   |-- full 16-item / seven-token forms --> 115 checks, 0 hits                 CLOSED
   |-- Genesis positions 2,3,5,7 --> 864 checks, 0 hits                       CLOSED
   `-- LEAD91 = 1+...+13 triangular matrix --> 2880 checks, 0 hits            CLOSED
```

These are bounded negative results, not evidence that the underlying streams
are irrelevant. The remaining live branch is the author-specific decoder that
combines `yellow blue primes matrixsumlist ... yinyang`; no exact operation
has yet been recovered from the primary artifacts.

```text
TRIANGULAR CROSS-STREAM RESCUE
   |
   `-- LEAD sums -> direct TAIL/even256 indices
                    1728 checks, 0 lock / door hits             FALSIFIED
```

The remaining `LEAD`/`TAIL` relationship is therefore not a natural sum-index
lookup. Any further cross-stream selector needs an independently specified
operation or new primary author evidence.
