// Prompt-method coding for the 27 source papers.
//
// Hand-coded from each source's TRIPOD-LLM item 9a (prompt design), 6c (inference
// settings) and 6d (output), cross-checked against its Methods section. This is a
// curator judgement per paper, not something derived from frontmatter tags, so it
// lives here rather than being recomputed at build time — if a source's prompt
// description changes, this file has to be updated by hand alongside it.
//
// Coding is conservative: a tactic is recorded only where the source states it.
// "not used" and "not reported" are therefore indistinguishable, which matters
// because roughly a third of these papers keep their prompt text in an appendix
// that was never released.

/** The eleven dimensions, in the order they are shown. */
export const PROMPT_DIMENSIONS = [
  { key: "zero", label: "Zero-shot", group: "shot" },
  { key: "one", label: "One-shot", group: "shot" },
  { key: "few", label: "Few-shot", group: "shot" },
  { key: "inputIter", label: "Input type iterated", group: "shape" },
  { key: "outputIter", label: "Output type iterated", group: "shape" },
  { key: "role", label: "Role playing", group: "shape" },
  { key: "proc", label: "Detailed procedure", group: "shape" },
  { key: "iter", label: "Iterations", group: "shape" },
  { key: "temp", label: "Temperature specified", group: "run" },
  { key: "reason", label: "Reasoning / thinking model", group: "run" },
  { key: "rag", label: "Retrieval-augmented", group: "run" },
] as const;

export type PromptDimension = (typeof PROMPT_DIMENSIONS)[number]["key"];

export type PromptTactics = {
  /** The Source node this coding describes, e.g. "SRC-001". */
  srcId: string;
  author: string;
  year: number | null;
  /** Which of PROMPT_DIMENSIONS this paper uses. */
  tactics: PromptDimension[];
  /** Disclosed sampling temperature, or null when the paper reports none. */
  temperature: string | null;
  /** The prompt as the paper states it, verbatim. */
  prompt: string;
  /** Where that quote comes from. */
  locator: string;
  /** What the coding turns on, in one or two sentences. */
  reading: string;
};

