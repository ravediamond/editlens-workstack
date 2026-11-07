#!/usr/bin/env python3
"""WS-134 part 2a (projects/pact-vla/PROTOCOL_BATCHED.md, frozen 2026-11-05 before any number): does "N-sample methods pay N chunks in series"
hold on the Orin, or only in a sequential engine? SmolVLA in PyTorch: one chunk, N chunks in series, prefix shared with N loops in series, and the
prefix shared with one denoising loop at batch N.

    IMAGE=lerobot-jetson:rc LEROBOT_SRC=image shared/gate/jetson_run.sh --python scripts/pact_batched_latency.py --checks \\
        --policy-path ravediamond/smolvla_2026-09-24_14-34-40 --revision c1d76f6
    ... same with --run [--power-label MAXN_SUPER] for the timings

Writes projects/pact-vla/results/batched_checks.json (--checks) or batched.json (--run). Nothing else may be on the GPU during --run."""
from __future__ import annotations

import argparse
import copy
import json
import statistics
import sys
import time
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "src"))
import pact_flowres as PF  # noqa: E402

OUT = ROOT / "projects/pact-vla/results"
STEPS, FRAMES, T_AT = 10, 5, 50
TOL_MEAN, TOL_MAX = 3e-3, 2e-2  # deviation 1 of PROTOCOL_BATCHED.md (2026-11-05): was 1e-3 mean; the float32 check C1b carries the strict test
TOL32_MEAN, TOL32_MAX = 1e-4, 1e-3


