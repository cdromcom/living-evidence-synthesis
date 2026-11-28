#!/usr/bin/env python3
"""Hover notes for the column headers of the review sheets (JP, 2026-11-26). Written for a reader outside the project: plain sentences, terms explained.
note_for(tab, header) returns the note text; every header the sheet builder writes must have one (selftest checks). Used by run_to_gsheet.py (openpyxl comments become Google Sheets notes)
and by apply_notes_requests() to add notes to an existing Google Sheet without regenerating it."""
import re

# Terms used in the notes: EVD = an evidence statement (one finding of a paper with its numbers); QUE = a research question; CLM = a claim; CVT = a caveat (limitation);
# PICOST = Population, Intervention, Comparator, Outcome, Study design, Timeframe.
N = {
 'Paper': 'The paper being processed (first author, year and a short title).',
 'File': 'File name of the PDF that was read.', 'Pages': 'Number of pages in the PDF.',
 'Status': 'Whether the paper was processed (ok) or why it was not.',
 'Primary findings': 'Number of findings that answer one of the paper\'s own research questions directly.',
 'Secondary findings': 'Number of findings that qualify or add context to a primary finding.',
 'Tertiary findings': 'Number of other, less central findings (background, side results).',
 'Flagged': 'Number of findings that an automatic check marked as doubtful and sent for a second reading.',
 'Disagreements': 'Number of re-read findings on which the second reader\'s numbers differed from the first reader\'s.',
 'Cost USD': 'Money spent on this paper\'s extraction, in US dollars, at batch-mode prices.',
 # findings
 'Id': 'Number of the finding within the paper (F1, F2, ...).',
 'Tier': 'How central the finding is: primary (answers a research question directly), secondary (qualifies a primary finding) or tertiary (other).',
 'Why this tier': 'The extracting model\'s one-sentence reason for the tier.',
 'Supports': 'For secondary and tertiary findings, the primary findings they support.',
 'Statement (Neon)': 'The finding as one sentence with its numbers, written by the extraction model (Gemini 4 Neon).',
 'Population': 'Who or what was studied (for example 112 systematic reviews).',
 'Intervention': 'What was tested or done (for example a language model and how it was prompted).',
 'Comparator': 'What the intervention was compared with (for example human experts or another model).',
 'Outcome': 'What was measured (for example agreement with human ratings).',
 'Study design': 'How the study was set up (for example a benchmark on a fixed dataset).',
 'Timeframe': 'When data were collected or models were run. "Not reported" means the paper does not say.',
 'Numbers with locators': 'Every number behind the finding, with where it appears in the paper (table, row, column, page).',
 'Confidence': 'The extracting model\'s own confidence in the finding (high, medium or low).',
 'Flags': 'Automatic warnings, for example evidence spread over two pages, a quote that differs from the printed text, or a number missing from the numbers list.',
 'Sent to recheck': 'Whether a second AI model (GPT-6.2 Sol) re-read this finding because of a flag.',
 'Sol vs Neon': 'Whether the second reader\'s numbers agree with the first reader\'s.',
 'Opus verdict': 'When the two readers differ, which one a third model (Claude Opus 5.5) judged correct.',
 'Merged screenshot (image; shown when the evidence crosses a page break)': 'One image that joins the evidence from the two pages it spans. Empty when the evidence is on one page.',
 'Evidence crop (image)': 'A cropped page image of the evidence with the quoted text highlighted.',
 'Highlighted page (image)': 'The PDF page with the quoted text highlighted.',
 'Answers question(s)': 'The paper\'s research questions that this finding helps answer.',
 'Candidate EVD: Sonnet 5.5': 'Evidence statement (EVD) drafted by Claude Sonnet 5.5 in the first drafting round. Only the main findings get drafts from three models.',
 'Candidate EVD: Sol 6.2': 'Evidence statement (EVD) drafted by GPT-6.2 Sol in the first drafting round.',
 'Candidate EVD: Neon (Gemini 4)': 'Evidence statement (EVD) drafted by Gemini 4 Neon in the first drafting round.',
 'Chosen EVD [author; how chosen]': 'The statement selected after critique and voting, with the model that wrote it and how it was chosen.',
 'Chosen EVD status': 'Result of the automatic checks on the chosen statement: pass, reworked by another model, or needs human review.',
 # quote checks
 'Finding': 'The finding (F1, F2, ...) this row is about.',
 'Span': 'Number of the quote within the finding.',
 'Quoted span (verbatim)': 'The exact text the extraction model quoted from the paper as evidence.',
 'Page cited': 'The PDF page the model named for the quote.',
 'Found in PDF text': 'Whether the quote was found in the PDF\'s text layer (yes or no).',
 'Pages where found': 'The PDF pages on which the quote text was actually found.',
 'Word boxes': 'Number of word rectangles located for the quote (used to highlight it).',
 # rechecks
 'Neon numbers': 'Numbers the first reader (Gemini 4 Neon) recorded for this finding.',
 'Sol numbers': 'Numbers the second reader (GPT-6.2 Sol) recorded for the same finding, read without seeing the first reader\'s.',
 'Compare': 'Whether the two readers\' numbers agree or differ.',
 'Opus verdict (A = Neon, B = Sol)': 'Which reader a third model (Claude Opus 5.5) judged correct: A is Neon, B is Sol.',
 'Opus reason': 'The third model\'s explanation of its judgment.',
 # decision-model checks
 'Statement': 'The finding as one sentence (first 300 characters).',
 'Relevancy': 'Average probability (0 to 1) from two decision models that the finding is relevant to the project\'s research question.',
 'Fidelity': 'Average probability (0 to 1) from two decision models that the statement restates its quoted source faithfully.',
 'Numbers found in source': 'Average probability (0 to 1) from two decision models that the statement\'s numbers appear in the quoted source or numbers list.',
 'Table cell matches': 'Average probability (0 to 1) from two decision models that numbers taken from a table match the right table cell. Empty when the finding is not based on a table.',
 'Score (lowest mean)': 'The lowest of the four averages. A low score means at least one check doubts the finding.',
 'Spread between models': 'The largest difference between the two decision models\' answers on any question.',
 'Why Sol looked': 'Why a screenshot check by GPT-6.2 Sol was run on this finding (every finding gets one).',
 'Sol vision': 'GPT-6.2 Sol\'s verdict after looking at the screenshot: pass, not matched or cannot verify.',
 'Sol reason': 'GPT-6.2 Sol\'s short explanation of its verdict.',
 'Opus (disputes only)': 'Verdict of Claude Opus 5.5, asked only when the decision models and the screenshot check disagree.',
 'Result': 'Final automatic result for the item (see the tab name for what is being judged).',
 'Crop Sol looked at (image)': 'The cropped page image that GPT-6.2 Sol examined.',
 'Liquid d1-ultra OLD: lowest question score': 'Lowest score for this finding from the earlier decision model Liquid d1-ultra, kept for comparison (0 to 1).',
 'Liquid d1.2-ultra: lowest question score': 'Lowest score for this finding from the current decision model Liquid d1.2-ultra (0 to 1).',
 'Perplexity Decider 1.3: lowest question score': 'Lowest score for this finding from the second decision model, Perplexity Decider 1.3 (0 to 1).',
 # drafts
 'Node': 'The drafted discourse-graph node: E- is an evidence statement, Q- a question, C- a claim, V- a caveat, followed by the source id.',
 'Type': 'Node type: EVD (evidence), QUE (question), CLM (claim) or CVT (caveat).',
 'Winner by': 'The AI model whose draft was chosen.',
 'How decided': 'How the winner was chosen (for example the other two models voted for it, or a tie was broken).',
 'Winning text': 'The chosen text of the node.',
 'Chars': 'Number of characters in the chosen text. Evidence statements may not exceed 247.',
 'Writing rules pass': 'Whether the text passes the automatic writing rules: length, numbers present in the source, at most two parenthesis sets, no brackets, no all-caps words, no em dash.',
 'Numbers not on the card': 'Numbers in the text that are missing from the finding\'s numbers list (the "card").',
 'Node-detail check': 'Whether a model found the drafted node consistent with its quote: pass, minor problem or fail.',
 'Fix suggested': 'The checking model\'s suggested correction, if any.',
 'Checked by': 'The model that ran the node-detail check.',
 'Decision-model score': 'Average decision-model score for the text (0 to 1). Below 0.60 sends an EVD to rework.',
 'First draft: Sonnet': 'First-round draft by Claude Sonnet 5.5.', 'First draft: Sol': 'First-round draft by GPT-6.2 Sol.', 'First draft: Neon': 'First-round draft by Gemini 4 Neon.',
 # low scores
 'Drafted EVD statement': 'The evidence statement as drafted.',
 'Score (lowest)': 'The lowest decision-model score for the statement (0 to 1).',
 'Lowest question': 'Which question gave the lowest score: relevancy, fidelity, numbers found in source or table cell matches.',
 'Numbers in the statement that are not in the source span': 'Numbers the statement contains that the quoted source does not.',
 'Source span length (characters)': 'Length of the quoted source text the models saw.',
 'Source span(s) the models saw': 'The quoted source text the decision models compared the statement with.',
 'Numbers with locators the models saw': 'The numbers list (with table and page) the decision models saw.',
 # rework
 'Original EVD statement': 'The statement before rework.',
 'Decision-model score before': 'Decision-model score of the original statement.',
 'Where Opus found each number': 'For each number in the statement, where Claude Opus 5.5 found it: in the quote, the numbers list, the screenshot or nowhere.',
 'Numbers found nowhere': 'Numbers Opus could not find in any source.',
 'Fidelity problems': 'Mismatches Opus found between the statement and its source (model names, comparator, direction, scope).',
 'Verdict': 'Opus\'s decision: ok (statement is fine), rewrite, or extraction problem (the source data look wrong).',
 'Proposed rewrite': 'The rewritten statement when Opus chose rewrite.',
 'Decision-model score after': 'Decision-model score of the rewrite.',
 'Rewrite accepted': 'Whether the rewrite scored well enough to replace the original.',
 'Note for the reviewer': 'What a person should check.',
 'Final status': 'Status of the statement after rework.',
 # writing rules
 'Text as drafted': 'The text that broke a writing rule.', 'Which rule failed': 'The rule or rules the text broke.', 'Characters': 'Number of characters in the text.',
 # verification
 'Node type': 'Kind of item checked: PICOST (one slot of a finding), QUOTE, QUE (question rewording), CLM (claim), CVT (caveat) or QUALITY (a quality rating). "CLM quote" means the quote behind a claim.',
 'Node id': 'Identifier of the item (finding F4, claim C2, caveat V1, and so on).',
 'What was checked': 'The question the verifiers answered about the item.',
 'Item (as extracted)': 'The extracted item being checked, as the pipeline wrote it.',
 'Screenshot (image)': 'Page image of the quote with the quoted text highlighted.',
 'Sonnet 5.5 score': 'Claude Sonnet 5.5\'s judgment: 1 supported, 0.5 unsure, 0 not supported. Empty when Sonnet was not called because the two decision models agreed.',
 'Sonnet 5.5 reason': 'Sonnet\'s one-sentence reason, or "not called" when the decision models agreed.',
 'Perplexity Decider 1.3 (probability)': 'Probability (0 to 1) from the decision model Perplexity Decider 1.3 that the item is supported by its passage.',
 'Liquid d1.2-ultra, text (probability)': 'Probability (0 to 1) from the decision model Liquid d1.2-ultra, reading text, that the item is supported by its passage.',
 'Majority vote': 'Pass, fail or split, from the models that voted.',
 'Mean score': 'Average of the available scores (0 to 1).',
 'Models agreeing with the majority': 'How many voting models gave the majority verdict.',
 'Sonnet pass (1 or 0)': 'Sonnet\'s verdict as 1 (pass) or 0; empty if unsure or not called.', 'Perplexity pass (1 or 0)': 'Perplexity\'s verdict as 1 (probability 0.5 or more) or 0.',
 'Liquid d1.2-ultra text pass (1 or 0)': 'd1.2-ultra\'s text verdict as 1 (probability 0.5 or more) or 0.', 'Majority pass (1 or 0)': 'The majority verdict as 1 or 0; empty when split.', 'Mean pass (1 or 0)': 'The mean score as 1 (0.5 or more) or 0.',
 'Truth used for scoring (formula)': 'Formula: the human reviewer\'s yes/no judgment turned into 1 or 0. The summary tab scores each verifier against it.',
 'Liquid d1.2-ultra reading the screenshot (probability)': 'Probability (0 to 1) from Liquid d1.2-ultra, looking at the screenshot, that the quote\'s digits match the highlighted text.',
 'Liquid screenshot score counts as a vote? (digit comparisons on quotes only)': 'yes when the screenshot score is used in the majority (quotes containing digits). Quotes without digits are checked by Sonnet 5.5 instead.',
 'Liquid d1-ultra OLD, text (probability)': 'Score from the earlier decision model Liquid d1-ultra, kept for comparison.', 'Liquid d1-ultra OLD pass (1 or 0)': 'The old model\'s verdict as 1 or 0.',
 'Liquid d1.2-ultra screenshot pass (1 or 0)': 'The screenshot verdict as 1 or 0.',
 'Passage or quote it was checked against': 'The text the item was compared with.',
 'Labeling queue (tonight)': 'The order in which the human reviewer is asked to label items: 1 claims, 2 caveats, 3 a random quarter of quality ratings, 4 question rewordings.',
 'Share of item words not found in the passage (CLM, CVT, QUE; 0 = every word is in the passage)': 'A simple similarity measure: the share of the item\'s content words that do not appear in its passage. Higher means the item goes further beyond its quote.',
 'Before the rerun (cited pages only, or the stricter question): Sonnet 5.5 score': 'Sonnet\'s score before the rerun that added the Methods pages or loosened the wording check.',
 'Before the rerun: Perplexity (probability)': 'Perplexity\'s probability before the rerun.', 'Before the rerun: Liquid d1.2-ultra text (probability)': 'd1.2-ultra\'s probability before the rerun.',
 'Baseten bison-1, text (probability; shadow verifier, not in any vote)': 'Probability (0 to 1) from the 31B decision model Baseten bison-1 that the item is supported by its passage. Shown for comparison; it does not count in the majority until the human reviewer\'s labels show how it performs.',
 # verification summary
 'Verifier': 'The model or combination being scored.', 'Items scored (not abstained)': 'Number of items on which the verifier gave a judgment.', 'Share judged correct': 'Share of scored items the verifier judged supported.',
 'Agreement with the majority vote': 'How often the verifier agrees with the majority verdict.', 'Items with JP ground truth': 'Number of items the human reviewer has labeled.',
 'Accuracy vs JP': 'Share of labeled items on which the verifier agrees with the human reviewer.',
 'Precision vs JP (of items it passed, how many JP calls correct)': 'Of the items the verifier passed, the share the human reviewer also judged correct.',
 'Recall vs JP (of items JP calls correct, how many it passed)': 'Of the items the human reviewer judged correct, the share the verifier passed.',
 'Specificity vs JP (of items JP calls wrong, how many it failed)': 'Of the items the human reviewer judged wrong, the share the verifier did not pass.',
 'Items': 'Number of items of this node type.', 'Share the majority judged correct': 'Share of items whose majority verdict was pass.', 'Split votes': 'Number of items on which the voting models did not reach a majority.',
 # quality signals per paper
 'Kind': 'Code-only check (automatic, no AI) or Signal (a quality signal rated by AI models).',
 'Signal or check': 'Name of the quality signal (for example Data Leakage) or of the automatic check (for example Retraction status).',
 'Agreement or status': 'For signals: whether the two raters agreed. For checks: ok, flag (needs a person) or unavailable.',
 'Summary': 'One sentence on the result.',
 'Neon rating': 'Rating by Gemini 4 Neon, one of three independent raters.', 'Neon quote and locator': 'The passage Neon quoted as evidence, with its section and page.', 'Neon screenshot (image)': 'Page image of Neon\'s quote, highlighted.',
 'Opus rating': 'Rating by Claude Opus 5.5, the second of three independent raters.', 'Opus quote and locator': 'The passage Opus quoted as evidence, with its section and page.', 'Opus screenshot (image)': 'Page image of Opus\'s quote, highlighted.',
 'Sol rating (third rater)': 'Rating by GPT-6.2 Sol, the third independent rater (older runs: asked only when Neon and Opus differed).',
 'Quote verifiers (mean score: Sonnet 5.5, Liquid d1.2-ultra, Perplexity)': 'Average scores (0 to 1) from three verifiers on whether the quotes support the ratings.',
 'Live-site tag (Aug 2026)': 'The value for this signal currently shown on the LIVES website, curated in August 2026, for comparison.',
 'Matches live-site tag?': 'Whether the final rating equals the value on the LIVES website.',
 'Code-only checks that apply': 'Automatic checks that bear on this signal, such as link or repository checks.',
 'Source and date': 'Where the check looked (web address) and when.',
 'TRIPOD-LLM item': 'The reporting item from the TRIPOD-LLM guideline (for example 5a Data sources): does the paper report it?',
 'New: fully reported': 'Number of the 40 rated TRIPOD-LLM items the paper fully reports, by the current raters.', 'New: partial': 'Number of items reported in part.', 'New: not reported': 'Number of items the paper does not report.', 'New: not applicable': 'Number of items that do not apply to this paper.',
 'New: share reported (partial counts half) and level': 'Share of applicable items reported (fully = 1, partial = 0.5) and a level: high 75% or more, moderate 50% or more, otherwise low. The level thresholds are a proposal and not validated.',
 'Old table: fully reported': 'Same count from the table curated earlier on the website (older Claude models).', 'Old: partial': 'Old table: items reported in part.', 'Old: not reported': 'Old table: items not reported.', 'Old: not applicable': 'Old table: items not applicable.', 'Old table: share and level': 'Same share and level computed from the old table.',
 'New rating equals old curated rating': 'On how many items the current rating equals the old table\'s rating (items rated in both).',
 # run summary
 'Vault citekey': 'The paper\'s identifier in the project\'s knowledge base.', 'Signals rated by models': 'Number of quality signals the AI raters rated.', 'All raters agree': 'Number of signals on which all raters gave the same rating.',
 'No majority': 'Number of signals with no majority rating.', 'Quotes not found in PDF': 'Number of rater quotes that could not be located in the PDF text.',
 'Matches live-site tag': 'How many ratings equal the value on the LIVES website, out of those that can be compared.',
 'Code-only checks ok': 'Number of automatic checks with nothing to flag.', 'Code-only checks flagged': 'Number of automatic checks that found something for a person to look at.',
 'Code-only checks unavailable': 'Number of automatic checks that could not run (for example no repository link).',
 'Rating cost USD': 'Money spent on the AI ratings for this paper, in US dollars, billed at batch prices.', 'Cost by model': 'The same cost split by model.',
 'Rating time (s, batch wait included)': 'Seconds from submitting the ratings to the last answer, including waiting in the provider\'s batch queue.', 'Code-only check time (s)': 'Seconds the automatic checks took (web lookups are cached for 30 days).',
 # numbers check
 'Cited PDF pages': 'PDF pages the finding\'s quotes come from.', 'Statement (first 200 characters)': 'The start of the finding\'s statement.',
 'Numbers not in the text of the cited pages': 'Numbers in the statement that the PDF text of the cited pages does not contain (they may sit in a table image).',
 'Liquid d1.2-ultra: number appears on the screenshots (probability)': 'Probability (0 to 1) that the number is visible on the screenshots, per number.',
 'Control: same number with one digit changed (should be low)': 'Same question with one digit changed. A high score here means the check is unreliable for that number.',
 'Result per number': 'Seen on screenshot, too short to check, unclear, or not found (needs a person).', 'Screenshots looked at (image)': 'The images the model examined.',
 # failure analysis
 'Where the item is': 'Row of the item in the Verification (all nodes) tab.', 'Passage it was checked against': 'The text the item was compared with.',
 'Classifier: who is right': 'The classifier model\'s view: the extraction is correct, the extraction is wrong, or unclear.', 'Classifier: kind of revision': 'Kind of revision to note that the classifier assigned (see the Revision kinds tab).',
 'Classifier: reason': 'The classifier\'s explanation naming the words or numbers involved.', 'Classifier: cheapest change': 'The simplest change that would remove this kind of revision.',
 'ambiguous_instruction': 'The question asked of the verifier allows more than one reading.', 'claim_stronger_than_quote': 'The claim is stronger or more general than the quote supports.',
 'detail_dropped': 'The item leaves out a qualifier or number that changes the meaning.', 'other': 'A problem that fits no other type.',
 'rating_defensible_quote_weak': 'The rating may be right, but the quote does not show why.', 'rating_not_supported_by_quote': 'The rating does not follow from the quote.',
 'scope_added': 'The item adds a population, dataset, model or condition that the quote does not name.', 'value_outside_shown_passage': 'The value is probably right but is stated somewhere the verifier was not shown, such as Methods.',
 'verifier_too_strict': 'The item is acceptable and the verifier asked for more than the question needs.', 'wrong_or_invented_value': 'A number, name or value is wrong or not in the paper.', 'verifier_misread': 'The verifier misread the passage or the question.',
 'Sampled items': 'Number of sampled items of this node type.',
 # raw ratings and votes
 'Signal': 'Name of the quality signal being rated.', 'Rater': 'The AI model that gave this rating.', 'Counted in the vote': 'yes when the rating counts toward the majority; benchmark-only otherwise.',
 'Rating': 'The rating this model gave.', 'Quote': 'The passage the model quoted as evidence, copied from the PDF text.', 'Locator': 'Section and page of the quote.', 'Quote found in PDF': 'Whether the quote was located in the PDF text.',
 'Quote highlighted and boxed in the PDF (image)': 'Page image with the quote highlighted.', 'Votes': 'Ratings given and how many raters gave each.', 'Majority': 'The rating chosen by most raters.',
 'Agreement': 'Whether the raters agreed, or which one the adjudicator sided with.', 'Quotes not found': 'Number of quotes behind this signal that were not found in the PDF.',
 # question groups
 'group id': 'Identifier of a group of similar research questions.', 'level': 'Position in the question hierarchy: primary, secondary or tertiary.', 'parent group id': 'The broader group this group sits under.',
 'unified question': 'One question worded to cover all members of the group.', 'member paper': 'The paper a member question comes from.', 'member id': 'Identifier of the member question.', 'member wording': 'The question as the paper wrote it.',
 'duplicate or related': 'Whether the member duplicates the unified question or is related to it.', 'reason': 'Why the model grouped the member this way.',
 # metrics, calls
 'Area': 'Part of the pipeline the metric describes.', 'Metric': 'What is measured.', 'Value': 'The measured value.', 'Note': 'Explanation of the metric.',
 'Time (UTC)': 'When the model call was made.', 'Step': 'Pipeline step the call belongs to.', 'Model': 'The AI model called.', 'Effort': 'Reasoning effort setting used for the call.',
 'Tokens in': 'Tokens sent to the model (a token is roughly three quarters of a word).', 'Tokens out (incl. thinking)': 'Tokens the model produced, including hidden reasoning.',
 'Cost USD (list price; batch is half)': 'Cost at list price; batch-mode calls cost half.', 'Notes': 'Extra detail about the call.',
}
TAB = {  # a header that means something different in one tab
 ('Drafts (EVD, QUE, CLM, CVT)', 'Status'): 'Outcome of the checks on the chosen draft: pass, pass with notes, reworked by another model, or needs human review.',
 ('Decision-model checks (EVD)', 'Result'): 'Final result for the finding: pass, fail or cannot verify (no screenshot could be made).',
 ('EVD rework (Opus 5.5)', 'Result'): 'Outcome of the rework for this statement.',
 ('Quality signals (raw ratings)', 'Rating'): 'The rating this model gave for the signal.',
 ('Rechecks (EVD findings)', 'Result'): 'Outcome of the recheck.',
 ('Rechecks (EVD findings)', 'Opus reason'): 'The third model\'s explanation of which reader it judged correct.',
 ('Writing-rules fails (all nodes)', 'Node type'): 'Node type: EVD, QUE, CLM or CVT.',
 ('Quality signals (votes)', 'Signal'): 'Name of the quality signal.',
}
JP = {  # "JP:" columns: the human reviewer's input
 'tier right?': 'For the human reviewer: is the tier (primary, secondary, tertiary) right? yes or no.', 'correct tier': 'For the human reviewer: the tier you would assign.',
 'statement and numbers right?': 'For the human reviewer: are the statement and its numbers right? yes or no.', 'missed finding': 'For the human reviewer: describe a finding the model missed.', 'notes': 'For the human reviewer: free notes.',
 'quote correct?': 'For the human reviewer: is the quote correct? yes or no.', 'who is right?': 'For the human reviewer: which reader had the right numbers (Neon, Sol or neither).',
 'is the finding right?': 'For the human reviewer: is the finding right? yes or no.', 'best text or your own': 'For the human reviewer: the best of the drafts, or your own wording.',
 'fidelity': 'For the human reviewer: does the text match its source? yes, partly or no.', 'style': 'For the human reviewer: is the style good, ok or poor?', 'suggested change': 'For the human reviewer: the change you suggest.',
 'right call?': 'For the human reviewer: was the rework decision right? yes or no.', 'is the extraction correct?': 'For the human reviewer: is the extracted item correct? yes, no or unsure.',
 'right?': 'For the human reviewer: is the result right? yes, no or unsure.', 'are the numbers right?': 'For the human reviewer: are the numbers right? yes or no.', 'is the classifier right?': 'For the human reviewer: is the classifier\'s answer right? yes or no.',
 'correct rating': 'For the human reviewer: the rating you consider correct.', 'group right?': 'For the human reviewer: is this grouping right? yes or no.', 'better wording or notes': 'For the human reviewer: a better wording, or notes.',
}