export const PROMPT_TACTICS: PromptTactics[] = [
  {
    "srcId": "SRC-001",
    "author": "Akyon et al.",
    "year": 2024,
    "tactics": [
      "zero",
      "role",
      "iter",
      "temp",
      "rag"
    ],
    "temperature": "0.1",
    "prompt": "You are an expert medical professor specialized in pediatric gastroenterology hepatology and nutrition, with a detailed understanding of various research methodologies, study types, ethical considerations, and statistical analysis procedures.",
    "locator": "TRIPOD 9a · p.12",
    "reading": "Persona is the whole prompt strategy. Each of 15 STROBE questions asked 10× per article per model at temperature 0.1."
  },
  {
    "srcId": "SRC-002",
    "author": "Alharbi et al.",
    "year": 2024,
    "tactics": [
      "zero",
      "role",
      "proc",
      "iter"
    ],
    "temperature": null,
    "prompt": "System prompts were initiated by introducing GPT-3.5 as an 'expert in systematic reviews' for PRISMA guidelines and an 'expert in clinical trial design' for CONSORT-A guidelines",
    "locator": "TRIPOD 9a · §2.6, p.3",
    "reading": "Names the tactic outright — “in-context expert impersonation.” Each item asks for quote, then reasoning, then a bracketed rating; re-run up to three times when the model skipped items."
  },
  {
    "srcId": "SRC-003",
    "author": "Bougie & Watanabe",
    "year": 2024,
    "tactics": [
      "zero",
      "role",
      "proc",
      "iter",
      "rag"
    ],
    "temperature": null,
    "prompt": "An example prompt block is provided below:",
    "locator": "TRIPOD 9a · §3.3, p.8",
    "reading": "Three to six reviewer agents, each given a different persona derived from historical OpenReview data, refine drafts across multiple rounds. Full prompt text deferred to an appendix not in the released preprint."
  },
  {
    "srcId": "SRC-004",
    "author": "D’Arcy et al.",
    "year": 2024,
    "tactics": [
      "zero",
      "role",
      "proc",
      "iter"
    ],
    "temperature": null,
    "prompt": "To tune prompts for review generation, we performed several hundred rounds of manual iteration on a small set of papers from ARIES",
    "locator": "TRIPOD 9a · §4.4, p.5",
    "reading": "The most heavily iterated prompt in the corpus. Leader, worker and three expert agents (experiments, clarity, impact) each carry a distinct role."
  },
  {
    "srcId": "SRC-005",
    "author": "Hasan et al.",
    "year": 2024,
    "tactics": [
      "zero",
      "inputIter",
      "iter"
    ],
    "temperature": null,
    "prompt": "The processes of data entry and prompt development were done iteratively until data were appropriately uploaded and a sensical output was obtained (ie, these processes were not prespecified).",
    "locator": "TRIPOD 9a · Methods, p.2",
    "reading": "Rare candour about un-prespecified prompting. Three ingestion routes piloted — PDF upload, full text, then Methods+Results pasted from Word — and only the third worked."
  },
  {
    "srcId": "SRC-006",
    "author": "Huntington-Klein et al.",
    "year": 2024,
    "tactics": [
      "few",
      "outputIter",
      "proc",
      "iter",
      "temp",
      "reason"
    ],
    "temperature": "0.7",
    "prompt": "In the direct approach, we ask the LLM whether a given variable is a confounder, in the following format: I have a data set consisting only of people who have been assigned to take a certain medication X…",
    "locator": "TRIPOD 9a · Methods, p.4",
    "reading": "The most systematic prompt ablation here: three worked examples, direct vs. indirect question framing, step-by-step reasoning toggled, answer order swapped, eight phrasings compared by Cohen’s kappa, ten calls each."
  },
  {
    "srcId": "SRC-007",
    "author": "Idahl & Ahmadi",
    "year": 2025,
    "tactics": [
      "zero",
      "role",
      "proc",
      "temp"
    ],
    "temperature": "0 (greedy)",
    "prompt": "OpenReviewer uses a system prompt that conditions the LLM on its reviewer role and defines a fixed set of reviewer guidelines",
    "locator": "TRIPOD 9a · §3.3, p.3",
    "reading": "Role and procedure are fixed by design — the contribution is a fine-tuned model, so the prompt is deliberately held constant at temperature 0."
  },
  {
    "srcId": "SRC-008",
    "author": "Leucuta et al.",
    "year": 2025,
    "tactics": [
      "zero",
      "proc"
    ],
    "temperature": null,
    "prompt": "we used only one single standardized prompt to ensure comparability across LLMs… We used a simple prompt to enact a scenario where researchers that are not trained in prompt engineering would use LLMs",
    "locator": "TRIPOD 9a · §4.1, p.17",
    "reading": "Deliberately un-engineered — the naïve prompt is the research design. Still specifies a turn-by-turn procedure through the QUADAS-2 signalling questions."
  },
  {
    "srcId": "SRC-009",
    "author": "Liang et al.",
    "year": 2024,
    "tactics": [
      "zero",
      "proc"
    ],
    "temperature": null,
    "prompt": "Following the reviewer report instructions from machine learning conferences…and Nature family journals…we provided specific instructions to generate four feedback sections",
    "locator": "TRIPOD 9a · Methods, p.9",
    "reading": "One forward pass per paper, no persona. The authors concede “the architecture and prompt used in our study only represent one of the many possible forms.”"
  },
  {
    "srcId": "SRC-010",
    "author": "Liu & Shah",
    "year": 2023,
    "tactics": [
      "zero",
      "one",
      "inputIter",
      "role",
      "iter",
      "temp"
    ],
    "temperature": "1.0, swept 0–2.0",
    "prompt": "System prompt: You are a computer science researcher currently reviewing a paper titled “[paper title]” for the NeurIPS computer science conference.",
    "locator": "TRIPOD 9a · §4.1, p.28",
    "reading": "One of only three sources to vary shot count: Prompt-Direct (zero-shot), Prompt-OneShot (one worked example) and Prompt-Parts (paper fed a sentence at a time) run head to head, three responses each."
  },
  {
    "srcId": "SRC-011",
    "author": "Lou et al.",
    "year": 2025,
    "tactics": [
      "zero",
      "inputIter",
      "outputIter",
      "proc",
      "iter",
      "reason"
    ],
    "temperature": null,
    "prompt": "we attach all the prompts used in this work, including prompts in data collection and model prediction",
    "locator": "TRIPOD 9a · Appendix E, p.18",
    "reading": "Varies both sides: long papers split into 2,000/3,000-word pieces then merged, and two output strategies (Labeling-All vs. Select-Deficient) ensembled under an “Either No” rule. Three runs, median reported."
  },
  {
    "srcId": "SRC-012",
    "author": "Roberts et al.",
    "year": 2023,
    "tactics": [
      "zero",
      "proc"
    ],
    "temperature": null,
    "prompt": "(A) Example prompt used to generate the OCS as per CONSORT-A criteria.",
    "locator": "TRIPOD 9a · Figure 1, p.2",
    "reading": "A single zero-shot prompt carrying the full CONSORT-A definitions; each abstract scored exactly once, with no few-shot variant tested."
  },
  {
    "srcId": "SRC-013",
    "author": "Sarol et al.",
    "year": 2024,
    "tactics": [
      "few",
      "inputIter",
      "proc",
      "rag"
    ],
    "temperature": null,
    "prompt": "The prompt consists of a detailed task instruction along with descriptions of three classes, which is followed by four demonstrations selected from the training set (one each for ACCURATE and IRRELEVANT, and two for NOT_ACCURATE)",
    "locator": "TRIPOD 6c · §2.5.4, p.4–5",
    "reading": "Class-balanced demonstrations — the only source that reports how its exemplars were distributed across labels. Retrieval depth varied at 5, 10 and 20 sentences."
  },
  {
    "srcId": "SRC-014",
    "author": "Shahid et al.",
    "year": 2025,
    "tactics": [
      "zero",
      "few",
      "inputIter",
      "proc",
      "iter",
      "reason",
      "rag"
    ],
    "temperature": null,
    "prompt": "We experimented with various numbers of in-context examples… and found that the best performance was achieved using 15 idea examples (random seed 100).",
    "locator": "TRIPOD 6c · Implementation Settings, p.6",
    "reading": "Treats exemplar count as a tuned hyperparameter, then compares against zero-shot, DSPy and TextGRAD on a train/validation/test split — the only source to optimise prompt wording automatically."
  },
  {
    "srcId": "SRC-015",
    "author": "Son et al.",
    "year": 2025,
    "tactics": [
      "zero",
      "role",
      "proc",
      "iter",
      "temp",
      "reason"
    ],
    "temperature": "0.6, top-p 0.95",
    "prompt": "You are a scientific-rigor auditor. You will receive the parsed contents of a research paper.",
    "locator": "TRIPOD 9a · Appendix F.2, p.32",
    "reading": "Persona plus a strict JSON schema for location and description. Eight independent inferences per paper feed a pass@K estimate bootstrapped 1,000 times."
  },
  {
    "srcId": "SRC-016",
    "author": "Sridharan & Sequeira",
    "year": 2024,
    "tactics": [
      "zero",
      "outputIter"
    ],
    "temperature": null,
    "prompt": "The AI platforms were prompted with ten case studies with open-ended questions",
    "locator": "TRIPOD 9a · Study Procedure, p.84",
    "reading": "Two output genres from the same models — free-text answers to ethics cases, and drafted SOPs across 16 IRB topics. Prompt text lives only in supplementary material."
  },
  {
    "srcId": "SRC-017",
    "author": "Sridharan & Sequeira",
    "year": 2025,
    "tactics": [
      "zero",
      "inputIter",
      "outputIter",
      "iter"
    ],
    "temperature": null,
    "prompt": "Below is the summary of a research proposal. Can you generate an ICD for the study participants?",
    "locator": "TRIPOD 9a · p.127",
    "reading": "The one source that varies prompt <em>delivery</em>: every query set is given twice — concatenated into a single prompt, then again one at a time as a dialogue — though no test compares the two conditions."
  },
  {
    "srcId": "SRC-018",
    "author": "Srinivasan et al.",
    "year": 2025,
    "tactics": [
      "zero",
      "role",
      "proc"
    ],
    "temperature": null,
    "prompt": "SYSTEM_PROMPT = “You are a highly skilled medical research assistant with extensive knowledge of randomized controlled trials and CONSORT guidelines…”",
    "locator": "TRIPOD 6c · Appendix, p.S-3",
    "reading": "Four-field structured output — criterion, chain-of-thought rationale, MET/NOT MET, and a self-reported confidence used to filter the 21,041-article run."
  },
  {
    "srcId": "SRC-019",
    "author": "Thelwall",
    "year": 2024,
    "tactics": [
      "zero",
      "inputIter",
      "proc",
      "iter",
      "temp"
    ],
    "temperature": "1 (default)",
    "prompt": "Six variations of the basic REF prompt were tested to assess whether alternative prompts might give better results.",
    "locator": "TRIPOD 9a · §2.3, p.5",
    "reading": "The cleanest input ablation in the corpus: titles only, titles plus abstracts, and truncated full text, each scored 30 times per article, with correlation recomputed for every k from 1 to 30."
  },
  {
    "srcId": "SRC-020",
    "author": "Tyser et al.",
    "year": 2024,
    "tactics": [
      "zero",
      "inputIter",
      "outputIter",
      "role",
      "proc"
    ],
    "temperature": null,
    "prompt": "P1 includes the full paper text (P) and conference review form (RF). P2 adds the reviewer guide (RG). P3 adds the code of ethics (CE) and code of conduct (CC). P4 adds guidelines for the area chair (AC). P5 adds the statistics of the previous year's conference.",
    "locator": "TRIPOD 6c · Appendix D, p.13",
    "reading": "A nested context ladder — each bundle strictly contains the last, so the ablation isolates what each added document buys. Four review-question formats explored alongside."
  },
  {
    "srcId": "SRC-021",
    "author": "Woelfle et al.",
    "year": 2024,
    "tactics": [
      "zero",
      "inputIter",
      "proc",
      "iter",
      "temp"
    ],
    "temperature": "0",
    "prompt": "1. Extract 1-3 relevant quotes from the full text. 2. Explain your reasoning in 1 paragraph. 3. Give a score X from 1 (very explanatory) to 5 (very pragmatic) in square brackets",
    "locator": "TRIPOD 6d · Box 1, p.6",
    "reading": "Quote-first procedure makes the rating auditable against the source text. Claude-3-Opus reads page images while the other four read plain text; every prompt run twice for intrarater reliability."
  },
  {
    "srcId": "SRC-022",
    "author": "Wrightson et al.",
    "year": 2025,
    "tactics": [
      "zero",
      "inputIter",
      "role",
      "proc",
      "iter",
      "temp"
    ],
    "temperature": "0.2, top-p 0.2",
    "prompt": "The system and user prompts were developed using the guidelines provided by OpenAI and included asking the model to adopt a persona (the system prompt), using delimiters to distinguish parts of the input and specifying the steps required to complete the task (the user prompt).",
    "locator": "TRIPOD 9a · Model choice and optimisation, p.4",
    "reading": "The only source to describe a closed prompt-improvement loop: the first ten wrong training answers were handed back to ChatGPT to rewrite the instructions, then re-run."
  },
  {
    "srcId": "SRC-023",
    "author": "Wu et al.",
    "year": null,
    "tactics": [
      "zero",
      "iter",
      "temp"
    ],
    "temperature": "0",
    "prompt": "we utilized the extracted title and methodology section of the papers to construct the prompt for ChatGPT. We requested ChatGPT to provide evaluations and summaries of the novelty of the methodology section, with a constraint of staying within 200 words.",
    "locator": "TRIPOD 9a · §3.2, p.12",
    "reading": "Prompting is a feature-extraction step, not the object of study — the LLM summary becomes an input stream to a SciBERT classifier. Results averaged over three rounds."
  },
  {
    "srcId": "SRC-024",
    "author": "Xu et al.",
    "year": 2025,
    "tactics": [
      "zero",
      "inputIter",
      "proc",
      "rag"
    ],
    "temperature": null,
    "prompt": "The prompts are provided in Figure 4 to Figure 14.",
    "locator": "TRIPOD 9a · §3.3, p.5",
    "reading": "Eleven prompts, one per limitation subtype. Retrieval augmentation is switched on and off so each model serves as its own before-and-after control."
  },
  {
    "srcId": "SRC-025",
    "author": "Zhang et al. (references)",
    "year": 2024,
    "tactics": [
      "zero",
      "inputIter",
      "role",
      "proc",
      "temp",
      "rag"
    ],
    "temperature": "0",
    "prompt": "The prompt template (Appendix C) was finalized before the start of the experiment.",
    "locator": "TRIPOD 9a · §3, p.2",
    "reading": "The only source to state its prompt was frozen before data collection — a genuine pre-specification claim. Four reference-context settings from title-only up to full PDF."
  },
  {
    "srcId": "SRC-026",
    "author": "Zhang et al. (withdrawn)",
    "year": 2025,
    "tactics": [
      "zero",
      "inputIter",
      "temp",
      "reason"
    ],
    "temperature": "0, seed 42",
    "prompt": "In our experiments, both approaches utilized the same simplistic, general task instruction (Appendix A)… The prompt was not customized for our dataset that is rich in math and physics papers.",
    "locator": "TRIPOD 9a · §2.2, p.3",
    "reading": "Deliberately generic instruction, held identical across five reasoning models. The varied axis is ingestion — PDF attachment versus raw LaTeX source."
  },
  {
    "srcId": "SRC-027",
    "author": "Zhou et al.",
    "year": 2024,
    "tactics": [
      "zero",
      "few",
      "inputIter",
      "outputIter",
      "role",
      "proc",
      "temp"
    ],
    "temperature": "0.3",
    "prompt": "a professional reviewer in computer science and machine learning",
    "locator": "TRIPOD 9a · Appendix A, p.10 · Methods",
    "reading": "The broadest sweep: zero-shot and few-shot compared, input switched between the human review and the paper itself, and three output genres — aspect scores, generated reviews, and multiple-choice answers."
  }
];

/** Papers that varied shot count as a condition rather than fixing it. */
export function variedShotCount(row: PromptTactics): boolean {
  return row.tactics.filter((t) => t === "zero" || t === "one" || t === "few").length > 1;
}

/** How many of the 27 sources use each dimension. */
export function dimensionCounts() {
  return PROMPT_DIMENSIONS.map((d) => ({
    ...d,
    n: PROMPT_TACTICS.filter((r) => (r.tactics as string[]).includes(d.key)).length,
  }));
}
