#!/usr/bin/env python3
"""Build a networkx graph of the GSMG puzzle — every verified route and connection."""
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).resolve().parent
OUT_PNG = OUT / "route_graph.png"

# Node = (id, label, kind)
# kind -> color
NODES = {
    # --- stages / artifacts ---
    "puzzle":   ("gsmg.io/puzzle\n(puzzle.png)", "artifact"),
    "seed":     ("theseedisplanted\nflower password", "artifact"),
    "phase2":   ("Phase 2 / Phase 3\npage", "artifact"),
    "phase32":  ("Phase 3.2\n(Beaufort + VIC + p32)", "artifact"),
    "sal":      ("SalPhaseIon\n(textarea_0, 1075 tok)", "artifact"),
    "cosmic":   ("Cosmic Duality / Dualite\n(textarea_1, 1344B)", "artifact"),
    # --- solved decodes ---
    "url":      ("gsmg.io/theseedisplanted\n(down-first CCW spiral)", "solved"),
    "matrix_tok":("matrixsumlist\n(MID104 a/b)", "solved"),
    "enter_tok": ("enter\n(R4A a/b)", "solved"),
    "r1_tok":   ("lastwordsbeforearchichoice\n(R1 bigint-hex)", "solved"),
    "r2_tok":   ("thispassword\n(R2 bigint-hex)", "solved"),
    "r3_tok":   ("yourlastcommand\n(R3ENG + shabef)", "solved"),
    "r4c_tok":  ("secondanswer\n(R4C 'ans too')", "solved"),
    "lead91":   ("LEAD91 (91 a-i)\nunsolved digit stream", "open"),
    "tail570":  ("TAIL570 (570 a-i)\nunsolved digit stream", "open"),
    # --- crypto chain ---
    "xor7":     ("XOR of 7 SHA-256\na795de11...", "key"),
    "cosmic_pt":("1327B cosmic plaintext\n4f7a1e4e...\n=103x103 matrix + ':'", "decrypt"),
    "matrix":   ("103x103 bit matrix\ndensity 0.49, non-sym", "decrypt"),
    "halfbetter":("Half/Better keys\n(DEAD - dust addrs)", "dead"),
    "chain1":   ("CHAIN 1 small blob\n79B K_C1/K_C2/E_C", "decrypt"),
    "chain2":   ("CHAIN 2 p32 blob\n79B K_S1/K_S2/E_S", "decrypt"),
    "chain4":   ("CHAIN 4 1151B e4269ed5\n+- + 29B op + 35x32B", "decrypt"),
    "blocks35": ("35 blocks (32B each)\n7 marked 0x77 / 28 unmarked", "decrypt"),
    "bifid":    ("Bifid decode (DBIFHCEGA)\nTAIL570 -> BTCSEED...", "decrypt"),
    "even256":  ("even256 = 16x16 over 23 letters\nsha 1740b55b...", "open"),
    "xortri":   ("XOR triangle (Lucas)\n24/28/103 -> 16 survivors", "open"),
    # --- targets ---
    "target1":  ("1GSMG1JC9w...\n(h160 a9553269...) ~1.256 BTC", "target"),
    "target2":  ("17ucy1K9ZU...\n(h160 4bc46844...) ~3.7505 BTC", "target"),
    "door":     ("Third door 1NULY7...\n(h160 eb862e...) no preimage", "target"),
    # --- hypotheses ---
    "h_dim":    ("H-DIM-003 23/16/7\nframe (SUPPORTED)", "hyp"),
    "h_prime":  ("H-PRIME-002 4x24\nprime confinement (FALSIFIED)", "dead"),
    "h_sel":    ("H-SEL-001 selector\n(FALSIFIED)", "dead"),
    "h_mech":   ("H-MECH-001 Half/Better\n(FALSIFIED)", "dead"),
}

