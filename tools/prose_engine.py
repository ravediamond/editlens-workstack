#!/usr/bin/env python3
"""WS-158: the two scanners behind scripts/prose_check.py. Runs under ~/venvs/prose (Python 3.12: slopscore-lint needs
>= 3.11, the hooks' python3 is 3.10), reads {"text": ...} on stdin and prints one JSON object:
  {"lang": "en", "slop": {...slopscore Report as a dict...}, "lm": [{"text": sentence, "p": ai_probability}, ...]}
or {"lang": "fr"} for a non-English text (neither tool is run). No network, no model tokens."""
import json
import sys


def main():
    text = json.load(sys.stdin)["text"]
    import lmscan

    lang = lmscan.detect_language(text)
    if lang not in ("en", "unknown"):
        print(json.dumps({"lang": lang}))
        return
    import slopscore

    rep = slopscore.scan_text(text, profile="blog")
    d = rep.model_dump() if hasattr(rep, "model_dump") else json.loads(rep.to_json())
    res = lmscan.scan(text)
    lm = [{"text": s.text, "p": round(float(s.ai_probability), 4)} for s in res.sentence_scores]
    print(json.dumps({"lang": "en", "slop": {"score": d["score"], "evidence": d["evidence"], "warnings": d.get("warnings", [])},
                      "lm": lm, "lm_doc_p": round(float(res.ai_probability), 4)}))


if __name__ == "__main__":
    main()
