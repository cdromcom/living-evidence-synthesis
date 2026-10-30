#!/usr/bin/env python3
"""
Run Pangram's AI-writing detector against source PDFs, via Pangram's true
asynchronous Bulk API (submit_bulk -> wait_for_bulk -> get_bulk_results) on
model "pangram-4" explicitly. The bulk file-upload endpoint
(predict_files/predict_file) does NOT support model selection, so this
script extracts each PDF's text itself (PyMuPDF) and submits text, not
files.

As of 2026-08 this covers the full 27-source corpus, having started as two
narrower triggers (a "Statistic Accuracy: Issues found" verdict, or a Data
Repo Check / Code Check of "No repository claimed") before being widened to
every source for model consistency. Text-only: Pangram's AI-image detector
is a research preview with no documented stable API, so it's skipped here.

Usage:
    export PANGRAM_API_KEY=...
    python3 misc/scripts/pangram_check.py

Prints a JSON report to stdout and writes it to
misc/pangram_check_<date>.json for reference.
"""
import json
import os
import sys
import time
from datetime import date
from pathlib import Path

import fitz  # PyMuPDF
from pangram import Pangram

VAULT = Path(__file__).resolve().parents[2]
PDF_DIR = VAULT / "source" / "pdfs"
MODEL = "pangram-4"

# citekey -> (SRC node id, PDF filename)
TARGETS = {
    "robertsComparativeStudyChatGPT2023": {"src_id": "SRC-012", "pdf": "Roberts et al. 2023 - Comparative study of ChatGPT and human evaluators.pdf"},
    "shahidLiteratureGroundedNoveltyAssessment2025": {"src_id": "SRC-014", "pdf": "Shahid et al. - 2025 - Literature-Grounded Novelty Assessment of Scientific Ideas.pdf"},
    "akyonEvaluatingCapabilitiesGenerative2024": {"src_id": "SRC-001", "pdf": "Akyon et al. - 2024 - Evaluating the capabilities of generative AI tools in understanding medical papers Qualitative stud.pdf"},
    "alharbiAutomatedAssessmentReporting2024": {"src_id": "SRC-002", "pdf": "Alharbi and Asiri - 2024 - Automated Assessment of Reporting Completeness in Orthodontic Research Using LLMs An Observational.pdf"},
    "bougieGenerativeAdversarialReviews2024a": {"src_id": "SRC-003", "pdf": "Bougie et al. - 2024 - Generative Adversarial Reviews.pdf"},
    "darcyMARGMultiAgentReview2024": {"src_id": "SRC-004", "pdf": "D'Arcy et al. - 2024 - MARG Multi-Agent Review Generation for Scientific Papers.pdf"},
    "hasanIntegratingLargeLanguage2024": {"src_id": "SRC-005", "pdf": "Hasan et al_2024_Integrating large language models in systematic reviews.pdf"},
    "huntington-kleinLLMsActRepositories2024": {"src_id": "SRC-006", "pdf": "Huntington-Klein and Murray - 2024. - Do LLMs Act as Repositories of Causal Knowledge.pdf"},
    "idahlOpenReviewerSpecializedLarge2025": {"src_id": "SRC-007", "pdf": "Idahl and Ahmadi - 2025 - OpenReviewer A Specialized LLM.pdf"},
    "leucutaRiskBiasAssessment2025": {"src_id": "SRC-008", "pdf": "Leucuta et al. 2025 - Risk of Bias Assessment of Diagnositic Accuracy Studies.pdf"},
    "liangCanLargeLanguage2024a": {"src_id": "SRC-009", "pdf": "Liang et al. - 2024 - Can Large Language Models Provide Useful Feedback on Research Papers A Large-Scale Empirical Analys.pdf"},
    "liuReviewerGPTExploratoryStudy2023": {"src_id": "SRC-010", "pdf": "Liu and Shah - 2023 - ReviewerGPT An Exploratory Study on Using Large Language Models for Paper Reviewing.pdf"},
    "louAAAR10AssessingAIs2025": {"src_id": "SRC-011", "pdf": "Lou et al. - 2025 - AAAR-1.0 Assessing AI's Potential to Assist Resea.pdf"},
    "sarolAssessingCitationIntegrity2024": {"src_id": "SRC-013", "pdf": "Sarol et al. - 2024 - Assessing citation integrity.pdf"},
    "sonWhenAICoScientists2025": {"src_id": "SRC-015", "pdf": "Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchmark for Automated Verification of Scientific Research.pdf"},
    "sridharanAssessingDecisionMakingCapabilities2024": {"src_id": "SRC-016", "pdf": "Sridharan and Sivaramakrishnan - 2024 - Assessing the Decision-Making Capabilities of AI.pdf"},
    "sridharanLeveragingArtificialIntelligence2025": {"src_id": "SRC-017", "pdf": "Sridharan and Sivaramakrishnan - 2024 - Leveraging artificial intelligence.pdf"},
    "srinivasanEvaluatingReportingQuality2025a": {"src_id": "SRC-018", "pdf": "Srinivasan et al. - 2025 - Evaluating the reporting quality of 21,041 randomized controlled trial articles.pdf"},
    "thelwallEvaluatingResearchQuality2024": {"src_id": "SRC-019", "pdf": "Thelwall - 2024 - Evaluating Research Quality with Large Language Models An Analysis of ChatGPT's Effectiveness with.pdf"},
    "tyserAIDrivenReviewSystems2024": {"src_id": "SRC-020", "pdf": "Tyser et al. - 2024 - AI-Driven Review Systems Evaluating LLMs in Scalable and Bias-Aware Academic Reviews.pdf"},
    "woelfleBenchmarkingHumanAICollaboration2024": {"src_id": "SRC-021", "pdf": "Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf"},
    "wrightsonGPTRCTsUsing2025": {"src_id": "SRC-022", "pdf": "Wrightson et al. - 2025 - GPT for RCTs Using AI to determine adherence to clinical trial reporting guidelines.pdf"},
    "wuAutomatedNoveltyEvaluationa": {"src_id": "SRC-023", "pdf": "Wu et al. - 2024 - Automated novelty evaluation.pdf"},
    "xuCanLLMsIdentify2025": {"src_id": "SRC-024", "pdf": "Xu et al. - 2025 - Can LLMs Identify Critical Limitations within Scientific Research A Systematic Evaluation on AI Res.pdf"},
    "zhangDetectingReferenceErrors2024": {"src_id": "SRC-025", "pdf": "Zhang and Abernethy - 2024 - Detecting Reference Errors in Scientific Literature with Large Language Models.pdf"},
    "zhangReviewingScientificPapers2025a": {"src_id": "SRC-026", "pdf": "Zhang and Abernethy - 2025 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs Baseline Approaches and Autom.pdf"},
    "zhouLLMReliableReviewer2024": {"src_id": "SRC-027", "pdf": "Zhou - Is LLM a Reliable Reviewer A Comprehensive Evalua.pdf"},
}


