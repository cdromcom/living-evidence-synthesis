#!/usr/bin/env python3
"""Run Jev, Gemini Decision 1 and Perplexity Decider 1.3 on the blinded EVD packets.

Tasks (same wording and inputs for every model):
  relevancy  Selection Relevancy        -> Relevant / Irrelevant (P(yes))
  fidelity   EVD vs Description quote   -> Met / Partially Met / Unmet
  quote      Grounding - Quote          -> Correct / Partially Correct / Incorrect / NA
  table      Grounding - Table/Figure   -> Correct / Partially Correct / Incorrect / Missing / NA

Keys come from the environment: PERPLEXITY_API_KEY, GEMINI_API_KEY, TYPESAFE_API_KEY.
Packets (build_packets.py) hold ONLY vault content: no JP or Claude judgments. This script never
touches the Google Sheet. Results are appended to results/<provider>.jsonl and resumed on re-run.

Examples
  python3 -I run_raters.py run --dry-run --evd 1-3                      # show what would be sent, no calls
  python3 -I run_raters.py run --providers perplexity --evd 1-3         # smoke test
  python3 -I run_raters.py run --providers perplexity,gemini,jev        # everything
  python3 -I run_raters.py export                                       # results/summary.csv
"""
import argparse
import base64
import csv
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
for _env in (Path.home() / ".config/lives-ai-raters/.env", HERE / ".env"):  # KEY=value lines; keep keys OUT of the vault
    if _env.exists():
        for _l in _env.read_text().splitlines():
            if "=" in _l and not _l.strip().startswith("#"):
                _k, _v = _l.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))
PACKETS = HERE / "packets"
RESULTS = HERE / "results"

MODELS = {"perplexity": "pplx-decider-v1.3", "liquid": "d1-ultra", "jev": "jev-1.14.0", "gemini": "gemini-decision-1"}
PRICE_PER_M = {"perplexity": 0.02, "liquid": 0.042, "jev": 0.042, "gemini": 0.10}  # USD per 1M input tokens (docs, 2026-11-23)
KEY_ENV = {"perplexity": "PERPLEXITY_API_KEY", "liquid": "LIQUID_API_KEY", "jev": "TYPESAFE_API_KEY", "gemini": "GEMINI_API_KEY"}
MAX_TOKENS = 230_000

CRITERION = (
    "LIVES is a living evidence synthesis on automated technologies (especially large language models) "
    "for research evaluation: peer review, evidence appraisal, error detection, citation integrity and "
    "reporting-quality assessment. An EVD (evidence node) is relevant when it reports how well an AI "
    "system performs a research-evaluation task, against humans, ground truth or other systems. It is "
    "irrelevant when it reports something else, for example human-only statistics about the reference "
    "standard, meta-research findings produced with an LLM rather than findings about the LLM's accuracy, "
    "or the generation of documents rather than the evaluation of research. It must also be worth "
    "learning: a specific, clear finding about such a system's performance."
)

FIDELITY = {
    "Met": "Every number and claim in the EVD statement is in the quoted text (paraphrase is fine).",
    "Partially Met": "The gist matches, but some number or claim in the EVD statement is not in the quoted text, or the statement slightly overstates or misframes the quote.",
    "Unmet": "The EVD statement contradicts the quoted text or is not supported by it.",
}
FIDELITY_V2 = {
    "Met": "The gist of the EVD statement (its main finding) is in the quoted text. Specific numbers and details that match closely are a bonus, not a requirement. Paraphrase, rounding, derived figures, abbreviations and study-context wording that is not in the quote are fine.",
    "Partially Met": "Use sparingly. Only part of the EVD statement's main finding is in the quoted text, or the statement says something noticeably different from what the quote says.",
    "Unmet": "The main finding of the EVD statement is not in the quoted text, or the quote contradicts it.",
}
QUOTE = {
    "Correct": "A screenshot on the evidence page shows the quoted text word for word (the screenshot must match the quote text; trivial differences such as hyphenation, line breaks or quote marks are fine). A wrong or different page number in the citation does not matter.",
    "Partially Correct": "The screenshots show only part of the quoted text, or the quote text has small unmarked edits or omissions compared with the text in the screenshots.",
    "Incorrect": "The screenshots show a different passage from the quote, or the quote text is materially different from the text in the screenshots.",
    "Missing": "No screenshot is shown on the evidence page.",
    "NA": "There is no quote to check.",
}
TABLE = {
    "Correct": "A screenshot shows the table or figure that holds the EVD statement's numbers or main finding (the one the caption or the paraphrased text describes), complete enough to read the relevant values.",
    "Partially Correct": "The right table or figure, but cropped so the relevant cells are missing, or only one of several needed.",
    "Incorrect": "The screenshots shown are not that table or figure (for example body text only, or a different table or figure).",
    "Missing": "The EVD statement's numbers appear to come from a table or figure (the caption or paraphrased text mentions one, or the numbers are too detailed to come from the quote alone) but none of the screenshots shown is that table or figure.",
    "NA": "The EVD statement's numbers are fully given in the quoted text and no table or figure is referenced, so none is needed.",
}


