#!/usr/bin/env python3
"""WS-064 gate A (projects/smooth-chunking/PROTOCOL.md, frozen 2026-10-31): ProMP projection and via-point conditioning
of SmolVLA chunks, training-free, offline on the 20 G13b episodes of so101_bowls_all.

Chunks: G13b's naive chunks regenerated with G13b's own hook (scripts/run_g13b_rtc_offline.py; its per-boundary rows
are no longer on disk). One chunk per frame f, seed = seed·1 000 003 + episode·10 007 + f + 1 (G13b's "new chunk"
rule), so a stream's chunk at f is G13b's naive chunk at the boundary f. Frames f = 0, s, 2s, … with f + H ≤ T; the
s = 50 frames are a subset of the s = 25 frames (same chunks). Sync (no inference delay): the chunk planned at f is
executed from its row 0.

Streams (rows of the commanded stream at frames f … f + s − 1):
  S0 raw:   chunk_f[0:s]
  S1 +WS:   (s = 25 only) linear ramp from chunk_{f−s}[s:H] to chunk_f[0:H−s], weight k/(s−1) on the new chunk
  S2 proj:  Ψŵ_f[0:s], ŵ_f = (ΨᵀΨ + λI)⁻¹Ψᵀ chunk_f, n = 10 Gaussian bases, λ = 10⁻⁶, normalised action space
  S3 cond:  S2 with ŵ_f conditioned (Eq. 3–4, Σ_w = I, Σ*_y = 10⁻¹, m = 1) on the previous stream's last commanded
            action as the via-point at τ = 0, per dimension; the gripper then clamped to its command floor
The first chunk of an episode has no seam (no blending, no conditioning).

Metrics (per episode, then medians over episodes; paired differences with an episode bootstrap, 2 000 resamples,
seed 0): within-chunk jerk = mean |Δ³a|·30³ of the 5 arm joints in normalised units, a sample at index i (the
difference over a[i−1 … i+2]) counted within-chunk if more than 2 steps from every seam, boundary if within ±2 steps;
clamp-proxy events per 100 commanded steps (limits in results/clamp_limits.json, from the demos, committed before any
stream is scored); error vs recorded = mean |stream − recorded actions| in degrees over the executed windows,
5 arm joints (G13b's metric with d = 0); first-action change |a₀(stream) − a₀(S0)| in degrees.

Checks (2 episodes, before the full run; stop if any fails): (1) the projection of a demonstrated chunk decodes to it
within 0.5° mean; (2) with Σ*_y = 10⁻¹² the conditioned first row equals the via-point to 10⁻⁶; (3) on the same
regenerated chunks, G13b's own boundary_metrics drift at d = 8 for its naive method equals this script's error
function at d = 8 to 0.01°.

    IMAGE=lerobot-jetson:rc LEROBOT_SRC=image shared/gate/jetson_run.sh --python scripts/smooth_chunking.py limits \\
        --out projects/smooth-chunking/results/clamp_limits.json
    … smooth_chunking.py chunks --policy-path ravediamond/smolvla_2026-09-24_14-34-40 --revision c1d76f6 \\
        --out outputs/smooth/chunks [--episodes 2]        # resumable per episode
    … smooth_chunking.py checks --chunks outputs/smooth/chunks --out projects/smooth-chunking/results/checks.json
    … smooth_chunking.py score --chunks outputs/smooth/chunks --out projects/smooth-chunking/results
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "src"))
G13B = ROOT / "shared/gate/data/2026-10-19_g13b_offline/g13b_summary.json"
REPO = "ravediamond/so101_bowls_all"
H, FPS, ARM, GRIP = 50, 30, slice(0, 5), 5
N_BASIS, LAM, SIGMA_Y = 10, 1e-6, 1e-1
GRID = (1e-3, 1e-2, 1e-1, 1.0)
GEOMS = {25: ("S0", "S1", "S2", "S3"), 50: ("S0", "S2", "S3")}
N_BOOT = 2000


# --------------------------------------------------------------------------------------------- basis and conditioning
def basis(n=N_BASIS, h=H):
    """n Gaussian bases over τ ∈ [0, 1], centres uniform, σ = half the centre spacing, rows normalised to sum to one."""
    tau = np.linspace(0, 1, h); c = np.linspace(0, 1, n); sig = (c[1] - c[0]) / 2
    phi = np.exp(-0.5 * ((tau[:, None] - c[None, :]) / sig) ** 2)
    return phi / phi.sum(1, keepdims=True)


PSI = basis()
PROJ = np.linalg.solve(PSI.T @ PSI + LAM * np.eye(N_BASIS), PSI.T)        # ŵ = PROJ @ A


def project(chunk):
    """(H, D) normalised chunk -> weights (n, D)."""
    return PROJ @ chunk


def condition(w, y, sigma_y=SIGMA_Y):
    """ProMP conditioning at τ = 0 per dimension: μ' = μ + K (y − ψ₀μ), K = Σ_w ψ₀ᵀ (Σ*_y + ψ₀ Σ_w ψ₀ᵀ)⁻¹, Σ_w = I."""
    psi0 = PSI[0]
    k = psi0 / (sigma_y + psi0 @ psi0)                                      # (n,)
    return w + np.outer(k, y - psi0 @ w)


