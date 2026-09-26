# Next-stage PROVENANCE

Run: 2026-09-04. Operator: forensic agent (this session). Policy: read-only
web (GitHub API, Wayback CDX/id_), offline-first, no submissions/broadcasts.

## Inputs read (pre-existing, not modified)

- Root Markdown: README, FINAL_SOLUTION, evidence, discoveries (#1–#22),
  dead_ends (#1–#5), hypothesis_tree, timeline, FULL_SUMMARY, route_tree.
- Experiment reports: sal_final_search/{REPORT, sal_regions},
  phase3_claim_verification, chains_verification, open_solutions.
- Cloned repos (pre-existing): puzzlehunt, Naddiseo, jackdevs66 forks.

## Inputs acquired this run (all read-only)

- GitHub API: pulls/68, pulls/68/files, pulls/68/comments (=0),
  issues/68/comments (=10), issues triage p1 (filter 90–109),
  issues/91+99+103+97 comments, fork tree @27ea50eb, fork puzzle.png +
  theseedisplanted.png.
- Wayback CDX: gsmg.io* (403 captures listed); id_ captures: SalPhaseIon
  ×6, phase-2 ×4, puzzle ×1, Cosmic-hash probes ×2 (boilerplate only).
- Local: shell histories, /tmp + /tmp/opencode (unrelated OCR tooling),
  git branch/tag/stash/fsck/deletion logs on 3 clones.

## Artifacts written

- `raw/web/archive/{salphaseion,phase2,puzzle}/` (11 captures) +
  `raw/web/archive/provenance.json` (new raw data — hashed next manifest run).
- `experiments/next_stage/{REPORT,DISCOVERIES,DEAD_ENDS,SOURCES}.md` + this file.
- /tmp scratch (API JSON, PNGs, gunzip outputs) — disposable, not evidence.

## Reproduction

Re-run the CDX queries and byte comparisons in REPORT §4; recompute shas
against `raw/web/archive/` + live ART-001/003/004. No credentials, no
transactions, no messages signed or sent.