EDGES = [
    ("puzzle", "url", "spiral decode"),
    ("url", "seed", "POST password"),
    ("seed", "phase2", "flower -> URL"),
    ("phase2", "phase32", "SHA256 -> AES"),
    ("phase32", "sal", "Beaufort/VIC -> clue"),
    ("sal", "matrix_tok", "MID104 a/b->8bit"),
    ("sal", "enter_tok", "R4A a/b->8bit"),
    ("sal", "r1_tok", "R1 a-o->hex"),
    ("sal", "r2_tok", "R2 a-o->hex"),
    ("sal", "r3_tok", "R3ENG english"),
    ("sal", "r4c_tok", "R4C english"),
    ("sal", "lead91", "offset 0-91"),
    ("sal", "tail570", "offset 195-765"),
    ("matrix_tok", "xor7", "token 1/5"),
    ("enter_tok", "xor7", "token 2"),
    ("r1_tok", "xor7", "token 3"),
    ("r2_tok", "xor7", "token 4"),
    ("r3_tok", "xor7", "token 6"),
    ("r4c_tok", "xor7", "token 7"),
    ("xor7", "cosmic_pt", "EVP-MD5 decrypt"),
    ("cosmic", "cosmic_pt", "7-token XOR decrypt"),
    ("cosmic_pt", "matrix", "103x103 + 7-bit trail"),
    ("matrix", "halfbetter", "base-38 (DEAD)"),
    ("halfbetter", "target1", "miss"),
    ("halfbetter", "target2", "miss"),
    ("sal", "chain1", "small blob 5-token"),
    ("phase32", "chain2", "p32 blob WIF"),
    ("cosmic_pt", "chain4", "mask+raw32 decrypt"),
    ("chain1", "chain4", "E_C"),
    ("chain2", "chain4", "E_S"),
    ("chain4", "blocks35", "parse 31+35x32"),
    ("lead91", "bifid", "key DBIFHCEGA"),
    ("tail570", "bifid", "input period 570"),
    ("bifid", "even256", "even stream - I/O"),
    ("even256", "h_dim", "23 letters / 16x16"),
    ("blocks35", "xortri", "28 unmarked = T7"),
    ("chain4", "xortri", "24 groups = 3x16"),
    ("matrix", "xortri", "103 rows"),
    ("xortri", "h_dim", "16 survivors + 7 = 23"),
    ("blocks35", "target1", "35 keys miss"),
    ("blocks35", "target2", "35 keys miss"),
    ("chain4", "target1", "chain keys miss"),
    ("even256", "target1", "all readings miss"),
    ("even256", "target2", "all readings miss"),
    ("h_prime", "target1", "falsified"),
    ("h_sel", "target1", "falsified"),
    ("h_mech", "target2", "falsified"),
]

COLORS = {
    "artifact": "#4da6ff",
    "solved":   "#2ecc71",
    "open":     "#f39c12",
    "key":      "#9b59b6",
    "decrypt":  "#1abc9c",
    "dead":     "#e74c3c",
    "target":   "#e67e22",
    "hyp":      "#f1c40f",
}

def build() -> nx.DiGraph:
    G = nx.DiGraph()
    for nid, (label, kind) in NODES.items():
        G.add_node(nid, label=label, kind=kind)
    for a, b, elabel in EDGES:
        G.add_edge(a, b, label=elabel)
    return G

def draw(G: nx.DiGraph, path: Path) -> None:
    plt.figure(figsize=(30, 22))
    # Layered layout
    pos = nx.spring_layout(G, k=2.2, seed=42, iterations=80)
    # Manually improve readability: use multipartite-ish by degree
    node_colors = [COLORS[G.nodes[n]["kind"]] for n in G.nodes]
    node_sizes = [3200 if G.nodes[n]["kind"] in ("artifact","target") else 2400 for n in G.nodes]
    labels = {n: G.nodes[n]["label"] for n in G.nodes}
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes,
                           alpha=0.92, edgecolors="#222", linewidths=1.2)
    nx.draw_networkx_edges(G, pos, edge_color="#888", arrows=True, arrowsize=14,
                           width=1.4, connectionstyle="arc3,rad=0.08", alpha=0.6)
    edge_labels = {(a, b): d["label"] for a, b, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7,
                                 font_color="#333", bbox=dict(boxstyle="round,pad=0.2",
                                 fc="#ffffffec", ec="none"))
    nx.draw_networkx_labels(G, pos, labels, font_size=8.5, font_weight="bold",
                            font_color="#111")
    # Legend
    from matplotlib.lines import Line2D
    legend = [Line2D([0],[0], marker='o', color='w', markerfacecolor=c, markersize=14,
                     label=k) for k, c in COLORS.items()]
    plt.legend(handles=legend, loc="upper right", fontsize=12, framealpha=0.95)
    plt.title("GSMG 5 BTC Puzzle — Verified Route Graph (2026-09-10)", fontsize=18, pad=20)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(path, dpi=140, bbox_inches="tight")
    print(f"Saved {path}")

def stats(G: nx.DiGraph) -> None:
    kinds = {}
    for n in G.nodes:
        k = G.nodes[n]["kind"]
        kinds[k] = kinds.get(k, 0) + 1
    print(f"Nodes: {G.number_of_nodes()}  Edges: {G.number_of_edges()}")
    print(f"Kinds: {kinds}")
    # Dead-end reachability
    dead = [n for n in G.nodes if G.nodes[n]["kind"] == "dead"]
    print(f"Dead nodes: {len(dead)}")

if __name__ == "__main__":
    G = build()
    stats(G)
    draw(G, OUT_PNG)
    # Also dump a JSON for any downstream tooling
    import json
    data = {
        "nodes": [{"id": n, "label": G.nodes[n]["label"], "kind": G.nodes[n]["kind"]} for n in G.nodes],
        "edges": [{"from": a, "to": b, "label": d["label"]} for a, b, d in G.edges(data=True)],
    }
    (OUT / "route_graph.json").write_text(json.dumps(data, indent=2))
    print(f"Saved {OUT / 'route_graph.json'}")
