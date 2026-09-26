# Route Graph — 2026-09-10 session

## What this is

A networkx visualization (`route_graph.png`) and machine-readable dump
(`route_graph.json`) of every verified route and connection in the GSMG 5 BTC
puzzle, colored by node kind:

- blue = primary artifact (live/canonical bytes)
- green = SOLVED decode (verified on primary bytes)
- orange = OPEN object (reproducible but unkeyed)
- purple = derived key material
- teal = verified decrypt/intermediate
- red = DEAD/FALSIFIED branch
- dark orange = funded target / door (exact offline oracle)
- yellow = SUPPORTED structural hypothesis

## Key findings this session (discoveries #37–#39)

1. **"Dualite" == Cosmic Duality** (byte-identical, sha `b1895055…`). The
   "second blob never opened" side-route is resolved — it is the same blob that
   opens to `4f7a1e4e…` (1327B = 103×103 matrix + 7-bit trail `:` = 0x3A).

2. **even256 structural frame** (SUPPORTED): Bifid decode of TAIL570
   (DBIFHCEGA, period 570) → even stream − I/O = 256 chars over 23 letters
   (sha `1740b55b…`). This instantiates the author's final clue:
   - 23 letters = "over twentythree ciphers"
   - 256 = 16×16 = "sixteen encryptions"
   - 7 tokens = "seven intertwined passwords" (XORed → `a795de11…`)
   - 16 + 7 = 23

3. **XOR-triangle → 16 survivors** (Lucas theorem, GalloClaudio64's "triangular
   … XOR triangle" hint): 24 CT-groups, 28 unmarked blocks (T7), and 103 matrix
   rows each reduce to exactly 16 survivors, matching "sixteen encryptions".

## Open bottleneck

The combine function that maps the 16 selected encryptions + 7 intertwined
passwords to the actual private key remains OPEN. The clue's "bruteforcing
might be required" points at a C(23,16) = 245,157 selection sweep, but the
readout function (16 values → key) is not artifact-stated, so it is held under
the workspace's no-fishing rule until a stated function appears.

## Rebuild

```
python3 derived/reports/04-route-graph/build_graph.py
```

Requires `networkx` and `matplotlib`.
