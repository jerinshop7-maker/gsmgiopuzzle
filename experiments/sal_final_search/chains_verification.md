# Chains 1–4 verification — 2026-09-04 (this report)

Source: Portuguese-language post specifying decoy address, image counts,
B2/B3/B4 branches, four crypto chains with exact values, and an open final
problem (privkey for uncompressed pubkey `f4d1bbd9…55633559`).

## VERIFIED byte-exact (promoted to evidence)

- Decoy `1GSMG1JC9Y9SoWJVDdQzMD96K4t9SHkN3`: checksum INVALID (payload hash160
  `02eb6662…`). BUT live puzzle.png OCR shows ONLY the real target — decoy
  presence in the image NOT confirmed on live capture.
- CHAIN 1: 5-token direct concat + MD5 on small blob → 79 bytes
  `9fa9db91…0ed1c5` = K_C1(32) + K_C2(32) + E_C(15). K_C1 == decoded WIF
  `5K2by…pz8AT` key; E_C == claimed AES-key bytes 0:15. Password form is
  direct-string (not sha256-hex) — first authenticated non-hex use on this blob.
- CHAIN 2: WIF string direct + MD5 on p32 blob → 79 bytes
  `b06fa6f2…23a2` = K_S1 + K_S2 + E_S; E_S == key bytes 15:30.
- CHAIN 3: 1327 layout [K_B1 K_B2 E_B(15) K_H1 K_H2 E_H(15)] + mystery 1169;
  E_B[:2]=`59cc` completes AES key `38d4f4c90…59cc`. Half/Better base38 keys
  are NOT substrings — overlay reading, not field reading; both coexist.
- Rebuilt AES-256 key from three independent blobs matches the posted
  `38d4f4c90…259cc` at every byte: three-way cross-validation.

## NOT reproduced / open

- CHAIN 4 (1169→1168→XOR-mask `b657264f2f6e6921`→AES→1151 bytes,
  sha `e4269ed5…`, `+-` structure): 8 natural readings (drop-first/last ×
  xor-order × ECB/CBC0) all bad-padding, no marker. Underspecified
  (mode/IV/byte-selection unstated) — will not brute-force; needs the poster spec.
- Final step: all 8 chain keys → 16 addresses, ZERO hits on either funded
  target (list in report JSON). Poster admits all families negative.
- Image B2/B3/B4 (0x41D464, sums 490/497, merlons) + 87/84/15/9/1 counts:
  untested (grid bbox still blocked); note conflict with secondary 86/86
  counts — the claimed off-white cell is new information either way.
- Debate hexdump discrepancy explained: their head16 differs but tail16
  matches ours exactly → their variant decrypted same-blob/same-key with a
  wrong first block (wrong IV or re-wrapped input); their entropy verdict was
  computed on corrupted bytes.

## Verdict

Chains 1–3 are the first VERIFIED multi-step decrypts beyond Cosmic in this
workspace (passwords: direct-concat+MD5, WIF+MD5). They yield structured key
material that cross-validates three ways — but no prize key. The chain
terminates at CHAIN 4 (underspecified) and the open pubkey-X problem.
Status: genuine progress, puzzle still NOT SOLVED.
