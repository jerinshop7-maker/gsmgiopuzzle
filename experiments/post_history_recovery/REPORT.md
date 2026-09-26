# Post-history recovery run — REPORT

Date: 2026-09-04. Prior run froze public history as exhausted; this run
targeted attestors, deleted gists, git objects, non-Wayback grids, and the
Chain-4 paper trail. Read-only web (GitHub API, Wayback, Common Crawl index,
bitcointalk) + local forensics. No submissions, no broadcasts.

## 1. Executive summary

- Chain-4 "c2"/K_I1/L4 material NOT recovered. Attestor graph built from
  issue text (7 names); all 8 gist accounts EMPTY (1 unrelated file);
  no paste URLs anywhere in issues; PR #68 is docs-only; fork images match
  live; git forensics empty; bitcointalk-5151725 is 2019 chatter.
- Chain-4 chronology RECONSTRUCTED instead: the 1169/1168/1151 numbers are
  mutually inconsistent under any standard single step (1168−1151=17, not a
  valid pad; the two layouts differ by a 17-byte header) — the spec is
  missing, not merely withheld detail.
- Grid via non-Wayback: Common Crawl has NO puzzle captures (only 2024
  homepage); no independent copy found. BLOCKED stands.
- Creator wording captured verbatim (relayed): "solved by finding the
  private key" — safe reading only: final solution needs THE key.
- Verdict: NO VERIFIED NEW DISCOVERY toward prize control.

## 2–4. Evidence / provenance / reproduction

See ATTESTOR_GRAPH.md, CHAIN4_TIMELINE.md, GRID_SOURCES.md, SOURCES.md,
PROVENANCE.md. Issue #55/#68 threads saved under
raw/github/puzzlehunt-gsmgio-5btc-puzzle/issues/{55,68}/.

## 5. Changed assumptions

- "c2 pipeline is versioned somewhere" → corrected: comment-lore only.
- imneomutfua end-claim logged UNVERIFIED (procedure withheld by design).
- Stale scan: FULL_SUMMARY contains no FEN/"10–15" staleness. Clean.

## 6–7. Tested / falsified

Attestor gists (8 accounts, 0 puzzle files); paste-URL grep (none);
PR #68 files (1 doc); fork tree+images (match live); git refs/tags/stash/
fsck/deletions (one image-reorg); shell/tmp (unrelated OCR tooling);
Wayback hash-URL probes (boilerplate); CC index (no puzzle captures);
code-search API (auth-walled, unavailable).

## 8. Open (unchanged, better mapped)

Chain-4 wiring; ca/cosmic_A/row1-4/K_I1 bytes; third-door preimage;
digit mechanism; grid matrix; pubkey-X derivation.

## 9. Exact next operation

Direct attestor contact is out of scope for this offline run — the only
remaining evidence-backed moves are: (a) deleted-gist recovery IF a gist
URL surfaces in future text; (b) 2019-grid from forum-attachment/CDN
caches outside Wayback+CC. Else: hold position, no compute justified.

## 10. Targets matched

None. Puzzle NOT SOLVED.
