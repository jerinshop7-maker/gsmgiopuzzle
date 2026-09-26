# Post-history recovery — PROVENANCE

Run: 2026-09-04 (post-history phase). Policy: read-only web (GitHub API,
Wayback, Common Crawl index, bitcointalk fetch), offline-first, no
submissions/broadcasts/credentials.

## Inputs read (pre-existing)

Root Markdown (all), sal_final_search + next_stage reports, clones
(puzzlehunt/Naddiseo/jackdevs66/floflo snapshot).

## Inputs acquired (read-only)

- GitHub API: pulls/68, pulls/68/files, pulls+issues/68/comments,
  issues triage p1, issues/55+91+97+99+103 comments, fork tree @27ea50eb,
  fork puzzle.png + theseedisplanted.png, 8× users/{}/gists.
- Saved: issues/{55,68}/comments.jsonl under puzzlehunt clone dir.
- Wayback: 4f7a-probes (boilerplate). Bitcointalk-5151725 HTML (/tmp only).
- Local: git branch/tag/stash/fsck/deletion logs ×3 clones; shell
  histories; /tmp + /tmp/opencode listing.
- Common Crawl: collinfo + 4 index queries (2024-10, 2025-30, 2026-30,
  2026-04-timeout).

## Artifacts written

- experiments/post_history_recovery/{REPORT,DISCOVERIES,DEAD_ENDS,
  SOURCES,PROVENANCE,ATTESTOR_GRAPH,CHAIN4_TIMELINE,GRID_SOURCES}.md
- issues/{55,68}/comments.jsonl (new secondary captures).

## Reproduction

Re-run listed API/CDX queries; recompute shas; re-grep corpus. No
credentials, transactions, or messages involved.
