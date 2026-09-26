# Thinking Swarm 2 — 30 solving agents (2026-09-09)

Mode: thinking-only, no brute force, no broadcasts. Each agent: single branch, evidence-cited, one hypothesis.
Status: **PUZZLE NOT SOLVED.** All single-checks below: 0 EXACT hits.

## 1. Password-assembly branch (10 agents)

- CHAIN1 re-derived: 5-token direct+MD5 opens small blob to `9fa9db91…` (verified locally this session). Why 5 in that order (head-5/7, R1+R2 adjacency, matrixsumlist bracket), why direct (hex fails), why MD5 (SHA fails), why duplicate (bracket/odd-even lead). Lesson: real prize likely same family (literal concat, direct, MD5-primary) with different subset.
- R3ENG `shabef|ourfirsthintis|yourlastcommand`: `sha|bef` = SHA256-before (a1z26 b=2,e=5,f=6 → sha256); equation first-hint = last-command = hash-the-text loop (Roses → HASHTHETEXT → `SHA256(GSMGIO5BTC…)=89727c59…`). R4C `shabef|ans|too` = hash second answer too (universalizes to twin locks). Strongest X satisfying both: image text / route hash (already swept; exact-byte audit only remaining gap).
- shabef KDF: TRUE = `sha256-hex + EVP-SHA256` (all solved stages; author-posts convention). `direct+MD5` = decoy/legacy family (CHAIN1/Cosmic) — byte-exact but prizeless, foreign KDF, wrong assembly history, interpretive inputs, high entropy.
- enter: (a) structural skip in blob + literal in password. (b) trailing `\n` and (c) POST both rejected (break anchors / no DOM endpoint). Exact bytes: P5 69B, P7 list, BLOB128 128 chars.
- secondanswer: length-preserving swap `thispassword(12)→secondanswer(12)` → `matrixsumlist+enter+lastwords+secondanswer+matrixsumlist` (69) targeting large Cosmic blob (door2→17ucy hypothesis); p32 already opened by WIF chain (don't re-target primarily). 6 variants × 2 forms × 2 KDFs × 2 locks falsifies one-swap family if all miss.
- yourlastcommand: winner = `SHA256(image text)` command (`echo -n … | sha256sum`, `89727c…`), no lookahead, fits shabef + loop. WIF/5-token/thematrixhasyou/causality/HASHTHETEXT all stale/future/circular.
- thispassword: geometry+linguistics rank (c) R3ENG-cataphora > (b) blob > (a) literal. R1+R2 = operator (pointer+deref), not operand — explains verified-but-prizeless double-count.
- 7-vs-5: 1-5 data plane (small lock, direct) vs 6-7 control plane (pointers, not XOR material). 7-XOR falsified (duplicate cancel, 210→1 = 36% chance, random 2/210, foreign KDF).
- literal-visible ranking: `yourlastcommand` family only one satisfying grammar + gaps (`your last command` spaced/case/newline, full sentence spaced vs Q-76 nospace never tested locally). All other singletons swept or self-referential.
- first-hint identity: (A) Roses 2020-01-14 verbatim Hint > (C) matrixsumlist > (D) HASHTHETEXT > (B) follow-rabbit paraphrase. Consequence: replace literal p6 with X/sha256(X); breaks Cosmic key (expected — accident target).

## 2. Digit-stream branch (10 agents)

- LEAD91: triangular T13 sum-demo + 7×13 complement to MID 8×13 (7+8=15); DBIFHCEGA = bifid9 sorted disclosure in 17 chars (1/362880); solely key-source (IoC skewed, remainder noise); 96-config unique (1e-8) proves function.
- TAIL570: 2·3·5·19 (even split for R/C fractionation); uniform IoC ciphertext-like; I/O=29 expected-value coincidence (not R2 pointer); 256-remainder P~7% luck; ciphertext wiring yes, plaintext no.
- even256: waypoint not key (23-letter, 1158 bits max, uppercase unhashable directly, 335M direct-to-key negative). Next: rank-23 map → 16×16 → prime-zero rows/cols 2,3,5,7 → 32 sums → chr a+z (32-char lowercase X) → sha-hex → both locks + door. 1 primary + 3 forms max.
- prime filter single pick: TAIL bifid9 / S={2,3,5,7} full / idx1 / keepPrime-zeroing preserving length / 19×30 fwd (+ LEAD 7×13). Gap: prior sweep did P2357-idx0 + Pfull-idx1, missed P2357-idx1; keep-zero-preserve never decrypt-tested.
- matrix chain single pick: bifid9 → P2357-idx1-zero → 7×13/19×30 id-fwd → R+C offset+7 → mod10 digits (LEAD20+TAIL49=69) → sha256-hex → EVP-SHA256. Untested combination.
- yinyang acceptance Y1-Y7 (exact 285/285, prime ~half + LEAD skew, lossless complement, orientation/encoding invariance, R/C balance, alphabet lock). Combine via XOR/sum-diff/EC-half-double/interleave+hash — never rotation.
- 14×14 R/C→TAIL lift: outer-product Y_diff/Y_eq (10×57 primary per lone-odd parity) → 570-bit → a/b/raw bytes → 12 encodings. Zeroing preserves shape; square-after-delete only if degenerate.
- triangular H-TRI-001 (UNTESTED): LEAD as 1..13 left-aligned triangle → 13 row sums (+7 chr variants, both mappings, R/C) = 12 passwords max. Rectangular sweep never covered triangles.
- yellow/blue partition: 1..24 primes P={2,3,5,7,11,13,17,19,23}=9=Y vs 15=B (p~7.6e-7). Secondary matrix gives YR overlap 2/9 — reconcile order (spiral/raster × MSB/LSB × fwd/rev × 0/1 = ≤32) then 3B pack (B2 0x41D464 wt9=Y if Y=1) → door+locks (<500 tests). Blocked on 2019-original bbox.
- BTCSEED post-steps: freeze square, audit I/O, even-285 payload / odd-285 check, Z-split hypothesis, row-stream bits, oracle battery EXACT-only.

## 3. Doors/targets/blobs branch (10 agents)

- twins ordered chain (not pair): small→WIF→p32, E_C+E_S+E_B[:2]=38d4…59cc sharded assembly. Prize = collect 3 fragments.
- large blob = (a) bulk Chain4 container (16.6×, same 64-col/MD5 family, 59cc 1/65536 > 1/256 padding). Not (b) digit-SHA lock (wrong size/family, exhausted) nor (c) pure decoy. Password family: direct raw + MD5 from chain material; needs poster spec.
- Chain4 minimal spec listed (1169 parent/offsets, trim drop-first/last + byte, mask repeat/scope/order, AES mode/IV/KDF/direction, 1151−1168=17B accounting, 31B vs 48B header, a80a399a vs e4269ed5 staging, provenance) + exact questions for marcofortina/EnigmAnderson/imneomutfua + pubkey-X rule.
- pubkey-X: escrow P fully known; DLOG ⇒ forward-construct only; prime-row-select least-bad (swept negative); XOR-triangle unrankable (missing ca/cosmic_A/rows); half/double FALSIFIED; singular THE key kills multisig.
- NULY family: ≤32B raw-lpad (not sha brainwallet): 24 color cells spiral 7..191, ranks 1..24, P prime set echoing Y9/B15, keep-primes zero rest, 24b→3B → 00*29||X compressed vs NULY.
- ONE key verdict: 1GSMG ~1.256 live; 17ucy ~3.75 administrative accumulation (5→2.5→1.25), zero spends, post-halving, unclued pre-halving, VIC predates split, matrix keys falsified. Solve THE key for 1GSMG; 17ucy comes free iff C/U pair else stays creator funds.
- Decentraland triple: L/R = TAIL[0::2]/TAIL[1::2] digit halves; invert = negation mod9/10 (0-fixed); mix = subtract then matrixsumlist→SHA256→locks+door. LEAD = spectrogram config, not channel; yellow/blue = checksum (15→15×19); A/B, small/p32, raw/bitrev rejected as sources (solved/downstream/transport).
- friends class H-X-CONTEXT (no instances): short everyday affectionate utterance, lowercase spaceless, friend-recognizable, tech-executable; share class features only, offline harness, no sweeps/doxxing.
- tiny+<3: tiny = 80ct family selector (small/p32, keep tiny z; 80/1328 ~6% tiny fraction; stop staring at Cosmic) STRONGLY as pointer; <3 = (a) itself 2-char payload + (b) heart/class pointer SUPPORTED, (c) prime-2 backup, (d) pixels WEAK; dots = ceremony not key-material.
- numbers gate: SURVIVE 91,104,40,63,29,15/9,{2,3,5,7},64-col,80ct; DIE 1327/103/103-txs/23×57+16/7×3/210/5-BMPs/R18/1357. Only survivors may enter construction.

## 4. Single-checks executed 2026-09-09 (offline, dual-lock ×2 forms ×2 digests + 6-construction door)

- P6-pageorder-6concat, nospace-check, second-swap, shabefanstoo-swap, `your last command`, `Your Last Command`, `our first hint is your last command`, full35-nospace, image-text, route-hash, HASHTHETEXT → 0 lock hits, 0 door hits. Note: route-hash gave `small/hexdigest/md5` VALID padding without address match = chance-rate (~1/256), not signal.
- matrix-P2357idx1-RC+7 (69 digits `06967…`) → 0/0. sha256 `581c6a69…`.
- even256-16×16-primezero-a (32-char `kaawamartb…`) → 0/0.
- mono-15×19 subtract-then-sums (34 digits) → 0/0.
- Prior session: aswideasfirstoneseen family, riddle, literals, even256/full570/even285 → 0/0.

Targets matched: none. Puzzle remains NOT SOLVED. Next evidence-backed moves only: Chain4 spec from attestors; 2019-grid bbox from non-Wayback archives; creator square confirmation. No further CPU sweeps.
