#!/usr/bin/env python3
"""
Simple keyword-frequency scan across all 27 SRC PDFs for a user-supplied
list of AI-writing-tell words. Not the Pangram AI-detection check — this is
a cheap, local, no-API keyword count.

Matching: case-insensitive, word-boundary, plus a plain plural ("s"/"es")
where the term is a singular noun. Root/inflected pairs the list already
distinguishes (genuine/genuinely, silent/silently, gating/gated) are kept
separate on purpose, not stemmed into one bucket.
"""
import json
import re
from pathlib import Path

import fitz  # PyMuPDF

PDF_DIR = Path("/Users/ppatel/Documents/living-synthesis/source/pdfs")

# word -> regex pattern (case-insensitive, word-boundary applied at use site)
WORDS = {
    "load-bearing": r"load[\s-]?bearing",
    "gating": r"gatings?",
    "dedup": r"dedups?|deduplicat\w*",
    "decisive": r"decisive(?:ly|ness)?",
    "verdict": r"verdicts?",
    "scaffolds": r"scaffolds?(?:ing)?",
    "settles": r"settles?|settled|settling",
    "handoff": r"hand[\s-]?offs?",
    "prod": r"prod\b",
    "gated": r"gated",
    "genuinely": r"genuinely",
    "honest": r"honest(?:ly|y)?",
    "signal": r"signals?",
    "blocker": r"blockers?",
    "drift": r"drift(?:s|ed|ing)?",  # user typed "drif" — treated as this typo
    "genuine": r"genuine\b",
    "silent": r"silent\b",
    "silently": r"silently",
    "quietly": r"quietly",
    "clean": r"clean(?:er|est)?\b",
    "surface": r"surfaces?(?:d|ing)?",
}

# citekey -> PDF filename, all 27 sources
PDFS = {
    "akyonEvaluatingCapabilitiesGenerative2024": "Akyon et al. - 2024 - Evaluating the capabilities of generative AI tools in understanding medical papers Qualitative stud.pdf",
    "alharbiAutomatedAssessmentReporting2024": "Alharbi and Asiri - 2024 - Automated Assessment of Reporting Completeness in Orthodontic Research Using LLMs An Observational.pdf",
    "bougieGenerativeAdversarialReviews2024a": "Bougie et al. - 2024 - Generative Adversarial Reviews.pdf",
    "darcyMARGMultiAgentReview2024": "D'Arcy et al. - 2024 - MARG Multi-Agent Review Generation for Scientific Papers.pdf",
    "hasanIntegratingLargeLanguage2024": "Hasan et al_2024_Integrating large language models in systematic reviews.pdf",
    "huntington-kleinLLMsActRepositories2024": "Huntington-Klein and Murray - 2024. - Do LLMs Act as Repositories of Causal Knowledge.pdf",
    "idahlOpenReviewerSpecializedLarge2025": "Idahl and Ahmadi - 2025 - OpenReviewer A Specialized LLM.pdf",
    "leucutaRiskBiasAssessment2025": "Leucuta et al. 2025 - Risk of Bias Assessment of Diagnositic Accuracy Studies.pdf",
    "liangCanLargeLanguage2024a": "Liang et al. - 2024 - Can Large Language Models Provide Useful Feedback on Research Papers A Large-Scale Empirical Analys.pdf",
    "liuReviewerGPTExploratoryStudy2023": "Liu and Shah - 2023 - ReviewerGPT An Exploratory Study on Using Large Language Models for Paper Reviewing.pdf",
    "louAAAR10AssessingAIs2025": "Lou et al. - 2025 - AAAR-1.0 Assessing AI's Potential to Assist Resea.pdf",
    "robertsComparativeStudyChatGPT2023": "Roberts et al. 2023 - Comparative study of ChatGPT and human evaluators.pdf",
    "sarolAssessingCitationIntegrity2024": "Sarol et al. - 2024 - Assessing citation integrity.pdf",
    "shahidLiteratureGroundedNoveltyAssessment2025": "Shahid et al. - 2025 - Literature-Grounded Novelty Assessment of Scientific Ideas.pdf",
    "sonWhenAICoScientists2025": "Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchmark for Automated Verification of Scientific Research.pdf",
    "sridharanAssessingDecisionMakingCapabilities2024": "Sridharan and Sivaramakrishnan - 2024 - Assessing the Decision-Making Capabilities of AI.pdf",
    "sridharanLeveragingArtificialIntelligence2025": "Sridharan and Sivaramakrishnan - 2024 - Leveraging artificial intelligence.pdf",
    "srinivasanEvaluatingReportingQuality2025a": "Srinivasan et al. - 2025 - Evaluating the reporting quality of 21,041 randomized controlled trial articles.pdf",
    "thelwallEvaluatingResearchQuality2024": "Thelwall - 2024 - Evaluating Research Quality with Large Language Models An Analysis of ChatGPT's Effectiveness with.pdf",
    "tyserAIDrivenReviewSystems2024": "Tyser et al. - 2024 - AI-Driven Review Systems Evaluating LLMs in Scalable and Bias-Aware Academic Reviews.pdf",
    "woelfleBenchmarkingHumanAICollaboration2024": "Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf",
    "wrightsonGPTRCTsUsing2025": "Wrightson et al. - 2025 - GPT for RCTs Using AI to determine adherence to clinical trial reporting guidelines.pdf",
    "wuAutomatedNoveltyEvaluationa": "Wu et al. - 2024 - Automated novelty evaluation.pdf",
    "xuCanLLMsIdentify2025": "Xu et al. - 2025 - Can LLMs Identify Critical Limitations within Scientific Research A Systematic Evaluation on AI Res.pdf",
    "zhangDetectingReferenceErrors2024": "Zhang and Abernethy - 2024 - Detecting Reference Errors in Scientific Literature with Large Language Models.pdf",
    "zhangReviewingScientificPapers2025a": "Zhang and Abernethy - 2025 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs Baseline Approaches and Autom.pdf",
    "zhouLLMReliableReviewer2024": "Zhou - Is LLM a Reliable Reviewer A Comprehensive Evalua.pdf",
}


def extract_text(pdf_path: Path) -> str:
    with fitz.open(pdf_path) as doc:
        return "\n".join(page.get_text() for page in doc)


def main():
    compiled = {w: re.compile(rf"\b{pat}\b", re.IGNORECASE) for w, pat in WORDS.items()}
    rows = []
    for citekey, pdf_name in PDFS.items():
        pdf_path = PDF_DIR / pdf_name
        if not pdf_path.exists():
            print(f"MISSING: {citekey} -> {pdf_path}")
            continue
        text = extract_text(pdf_path)
        word_count = len(re.findall(r"\b\w+\b", text))
        counts = {w: len(rx.findall(text)) for w, rx in compiled.items()}
        total = sum(counts.values())
        rows.append({
            "citekey": citekey,
            "word_count": word_count,
            "total_hits": total,
            "rate_per_1000": round(total / word_count * 1000, 2) if word_count else 0,
            "counts": counts,
        })
    out_path = Path("/private/tmp/claude-501/-Users-ppatel/e5c11288-2632-4b4e-9ba3-04dc3e16228c/scratchpad/keyword_freq_results.json")
    out_path.write_text(json.dumps(rows, indent=2))
    print(f"Wrote {out_path}")
    print(f"Processed {len(rows)} of {len(PDFS)} papers")


if __name__ == "__main__":
    main()
