# Next-stage forensic run — REPORT

Date: 2026-09-04. Scope: Chain-4 spec recovery, historical forensics,
third-door structure. No sweeps, no brute force, no broadcasts. Offline
except read-only web (GitHub API, Wayback CDX).

## 1. Executive summary

Biggest result: **the puzzle's static content is frozen since 2020** —
SalPhaseIon textarea byte-identical Jun 2023→live, phase-2/3 blobs identical
2020→live, puzzle.png identical Nov 2020→live. The "live differs" hypothesis
is dead; grid-extraction failure is a method problem. Second: the Chain-4
paper trail now has exact provenance (GalloClaudio64 issue #68, Jan 2026;
PR #68 is an unrelated gap-analysis doc; its fork's images match live).
Chain-4 wiring itself, `cosmic_A`/`ca`/`row1-4`/`K_I1` bytes, and the third-door
preimage were NOT recovered — an independent June OSINT sweep already
exhausted forks/issues/Wayback for them. **NO VERIFIED NEW DISCOVERY toward
the prize; one Level-A negative (content frozen) + full provenance map.**

Targets matched: none. Puzzle NOT SOLVED.

## 2. New evidence found

- E1 (Level A): 6 Wayback SalPhaseIon captures (2023–2026) — ta0 identical
  (d39d10b1…), Cosmic identical modulo wrap; only chrome changed. Preserved
  under `raw/web/archive/salphaseion/`.
- E2 (Level A): 4 phase-2 captures (2020–2026) — both blobs identical;
  2020 puzzle.png identical to live. Preserved under `raw/web/archive/`.
- E3 (Level B): PR #68 = gap-analysis doc only (1 file, GAP_ANALYSIS.md);
  fork images byte-match live. "PR #68 c2" pipeline lives in issue comments,
  not versioned code.
- E4 (secondary): issue #84 documents chain4 1168B (sha a80a399a…) vs
  canonical 1151B (e4269ed5…) divergence + 12 failed reconciliations;
  issue #87 attests K_I1/multi-operand structure ("never meant to open the
  last door" alone) and L4/crib-drag provenance; issue #92's OSINT sweep
  (65 forks/82 issues/Wayback) found no public ca/cosmic_A/row1-4/K_I1.
- E5: Naddiseo (issue #97) relays creator position: solution = find THE
  private key (singular) — kills multisig readings (secondary attribution).
- E6: third door formalized — v0, hash160 `eb862e…`, checksum valid;
  `NULY` needs only ~58⁴ grind, consistent with creator's other vanities;
  no other workspace occurrences.

## 3. Sources / provenance

See SOURCES.md (per-source table) and PROVENANCE.md (capture log). Raw
artifacts: `raw/web/archive/{salphaseion,phase2,puzzle}/`.

## 4. Reproduction procedure

CDX query → `id_` original capture → gunzip if needed → textarea regex →
compact compare → sha256. All commands inline in session; captures preserved.

## 5. Changed assumptions

- "Live may differ from original" → FALSIFIED for all static content.
- "PR #68 contains the pipeline" → corrected: doc-only PR; pipeline is
  comment-lore referencing an unversioned "c2".
- Grid hunt failure reclassified: method problem, not changed bytes.

## 6. What was tested

Operand search (all missing-operand strings — hits only in known places);
unread issues 84/87/90–93/95–103/109 (E4 + imneomutfua end-claim noted,
unverifiable); fork tree + images; git branches/tags/stash/fsck/deletions
(single image-reorg commit, no dangling); shell history + /tmp (unrelated
OCR tooling, no sweep scripts); Wayback CDX (403 gsmg.io captures listed;
puzzle/SalPhaseIon/phase-2 fetched); third-door decode + mention search.

## 7. What was falsified

Live-vs-original divergence (all content); PR-#68-as-code; hidden git
objects; prior-session witnesses on this machine.

## 8. What remains open (unchanged, now better mapped)

Chain-4 wiring; ca/cosmic_A/row1-4/K_I1 bytes; third-door preimage;
digit-stream mechanism; grid per-cell matrix; pubkey-X derivation.

## 9. Exact next operation

Only two evidence-backed moves remain: (a) obtain Chain-4 "c2"/K_I1 material
from its attestors (EnigmAnderson/imneomutfua/marcofortina) or deleted-gist
recovery; (b) 2019-grid recovery from non-Wayback archives (forum
attachments, Discord CDN, search caches). Everything else is swept or
missing-input-blocked.

## 10. Targets matched

None. NO VERIFIED NEW DISCOVERY toward prize control (per §17 rule, the
Level-A stability finding + provenance map are recorded as new evidence,
not as solution progress).
