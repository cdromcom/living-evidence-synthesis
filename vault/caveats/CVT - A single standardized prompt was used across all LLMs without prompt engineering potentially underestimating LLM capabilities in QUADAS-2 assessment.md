---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/internal-validity
  - cvt/mechanism/single-prompt
  - cvt/type/author-stated
  - cvt/severity/moderate
  - 5c/credibility
appliesTo:
  - "[[EVD - Mean correct QUADAS-2 assessment rate across four LLMs was 72.95% with Grok 3 highest at 77.27% and Gemini 2.0 Flash lowest at 67.27% - @leucutaRiskBiasAssessment2025]]"
  - "[[EVD - LLMs demonstrated systematic reasoning errors in QUADAS-2 patient selection domain including misinterpreting consecutive sampling and case-control design - @leucutaRiskBiasAssessment2025]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6ba6-760c-8784-4728c698876e
type: author-stated
severity: moderate
---

## Source

[[@leucutaRiskBiasAssessment2025]]

### Limitation

A single identical prompt was used for all four LLMs across all studies, without prompt engineering optimized per model or per domain. The authors acknowledge that model-specific prompt engineering could substantially improve accuracy, meaning the reported 67–77% accuracy range likely represents a lower bound on achievable performance rather than ceiling-level capability.

### Supporting Quote

> [!info] Quotes
> "Fourth, we used only one single standardized prompt to ensure comparability across LLMs. Different prompts for the same model would have elicited different responses with different accuracy in assessing the risk or bias. We used a simple prompt to enact a scenario where researchers that are not trained in prompt engineering would use LLMs assess the RoB for their systematic reviews. We acknowledge that more complex prompts could produce better answers or reasoning." (Leucuta et al., 2025, p. 17)
>
> ![[leucutaRiskBiasAssessment2025-cvt-p17-1.png]]

### Applies To

- [[EVD - Mean correct QUADAS-2 assessment rate across four LLMs was 72.95% with Grok 3 highest at 77.27% and Gemini 2.0 Flash lowest at 67.27% - @leucutaRiskBiasAssessment2025]]

- [[EVD - LLMs demonstrated systematic reasoning errors in QUADAS-2 patient selection domain including misinterpreting consecutive sampling and case-control design - @leucutaRiskBiasAssessment2025]]
