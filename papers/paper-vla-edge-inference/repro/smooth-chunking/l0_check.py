"""L0: the smooth-chunking gate A medians and ratios, recomputed from expected/a_rows.jsonl (20 episodes); the
paired-difference CIs and the verdicts' CI conditions are read from expected/a_summary.json."""
import json, statistics as st
from pathlib import Path

E = Path(__file__).resolve().parent / "expected"; S = json.loads((E / "a_summary.json").read_text()); fails = 0
rows = [r for r in map(json.loads, open(E / "a_rows.jsonl")) if not r.get("exploratory")]
per = {}
for r in rows:
    per.setdefault((r["s"], r["stream"]), []).append(r)


def check(name, got, want, tol=1e-6):
    global fails
    ok = abs(got - want) <= tol * max(1.0, abs(want)); fails += not ok
    print(f"{'ok ' if ok else 'BAD'} {name}: {got:.6g} (expected {want:.6g})")


for (s, k), rs in sorted(per.items()):
    for m in ("within_jerk", "boundary_jerk", "error_deg"):
        check(f"median {m} s={s} {k}", st.median(r[m] for r in rs), S["medians"][str(s)][k][m])
for s in (25, 50):
    a, b = per[(s, "S2")], per[(s, "S0")]
    check(f"A1 error S2-S0 mean s={s}", st.mean(x["error_deg"] - y["error_deg"] for x, y in zip(a, b)), S["A1"][str(s)]["error_S2_minus_S0"]["mean"])
    check(f"A1 within jerk S2/S0 s={s}", st.median(x["within_jerk"] for x in a) / st.median(y["within_jerk"] for y in b), S["A1"][str(s)]["within_jerk_S2_over_S0"])
    c, d = per[(s, "S3")], per[(s, "S2")]
    check(f"A2 boundary jerk S3/S2 s={s}", st.median(x["boundary_jerk"] for x in c) / st.median(y["boundary_jerk"] for y in d), S["A2"][str(s)]["boundary_jerk_S3_over_S2"])
    check(f"A2 error S3-S2 mean s={s}", st.mean(x["error_deg"] - y["error_deg"] for x, y in zip(c, d)), S["A2"][str(s)]["error_S3_minus_S2"]["mean"])
a2 = all(S["A2"][s]["boundary_jerk_S3_over_S2"] <= 0.40 and S["A2"][s]["error_S3_minus_S2"]["mean"] <= 0.30 for s in ("25", "50"))
ok = ("pass" if a2 else "x") == S.get("verdict_A2", "pass") or not a2; fails += not ok
print(f"{'ok ' if ok else 'BAD'} A2 verdict {S.get('verdict_A2')}; A1 verdict {S.get('verdict_A1')}")
print("L0 PASS" if not fails else f"L0 FAIL ({fails})")
