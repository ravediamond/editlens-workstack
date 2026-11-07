import sys, json, subprocess
sys.path.insert(0, str((next(p for p in __import__("pathlib").Path(__file__).resolve().parents if (p / "AGENTS.md").exists())) / "tools"))
import paper_map as M
from pathlib import Path
out = {}
for r in ["paper-register-reproducibility","paper-jepa-world-model","paper-reward-models-stopping-rule","paper-vla-edge-inference"]:
    repo = (next(p for p in __import__("pathlib").Path(__file__).resolve().parents if (p / "AGENTS.md").exists()))/"papers"/r
    ins = M.find_inputs(str(repo))
    label, path, kind = next(i for i in ins if i[2]=="md")
    secs = M.md_sections(Path(path).read_text(), "md")
    paras = []
    for s in secs:
        for p in s["paras"]:
            paras.append({"sec": s["title"], "l0": p["l0"], "l1": p["l1"], "text": p["text"]})
    out[r] = {"file": str(path), "paras": paras}
json.dump(out, open("inventory.json","w"), indent=1)
for r,v in out.items(): print(r, v["file"], len(v["paras"]), "paras", sum(len(p["text"].split()) for p in v["paras"]), "words")
