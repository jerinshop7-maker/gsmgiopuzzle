# Indonesian walkthrough verification — 2026-09-04 (this report)

Source: 23-tahap walkthrough (phases → VIC → SalPhaseIon → Cosmic → hidden
files → 23-layer BLOB1 → 40B slices → BIP39/NULL → chain queries).

## VERIFIED

- 6 token SHA-256 values: ALL MATCH (matrixsumlist, enter,
  lastwordsbeforearchichoice, thispassword, yourlastcommand, secondanswer).
- 14×14 matrix: spiral decodes to `gsmg.io/theseedisplanted` exactly
  (third independent transcription; 101 ones / 95 zeros).
- 9-slice address derivation: slice0 → `1BypfyXN…` MATCH; full 40B oracle +
  door checks: all miss (consistent with their own "TIDAK COCOK").
- Donation-address OP_RETURNs, Blockstream read-only: "for ying yang thank
  you!" (block 898096) and "it myself 140 investment" (block 898064), both
  from `1MScxQEes…` (May 2025, third-party solver-era messages, NOT creator
  messages — but the yinyang/140-investment motifs are on-chain fact).

## DEBUNKED: TAHAP-14 "5 hidden BMP files"

- The 5 offset/key/size triples verify mechanically (each XOR slice starts
  with `BM`) — but a complete scan finds these are ALL offsets in the 1327
  bytes where adjacent bytes differ by 0x0F (5 found vs ~5.2 expected).
- The "discovery" is a complete enumeration of a 1/256 event presented as
  five findings. TAHAP 15–21 (base64 of slices, 23 unspecified layers, 40B,
  BIP39, NULL cipher) all build on these chance slices. FALSIFIED as designed
  content; the 40B object itself tested clean (misses prize + door).

## NOTED (untestable here)

- Part-7 FEN rank-3 discrepancy: live page `B5KR/1r5B/6R1/…` vs doc
  `B5KR/1r5B/2R5/…` — doc transcription error (documented digest unaffected).
- Conclusion's multisig/design speculation: no evidence either way; the
  verified chains need no multisig hypothesis and the final step stays open.

## Verdict

Walkthrough's solved-chain content corroborates ours; its novel claims split:
OP_RETURNs real, hidden-BMPs chance artifacts, 40B prizeless. Puzzle NOT SOLVED.