def noul(q):
    return {"type": "noul", "instructions": q}


def choice(q, opts):
    return {"type": "choice", "instructions": q, "criteria": opts}


EXAMPLES = HERE / "examples" / "fidelity_examples.json"


def example_text():
    ex = json.loads(EXAMPLES.read_text())["examples"]
    out = ["WORKED EXAMPLES (already judged by an expert reviewer; the item to judge comes after them):"]
    for i, e in enumerate(ex, 1):
        out.append(f"\nExample {i}\nEVD STATEMENT: {e['evd_statement']}\nQUOTED TEXT: {e['quote_text']}\n"
                   f"EXPERT RATING: {e['label']}. Why: {e['why']}")
    return "\n".join(out) + "\n\n--- ITEM TO JUDGE ---\n"


def example_evds():
    return {e["evd"] for e in json.loads(EXAMPLES.read_text())["examples"]} if EXAMPLES.exists() else set()


def build_task(task, p, with_images, fid_v=1):
    """Return (parts, questions, n_images). parts = [{'text':..}|{'image': path}]."""
    parts, evd = [], f"EVD STATEMENT (the claim being checked):\n{p['evd_statement']}"
    imgs = [i for i in p["images"] if with_images]

    if task == "relevancy":
        parts.append({"text": f"REVIEW QUESTION(S) this EVD was found under:\n{p['review_questions']}\n\nREVIEW CRITERION:\n{CRITERION}\n\n{evd}\n\nQUOTED EVIDENCE FROM THE PAPER:\n{p['quote_text']}\n\n"
                              f"TABLE/FIGURE CAPTION shown on the evidence page (may be empty):\n{p['grounding_table_text'] or '(none)'}"})
        qs = {"relevant": noul("Is this EVD relevant to the REVIEW QUESTION(S) and the REVIEW CRITERION, and worth learning? Yes means Relevant; No means Irrelevant.")}
        return parts, qs, 0
    if task == "fidelity":
        if fid_v in (2, 3):
            parts.append({"text": (example_text() if fid_v == 3 else "") + f"{evd}\n\nQUOTED TEXT (the quote shown with the EVD):\n{p['quote_text']}"})
            qs = {"fidelity": choice("Is the gist of the EVD statement in the quoted text? Choose Met when its main finding is there; missing specific numbers or details do not matter.", FIDELITY_V2),
                  "all_numbers_in_quote": noul("Does every number in the EVD statement appear in the quoted text itself (rounding allowed)?")}
            return parts, qs, 0
        parts.append({"text": f"{evd}\n\nQUOTED TEXT (the quote shown with the EVD):\n{p['quote_text']}"})
        qs = {"fidelity": choice("Does the EVD statement match what the quoted text says?", FIDELITY),
              "all_numbers_in_quote": noul("Does every number in the EVD statement appear in the quoted text (rounding allowed)?")}
        return parts, qs, 0
    def add_all_images():                 # every screenshot on the evidence page, whichever slot the vault page put it in
        n = 0
        for i in p["images"]:
            if with_images:
                n += 1
                parts.append({"text": f"\nSCREENSHOT {n} on the evidence page:"})
                parts.append({"image": str(PACKETS / f"EVD-{p['evd']:02d}" / i["file"])})
        return n
    def shot_qs(n):
        return {f"shot{k}_connects_to_quote": noul(f"Does SCREENSHOT {k} show text or a table or figure that connects to the quoted text?") for k in range(1, n + 1)}
    if task == "quote":
        parts.append({"text": f"{evd}\n\nQUOTED TEXT (as shown on the evidence page, with its cited page number):\n{p['quote_text']}"})
        n = add_all_images()
        if not n:
            parts.append({"text": "\n\n(No screenshot is shown on the evidence page.)"})
        qs = {"quote_grounding": choice("Do the screenshots on the evidence page correctly show the quoted text?", QUOTE)}
        if n:
            qs["screenshot_shows_quote"] = noul("Does any SCREENSHOT show the quoted passage?")
            qs.update(shot_qs(n))
        return parts, qs, n
    if task == "table":
        para = p.get("description_other_text", "").strip() or "(none)"
        parts.append({"text": f"{evd}\n\nQUOTED TEXT:\n{p['quote_text']}\n\nTABLE/FIGURE CAPTION shown on the evidence page (may be empty):\n{p['grounding_table_text'] or '(none)'}\n\nPARAPHRASED TEXT shown under the table/figure (unquoted; may be empty):\n{para}"})
        n = add_all_images()
        if not n:
            parts.append({"text": "\n\n(No screenshot is shown on the evidence page.)"})
        qs = {"table_fig_grounding": choice("Does the evidence page show the correct table or figure for the EVD statement's numbers?", TABLE),
              "screenshots_contain_numbers": noul("Do the screenshots shown contain the EVD statement's key numbers?")}
        qs.update(shot_qs(n))
        return parts, qs, n
    raise ValueError(task)


