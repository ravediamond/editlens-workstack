# 2026-10-20 — G-lat-2: one YOLO11n-seg inference per unit action, at rest (no arm) — **PASS**

Pre-registered in [`GATES_RUNBOOK.md`](../../../../projects/vla-jepa-world-model/GATES_RUNBOOK.md) §8 (commit
`82fdc15`, before any G-lat-2 data), after [G-lat](../2026-10-20_glat/README.md) failed (continuous 15 FPS seg:
+14.5 %). **Bar: added time per action <= 100 ms (max over 50 actions) AND vla chunk latency +<= 2 % vs 238 ms
(mean over all chunks).**

- `glat2_gpu640_summary.json` — the summary and verdict. Per-action and per-chunk rows stay in `outputs/glat2/` on the Orin.

## Result (arm `gpu640`: GPU TensorRT FP16 engine, 640 px)

| | measured | bar | |
|---|---|---|---|
| added time per action, **max** of 50 | **81.1 ms** (mean 72.4, p90 72.6) | <= 100 ms | ✔ |
| vla chunk latency, **mean** of 400 | **239.3 ms = +0.56 %** vs 238 (p50 239.0, p99 243.7) | <= +2 % (242.76 ms) | ✔ |

**G-lat-2 passes.** As registered, the DLA (`useDLA`) and 320 px arms run only if G-lat-2 fails, so they were not run.

Breakdown of the added time per action:

| part | mean | p99 |
|---|---|---|
| seg step (predict + mask resized to 640×480), once, at rest | 12.4 ms | 17.1 ms |
| SEVO blend on the CPU, 8 per action (one per chunk request) | 59.9 ms (7.5 ms each) | 64.0 ms |
| engine load + 30 warm-up predictions, once per session (not counted) | 1432 ms | – |

Server side during the actions: total 219.0 ms, vision 151.0, prefill + denoise 67.3, the same as vla alone in G-lat
(219.4 / 151.2 / 67.6). With seg kept out of the chunk requests, the vla sees no contention.

## Notes (not changes of the bar)

- **The blend costs more than the segmentation.** The float32 numpy blend over the full 640×480 frame takes 7.5 ms
  per chunk; the bar counts it in the added time. In a real loop it sits on the path before each chunk request,
  adding ~7.5 ms (~3 % of 238 ms) per chunk. That cost is not in the chunk latency as defined, which is the client
  call. It can be cut by blending only inside the mask's bounding box or with a uint8 LUT, if it ever matters.
- A mask was found in 50/50 actions. That is any COCO class at the highest confidence: this measures timing, not
  whether the right part was found.
- 8 chunk requests per action, back to back: a stress test. The real loop requests one chunk every ~1.9 s.

## Setup

As G-lat (same Orin, `MAXN_SUPER`, engine `yolo11n-seg.engine` 640 px FP16, vla-server `--flash-attn 1 --mm-prec
default` on branch `805570d`, real `vla_cpp` client in `lerobot-jetson:rc`), except:
- 50 actions, one frame each: every 90th top and wrist frame of `so101_bowls_all` `file-001`.
- The host process runs seg and blend, and drives the container client one chunk at a time over stdin. The seg step
  happens with no chunk request in flight (the arm at rest). Per chunk, the host writes the blended top frame as
  `.npy`; that file write is not timed.

```bash
python3 scripts/bench_glat2_per_action.py --engine ~/models/yolo/yolo11n-seg.engine --imgsz 640 --label gpu640 \
    --out shared/gate/data/2026-10-20_glat2
```

No smoke run this time: the full registered run was the first run of the script.
