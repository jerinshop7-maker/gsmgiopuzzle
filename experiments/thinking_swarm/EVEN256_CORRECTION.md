# Even-256 correction — verified 2026-09-09

Tool: `experiments/sal_final_search/sal_bifid.py` (5×5 DBIFHCEGA+alpha J-omitted, RC DECODE, period 570).

- Output len 570, head `BTCSEED`, Z count 1 at 97.
- `odd = r[0::2]` (1-indexed odd positions): 285, set {B,C,D,E}, I=0, O=0 → minus I/O = 285.
- `even = r[1::2]` (0-based odd): 285, I=13, O=16, total I/O = 29 (= R2_29 length), minus I/O = 256 over 23 letters {A-Z minus J,I,O}.
- Full I/O = 29. even256 head `TSEDMKAHSHKDSKVXPHRQEDBNSDPGPNNSSGDLNMUUQADLZLMFFSWKYUW…`, sha256 `1740b55ba5d224e86f61054bacd7caf90a8cf2c4418535c67d092903c4509f35`.
- Single deterministic oracle (dual-lock both forms × both digests + 6-construction door): even256 / full570 / even285 → 0 hits (waypoint, not key; consistent with 335M ledger).

Correction to Discovery #21: the `285→256/23-letter` step is IMPOSSIBLE on the odd stream (0 I/O) but EXACT on the even stream (29 I/O → 256). Prior sweep testing odd-stream I/O-drop tested the wrong half. The 256 object is real and structurally privileged (23-letter Base58-like alphabet, 29-drop echoing R2_29, Z@97 in yang stream) — its onward use as direct key remains negative; `lead 7` (256 = waypoint to AES route, not key) stands.

Repro: `python3 -c "import sys; sys.path.insert(0,'experiments/sal_final_search'); from sal_bifid import *; ..."` (see SWARM_REPORT §4).
