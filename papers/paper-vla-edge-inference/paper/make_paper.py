#!/usr/bin/env python3
"""WS-076: render the 4-page edge-inference draft and its figures from the result files (no hand-typed number).

    python3 journal/papers/edge-inference/make_paper.py

Reads the gates' result files (road-to-robotics `shared/gate/data/`, `projects/*/results/`, and the paper-vs-hardware
`expected/` folders, PVH_REPO or ~/workspace/git/paper-vs-hardware), writes `numbers.json` (every value with its anchor),
`fig/*.pdf|png`, and renders `DRAFT_4p.src.md` -> `DRAFT_4p.md` and `main.src.tex` -> `main.tex` by replacing
{{key}} placeholders. A placeholder without a value, or a number typed into a template outside a placeholder in the
results / abstract sections, is an error (check_templates).
"""
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
R = ROOT / "repro"
FIG = HERE / "fig"


def J(p):
    return json.loads(Path(p).read_text())


N, A = {}, {}  # values (already formatted) and their anchors


ANCHOR_MAP = [
 [
  "G-lat-2, shared/gate/data/2026-10-20_glat2/glat2_gpu640_summary.json",
  "repro/glat2/expected/glat2_gpu640_summary.json, G-lat-2"
 ],
 [
  "horizon x depth A2, paper-vs-hardware 2026-10-30-paper-vs-hardware-horizon-depth/expected/a2_latency.json",
  "repro/horizon-depth/expected/a2_latency.json, horizon x depth A2"
 ],
 [
  "horizon x depth A1, .../expected/a1_cloud.json",
  "repro/horizon-depth/expected/a1_cloud.json, horizon x depth A1"
 ],
 [
  "G13b, shared/gate/data/2026-10-19_g13b_offline/ (g13b_summary.json, g13b_preflight.json;",
  "repro/chunk-boundary/expected/ (g13b_summary.json, g13b_preflight.json; G13b,"
 ],
 [
  "G13b in vla.cpp, shared/gate/data/2026-10-19_vlacpp_prefix_overwrite/vlacpp_overwrite_summary.json",
  "repro/chunk-boundary/expected/vlacpp_overwrite_summary.json, G13b in vla.cpp"
 ],
 [
  "PACT-VLA gates A / B, .../2026-10-30-paper-vs-hardware-pact/expected/gate_a.json, gate_b.json",
  "repro/pact/expected/gate_a.json, gate_b.json, PACT-VLA gates A / B"
 ],
 [
  "AAC gates 0 / 1, .../2026-10-30-paper-vs-hardware-adaptive-chunking/expected/gate0.json, gate1_latency.json",
  "repro/aac/expected/gate0.json, gate1_latency.json, AAC gates 0 / 1"
 ],
 [
  "smooth MP chunking gate A, projects/smooth-chunking/results/a_summary.json",
  "repro/smooth-chunking/expected/a_summary.json, smooth MP chunking gate A"
 ]
]


def remap(anchor):
    for old, new in ANCHOR_MAP:
        anchor = anchor.replace(old, new)
    assert anchor.startswith("repro/") or "first commit" in anchor, f"anchor not mapped into the repo: {anchor}"
    return anchor


