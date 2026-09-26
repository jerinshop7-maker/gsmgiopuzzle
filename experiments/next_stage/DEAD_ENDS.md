# Next-stage DEAD_ENDS (this run only; root log unchanged unless noted)

## N1 — Live-vs-original divergence (all static content)

- Question: do live bytes differ from historical originals?
- Test: 6 SalPhaseIon + 4 phase-2 + 1 puzzle.png Wayback captures vs live.
- Observed: all identical (modulo Cosmic line-wrap + page chrome).
- Status: FALSIFIED. Grid failure = method problem. (Root H-PROV-001 rather
  than dead_ends.md proper; recorded here per brief.)

## N2 — PR #68 as Chain-4 code source

- Question: does PR #68 version the "c2" pipeline?
- Test: fetched PR file list + fork tree.
- Observed: single-file doc PR (GAP_ANALYSIS.md); "c2" lives only in issue
  comments referencing unversioned material.
- Status: FALSIFIED as code source. (The "c2" pipeline content itself stays
  UNRESOLVED, not dead — different claim.)

## N3 — Hidden git objects / prior-session witnesses

- Question: do clones/shell/tmp hold deleted files or sweep scripts?
- Test: branches/tags/stash/fsck/deletion-logs; history + /tmp inspection.
- Observed: single branch each, no tags/stash/dangling; one image-reorg
  deletion commit; /tmp holds unrelated OCR tooling + image copies.
- Status: FALSIFIED (nothing hidden). Prior-session 2.5B-witness scripts
  confirmed absent from this machine.
