#!/usr/bin/env python3
"""TRIPOD-LLM reporting items rated by the paper processor (JP, 2026-11-26). The 40 rows are the ones every curated source page carries (item 2, the Abstract, is assessed
separately and item 17, Performance, is reported per EVD). Ids and names are taken from the 27 source pages; the one-line descriptions are written here to give the raters
the same reading for each row. Healthcare wording in the guideline is read as research-evaluation context (as on the source pages)."""
ITEMS = {
 '1': ('Title', 'The title identifies the work as developing or evaluating a large language model and names the task or domain.'),
 '3a': ('Background: context + rationale', 'The introduction explains the context and the reason for the study.'),
 '3b': ('Background: target population', 'The intended users, population or setting of the LLM application is stated.'),
 '4': ('Objectives', 'The objectives or research questions are stated.'),
 '5a': ('Data sources', 'The sources of the data used for development or evaluation are named (dataset, database, collection method).'),
 '5b': ('Data points + distribution', 'The number of data points and their distribution (classes, categories, sizes) are reported.'),
 '5c': ('Date range of data', 'The dates the data cover, or when data were collected, are reported.'),
 '5d': ('Pre-processing / quality checks', 'Pre-processing and data quality checks are described.'),
 '5e': ('Missing / imbalanced data', 'Missing, excluded or imbalanced data and how they were handled are described.'),
 '6a': ('LLM name + version', 'Each LLM is named with its version, snapshot or date.'),
 '6b': ('Development process', 'How the model was developed, fine-tuned or adapted is described (or the paper states it used models off the shelf).'),
 '6c': ('Inference settings / prompting', 'Inference settings (for example temperature, number of runs) and the prompting approach are reported.'),
 '6d': ('Output', 'The form of the model output and how it is used or parsed is described.'),
 '6e': ('Classification thresholds', 'Thresholds or decision rules applied to model output are reported (not applicable when nothing is thresholded).'),
 '7a': ('Quality metrics', 'The metrics used to judge output quality are named and defined.'),
 '7b': ('Relevance to downstream use', 'The paper explains why the metrics matter for the intended downstream use.'),
 '7c': ('Outcome definition', 'The outcome or reference standard is defined.'),
 '7d': ('Subjective interpretation', 'Subjective judgments in evaluation (for example rating or free-text grading) are described and handled.'),
 '7e': ('Comparison', 'Comparators (humans, other models, baselines) are described.'),
 '8a': ('Annotation guidelines', 'Annotation or rating guidelines are described or provided (not applicable when nothing was annotated).'),
 '8b': ('Annotators + IAA', 'The number of annotators and inter-annotator agreement are reported.'),
 '8c': ('Annotator background', 'The expertise or background of annotators is reported.'),
 '9a': ('Prompt design', 'The prompts, or how they were designed, are reported.'),
 '9b': ('Prompt-development data', 'The data used to develop or tune prompts are described and kept apart from evaluation data.'),
 '10': ('Summarization', 'Evaluation of summarization quality, when the LLM summarizes (not applicable otherwise).'),
 '11': ('Instruction tuning / alignment', 'Instruction tuning or alignment of the model is described (not applicable for off-the-shelf use).'),
 '12': ('Compute', 'Compute resources (hardware, run time, cost) are reported.'),
 '13': ('Ethical approval', 'Ethical approval, exemption or a statement that none was needed is reported.'),
 '14a': ('Funding', 'Funding sources are reported.'),
 '14b': ('Conflicts of interest', 'Conflicts of interest are reported.'),
 '14c': ('Protocol', 'A study protocol is available or its absence is stated.'),
 '14d': ('Registration', 'Study registration is reported or its absence is stated.'),
 '14e': ('Data availability', 'Where the data can be accessed, or why they cannot, is reported.'),
 '14f': ('Code availability', 'Where the code or prompts can be accessed, or why they cannot, is reported.'),
 '15': ('Patient/public involvement', 'Involvement of patients, the public or end users in the study is reported (not applicable when none).'),
 '16a': ('Flow of data', 'The flow of data through the study (for example how many items were included at each step) is reported.'),
 '16b': ('Characteristics', 'The characteristics of the data or participants are reported.'),
 '16c': ('Distribution comparison', 'Development and evaluation data are compared (for example class distributions).'),
 '16d': ('N per analysis', 'The number of data points in each analysis is reported.'),
 '18': ('LLM updating', 'Whether the LLM changed during the study (version updates, drift) and how that was handled is reported.'),
}
VALUES = 'fully | partial | not-reported | not-applicable'
ICON_TO_RATING = {'✅': 'fully', '●': 'fully', '⚠️': 'partial', '◐': 'partial', '❌': 'not-reported', '○': 'not-reported', '➖': 'not-applicable', '–': 'not-applicable'}


def signals():
    return {f'tripod-{k}': (f'TRIPOD-LLM item {k} ({name}): {desc} Rate whether the paper reports it. Healthcare wording in the guideline is read as research-evaluation context.', VALUES) for k, (name, desc) in ITEMS.items()}


def label(sig):
    k = sig.replace('tripod-', '', 1); return f"TRIPOD-LLM {k}: {ITEMS[k][0]}" if k in ITEMS else sig


def summary(ratings):
    """ratings: {signal id: rating}. Share of applicable items fully reported, with partial counting half (a proposed measure; the thresholds for the level are not validated). Rows marked needs_human (the raters were not confident) are left out of the share and counted separately."""
    r = [v for s, v in ratings.items() if s.startswith('tripod-') and v in ('fully', 'partial', 'not-reported', 'not-applicable')]
    n = {k: r.count(k) for k in ('fully', 'partial', 'not-reported', 'not-applicable')}; app = len(r) - n['not-applicable']
    pct = round(100 * (n['fully'] + 0.5 * n['partial']) / app) if app else None
    return {**n, 'needs_human': sum(1 for s, v in ratings.items() if s.startswith('tripod-') and v == 'needs_human'), 'applicable': app, 'pct': pct, 'level': None if pct is None else ('high' if pct >= 75 else 'moderate' if pct >= 50 else 'low')}