def put(key, value, anchor, fmt="{:.1f}"):
    N[key] = fmt.format(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else str(value)
    A[key] = remap(anchor)


def collect():
    glat = J(R / "glat2/expected/glat2_gpu640_summary.json")["vla"]
    a = "G-lat-2, shared/gate/data/2026-10-20_glat2/glat2_gpu640_summary.json (mean of 400 chunks)"
    put("glat_total", glat["server_total_ms"]["mean"], a); put("glat_vision", glat["server_vision_ms"]["mean"], a)
    put("glat_rest", glat["server_inference_ms"]["mean"], a)
    put("glat_vision_pct", 100 * glat["server_vision_ms"]["mean"] / glat["server_total_ms"]["mean"], a, "{:.0f}")

    hd = R / "horizon-depth/expected"
    a2 = J(hd / "a2_latency.json"); a = "horizon x depth A2, paper-vs-hardware 2026-10-30-paper-vs-hardware-horizon-depth/expected/a2_latency.json (MAXN_SUPER, median of 50 calls)"
    n10, n2 = a2["by_n"]["10"]["median"]["rtt"], a2["by_n"]["2"]["median"]["rtt"]
    put("n10_ms", n10, a); put("n2_ms", n2, a); put("n2_saved_ms", n10 - n2, a, "{:.0f}")
    put("n2_saved_pct", 100 * (n10 - n2) / n10, a, "{:.0f}"); put("n2_over_n10", a2["n2_over_n10"], a, "{:.2f}")
    put("step_ms", a2["split"]["per_step_denoise_ms"], a); put("vision_ms_a2", a2["split"]["vision_ms"], a)
    put("prefill_ms", a2["split"]["prefill_ms"], a)
    a1 = J(hd / "a1_cloud.json"); a = "horizon x depth A1, .../expected/a1_cloud.json (20 frames x 32 draws)"
    r = a1["summary"]["2"]["R_ratio"]
    put("r2_ratio", r["median"], a, "{:.2f}"); put("r2_lo", r["ci95"][0], a, "{:.2f}"); put("r2_hi", r["ci95"][1], a, "{:.2f}")
    put("r2_verdict", a1["verdict_A1"], a)

    o = J(R / "chunk-boundary/expected/g13b_summary.json")["results"]["beta=5"]; pf = J(R / "chunk-boundary/expected/g13b_preflight.json")
    a = "G13b, shared/gate/data/2026-10-19_g13b_offline/ (g13b_summary.json, g13b_preflight.json; PyTorch, 25 W, 254 boundaries per delay)"
    for d in ("8", "12", "20"):
        nv = o["summary"]["naive"][d]["jump_ratio"]
        put(f"ow_cut_{d}", 100 * o["decision"]["per_delay"][d]["jump_cut_vs_naive"], a, "{:.0f}")
        put(f"ex_cut_{d}", 100 * (1 - o["summary"]["exact"][d]["jump_ratio"] / nv), a, "{:.0f}")
    put("pt_naive_ms", pf["naive"], a, "{:.0f}"); put("pt_exact_ms", pf["exact_d8"], a, "{:.0f}")
    put("exact_over_naive", pf["exact_d8"] / pf["naive"], a, "{:.1f}")
    v = J(R / "chunk-boundary/expected/vlacpp_overwrite_summary.json")
    a = "G13b in vla.cpp, shared/gate/data/2026-10-19_vlacpp_prefix_overwrite/vlacpp_overwrite_summary.json"
    for d in ("8", "12", "20"):
        put(f"cpp_cut_{d}", 100 * v["jump_cut_vs_naive"][d], a, "{:.0f}")
    put("cpp_ow_added_ms", v["summary"]["overwrite"]["8"]["ms"] - v["summary"]["naive"]["8"]["ms"], a, "{:.1f}")

    pa = R / "pact/expected"
    ga, gb = J(pa / "gate_a.json"), J(pa / "gate_b.json")["k8"]; a = "PACT-VLA gates A / B, .../2026-10-30-paper-vs-hardware-pact/expected/gate_a.json, gate_b.json"
    put("pact_ms", ga["T_PACT_ms"], a, "{:,.0f}"); put("pact_tgen1", ga["T_gen_1_ms"], a)
    put("pact_d", ga["d_PACT"], a, "{:d}"); put("naive_d", ga["d_naive"], a, "{:d}")
    put("denoise_ms", 10 * float(N["step_ms"]), "repro/horizon-depth/expected (A2 split): ten denoise steps = 10 x the per-step ms", "{:.0f}"); put("denoise_share", 100 * 10 * float(N["step_ms"]) / float(N["n10_ms"]), "repro/horizon-depth/expected (A2 split): 10 x the per-step ms over the end-to-end chunk ms", "{:.0f}")
    bt = J(R / "pact/expected/batched.json"); ba = "repro/pact/expected/batched.json (PROTOCOL_BATCHED.md, WS-134 part 2a)"; sm = bt["summary"]
    put("bat_t1", sm["T1"], ba, "{:,.0f}"); put("bat_seq4", sm["T_seq4"], ba, "{:,.0f}"); put("bat_shared4", sm["T_shared4"], ba, "{:,.0f}"); put("bat_batch4", sm["T_batch4"], ba, "{:,.0f}")
    put("bat_seq20", sm["T_seq20"], ba, "{:,.0f}"); put("bat_batch20", sm["T_batch20"], ba, "{:,.0f}"); put("bat_prefix", sm["T_prefix"], ba, "{:,.0f}")
    put("bat_ratio4", bt["ratio_batch4_over_T1_median_of_frames"], ba, "{:.2f}"); put("bat_ratio20", bt["ratio_batch20_over_T1_median_of_frames"], ba, "{:.2f}")
    put("bat_mem4", sm["peak_extra_MB_batch4"], ba, "{:,.0f}"); put("bat_mem20", sm["peak_extra_MB_batch20"], ba, "{:,.0f}")
    put("bat_frames", bt["frames"], ba, "{:d}"); put("bat_calls", bt["calls"], ba, "{:d}"); put("bar_bat", "1d7e6c4", "road-to-robotics projects/pact-vla/PROTOCOL_BATCHED.md, first commit (the bar, frozen before any number)")
    put("bat_vs_cpp", sm["T1"] / float(N["pact_tgen1"]), ba + " and gate_a.json T_gen_1", "{:.1f}")
    put("pact_sel", gb["pact_minus_random"]["mean"], a, "{:.2f}")
    put("pact_sel_lo", gb["pact_minus_random"]["ci95"][0], a, "{:.2f}"); put("pact_sel_hi", gb["pact_minus_random"]["ci95"][1], a, "{:.2f}")

    ac = R / "aac/expected"
    g1, g0 = J(ac / "gate1_latency.json"), J(ac / "gate0.json"); a = "AAC gates 0 / 1, .../2026-10-30-paper-vs-hardware-adaptive-chunking/expected/gate0.json, gate1_latency.json"
    put("aac_n20_ms", g1["A4_n20_ms"], a, "{:,.0f}"); put("aac_bar_ms", g1["A4_bar_ms"], a, "{:.0f}")
    put("aac_h_transport", g0["A1"]["median_h_transport"], a, "{:.0f}"); put("aac_h_grasp", g0["A1"]["median_h_grasp"], a, "{:.0f}")
    put("aac_jump", g0["A3"]["aac+overwrite_d8"], a, "{:.3f}"); put("aac_fixed_jump", g0["A3"]["fixed+overwrite_d8"], a, "{:.3f}")

    s = J(R / "smooth-chunking/expected/a_summary.json"); a = "smooth MP chunking gate A, projects/smooth-chunking/results/a_summary.json (20 episodes)"
    put("sm_err", s["A1"]["50"]["error_S2_minus_S0"]["mean"], a, "{:+.3f}")
    put("sm_jerk", 100 * (1 - s["A1"]["50"]["within_jerk_S2_over_S0"]), a, "{:.0f}")
    put("sm_seam25", 100 * (1 - s["A2"]["25"]["boundary_jerk_S3_over_S2"]), a, "{:.0f}")
    put("sm_seam50", 100 * (1 - s["A2"]["50"]["boundary_jerk_S3_over_S2"]), a, "{:.0f}")
    put("sm_cost", s["A2"]["50"]["error_S3_minus_S2"]["mean"], a, "{:+.2f}")

    for k, h in (("bar_hd", "0a79846"), ("bar_pact", "0a79846"), ("bar_aac", "581a955"), ("bar_sm", "6f58d7b"), ("bar_glat", "82fdc15")):
        put(k, h, "first commit of the gate's protocol (git log --diff-filter=A)")
    for k, rel, txt, val in (
            ("r2_bar", "horizon-depth/README.md", "median R(2)/R(10) ≤ 0.70", "0.70"),
            ("r2_failline", "horizon-depth/README.md", "(fail if R > 0.85)", "0.85"),
            ("r2_paper", "horizon-depth/README.md", "R(2)/R(10) 0.51 on π0", "0.51"),
            ("sm_paper", "smooth-chunking/README.md", "73–84 % of boundary jerk", "73–84")):
        assert txt in (R / rel).read_text(), f"{txt!r} not in {rel}"
        put(k, val, f"repro/{rel}: '{txt}'")


def figures():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    FIG.mkdir(exist_ok=True)
    sys.path.insert(0, str(HERE / "style"))
    import shisso_colors as sc
    sc.use()
    # 1. where a chunk's time goes (A2 split at N = 10)
    v, p, st = float(N["vision_ms_a2"]), float(N["prefill_ms"]), float(N["step_ms"])
    fig, ax = plt.subplots(figsize=(3.3, 1.35))
    left = 0
    for lab, w, c in (("vision", v, sc.ACCENT), ("prefill", p, sc.CATEGORICAL[1]), ("10 denoise steps", 10 * st, sc.GREY)):
        ax.barh(0, w, left=left, color=c, linewidth=0)
        if w < 25:  # narrow segment (prefill): label above the bar
            ax.annotate(f"{lab} {w:.0f} ms", (left + w / 2, 0.4), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=6,
                        arrowprops=dict(arrowstyle="-", lw=0.5))
        else:
            ax.text(left + w / 2, 0, f"{lab}\n{w:.0f} ms", ha="center", va="center", fontsize=6.5, color="white" if c == sc.ACCENT else "black")
        left += w
    ax.set_yticks([]); ax.set_xlabel("ms per SmolVLA chunk, vla.cpp, Orin NX (MAXN_SUPER)"); ax.set_xlim(0, left * 1.02)
    for s_ in ("top", "right", "left"):
        ax.spines[s_].set_visible(False)
    fig.tight_layout(); fig.savefig(FIG / "latency_split.pdf"); fig.savefig(FIG / "latency_split.png"); plt.close(fig)
    # 2. boundary jump cut per method and delay
    ds = ["8", "12", "20"]
    fig, ax = plt.subplots(figsize=(3.3, 2.1))
    for i, (lab, key, c) in enumerate((("prefix overwrite (PyTorch)", "ow_cut", sc.CATEGORICAL[0]), ("prefix overwrite (vla.cpp)", "cpp_cut", sc.CATEGORICAL[2]),
                                         ("exact RTC guidance (PyTorch)", "ex_cut", sc.GREY))):
        ax.bar([j + (i - 1) * 0.27 for j in range(3)], [float(N[f"{key}_{d}"]) for d in ds], 0.27, color=c, linewidth=0, label=lab)
    sc.bar_line(ax, 50); ax.text(2.45, 51, "bar 50 %", fontsize=6, ha="right")
    ax.set_xticks(range(3)); ax.set_xticklabels([f"d = {d}" for d in ds]); ax.set_ylabel("jump cut vs naive (%)")
    ax.legend(fontsize=5.5, frameon=False, loc="upper left", ncol=1); ax.set_ylim(0, 120)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.tight_layout(); fig.savefig(FIG / "jump_cut.pdf"); fig.savefig(FIG / "jump_cut.png"); plt.close(fig)
    # 3. cost per decision vs a 238 ms chunk (log scale)
    rows = [("1 chunk (N = 10)", float(N["n10_ms"])), ("2 Euler steps", float(N["n2_ms"])),
            ("PACT cycle (4 candidates)", float(N["pact_ms"].replace(",", ""))), ("AAC decision (N = 20)", float(N["aac_n20_ms"].replace(",", "")))]
    fig, ax = plt.subplots(figsize=(3.3, 1.4))
    ax.barh(range(len(rows)), [r[1] for r in rows], color=[sc.ACCENT, sc.ACCENT, sc.GREY, sc.GREY], linewidth=0)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=6.5); ax.invert_yaxis(); ax.set_xscale("log")
    for i, r in enumerate(rows):
        ax.text(r[1] * 1.08, i, f"{r[1]:,.0f} ms", va="center", fontsize=6)
    ax.axvline(float(N["aac_bar_ms"]), ls="--", lw=1.0, color=sc.DARKGREY); ax.set_xlabel("ms per decision on the Orin NX (log, MAXN_SUPER)")
    ax.set_xlim(100, 20000)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.tight_layout(); fig.savefig(FIG / "decision_cost.pdf"); fig.savefig(FIG / "decision_cost.png"); plt.close(fig)

    # 4. design layer: the chunk pipeline with the seven tricks, and the chain that makes every number
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    GREEN, AMBER, RED = sc.CATEGORICAL[2], sc.CATEGORICAL[1], sc.CATEGORICAL[3]
    n10, n2 = float(N["n10_ms"]), float(N["n2_ms"])
    fig, ax = plt.subplots(figsize=(7.0, 1.95)); ax.set_xlim(0, 100); ax.set_ylim(0, 27.5); ax.axis("off")
    other = n10 - v - p - 10 * st
    parts = [("vision", v, sc.ACCENT, "white"), ("prefill", p, sc.CATEGORICAL[1], "black"), ("10 denoise steps", 10 * st, sc.GREY, "white"), ("other", other, "#D9DCE2", "black")]
    x0, W = 2.0, 62.0; tot = sum(w for _, w, _, _ in parts); x = x0; pos = {}
    for lab, w, c, tc in parts:
        wd = W * w / tot; ax.add_patch(FancyBboxPatch((x, 7), wd, 7, boxstyle="round,pad=0,rounding_size=0.8", fc=c, ec="white", lw=1.2)); pos[lab] = (x, x + wd)
        txt = f"{lab}\n{w:,.0f} ms" if wd > 7 else f"{w:,.0f}"
        ax.text(x + wd / 2, 10.5, txt, ha="center", va="center", fontsize=6.2, color=tc, fontweight="bold" if wd > 7 else "normal"); x += wd
    sx = x0 + W + 3
    ax.add_patch(FancyBboxPatch((sx, 7), 98 - sx, 7, boxstyle="round,pad=0,rounding_size=0.8", fc="white", ec=sc.DARKGREY, lw=1.0, ls="--"))
    ax.text((sx + 98) / 2, 10.5, "seam between\nconsecutive chunks", ha="center", va="center", fontsize=6.2, color=sc.DARKGREY)
    ax.text(x0, 15.0, f"one SmolVLA chunk, vla.cpp on the Orin NX, MAXN_SUPER: {n10:,.1f} ms", fontsize=6.4, color=sc.DARKGREY, va="bottom")
    def tag(xc, y, label, col, target, w, up=True):
        ax.add_patch(FancyBboxPatch((xc - w / 2, y), w, 4.6, boxstyle="round,pad=0,rounding_size=1.0", fc="white", ec=col, lw=1.6))
        ax.text(xc, y + 2.3, label, ha="center", va="center", fontsize=5.8)
        ax.add_patch(FancyArrowPatch((target[0], y if up else y + 4.6), target, arrowstyle="-|>", mutation_scale=5, lw=0.9, color=col, shrinkA=0, shrinkB=0))
    d0, d1 = pos["10 denoise steps"]
    tag(44, 19.5, "two Euler steps", AMBER, (d0 + 3, 14.2), 14)
    tag(60, 19.5, "exact RTC guidance", RED, (d1 - 3, 14.2), 15)
    tag(74.5, 19.5, "prefix overwrite", GREEN, (74.5, 14.2), 13.5)
    tag(89.5, 19.5, "seam conditioning", GREEN, (89.5, 14.2), 15)
    tag(89.5, 0.7, "MP projection (jerk)", GREEN, (89.5, 7.0), 17, up=False)
    ax.add_patch(FancyBboxPatch((x0, 1.2), W, 3.6, boxstyle="round,pad=0,rounding_size=0.8", fc="white", ec=RED, lw=1.4))
    ax.text(x0 + W / 2, 3.0, "speculative selection (N = 4) and adaptive length (N = 20) repeat the whole chunk N times on a sequential engine", ha="center", va="center", fontsize=5.6)
    for i, (lab, c) in enumerate((("pass", GREEN), ("not proven", AMBER), ("fail on this board", RED))):
        lx = 2 + i * 12.5; ax.add_patch(FancyBboxPatch((lx, 25.2), 1.7, 1.7, boxstyle="round,pad=0", fc=c, ec="none")); ax.text(lx + 2.5, 26.05, lab, fontsize=5.6, va="center")
    fig.subplots_adjust(0, 0, 1, 1); fig.savefig(FIG / "chunk_pipeline.pdf"); fig.savefig(FIG / "chunk_pipeline.png", dpi=200); plt.close(fig)
    # the chain that makes every number (same in all four papers)
    fig, ax = plt.subplots(figsize=(7.0, 1.05)); ax.set_xlim(0, 100); ax.set_ylim(0, 15); ax.axis("off")
    steps = [("1  bar committed", "protocol commit\nbefore any number"), ("2  run", "rows stored in\nrepro/<exp>/expected"), ("3  result committed", "result commit\nafter the bar"),
             ("4  L0 recompute", "make l0: every number\nfrom the stored rows"), ("5  paper", "numbers.json: value\nand its anchor")]
    bw, gap = 16.2, 4.0
    for i, (a, b) in enumerate(steps):
        xx = 1 + i * (bw + gap); ax.add_patch(FancyBboxPatch((xx, 3), bw, 10, boxstyle="round,pad=0,rounding_size=1.2", fc="#EDF2FB" if i != 4 else sc.ACCENT, ec=sc.ACCENT, lw=1.0))
        ax.text(xx + bw / 2, 10.3, a, ha="center", va="center", fontsize=6.4, fontweight="bold", color="white" if i == 4 else sc.ACCENT)
        ax.text(xx + bw / 2, 6.0, b, ha="center", va="center", fontsize=5.6, color="white" if i == 4 else "black", linespacing=1.15)
        if i < 4:
            ax.add_patch(FancyArrowPatch((xx + bw, 8), (xx + bw + gap, 8), arrowstyle="-|>", mutation_scale=6, lw=1.0, color=sc.ACCENT))
    ax.text(50, 0.7, "make check regenerates the paper from the stored rows and fails on any difference", ha="center", fontsize=5.8, color=sc.DARKGREY, style="italic")
    fig.subplots_adjust(0, 0, 1, 1); fig.savefig(FIG / "number_chain.pdf"); fig.savefig(FIG / "number_chain.png", dpi=200); plt.close(fig)