def b64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()


def est_tokens(parts):
    return int(sum(len(x.get("text", "")) for x in parts) / 3.5 + 1000 * sum(1 for x in parts if "image" in x))


def request_for(provider, parts, qs, model, jev_images):
    if provider == "perplexity":
        state = []
        for x in parts:
            state.append(x["text"] if "text" in x else
                         {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64(x["image"])}})
        return ("https://api.perplexity.ai/v1/decisions",
                {"Authorization": f"Bearer {os.environ.get('PERPLEXITY_API_KEY', '')}", "Content-Type": "application/json"},
                {"model": model, "state": state, "questions": qs})
    if provider == "gemini":
        blocks = []
        for x in parts:
            blocks.append({"type": "text", "text": x["text"] + "\n"} if "text" in x else
                          {"type": "image", "data": b64(x["image"]), "mime_type": "image/png", "resolution": "high"})
        return ("https://generativelanguage.googleapis.com/v1beta/decisions",
                {"x-goog-api-key": os.environ.get("GEMINI_API_KEY", ""), "Content-Type": "application/json"},
                {"model": model, "input": blocks, "questions": qs})
    if provider == "liquid":
        text, imgs = [], []
        for x in parts:
            if "text" in x:
                text.append(x["text"])
            else:
                imgs.append("data:image/png;base64," + b64(x["image"]))
                text.append(f"[image {len(imgs)} attached]")
        body = {"model": model, "state": "\n".join(text), "questions": qs}
        if imgs:
            body["images"] = imgs
        return ("https://api.liquid.ai/decisions/v1/systemone",
                {"Authorization": f"Bearer {os.environ.get('LIQUID_API_KEY', '')}", "Content-Type": "application/json"}, body)
    if provider == "jev":
        import uuid
        text, assets = [], {}
        for x in parts:
            if "text" in x:
                text.append(x["text"])
            else:
                ref = f"imgref-{uuid.uuid4().hex[:12]}"
                assets[ref] = {"type": "image", "format": "png", "data_base64": b64(x["image"])}
                text.append(ref)
        state = "\n".join(text)
        headers = {"Authorization": f"Bearer {os.environ.get('TYPESAFE_API_KEY', '')}", "Content-Type": "application/json"}
        if assets:
            headers["TypeSafe-Danger-Zone-Images"] = "true"
        if len(state) / 3.5 + 3000 * len(assets) > 25_000:
            headers["TypeSafe-Danger-Zone-Long-Context"] = "true"
        body = {"model": model, "state": state, "questions": qs}
        if assets:
            body["assets"] = assets
        return ("https://api.typesafe.ai/v1/systemone", headers, body)
    raise ValueError(provider)


