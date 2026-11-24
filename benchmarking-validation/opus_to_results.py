#!/usr/bin/env python3
"""Convert the Claude Opus 5.5 rater files (opus-blind/out/EVD-NN.json) into results/opus.<run>.jsonl, the same schema as
the decision models, so agreement.py, error_analysis.py and metrics.py treat Opus like any other rater.
Usage: python3 -I opus_to_results.py <folder with EVD-NN.json> [run-id] [meta.json with tokens/time per batch]"""
import json, sys
from datetime import datetime, timezone
from pathlib import Path
HERE = Path(__file__).resolve().parent
src = Path(sys.argv[1]); run = sys.argv[2] if len(sys.argv) > 2 else "r1"
n_ok = 0
with open(HERE / f"results/opus.{run}.jsonl", "w") as out:
    for n in range(1, 78):
        f = src / f"EVD-{n:02d}.json"
        d = json.loads(f.read_text()); ts = datetime.now(timezone.utc).isoformat()
        base = {"run_id": run, "evd": n, "provider": "opus", "model": "claude-opus-5-5", "requested_model": "claude-opus-5-5 (Claude Code subagent)", "ts": ts, "error": None}
        r = d["relevancy"]
        out.write(json.dumps({**base, "task": "relevancy", "answers": {"relevant": {"type": "noul", "noul": float(r["p_relevant"])}}, "reason": r["reason"]}) + "\n")
        if d.get("fidelity"):
            x = d["fidelity"]; out.write(json.dumps({**base, "task": "fidelity", "fidelity_version": 3, "answers": {"fidelity": {"type": "choice", "choice": x["label"], "probabilities": x["probs"], "confidence": max(x["probs"].values())}}, "reason": x["reason"]}) + "\n")
        x = d["quote"]
        out.write(json.dumps({**base, "task": "quote", "answers": {"quote_grounding": {"type": "choice", "choice": x["label"], "probabilities": x["probs"], "confidence": max(x["probs"].values())}, "screenshot_shows_quote": {"type": "noul", "noul": float(x["p_screenshot_shows_quote"])}}, "reason": x["reason"]}) + "\n")
        if d.get("table"):
            x = d["table"]; out.write(json.dumps({**base, "task": "table", "answers": {"table_fig_grounding": {"type": "choice", "choice": x["label"], "probabilities": x["probs"], "confidence": max(x["probs"].values())}}, "reason": x["reason"]}) + "\n")
        else:
            out.write(json.dumps({**base, "task": "table", "model": "rule", "rule_based": True, "answers": {"table_fig_grounding": {"type": "choice", "choice": "Missing", "probabilities": {"Missing": 1.0}, "confidence": 1.0}}, "reason": "Rule: no table/figure screenshot shown, so Missing."}) + "\n")
        n_ok += 1
print(n_ok, "EVDs converted ->", HERE / f"results/opus.{run}.jsonl")
