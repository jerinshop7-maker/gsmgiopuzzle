# OPEN-items solving pass — 2026-09-04 (this report)

Rule: every branch states CLUE → OBJECT → OPERATION → EXPECTED SHAPE →
INDEPENDENT VALIDATION. No sweeps; single deterministic chains only.

## OPEN-1: Chain-4 forensics — NEGATIVE, stays OPEN

24 slices (drop-first/last × xor-order × ECB/CBC0 × first1151/last1151/full):
no `e4269ed5…` sha, no early `+-` marker. The spec (bytes/mask-order/mode/IV)
is genuinely missing, not merely unfound.

## OPEN-2: Grid via 87/84/15/9/1 counts — BLOCKED (deepened)

- Center-pixel count search (15k+ bbox/scale combos): best err 144, yellow
  always 0 — sampling background, not grid.
- Yellow/blue pixels scatter across the upper 2/3 (photo art: 51k/87k px),
  not confined to any bottom block.
- Template match of the known 14×14 bit pattern at scales 8–40: max corr
  44/196 (chance ≈ 0±28) — pattern not present at any tested scale.
Conclusion: the grid is not locatable in the LIVE capture by brightness,
counts, or template. Either the live image differs from the 2019 original
or the grid is sub-8px/rendered decoratively. B1–B4 stay untestable.

## OPEN-3: Chain strings → third door — NEGATIVE

9 chain-derived strings (K_C1/K_C2/E_C/K_S1/K_S2/E_S/AES-key/WIF/XOR) × door
constructions: 0 hits. Chain material does not open the third door.

## OPEN-4: Ordered pipeline 6×91+24 — NEGATIVE on all sub-tests

- Column sums S (12–39, mean 26.2) vs LEAD91: 0/91 equal, S−L 23 distinct
  values — no correspondence (scales incompatible: sums vs digits).
- Remainder `212112105184820438422425`: mod2 8/24 ones (not 15/9), primeval
  10/24, flat distribution — no colored-cell signature.
The "most wanted experiment" fails its own falsification tests. The 24/24
coincidence does not survive measurement.

## Verdict

All four OPEN attacks executed with artifact-derived parameters only: 3
negative, 1 deepened-blocked. Nothing promoted. Puzzle NOT SOLVED.
