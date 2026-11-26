---
type: template-spec
title: EVD tiers (primary, secondary, tertiary)
status: draft for the pilot with JP
written: 2026-11-25
---

# EVD tiers: primary, secondary, tertiary (JP, 2026-11-25)

Every EVD is tied to the research question (RQ) of the QUE it serves and carries one tier. The tier says how directly the finding answers the RQ. The caps below are first guesses; the pilot with JP on four seed papers sets them.

| Tier | What it is | Typical examples | Cap per paper (first guess) | Draft loop |
|---|---|---|---|---|
| **primary** | A finding that answers the RQ directly: what the LLM or tool achieved on the task the RQ asks about, against its comparator. | Model A vs human raters on task T (kappa, F1, accuracy); the headline test of the paper's main claim. | 6 (the seed papers have 1 to 6 EVDs each, median 3) | full debate |
| **secondary** | Meta or contextual information about a primary finding that helps a reader interpret, qualify or trust it. Always names the primary EVD(s) it supports. | Agreement among the human raters; dataset or sample properties; sensitivity to prompt or setting; failure analysis; cost or time; a quantified limitation. | 4 | full debate |
| **tertiary** | Other context that may matter, only when it clearly adds something. | Descriptive statistics of the corpus; exploratory subgroup results; side findings. | 2 | one draft, lint, check |

**Rules.**
1. The tier is decided against the RQ, so the RQ is required to run the extraction (`lives_run.py --question`).
2. A secondary EVD must list the primary EVD(s) it supports (`supports`). A secondary EVD with no primary parent is a sign the primary finding was missed or the tier is wrong.
3. One finding per EVD in every tier. Do not fold a secondary finding into the primary EVD's statement.
4. A paper may have no primary EVD for a given RQ (it answers a different question): then its findings are secondary or tertiary for this RQ, and the paper may belong to another QUE.
5. Findings beyond a tier's cap are not dropped silently: the extraction reports a count and one line per tier (`omitted`), and JP decides.
6. The EVD statement style, the 247-character limit, locators and quotes are the same in every tier (`Skill-templates.md`).

## Frontmatter fields added to the EVD template

```yaml
evd_tier: primary            # primary | secondary | tertiary
evd_tier_reason: ""          # one line: why this tier for this RQ
answers_QUE: ""              # [[QUE - ...]] the tier is defined against
supports_EVD: []             # for secondary and tertiary: [[EVD - ...]] of the primary finding(s)
```

## Review in the sheet

The run review sheet (`Review-sheets-spec.md`, tab Findings) shows the tier and its reason and has JP columns "tier right?" and "correct tier", so JP's corrections become the ground truth for tier accuracy and for the caps.

## Open questions for the pilot
- Are the caps (6, 4, 2) right, or does JP want to extract more secondary EVDs?
- Do secondary EVDs deserve the full debate, or one draft?
- Should the web app show tiers (primary first, secondary as "context")?
- Do tertiary EVDs earn their cost?
