"""L0: the SmolVLA timing split the paper reads from G-lat-2, and the gate's own pass flags from its bar."""
import json
from pathlib import Path

S = json.loads((Path(__file__).resolve().parent / "expected/glat2_gpu640_summary.json").read_text()); fails = 0
v = S["vla"]; tot, vis, inf = v["server_total_ms"]["mean"], v["server_vision_ms"]["mean"], v["server_inference_ms"]["mean"]
print(f"ok  server total {tot:.1f} ms, vision {vis:.1f} ms ({100 * vis / tot:.0f} %), the rest {inf:.1f} ms, n = {v['server_total_ms']['n']}")
ok = abs(vis + inf - tot) < 1.0; fails += not ok
print(f"{'ok ' if ok else 'BAD'} parts sum to the total within 1 ms ({vis + inf:.2f} vs {tot:.2f})")
pa = S["added_ms"]["p50"] <= S["bar"]["added_ms_max"]; ok = pa == S["pass_added"]; fails += not ok
print(f"{'ok ' if ok else 'BAD'} added-latency bar: {pa} (p50 {S['added_ms']['p50']:.1f} ms vs {S['bar']['added_ms_max']} ms)")
print("L0 PASS" if not fails else "L0 FAIL")