# Model names in headers come from pipeline/config/models.json (JP, 2026-11-27), so a swapped model is named correctly: run_to_gsheet.py imports these names.
import sys as _sys
from pathlib import Path as _P
_sys.path.insert(0, str(_P(__file__).resolve().parent))
import config as _C
_JROLE = _C.ROLES.get('verify_judge') or _C.ROLES['quote_check']
JD = _C.role_display(_JROLE); JS = _C.short(_JROLE)                      # verification judge: 'GPT-6.2 Sol', 'Sol'
AD = _C.short(_C.ROLES['adjudicate'])                                    # settles Neon-versus-Sol disagreements: 'Sonnet 5.5'
VD = _C.short(_C.ROLES['vision_dispute'])
RWS = _C.short(_C.ROLES['evd_rework']); RWT = f"EVD rework ({_C.role_display(_C.ROLES['evd_rework'])})"   # EVD rework model, tab title
QCD = _C.role_display(_C.ROLES['quote_check'])                           # reads the screenshot of every quote
N.update({
 f'{JD} score': f"{JD}'s judgment: 1 supported, 0.5 unsure, 0 not supported. Empty when {JD} was not called because the two decision models agreed.",
 f'{JD} reason': f"{JD}'s one-sentence reason, or \"not called\" when the decision models agreed.",
 'Sonnet 5.5 reason': 'The foundation model\'s one-sentence reason for the item (the model named in the run\'s ABOUT tab, roles.verify_judge), or "not called" when the decision models agreed.',
 f'{JS} pass (1 or 0)': f"{JS}'s verdict as 1 (pass) or 0; empty if unsure or not called.",
 f'Before the rerun (cited pages only, or the stricter question): {JD} score': f"{JD}'s score before the rerun that added the Methods pages or loosened the wording check.",
 f'Quote verifiers (mean score: {JD}, Liquid d1.2-ultra, Perplexity)': 'Average scores (0 to 1) from three verifiers on whether the quotes support the ratings.',
 'Liquid screenshot score counts as a vote? (digit comparisons on quotes only)': f'yes when the screenshot score is used in the majority (quotes containing digits). Quotes without digits are checked by {QCD} instead.',
 f'{AD} verdict': f'When the two readers differ, which one a third model ({_C.role_display(_C.ROLES["adjudicate"])}) judged correct.',
 f'{AD} verdict (A = Neon, B = Sol)': f'Which reader a third model ({_C.role_display(_C.ROLES["adjudicate"])}) judged correct: A is Neon, B is Sol.',
 f'Where {RWS} found each number': f"For each number in the statement, where {_C.role_display(_C.ROLES['evd_rework'])} found it: in the quote, the numbers list, the screenshot or nowhere.",
 'Numbers found nowhere': f'Numbers {RWS} could not find in any source.',
 'Fidelity problems': f'Mismatches {RWS} found between the statement and its source (model names, comparator, direction, scope).',
 'Verdict': f"{RWS}'s decision: ok (statement is fine), rewrite, or extraction problem (the source data look wrong).",
 'Proposed correction': f'The statement with only the wrong words or numbers corrected, when {RWS} found an error. Everything else is kept word for word.',
 'Exact changes (old -> new: reason)': f'Every edit {RWS} made, as old text -> new text with the reason. The correction is applied only if these edits reproduce the proposed statement exactly and the writing rules and decision-model checks pass.',
 'Flag for human examination (reason)': 'Why a person should look at this item. Flagged when the judge model scored it below 0.75 or gave no answer; when Perplexity, Liquid or bison-1 scored it below 0.5 and the judge did not pass it; or when the judge and the majority of the decision models disagree. bison-1 takes part in the flag but not in the pass or fail vote. Flagged items come first in the labeling queue within each node type.',
 'Judge model (the one that did not produce the item)': 'The foundation model that judged this item. A model never judges its own work: items Neon produced go to the first judge, quality ratings the first judge made go to the second judge.',
 f'{VD} (disputes only)': f'Verdict of {_C.role_display(_C.ROLES["vision_dispute"])}, asked only when the decision models and the screenshot check disagree.',
 'Sol rating (fallback or third rater)': 'Rating by GPT-6.2 Sol. With one primary rater (2026-11-27 procedure) Sol rates only the rows where the first rater reported low confidence (the fallback rater); in the three-rater mode it is the third independent rater; older runs: asked only when Neon and Opus differed.',
 'Confidence reported': 'The rater\'s own confidence in the rating (high, medium or low). A low rating goes to the fallback rater; if that one is also low the row is marked needs_human.',
 'New: needs your judgment (needs_human)': 'TRIPOD-LLM items on which the first rater and the fallback rater both reported low confidence. They are left out of the share reported and are yours to rate.',
 'Needs your judgment (needs_human)': 'Signals on which the first rater and the fallback rater both reported low confidence, or gave no valid rating. They are yours to rate.',
 'Fallback rater decided': 'Signals on which the first rater reported low confidence and the fallback rater (GPT-6.2 Sol) gave the rating.',
})
TAB[('Decision-model checks (EVD)', f'{VD} reason')] = "The dispute model's explanation of its verdict."
TAB[(RWT, 'Result')] = 'Outcome of the rework for this statement.'
TAB[('Rechecks (EVD findings)', f'{AD} reason')] = "The third model's explanation of which reader it judged correct."
TAB[('Drafts (EVD, QUE, CLM, CVT)', 'Checked by')] = 'The model that checked the details of the node. "(own draft)" means the checker also wrote the winning text, so the check is not independent.'