def expand(obj, n):
    """Batch-1 tensors of a nested cache structure expanded to batch n (views; the caller's timing includes the expansion)."""
    if hasattr(obj, "batch_repeat_interleave"):  # transformers DynamicCache: a real copy repeated along the batch dimension
        c = copy.deepcopy(obj); c.batch_repeat_interleave(n); return c
    if isinstance(obj, torch.Tensor):
        return obj.expand(n, *obj.shape[1:]) if obj.shape[0] == 1 else obj
    if isinstance(obj, dict):
        return {k: expand(v, n) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return type(obj)(expand(v, n) for v in obj)
    raise TypeError(f"cannot expand a {type(obj).__name__} along the batch dimension")


def shapes(obj):
    if hasattr(obj, "get_seq_length"):
        try:
            return {"cache": type(obj).__name__, "seq_len": int(obj.get_seq_length()), "batch": int(obj.layers[0].keys.shape[0]), "layers": len(obj.layers)}
        except Exception:
            return {"cache": type(obj).__name__, "seq_len": int(obj.get_seq_length())}
    if isinstance(obj, torch.Tensor):
        return list(obj.shape)
    if isinstance(obj, dict):
        return {k: shapes(v) for k, v in list(obj.items())[:2]}
    if isinstance(obj, (list, tuple)):
        return [shapes(v) for v in list(obj)[:2]]
    return type(obj).__name__


@torch.no_grad()
def denoise(mdl, pad, kv, x, steps=STEPS):
    """SmolVLA's own Euler loop (sample_actions) from x at t = 1 to t = 0, on whatever batch x has."""
    dt = -1.0 / steps; t = torch.tensor(1.0, dtype=torch.float32, device=x.device)
    while t >= -dt / 2:
        v = mdl.denoise_step(prefix_pad_masks=pad, past_key_values=kv, x_t=x, timestep=t.expand(x.shape[0]))
        x = x + dt * v; t = t + dt
    return x


def timed(fn, n=50, warm=15):
    for _ in range(warm):
        fn()
    torch.cuda.synchronize(); ts = []
    for _ in range(n):
        t0 = time.perf_counter(); fn(); torch.cuda.synchronize(); ts.append((time.perf_counter() - t0) * 1e3)
    return ts


def timed_interleaved(fns, n=50, warm=15, seed=0):
    """Deviation 2: every round times each variant once, in random order, so slow drift hits all variants alike."""
    import random
    rng = random.Random(seed)
    for _ in range(warm):
        for f in fns.values():
            f()
    torch.cuda.synchronize(); ts = {k: [] for k in fns}
    for _ in range(n):
        order = list(fns); rng.shuffle(order)
        for k in order:
            t0 = time.perf_counter(); fns[k](); torch.cuda.synchronize(); ts[k].append((time.perf_counter() - t0) * 1e3)
    return ts


def gpu_temp_c():
    try:
        hot = []
        for z in Path("/sys/devices/virtual/thermal").glob("thermal_zone*"):
            if "gpu" in (z / "type").read_text().lower():
                hot.append(int((z / "temp").read_text()) / 1000)
        return max(hot) if hot else None
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--policy-path", required=True); ap.add_argument("--revision"); ap.add_argument("--repo-id", default="ravediamond/so101_bowls_all")
    g = ap.add_mutually_exclusive_group(required=True); g.add_argument("--checks", action="store_true"); g.add_argument("--run", action="store_true")
    ap.add_argument("--power-label", default="unlabelled"); ap.add_argument("--calls", type=int, default=50)
    a = ap.parse_args()
    from huggingface_hub import snapshot_download
    from so101_harness.episodes import EpisodeDataset, download

    m = PF.Pact(snapshot_download(a.policy_path, revision=a.revision) if a.revision else a.policy_path, "cuda")
    mdl, H, A = m.policy.model, m.horizon, m.action_dim
    ds = EpisodeDataset(download(a.repo_id, with_videos=True))
    eps = json.loads(PF.G13B.read_text())["meta"]["episodes"][:FRAMES]
    obs_list = [{"state": ds.states(ep)[T_AT], "task": ds.task(ep), **{k: ds.frame(ep, T_AT, k) for k in m.image_keys}} for ep in eps]
    res = {"power_label": a.power_label, "policy": a.policy_path, "revision": a.revision, "frames": FRAMES, "calls": a.calls, "steps": STEPS, "gpu_temp_start_c": gpu_temp_c()}
    gen = torch.Generator(device="cuda")

    def noise(n, seed):
        gen.manual_seed(seed); return torch.randn(n, H, A, device="cuda", generator=gen)

    # --- C3 shapes and C1 parity (two frames, N = 4)
    pad, kv = m.prefix(obs_list[0]); kv4 = expand(kv, 4); pad4 = pad.expand(4, *pad.shape[1:])
    res["C3_shapes"] = {"prefix_kv": shapes(kv), "expanded_kv": shapes(kv4), "pad": list(pad.shape), "output": [4, H, A]}
    par = []
    for i in range(2):
        pad, kv = m.prefix(obs_list[i]); kv4 = expand(kv, 4); pad4 = pad.expand(4, *pad.shape[1:]); n4 = noise(4, 100 + i)
        xb = denoise(mdl, pad4, kv4, n4)
        for r in range(4):
            x1 = denoise(mdl, pad, kv, n4[r:r + 1]); d = (xb[r] - x1[0]).abs().float()
            par.append({"frame": i, "row": r, "mean_abs": float(d.mean()), "max_abs": float(d.max())})
    res["C1_parity"] = {"rows": par, "mean_max": max(p["mean_abs"] for p in par), "max_max": max(p["max_abs"] for p in par),
                        "pass": all(p["mean_abs"] <= TOL_MEAN and p["max_abs"] <= TOL_MAX for p in par)}
    # --- C2 harness (deviation 2): the batch-1 step through m.velocity, the function the gate A reference used, after 15 warm-up calls
    pad, kv = m.prefix(obs_list[0]); x1c = torch.randn(1, H, A)
    step = statistics.median(timed(lambda: m.velocity((pad, kv), x1c, 0.5), 30, warm=15))
    xg, tt = noise(1, 1), torch.tensor([0.5], device="cuda")
    direct = statistics.median(timed(lambda: mdl.denoise_step(prefix_pad_masks=pad, past_key_values=kv, x_t=xg, timestep=tt), 30, warm=15))
    ref = json.loads((OUT / "ver_ratio.json").read_text())["pytorch_step_ms"]
    res["C2_harness"] = {"step_ms": step, "step_direct_ms_descriptive": direct, "reference_ms": ref, "within_25pct": abs(step - ref) / ref <= 0.25}
    print(json.dumps({k: res[k] for k in ("C3_shapes", "C2_harness")}, indent=1)); print("C1", res["C1_parity"]["pass"], res["C1_parity"]["mean_max"], res["C1_parity"]["max_max"])
    OUT.mkdir(parents=True, exist_ok=True)
    res["dtype"] = str(next(mdl.parameters()).dtype)
    if a.checks:  # C1b: the same parity in float32, where batch-1 and batch-4 kernels must agree to rounding of the last bits
        dt0 = next(mdl.parameters()).dtype; m.policy.float(); par32 = []
        for i in range(2):
            pad, kv = m.prefix(obs_list[i]); kv4 = expand(kv, 4); pad4 = pad.expand(4, *pad.shape[1:]); n4 = noise(4, 100 + i).float()
            xb = denoise(mdl, pad4, kv4, n4)
            for r in range(4):
                d = (xb[r] - denoise(mdl, pad, kv, n4[r:r + 1])[0]).abs().float(); par32.append({"frame": i, "row": r, "mean_abs": float(d.mean()), "max_abs": float(d.max())})
        res["C1b_parity_float32"] = {"rows": par32, "mean_max": max(p["mean_abs"] for p in par32), "max_max": max(p["max_abs"] for p in par32),
                                     "pass": all(p["mean_abs"] <= TOL32_MEAN and p["max_abs"] <= TOL32_MAX for p in par32)}
        print("C1b float32", res["C1b_parity_float32"]["pass"], res["C1b_parity_float32"]["mean_max"], res["C1b_parity_float32"]["max_max"]); m.policy.to(dt0)
    if a.checks:
        (OUT / "batched_checks.json").write_text(json.dumps(res, indent=1)); return
    ck = json.loads((OUT / "batched_checks.json").read_text()) if (OUT / "batched_checks.json").exists() else {}
    if not (ck.get("C1b_parity_float32", {}).get("pass") and res["C1_parity"]["pass"] and res["C2_harness"]["within_25pct"]):
        sys.exit("a check failed: no timing taken (protocol: fix and record a deviation first)")

    # --- timings, per frame (deviation 2: interleaved rounds)
    rows = []
    t_end = time.time() + 5
    p0, k0 = m.prefix(obs_list[0])
    while time.time() < t_end:  # 5 s burn-in
        denoise(mdl, p0, k0, noise(1, 3))
    for f, obs in enumerate(obs_list):
        if (gpu_temp_c() or 0) >= 90:
            sys.exit("GPU temperature at 90 C: aborted (protocol)")
        n1, n4, n20 = noise(1, 10 + f), noise(4, 20 + f), noise(20, 30 + f); noise_pool = {4: n4, 20: n20}

        def one_chunk():
            p, k = m.prefix(obs); return denoise(mdl, p, k, n1)

        def seq(n):
            def fn():
                for _ in range(n):
                    one_chunk()
            return fn

        def shared(n):
            def fn():
                p, k = m.prefix(obs)
                for r in range(n):
                    denoise(mdl, p, k, noise_pool[n][r:r + 1])
            return fn

        def batched(n):
            def fn():
                p, k = m.prefix(obs); return denoise(mdl, p.expand(n, *p.shape[1:]), expand(k, n), noise_pool[n])
            return fn
        a_set = timed_interleaved({"T1": one_chunk, "T_prefix": lambda: m.prefix(obs), "T_seq4": seq(4), "T_shared4": shared(4), "T_batch4": batched(4)}, a.calls, 15)
        b_set = timed_interleaved({"T_seq20": seq(20), "T_shared20": shared(20), "T_batch20": batched(20)}, 20, 3, seed=1)
        row = {"frame": f}
        for k, v in {**a_set, **b_set}.items():
            row[k] = statistics.median(v); row[k + "_p10"] = sorted(v)[len(v) // 10]; row[k + "_p90"] = sorted(v)[(9 * len(v)) // 10]
        for n in (4, 20):
            torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats(); base = torch.cuda.memory_allocated()
            for _ in range(3):
                batched(n)()
            torch.cuda.synchronize(); row[f"peak_extra_MB_batch{n}"] = (torch.cuda.max_memory_allocated() - base) / 2 ** 20
        rows.append(row); print(json.dumps({k: round(v, 1) if isinstance(v, float) else v for k, v in row.items() if not k.endswith(("_p10", "_p90"))}), flush=True)
    med = lambda k: statistics.median(r[k] for r in rows)  # noqa: E731
    res["rows"] = rows; res["gpu_temp_end_c"] = gpu_temp_c()
    res["summary"] = {k: med(k) for k in rows[0] if k != "frame"}
    res["ratio_batch4_over_T1_median_of_frames"] = statistics.median(r["T_batch4"] / r["T1"] for r in rows)
    res["ratio_batch20_over_T1_median_of_frames"] = statistics.median(r["T_batch20"] / r["T1"] for r in rows)
    res["bar"] = {"threshold": 2.0, "claim_is_about_the_hardware": res["ratio_batch4_over_T1_median_of_frames"] >= 2.0}
    (OUT / "batched.json").write_text(json.dumps(res, indent=1)); print(json.dumps({k: res[k] for k in ("ratio_batch4_over_T1_median_of_frames", "ratio_batch20_over_T1_median_of_frames", "bar")}, indent=1))


if __name__ == "__main__":
    main()