def post(url, headers, body):
    for attempt in range(5):
        try:
            r = requests.post(url, headers=headers, json=body, timeout=180)
        except requests.RequestException as e:
            err = str(e)
        else:
            if r.status_code == 200:
                return r.json(), None
            err = f"HTTP {r.status_code}: {r.text[:400]}"
            if r.status_code not in (429, 500, 502, 503, 504, 529):
                return None, err
        time.sleep(2 ** attempt * 2)
    return None, err


def parse_evd_list(s, n=77):
    if not s:
        return list(range(1, n + 1))
    out = []
    for part in s.split(","):
        a, _, b = part.partition("-")
        out += list(range(int(a), int(b or a) + 1))
    return out


def cmd_run(a):
    RESULTS.mkdir(exist_ok=True)
    providers, tasks = a.providers.split(","), a.tasks.split(",")
    jobs, done = [], {}
    for pv in providers:
        f = RESULTS / f"{pv}.{a.run_id}.jsonl"
        done[pv] = {(r["evd"], r["task"]) for r in map(json.loads, f.read_text().splitlines())
                    if not r.get("error")} if f.exists() else set()
        for e in parse_evd_list(a.evd):
            for t in tasks:
                if t == "fidelity" and a.fidelity_version == 3 and e in example_evds():
                    continue
                if (e, t) not in done[pv]:
                    jobs.append((pv, e, t))
    total_tokens = {pv: 0 for pv in providers}
    prepared = []
    for pv, e, t in jobs:
        p = json.loads((PACKETS / f"EVD-{e:02d}" / "packet.json").read_text())
        parts, qs, n_img = build_task(t, p, with_images=True, fid_v=a.fidelity_version)
        model = a.jev_model if pv == "jev" else (a.liquid_model if pv == "liquid" else MODELS[pv])
        tok = 0 if (t == "table" and n_img == 0) else est_tokens(parts)
        total_tokens[pv] += tok
        prepared.append((pv, e, t, parts, qs, n_img, model, tok))
    print(f"{len(prepared)} requests to run (skipping {sum(len(v) for v in done.values())} already done)")
    for pv in providers:
        print(f"  {pv}: ~{total_tokens[pv]:,} input tokens, ~${total_tokens[pv] / 1e6 * PRICE_PER_M[pv]:.2f} (estimate)")
    if a.dry_run:
        d = HERE / "dry-run"
        d.mkdir(exist_ok=True)
        for pv, e, t, parts, qs, n_img, model, tok in prepared[: a.dry_limit]:
            txt = "\n".join(x["text"] if "text" in x else f"<<image {Path(x['image']).name}>>" for x in parts)
            (d / f"{pv}-EVD{e:02d}-{t}.txt").write_text(
                f"MODEL {model}\nQUESTIONS\n{json.dumps(qs, indent=1)}\n\nSTATE (what the model sees)\n{txt}")
        print(f"Dry run: wrote {min(len(prepared), a.dry_limit)} request previews to {d} (no API calls made)")
        return
    for pv in providers:
        if not os.environ.get(KEY_ENV[pv]):
            sys.exit(f"Set {KEY_ENV[pv]} first.")

    def work(job):
        pv, e, t, parts, qs, n_img, model, tok = job
        if t == "table" and n_img == 0:  # no screenshot at all on the evidence page -> Missing, no model call (models now see every screenshot and decide)
            rec = {"run_id": a.run_id, "fidelity_version": None, "evd": e, "task": t, "provider": pv, "model": "rule",
                   "requested_model": "rule", "rule_based": True, "ts": datetime.now(timezone.utc).isoformat(), "est_input_tokens": 0,
                   "images_sent": 0, "images_available": 0, "error": None, "usage": None,
                   "answers": {"table_fig_grounding": {"type": "choice", "choice": "Missing", "probabilities": {"Missing": 1.0}, "confidence": 1.0},
                               "screenshots_contain_numbers": {"type": "noul", "noul": 0.0}}}
            with lock_file(pv):
                with open(RESULTS / f"{pv}.{a.run_id}.jsonl", "a") as fh:
                    fh.write(json.dumps(rec) + "\n")
            print(f"  {pv} EVD {e:>2} {t:<9} rule: Missing (no screenshot)", flush=True)
            return rec
        url, headers, body = request_for(pv, parts, qs, model, False)
        _t0 = time.time()
        resp, err = post(url, headers, body)
        latency = round(time.time() - _t0, 3)
        rec = {"run_id": a.run_id, "fidelity_version": a.fidelity_version if t == "fidelity" else None,
               "evd": e, "task": t, "provider": pv, "model": (resp or {}).get("model", model), "requested_model": model,
               "ts": datetime.now(timezone.utc).isoformat(), "est_input_tokens": tok,
               "images_sent": n_img, "images_available": n_img, "error": err, "latency_s": latency,
               "answers": (resp or {}).get("answers"), "usage": (resp or {}).get("usage")}
        with lock_file(pv):
            with open(RESULTS / f"{pv}.{a.run_id}.jsonl", "a") as fh:
                fh.write(json.dumps(rec) + "\n")
        print(f"  {pv} EVD {e:>2} {t:<9} {'ERROR ' + err[:80] if err else 'ok'}", flush=True)
        return rec

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        list(ex.map(work, prepared))