def note_for(tab, header):
    h = str(header or '').strip()
    if not h: return None
    if (tab, h) in TAB: return TAB[(tab, h)]
    if tab.startswith('QS ') and h == 'Result': return 'The final rating for a signal, or the one-sentence outcome of a code-only check.'
    if h in N: return N[h]
    if h.startswith('EVD draft (chosen'): return 'A short evidence statement (EVD: one finding with its numbers) chosen among drafts by three AI models; at most 247 characters. The header says which writing rules were in force.'
    if h.startswith('JP:'):
        key = re.sub(r'\s*\(.*?\)\s*$', '', h[3:].strip()); key = JP.get(key) and key or next((k for k in JP if key.startswith(k)), key)
        return JP.get(key, 'For the human reviewer to fill in.')
    return None


def apply_notes_requests(sheet_ids_by_title, headers_by_title):
    """Sheets API requests that put these notes on the header cells of an existing spreadsheet (updateCells with the note field)."""
    reqs = []
    for title, hdr in headers_by_title.items():
        sid = sheet_ids_by_title.get(title)
        if sid is None: continue
        vals = [{'note': note_for(title, h) or ''} if note_for(title, h) else {} for h in hdr]
        reqs.append({'updateCells': {'rows': [{'values': vals}], 'fields': 'note', 'start': {'sheetId': sid, 'rowIndex': 0, 'columnIndex': 0}}})
    return reqs
