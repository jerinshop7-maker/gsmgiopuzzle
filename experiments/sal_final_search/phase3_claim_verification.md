# Phase-3 claim verification — 2026-09-04 (`verify_sig.py`, this report)

Claim under test (posted 2026-02-20, plus reproducible-derivation note):
Half `1JG648ya…` / Better Half `145ZQ9si…` derived via 7-token XOR → Cosmic
decrypt → 103×103 → +7-offset secondary → base-38, with two Bitcoin compact
signatures as proof of ownership, asking for the final prize step.

## What verifies (byte chain, all MATCH)

- XOR key `a795de11…0735`: MATCH from the 7 listed tokens in order.
- Cosmic decrypt (live textarea_1, salt `2d3f6fe06dc950e6`, EVP-MD5, raw-key
  password): 1327 bytes, SHA-256 `4f7a1e4e…c081`: MATCH.
- 103×103 row/col sums, secondary[i]=row[i]+col[(i+7)%103]: 103 chars in
  80..117, byte-identical to the quoted `Vmfgiel…` string: MATCH.
- Base-38 decode → 68 bytes: Half `0423d911…fcc35`, Better `48cc46e6…623971`,
  trail `fc0c1b02`: MATCH.
- All 4 quoted addresses (compressed + uncompressed, both keys): MATCH via the
  offline verifier (`verify_sig.py` self-test recovers correctly).

## What fails

- **Prize equality: False.** Neither key derives `1GSMG1JC…` or `17ucy1K9…`.
  Unchanged from Dead End #2 — reproduced here for the newly posted material.
- **Both ownership signatures: INVALID.** Offline compact-signature recovery
  (self-tested implementation) recovers unrelated addresses under the stated
  message and 5 message variants (strip/newline/lower/dash/spacing); none match
  either the compressed or uncompressed Half/Better addresses. The posted
  signatures do not authenticate ownership of the claimed addresses.
- **Chain activity is dust, not prize flows** (Blockstream read-only,
  2026-09-04): Half — 103 txs, funded 1,761,275 sats total (~0.0176 BTC), fully
  spent. Better — 103 txs, funded 1,785,085 sats (~0.0179 BTC), fully spent.
  ~92 tiny outputs each: solver-sweep dust after public key exposure (keys were
  published in earlier issues), not "funds to live."

## Verdict

The post re-derives the known reproducible intermediate (Dead Ends #2/#4) and
adds two non-verifying signatures plus already-public keys. It proves neither
ownership (signatures INVALID) nor prize control (addresses != targets; dust
only). **NOT a solution; prize remains unclaimed by this chain.**
Status of the Cosmic blob itself stays UNRESOLVED (frozen per checkpoint).

## Addendum: `validate_uniqueness.py` forensics

- As shipped, the script **does not run**: it reads `cosmic_duality.txt` from
  the repo root, but the file lives in `working/` → `FileNotFoundError`. The
  claimed "UNIQUE and HASH OK" output cannot come from this script as committed.
- With the path corrected (read-only rerun, same 7×5×6 = 210 combos): exactly
  1 success (p5=matrixsumlist, p6=yourlastcommand, p7=secondanswer). Mechanical
  reproduction: yes. Evidentiary value: none — P(exactly 1 hit | pure chance) =
  36.2%, P(≥1) = 56.0% at the 1/256 padding rate. "Exactly one" is the modal
  chance outcome, and the hash check is circular (hash of whatever padded).
- The README's own words ("constrained search + validation", "alternatives
  … tested and rejected", "only one candidate … yields valid padding") document
  a fitting procedure, not a derivation: p5/p7 were searched until padding
  validated, which ~56% of such searches do by accident.

## Addendum 2: "openssl says bad decrypt" rebuttal (openssl itself, 2026-09-04)

Claim: direct `openssl aes-256-cbc -a -d -k <hex>` gives "bad decrypt", so
pycryptodome "hides" the failure. Verdict: the CLI test is malformed —
`-k` takes a password STRING (here the ASCII hex, via default MD5 KDF), while
the solver feeds RAW unhexlified key bytes to EVP-MD5. Different password →
different key/iv → random bytes → bad padding. Expected, not exculpatory.
Proven with the same openssl 3.5.4 binary on live bytes:

1. Their exact `-k <hex>` command: reproduced → "bad decrypt" (exit≠0).
2. `-K/-iv` (solver's derived key/iv) on the header-included blob: exit 0 with
   garbage 1343 bytes — header must be stripped first (and a chance 1-byte pad
   passing here is itself a live padding-accident demo).
3. `-K/-iv` on the proper 1328-byte ciphertext: exit 0, **1327 bytes,
   SHA-256 `4f7a1e4e…c081` exactly** — openssl validates the identical bytes
   pycryptodome produced. Nothing is hidden; padding is genuinely valid under
   the solver's derivation.
Note: their `cosmic.text.bin` hash (`9a8172dd…`) differs from live textarea
bytes (`82947b02…`) despite a matching first line — re-wrapped copy, not page
bytes; decoded blob identical. This changes nothing about Dead End #5: valid
padding under a fitted key is still not the prize mechanism.

## Addendum 3: debate adjudication with new experiments (2026-09-04)

(a) Round-trip "proof" is a tautology — the critic is right. DECRYPT(CT,K2,IV)
then ENCRYPT back reproduces CT for EVERY key by AES reversibility; the salt
plays no role in re-encryption. It adds zero evidence beyond padding validity.
The claimant's "anchors the key" is formally wrong.

(b) "Find another validating F(p1..p7)" — done, against the claimant. 210
RANDOM 7-token gibberish sets through the identical Cosmic KDF/decrypt yield
**2 valid paddings** (vs their 1/210 "unique" hit). Chance predicts everything
observed; the constrained-set uniqueness is empty. P(≥1|210,chance)=56%.

(c) XOR-key → small/p32 locks (the hint names no blob — legitimate open test):
7 of 8 combos no-padding; one hit — XOR-hex + SHA-256 on the SMALL blob gives
a **79-byte** high-entropy plaintext (printable 0.37, sha `4f1e7315…`). Full
oracle: all 4 readings → 8 addresses, **zero prize hits** (`18fsPH5…`,
`1MrfiV1d…`, `1BRYY9Q4…`, `14VW54c2…`, `1MuTveMT…`, `1LwDhdPQ…`,
`18rnf1Wi…`, `14ahBDY1…`). At 8 tries the single padding is chance-rate
(~3% for ≥1); entropy + total miss = accident, recorded as such. (Curious:
79 bytes echoes the #108 claimed length — same accident class, still no key.)

(d) 1327 numerology: 1327 is PRIME (no factor structure; the 103×103 fit
forces a 7-bit trim). 23×57+16=1327 is true arithmetic matching the
architect's 23/7/16 headcount — with no proposed mechanism and no
falsification test, it stays numerology, not a lead. The same "7" appears in
the trim, the males, and the tokens: coincidence stacking, explicitly not
promoted.

(e) "Enter + thispassword are instructions, matrixsumlist is an extraction
instruction, last-words needs Matrix Reloaded transcript variants" — the
instruction-reading of tokens is compatible with our checkpoint (tokens as
mixed data/instructions/labels) and the transcript-variant last-words attack
is legitimate and UNTESTED here (we swept monologue-derived forms, not film-
transcript windows at scale). Logged as open, not as evidence.