# --------------------------------------------------------------------------------------------- data and chunks
def affine(model):
    """robot = sc · model + off per dimension (the postprocessor is affine)."""
    import torch
    real = model.real_dim
    z = torch.zeros(model.horizon, real); o = torch.ones(model.horizon, real)        # predict returns real dims
    off = model.to_robot(z)[0, :real]; sc = model.to_robot(o)[0, :real] - off
    return sc, off


def cmd_limits(a):
    """Clamp-proxy limits from the demos: per joint 1.3 × p99.9 |commanded speed| (deg/s) + 0.15 rad/s in deg/s."""
    from so101_harness.episodes import EpisodeDataset, download
    ds = EpisodeDataset(download(REPO))
    sp = np.concatenate([np.abs(np.diff(ds.actions(e), axis=0)) * FPS for e in ds.episode_indices()])
    lim = 1.3 * np.percentile(sp, 99.9, axis=0) + np.degrees(0.15)
    grip_floor = float(min(ds.actions(e)[:, GRIP].min() for e in ds.episode_indices()))
    res = {"rule": "1.3 × p99.9 commanded speed of the demos + 0.15 rad/s, per joint, deg/s", "deg_per_s": lim.tolist(),
           "gripper_command_floor": grip_floor, "episodes": len(ds.episode_indices())}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(res, indent=1)); print(json.dumps(res))


def cmd_chunks(a):
    import run_g13b_rtc_offline as G
    from so101_harness.episodes import download
    G.check_hook()
    from huggingface_hub import snapshot_download
    model = G.LeRobotSmolVLA(snapshot_download(a.policy_path, revision=a.revision), a.device)
    sc, off = affine(model)
    root = Path(download(REPO, with_videos=True))
    eps = json.loads(G13B.read_text())["meta"]["episodes"][: a.episodes]
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    (out / "affine.json").write_text(json.dumps({"scale": sc.tolist(), "offset": off.tolist()}))
    for e, ep in enumerate(eps):
        f_out = out / f"ep{ep}.npz"
        if f_out.exists():
            continue
        data = G.load_episode(root, ep, 25, model.image_keys)
        T = data["T"]; frames = [f for f in range(0, T, 25) if f + H <= T and f in data["obs"]]
        ch_n, ch_d = [], []
        for f in frames:
            c = model.predict(data["obs"][f], model.noise(0 * 1_000_003 + e * 10_007 + f + 1), "naive", 0, None)
            ch_n.append(c[:, : model.real_dim].numpy()); ch_d.append(model.to_robot(c))
        np.savez(f_out, frames=np.array(frames), chunks_norm=np.array(ch_n), chunks_deg=np.array(ch_d),
                 recorded=data["actions"], T=T, e=e)
        print(f"episode {e + 1}/{len(eps)} ({ep}): {len(frames)} chunks", flush=True)


# --------------------------------------------------------------------------------------------- streams and metrics
def stream(kind, s, d, sigma_y=SIGMA_Y, floor_norm=None):
    """Commanded stream (normalised) for one episode and geometry; seams = the frame index of each chunk switch."""
    frames, ch = d["frames"], d["chunks_norm"]
    keep = [i for i, f in enumerate(frames) if f % s == 0]
    rows, seams, first = [], [], []
    prev, prev_last = None, None
    for j, i in enumerate(keep):
        c = ch[i]
        if kind == "S0":
            seg = c[:s]
        elif kind == "S1":
            if prev is None:
                seg = c[:s]
            else:
                wnew = (np.arange(s) / (s - 1))[:, None]
                seg = (1 - wnew) * prev[s:H] + wnew * c[: H - s]
        else:
            w = project(c)
            if kind == "S3" and prev_last is not None:
                w = condition(w, prev_last, sigma_y)
            seg = (PSI @ w)[:s]
            if kind == "S3" and floor_norm is not None:
                seg[:, GRIP] = np.maximum(seg[:, GRIP], floor_norm)
        if j:
            seams.append(sum(len(r) for r in rows))                         # index of the first row of this chunk
        first.append(seg[0].copy())
        rows.append(seg); prev = c; prev_last = seg[-1]
    return np.concatenate(rows), np.array(seams, int), np.array(first)


