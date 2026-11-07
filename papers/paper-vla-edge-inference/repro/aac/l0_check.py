"""L0: recompute the AAC bars (A1, A3, A4) from expected/gate0_rows.jsonl (one row per query: h*, phase, jump rates, N = 20 decision ms) and
expected/gate1_latency.json; gate0.json is read only for the metadata and compared with the recomputed summary. Standard library only."""
import json, statistics, sys
from pathlib import Path

E = Path(__file__).resolve().parent / "expected"
g0, g1 = (json.loads((E / f).read_text()) for f in ("gate0.json", "gate1_latency.json"))
rows = [json.loads(l) for l in (E / "gate0_rows.jsonl").read_text().splitlines() if l.strip()]
fails = 0


def check(name, got, want, tol=0.0005):
    global fails
    ok = abs(got - want) <= tol
    fails += not ok
    print(f"{'ok ' if ok else 'BAD'} {name}: {got:.4f} (post: {want}, tol {tol})")


med = statistics.median
by = lambda ph: [r["h_star"] for r in rows if r["phase"] == ph]  # noqa: E731
jump = lambda k, d: med([r["jump"][f"{k}|{d}"] for r in rows if f"{k}|{d}" in r["jump"]])  # noqa: E731
check("queries in the rows", len(rows), g0["A1"]["n_all"], 0)
check("queries in the grasp window (recomputed)", len(by("grasp")), g0["A1"]["n_grasp"], 0)
check("queries in transport (recomputed)", len(by("transport")), g0["A1"]["n_transport"], 0)
a1 = {"median_h_grasp": med(by("grasp")), "median_h_transport": med(by("transport"))}
check("A1 median h* transport (recomputed)", a1["median_h_transport"], 2, 0)
check("A1 median h* grasp window (recomputed)", a1["median_h_grasp"], 2, 0)
check("A1: transport >= grasp + 2 (recomputed; 0 = fail)", float(a1["median_h_transport"] >= a1["median_h_grasp"] + 2), 0, 0)
a3 = {"aac+overwrite_d8": round(jump("aac+overwrite", 8), 4), "fixed+overwrite_d8": round(jump("fixed+overwrite", 8), 4)}
check("A3 AAC + overwrite, d = 8 (recomputed)", a3["aac+overwrite_d8"], 0.973, 0.0005)
check("A3 fixed + overwrite, d = 8 (recomputed)", a3["fixed+overwrite_d8"], 0.940, 0.0005)
check("A3: AAC <= fixed (recomputed; 0 = fail)", float(a3["aac+overwrite_d8"] <= a3["fixed+overwrite_d8"]), 0, 0)
n20 = g1["by_n"]["20"]["median_ms"]
check("A4 N = 20 decision, ms (read)", n20, 4751, 1)
check("A4: N = 20 <= 298 ms (recomputed; 0 = fail)", float(n20 <= 298.0), 0, 0)
check("timing at MAXN_SUPER (read; 1 = yes)", float("MAXN_SUPER" in g1["power"]), 1, 0)
for k in ("fixed+naive", "fixed+overwrite", "aac+naive", "aac+overwrite"):
    for d in (8, 12, 20):
        check(f"descriptive jump {k} d = {d} (recomputed)", round(jump(k, d), 4), g0["A2_descriptive"][f"{k}|{d}"]["median"])
check("median N = 20 decision over the rows, ms (recomputed)", med([r["ms_n20"] for r in rows]), g0["ms_n20_median"], 0.01)
print("L0", "PASS" if fails == 0 else f"FAIL ({fails})")
sys.exit(1 if fails else 0)