_locks = {}


def lock_file(pv):
    import threading
    return _locks.setdefault(pv, threading.Lock())


def cmd_export(a):
    rows = {}
    for f in RESULTS.glob(f"*.{a.run_id}.jsonl"):
        for r in map(json.loads, f.read_text().splitlines()):
            if r.get("error") or not r.get("answers"):
                continue
            row = rows.setdefault(r["evd"], {"EVD": r["evd"]})
            pv, A = r["provider"], r["answers"]
            if r["task"] == "relevancy":
                p = A["relevant"]["noul"]
                row[f"{pv}_relevancy"] = "Relevant" if p >= 0.5 else "Irrelevant"
                row[f"{pv}_relevancy_P"] = round(p, 3)
            elif r["task"] == "fidelity":
                row[f"{pv}_fidelity"] = A["fidelity"]["choice"]
                row[f"{pv}_fidelity_allnumbers_P"] = round(A["all_numbers_in_quote"]["noul"], 3)
            elif r["task"] == "quote":
                row[f"{pv}_quote"] = A["quote_grounding"]["choice"]
                row[f"{pv}_quote_screenshot_P"] = round(A["screenshot_shows_quote"]["noul"], 3) if "screenshot_shows_quote" in A else ""
            elif r["task"] == "table":
                row[f"{pv}_tablefig"] = A["table_fig_grounding"]["choice"]
    cols = ["EVD"] + sorted({k for r in rows.values() for k in r if k != "EVD"})
    out = RESULTS / f"summary-{a.run_id}.csv"
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for e in sorted(rows):
            w.writerow(rows[e])
    print(f"Wrote {out} ({len(rows)} EVDs)")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--providers", default="perplexity,liquid,jev")
    r.add_argument("--tasks", default="relevancy,fidelity,quote,table")
    r.add_argument("--evd", default="", help="e.g. 1-5,9 (default all 77)")
    r.add_argument("--workers", type=int, default=4)
    r.add_argument("--jev-model", default=MODELS["jev"])
    r.add_argument("--liquid-model", default=MODELS["liquid"], help="d1-ultra is listed as deprecated by Liquid; d1.2-ultra is its replacement")
    r.add_argument("--run-id", default="r1", help="label for this pass; results/<provider>.<run-id>.jsonl (r1 = judgment of record)")
    r.add_argument("--fidelity-version", type=int, choices=(1, 2, 3), default=3, help="1 = original rubric; 2 = gist rule (JP, 2026-11-23): Met when the headline EVD's gist is in the quote; 3 = version 2 plus worked examples from EVD 1-3 (those EVDs are skipped for fidelity)")
    r.add_argument("--dry-run", action="store_true")
    r.add_argument("--dry-limit", type=int, default=12)
    r.set_defaults(fn=cmd_run)
    e = sub.add_parser("export")
    e.add_argument("--run-id", default="r1")
    e.set_defaults(fn=cmd_export)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