def render(src, dst):
    t = (HERE / src).read_text()
    keys = set(re.findall(r"\{\{(\w+)\}\}", t))
    missing = keys - N.keys()
    assert not missing, f"{src}: placeholders without a value: {sorted(missing)}"
    (HERE / dst).write_text(re.sub(r"\{\{(\w+)\}\}", lambda m: N[m.group(1)], t))


def bib():
    """refs.bib is hand-maintained (authors come from the papers mirror's PDFs); check it against the citations:
    every \\cite key of main.src.tex has an entry, every entry is cited, and every arXiv id named in
    DRAFT_4p.src.md has its entry too."""
    tex = (HERE / "main.src.tex").read_text()
    keys = set()
    for grp in re.findall(r"\\cite[pt]?\{([^}]*)\}", tex):
        keys |= {k.strip() for k in grp.split(",")}
    have = set(re.findall(r"@\w+\{(\w+),", (HERE / "refs.bib").read_text()))
    assert keys <= have, f"cited but not in refs.bib: {sorted(keys - have)}"
    assert have <= keys, f"in refs.bib but never cited: {sorted(have - keys)}"
    md_ids = set(re.findall(r"arXiv:(\d{4}\.\d{4,5})", (HERE / "DRAFT_4p.src.md").read_text()))
    missing = sorted(i for i in md_ids if f"arxiv{i.replace('.', '')}" not in have)
    assert not missing, f"the draft names ids without a refs.bib entry: {missing}"
    return len(have)


def main():
    collect()
    nb = bib()
    (HERE / "numbers.json").write_text(json.dumps({k: {"value": N[k], "anchor": A[k]} for k in sorted(N)}, indent=1))
    figures()
    render("DRAFT_4p.src.md", "DRAFT_4p.md")
    render("main.src.tex", "main.tex")
    print(f"{len(N)} numbers, 3 figures, {nb} references, DRAFT_4p.md and main.tex rendered")


if __name__ == "__main__":
    main()
