---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "CVT - The LimitGen benchmark focused only on AI research limiting applicability to other scientific domains"
tags:
  - cvt/domain/external-validity
  - cvt/mechanism/single-domain
  - cvt/type/author-stated
  - cvt/severity/moderate
  - 5c/credibility
appliesTo:
  - "[[EVD - GPT-4o reached 52% on LimitGen-Syn vs 86% for experts and 68.1% for MARG|EVD - GPT-4o identified 52% coarse accuracy on LimitGen-Syn while human experts achieved 86% and MARG reached 68.1%]]"
  - "[[EVD - RAG raised GPT-4o limitation accuracy by 12.2 points|EVD - RAG augmentation improved GPT-4o limitation identification coarse accuracy by 12.2 percentage points on LimitGen-Syn]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bbe-7697-8790-1b06a6f7fb5f
type: author-stated
severity: moderate
title: "The LimitGen benchmark focused only on AI research limiting applicability to other scientific domains"
---

## Source

[[@xuCanLLMsIdentify2025]]

### Limitation

LIMITGEN focused on AI/NLP research papers, limiting the generalizability of findings to other scientific domains with different methodological norms and limitation types.

### Supporting Quote

> [!info] Quotes
> "our taxonomy and benchmark focus primarily on AI, as this is the field we are most familiar with. Although we conducted a user study to assess its applicability to other domains, the nuances of different scientific disciplines may introduce challenges and limitation types that our framework does not fully address." (Xu et al., 2025, p. 20661)
>
> ![[xuCanLLMsIdentify2025-acl-cvt-p10-1.png]]

- PDF check 2026-11-24: ACL 2025 version used. Page citation (Xu et al., 2025) p. 12 -> p. 20661 (Limitations section, PDF page 10; the old p. 12 was wrong). Quote verbatim in the new version.

### Applies To

- [[EVD - GPT-4o reached 52% on LimitGen-Syn vs 86% for experts and 68.1% for MARG|EVD - GPT-4o identified 52% coarse accuracy on LimitGen-Syn while human experts achieved 86% and MARG reached 68.1%]]

- [[EVD - RAG raised GPT-4o limitation accuracy by 12.2 points|EVD - RAG augmentation improved GPT-4o limitation identification coarse accuracy by 12.2 percentage points on LimitGen-Syn]]
