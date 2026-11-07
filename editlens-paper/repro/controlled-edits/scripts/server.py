import json, sys, time, os
from pathlib import Path
sys.path.insert(0, str((next(p for p in __import__("pathlib").Path(__file__).resolve().parents if (p / "AGENTS.md").exists())) / "tools"))
import paper_map as M
D = Path(__file__).resolve().parent
sc = M.EditLensScorer()
(D / "ready").write_text("1")
while True:
    for f in sorted((D / "req").glob("*.json")):
        try:
            texts = json.loads(f.read_text())
        except Exception:
            continue
        out = [round(sc.score(M.clean_text(t))[0], 4) for t in texts]
        (D / "resp" / f.name).write_text(json.dumps(out))
        f.rename(D / "req" / (f.name + ".done"))
    time.sleep(0.3)
