# CHECKPOINT-2026-09-04-SALFINAL

Date: 2026-09-04 (UTC). Investigation phase: controlled attack on
SalPhaseIon → prime/zeroing → yin-yang → final command mechanism.

## Frozen inputs (byte-identical, primary)

- S0 = SalPhaseIon textarea bytes, `raw/web/live/salphaseion/response.bin`
  textarea 0. Raw 2149 bytes, sha256
  `d39d10b1e1902d2620eb19ebcad4215e23c048de639466cca9a26bdc9303330c`.
  Byte-identical to canonical
  `raw/github/jackdevs66-GSMG5_CDuality/working/SalPhaseIon.txt`.
  Compact (whitespace removed): 1075 single-char tokens, sha256
  `26e37652067c549c0eee624356be9ffd40a243901197335a41f91fb6c78e6156`.
- Full HTML ART-004 sha256
  `a83d3de7810f26b19b4965339b76d403e44f6b6877e5d7de2555480ca1779d77`.
- Region map: `experiments/sal_final_search/sal_regions.json` (this checkpoint's
  machine-readable record: region_id, token offsets, char offsets, raw_bytes,
  alphabet, length, decoded_value where deterministic).

## Explicitly NOT inputs / oracles for the new attack

Per the 2026-09-04 directive, the following remain historical artifacts only and
MUST NOT be used as inputs, oracles, or acceptance criteria for the new search:

- Half (`0423d911...`)
- Better Half (`48cc46e6...`)
- `fc0c1b02` trail
- 103×103 matrix interpretation
- claimed 1327-byte plaintext (sha256 `4f7a1e4e...`) as solution
- Issue #108 correction (positions 18/51; already no-op on capture; 79-byte
  non-block-aligned concatenation)
- any claimed private key / WIF / address derived from the above

They may be cited in falsification records but no new branch may depend on them.

## Corrected structural fact (supersedes Dead End #1 framing)

- The small blob is 128 Base64 chars → 96 bytes (`Salted__` + 8 salt + 80 ct),
  salt `3ab585348552415d`, block-aligned. It is:
  `R3b64A (toks 895:958, 63) + z (tok 958, 1) + R4b (toks 999:1063, 64)`.
  The 40-char `enter` span (toks 959:999) is the page's encoded line break
  between the two 64-char lines (64-col wrapping). Concatenating A+B without the
  `z` (127 chars → padding error / 79-byte non-aligned reading) is therefore
  the wrong assembly and MUST NOT be used. This matches the independent
  `BLOB_B64` in floflo777 `tools/oracle.py` (verified locally: decodes to 96
  bytes, header `Salted__`, salt `3ab585348552415d`).
- `z` at token 958 is BLOB DATA (valid Base64), not a region separator. The
  `z` tokens at 765/829/859 are separators (outside a–o alphabet).

## Scope of the new attack

SalPhaseIon → official clues (primes 2,3,5,7; zeroed out; yinyang; yellow/blue;
`matrixsumlist`; `lastwordsbeforearchichoice`) → prime selection → zeroing →
matrix → sum list → yin/yang → password/command → encrypted material →
candidate key → EXACT target address:

- `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` (primary escrow, ~1.256 BTC)
- `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` (halving split-off, only if an
  independent payout link is established; otherwise recorded separately)

No branch becomes SOLUTION CANDIDATE without exact Base58Check equality via the
offline verifier. Printable ASCII, valid WIF, valid padding, matching length,
or self-referential hash equality are NOT acceptance.

## External corroboration imported (not trusted blindly)

- floflo777/open-crypto-puzzles `gsmg-io-5btc-puzzle` README + `tools/oracle.py`
  + `analysis/tested.md` + `analysis/leads.md` + `data/planted-addresses.csv`
  (fetched 2026-09-04): small-blob oracle (sha256(X) hex → EVP_BytesToKey →
  AES-256-CBC → 4 readings → uncompressed P2PKH), planted-address oracle
  (8 verified preimages + open third door `1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9`),
  Bifid-570 → BTCSEED → 285 → 256-symbol/23-letter claim, 335M+ negative ledger.
  All imported claims must be locally reproduced before use; sweep counts are
  SECONDARY until rerun here.
- Naddiseo `salphaseion.ipynb` cells 3/11/12 document the deterministic decodes
  re-verified here: 104-char a/b → `matrixsumlist`; 40-char a/b → `enter`;
  R1 bigint-hex → `lastwordsbeforearchichoice`; R2 bigint-hex → `thispassword`.

## Next steps (priority order)

1. Exact region reconstruction (this checkpoint + sal_regions.json).
2. Prime-position/prime-value + zeroing finite enumeration.
3. `matrixsumlist` as instruction; matrix-dimension factor/triangular tests.
4. Yin/yang complementary ops; prime-valued sum masks.
5. `lastwordsbeforearchichoice` contextual extraction; 7-token sequence tests.
6. Two-fragment (A+z+B) + Cosmic re-derivation ONLY after its inputs justified.
7. Bitcoin acceptance ONLY on exact target equality.