def jerks(a, seams):
    j = np.abs(np.diff(a[:, ARM], n=3, axis=0)).mean(1) * FPS ** 3          # sample i spans a[i … i+3]
    pos = np.arange(len(j)) + 1                                              # its centre index
    near = np.zeros(len(j), bool)
    for sm in seams:
        near |= np.abs(pos - sm) <= 2
    return float(j[~near].mean()) if (~near).any() else float("nan"), float(j[near].mean()) if near.any() else float("nan")


def score_episode(d, s, kind, sc, off, lim, sigma_y=SIGMA_Y, floor_norm=None):
    a, seams, first = stream(kind, s, d, sigma_y, floor_norm)
    deg = a * sc + off
    rec = d["recorded"][: len(deg)]
    within, boundary = jerks(a, seams)
    speed = np.abs(np.diff(deg, axis=0)) * FPS
    clamps = float((speed > lim[None, :]).sum() / max(len(speed), 1) * 100)   # per joint, per 100 steps
    err = float(np.abs(deg[: len(rec), ARM] - rec[:, ARM]).mean())
    return {"within_jerk": within, "boundary_jerk": boundary, "clamps_per_100": clamps, "error_deg": err,
            "first": first * sc + off, "n_steps": len(a)}


def boot(x, seed=0):
    rng = np.random.default_rng(seed); x = np.asarray(x, float)
    b = [rng.choice(x, len(x)).mean() for _ in range(N_BOOT)]
    return [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]


def load_chunks(path):
    out = []
    for f in sorted(Path(path).glob("ep*.npz")):
        z = np.load(f); out.append({k: z[k] for k in z.files})
    return out


def cmd_checks(a):
    import run_g13b_rtc_offline as G
    eps = load_chunks(a.chunks)[:2]
    aff = json.loads((Path(a.chunks) / "affine.json").read_text()); sc, off = np.array(aff["scale"]), np.array(aff["offset"])
    worst1, worst2, worst3 = 0.0, 0.0, 0.0
    for d in eps:
        rec = d["recorded"]
        for f in d["frames"]:
            demo = (rec[f: f + H] - off) / sc
            dec = PSI @ project(demo)
            worst1 = max(worst1, float(np.abs(dec * sc - demo * sc)[:, ARM].mean()))
        c = d["chunks_norm"][1]
        y = d["chunks_norm"][0][24]
        w = condition(project(c), y, 1e-12)
        worst2 = max(worst2, float(np.abs((PSI @ w)[0] - y).max()))
        for k in range(1, len(d["frames"])):
            t = d["frames"][k]
            prev, new = d["chunks_deg"][k - 1], d["chunks_deg"][k]
            g = G.boundary_metrics(prev, new, 25, 8, rec[t:])["drift"]
            rr = rec[t + 8: t + 8 + 25, ARM]
            mine = float(np.abs(new[8: 8 + len(rr), ARM] - rr).mean())
            worst3 = max(worst3, abs(g - mine))
    res = {"check1_projection_decode_max_mean_deg": worst1, "check1_ok": worst1 <= 0.5,
           "check2_condition_first_row_max_abs": worst2, "check2_ok": worst2 <= 1e-6,
           "check3_g13b_drift_vs_mine_max_abs_deg": worst3, "check3_ok": worst3 <= 0.01, "episodes": len(eps)}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(res, indent=1)); print(json.dumps(res, indent=1))
    if not (res["check1_ok"] and res["check2_ok"] and res["check3_ok"]):
        raise SystemExit("a check failed: stop and report")