def extract_text(pdf_path: Path) -> str:
    with fitz.open(pdf_path) as doc:
        return "\n".join(page.get_text() for page in doc)


def main() -> int:
    if not os.environ.get("PANGRAM_API_KEY"):
        print("PANGRAM_API_KEY is not set in the environment.", file=sys.stderr)
        return 1

    client = Pangram()

    # --resume <bulk_id>: skip (re-billed) submission entirely and just poll
    # an already-submitted job. Use this after a crash/network error during
    # wait_for_bulk so a transient failure never costs a re-submission. We
    # don't know which citekeys were in that job ahead of time, so accept
    # whatever comes back rather than filtering/validating against TARGETS.
    resuming = len(sys.argv) >= 3 and sys.argv[1] == "--resume"

    if resuming:
        bulk_id = sys.argv[2]
        selected = None
        print(f"Resuming bulk job {bulk_id} (no new submission)...", file=sys.stderr)
    else:
        # Optional citekey filter (argv) so a limited-credit run can target a
        # specific subset instead of the full TARGETS dict.
        selected = sys.argv[1:] or list(TARGETS.keys())
        unknown = [c for c in selected if c not in TARGETS]
        if unknown:
            print(f"Unknown citekey(s): {unknown}", file=sys.stderr)
            return 1
        items = []
        for citekey in selected:
            meta = TARGETS[citekey]
            pdf_path = PDF_DIR / meta["pdf"]
            if not pdf_path.exists():
                print(f"Missing PDF for {citekey}: {pdf_path}", file=sys.stderr)
                return 1
            text = extract_text(pdf_path)
            items.append({"id": citekey, "text": text})

        print(f"Submitting {len(items)} items to Pangram Bulk API (model={MODEL})...", file=sys.stderr)
        job = client.submit_bulk(items=items, model=MODEL)
        bulk_id = job["bulk_id"]
        print(f"Bulk job id: {bulk_id}  (save this — pass '--resume {bulk_id}' to recover "
              f"without re-submitting if anything below fails)", file=sys.stderr)

    print("Waiting for completion...", file=sys.stderr)
    last_error = None
    for attempt in range(6):
        try:
            client.wait_for_bulk(bulk_id)
            last_error = None
            break
        except ValueError as exc:
            last_error = exc
            print(f"Transient error polling bulk status (attempt {attempt + 1}/6): {exc}", file=sys.stderr)
            time.sleep(min(2 ** attempt, 30))
    if last_error is not None:
        print(f"Giving up polling {bulk_id}; resume later with '--resume {bulk_id}'.", file=sys.stderr)
        raise last_error

    for attempt in range(6):
        try:
            bulk_results = client.get_bulk_results(bulk_id)
            break
        except ValueError as exc:
            print(f"Transient error fetching results (attempt {attempt + 1}/6): {exc}", file=sys.stderr)
            time.sleep(min(2 ** attempt, 30))
            if attempt == 5:
                print(f"Giving up fetching results for {bulk_id}; resume later with '--resume {bulk_id}'.", file=sys.stderr)
                raise

    results = {}
    for item in bulk_results["items"]:
        citekey = item["id"]
        if citekey not in TARGETS:
            print(f"Unmatched result id: {citekey}", file=sys.stderr)
            continue
        results[citekey] = {**TARGETS[citekey], "pangram_result": item["result"]}

    missing = (set(selected) - set(results)) if selected is not None else set()
    if missing:
        print(f"No result returned for: {sorted(missing)}", file=sys.stderr)

    out_path = VAULT / "misc" / f"pangram_check_{date.today().isoformat()}.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))
    print(f"\nWrote {out_path}", file=sys.stderr)
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
