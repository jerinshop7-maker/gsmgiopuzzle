# CHAIN4_TIMELINE (documentary — numbers as attested, not endorsed)

| Date | Source | Claim (inputs → outputs, params) |
|---|---|---|
| 2025-12-25 | #68 GalloClaudio64 | "think triangular… XOR triangle" (pointer, no bytes) |
| 2026-01-01 | #68 GalloClaudio64 | chains trunk; 1169→1168 trim + XOR mask b657264f… + AES key E_C\|\|E_S\|\|E_B[:2] → 1151B e4269ed5, `+-`/operand/35×32 |
| 2026-03/04 | #87 EnigmAnderson | K_C1/K_I1/L4 via crib-drag; 1151 split@246 (head 7.150 / tail 7.790, tail sha 9f06936a); K_I1 insufficient alone |
| 2026-04-26 | #84 andersonbig | chain4.bin 1168B a80a399a = 48B header + 35×32; XOR pyramids/triangles negative; asks "c2" reconcilers (12 failed hypotheses noted in reply) |
| 2026-06-10 | #92 marcofortina | layout "+-" + 31B prefix + 35×32 region; tail sha agrees 9f06936a |
| 2026-07-11 | #92 valleytainment | adds cosmic_A cd3fea3d…, LCP7, anchor e2590f158 (all names, no bytes) |

## The 1169/1168/1151 discrepancy, analyzed (no brute force)

- Verified parse: 1327 = 158 header + 1169 mystery.
- Attested: 1169 →(drop 1, end unstated) 1168 → XOR → AES → 1151 (e4269ed5).
- 1168 − 1151 = 17: NOT a valid PKCS#7 strip (max 16). No standard single
  step connects the posted numbers.
- Layout arithmetic: 48 + 1120 = 1168 (a80a399a object) vs 31 + 1120 = 1151
  (e4269ed5 object, marker inside the 31). Difference is a 17-byte header,
  i.e. the two objects are different stagings (pre- vs post- something
  undisclosed), not input/output of one documented step.
- "12 reconciliation hypotheses → 0 matched a80a399a" (reply thread):
  independent confirmation the stagings do not reconcile publicly.
- Conclusion: spec missing (not hidden). Next evidence must be the "c2"
  transform itself or K_I1 bytes — both currently names without artifacts.