def cmd_score(a):
    eps = load_chunks(a.chunks)
    aff = json.loads((Path(a.chunks) / "affine.json").read_text()); sc, off = np.array(aff["scale"]), np.array(aff["offset"])
    lims = json.loads((Path(a.out) / "clamp_limits.json").read_text())
    lim = np.array(lims["deg_per_s"]); floor_norm = (lims["gripper_command_floor"] - off[GRIP]) / sc[GRIP]
    out = Path(a.out); rows = []
    per = {}
    for d in eps:
        for s, kinds in GEOMS.items():
            res = {k: score_episode(d, s, k, sc, off, lim, floor_norm=floor_norm) for k in kinds}
            for k, r in res.items():
                fa = float(np.abs(r["first"][:, ARM] - res["S0"]["first"][:, ARM]).mean())
                row = {"episode": int(d["e"]), "s": s, "stream": k, **{x: r[x] for x in ("within_jerk", "boundary_jerk",
                       "clamps_per_100", "error_deg", "n_steps")}, "first_action_change_deg": fa}
                rows.append(row); per.setdefault((s, k), []).append(row)
            for sy in GRID:                                                  # exploratory Σ*_y grid
                r = score_episode(d, s, "S3", sc, off, lim, sy, floor_norm)
                rows.append({"episode": int(d["e"]), "s": s, "stream": f"S3_sigma{sy:g}", "exploratory": True,
                             **{x: r[x] for x in ("within_jerk", "boundary_jerk", "clamps_per_100", "error_deg")}})
    with open(out / "a_rows.jsonl", "w") as f:
        f.writelines(json.dumps(r) + "\n" for r in rows)
    summ = {}
    for (s, k), rs in per.items():
        summ.setdefault(str(s), {})[k] = {m: float(np.median([r[m] for r in rs])) for m in
                                          ("within_jerk", "boundary_jerk", "clamps_per_100", "error_deg", "first_action_change_deg")}

    def paired(s, a_, b_, m):
        x = [ra[m] - rb[m] for ra, rb in zip(per[(s, a_)], per[(s, b_)])]
        return {"mean": float(np.mean(x)), "ci95": boot(x)}

    def ratio(s, a_, b_, m):
        return float(np.median([ra[m] for ra in per[(s, a_)]]) / np.median([rb[m] for rb in per[(s, b_)]]))
    A1 = {}
    for s in GEOMS:
        A1[str(s)] = {"error_S2_minus_S0": paired(s, "S2", "S0", "error_deg"),
                      "within_jerk_S2_over_S0": ratio(s, "S2", "S0", "within_jerk")}
    a1_pass = all(v["error_S2_minus_S0"]["mean"] <= 0.30 and v["error_S2_minus_S0"]["ci95"][1] <= 0.50
                  and v["within_jerk_S2_over_S0"] <= 0.5 for v in A1.values())
    a1_fail = any(v["error_S2_minus_S0"]["mean"] > 0.50 for v in A1.values())
    A2 = {}
    for s in GEOMS:
        A2[str(s)] = {"boundary_jerk_S3_over_S2": ratio(s, "S3", "S2", "boundary_jerk"),
                      "error_S3_minus_S2": paired(s, "S3", "S2", "error_deg")}
    a2_pass = all(v["boundary_jerk_S3_over_S2"] <= 0.40 and v["error_S3_minus_S2"]["mean"] <= 0.30 for v in A2.values())
    a2_fail = A2["50"]["boundary_jerk_S3_over_S2"] > 0.60
    res = {"episodes": len(eps), "medians": summ, "A1": A1, "verdict_A1": "pass" if a1_pass else "fail" if a1_fail else "not proven",
           "A2": A2, "verdict_A2": "pass" if a2_pass else "fail" if a2_fail else "not proven",
           "descriptive_S1_vs_S3_s25": {"boundary_jerk_S1_over_S3": ratio(25, "S1", "S3", "boundary_jerk"),
                                        "error_S1_minus_S3": paired(25, "S1", "S3", "error_deg")}}
    (out / "a_summary.json").write_text(json.dumps(res, indent=1)); print(json.dumps(res, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    li = sub.add_parser("limits"); li.add_argument("--out", required=True)
    ch = sub.add_parser("chunks"); ch.add_argument("--policy-path", required=True); ch.add_argument("--revision")
    ch.add_argument("--device", default="cuda"); ch.add_argument("--episodes", type=int, default=20); ch.add_argument("--out", required=True)
    ck = sub.add_parser("checks"); ck.add_argument("--chunks", required=True); ck.add_argument("--out", required=True)
    sc_ = sub.add_parser("score"); sc_.add_argument("--chunks", required=True); sc_.add_argument("--out", required=True)
    a = ap.parse_args()
    {"limits": cmd_limits, "chunks": cmd_chunks, "checks": cmd_checks, "score": cmd_score}[a.cmd](a)


if __name__ == "__main__":
    main()
