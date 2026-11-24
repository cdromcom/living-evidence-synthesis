# Permissions and licences for republished material

Status: draft for JP to review. This is a data summary, not legal advice.

The vault republishes screenshots (figure and table crops and quoted-text crops) from 27 source papers. This file records, for each paper, what licence the publisher metadata states, so JP can decide what is safe to keep online. Licences were looked up on 2026-11-23 from the Crossref REST API (`api.crossref.org/works/<doi>`) and, where Crossref had no licence, OpenAlex (`api.openalex.org/works/doi:<doi>`). Unpaywall was not needed. Nothing was guessed: "none found" means neither service listed a licence. The same values are in each source note's frontmatter (`license`, `license_source`, `oa_status`). Where the licence comes from OpenAlex it names a licence family (for example `cc-by`) without a version number, and it can describe the preprint copy rather than the published version, so check the paper's own page before relying on it.

Screenshot counts are the distinct image files from that paper embedded in vault pages and present in `vault/evidence/Attachments` (443 in total).

## Per-paper table

| Source | DOI | Licence | OA status | Publisher | Screenshots republished | Republishing under that licence |
|---|---|---|---|---|---|---|
| @akyonEvaluatingCapabilitiesGenerative2024 | 10.2196/59258 | cc-by | gold | JMIR Publications Inc. | 15 | allowed (attribution required) |
| @alharbiAutomatedAssessmentReporting2024 | 10.3390/app142210323 | https://creativecommons.org/licenses/by/4.0/ | gold | MDPI AG | 11 | allowed (attribution required) |
| @bougieGenerativeAdversarialReviews2024a | 10.48550/arXiv.2412.10415 | none found | green | Cornell University | 18 | needs checking (no licence found; fair use only) |
| @darcyMARGMultiAgentReview2024 | 10.48550/arXiv.2401.04259 | cc-by | green | Cornell University | 13 | allowed (attribution required) |
| @hasanIntegratingLargeLanguage2024 | 10.1136/bmjebm-2023-112597 | none found | closed | BMJ | 9 | not allowed (no open licence; fair use only) |
| @huntington-kleinLLMsActRepositories2024 | 10.48550/arXiv.2412.10635 | cc-by | gold | De Gruyter | 13 | allowed (attribution required) |
| @idahlOpenReviewerSpecializedLarge2025 | 10.48550/arXiv.2412.11948 | none found | green | Cornell University | 17 | needs checking (no licence found; fair use only) |
| @leucutaRiskBiasAssessment2025 | 10.3390/diagnostics15121451 | https://creativecommons.org/licenses/by/4.0/ | gold | MDPI AG | 12 | allowed (attribution required) |
| @liangCanLargeLanguage2024a | 10.1056/AIoa2400196 | none found | green | Massachusetts Medical Society | 24 | needs checking (no licence found; fair use only) |
| @liuReviewerGPTExploratoryStudy2023 | 10.48550/arXiv.2306.00622 | none found | green | Cornell University | 21 | needs checking (no licence found; fair use only) |
| @louAAAR10AssessingAIs2025 | 10.48550/arXiv.2410.22394 | none found | green | unknown | 17 | needs checking (no licence found; fair use only) |
| @robertsComparativeStudyChatGPT2023 | 10.1136/bmjhci-2023-100830 | https://creativecommons.org/licenses/by/4.0/ | gold | BMJ | 16 | allowed (attribution required) |
| @sarolAssessingCitationIntegrity2024 | 10.1093/bioinformatics/btae420 | https://creativecommons.org/licenses/by/4.0/ | gold | Oxford University Press (OUP) | 22 | allowed (attribution required) |
| @shahidLiteratureGroundedNoveltyAssessment2025 | 10.48550/arXiv.2506.22026 | cc-by | hybrid | Association for Computational Linguistics | 20 | allowed (attribution required) |
| @sonWhenAICoScientists2025 | 10.48550/arXiv.2505.11855 | cc-by | green | Cornell University | 19 | allowed (attribution required) |
| @sridharanAssessingDecisionMakingCapabilities2024 | 10.1177/15562646241263200 | none found | bronze | SAGE Publications | 16 | not allowed (no open licence; fair use only) |
| @sridharanLeveragingArtificialIntelligence2025 | 10.1136/jme-2023-109767 | none found | closed | BMJ | 13 | not allowed (no open licence; fair use only) |
| @srinivasanEvaluatingReportingQuality2025a | 10.1101/2025.03.06.25323528 | http://creativecommons.org/licenses/by-nc/4.0/ | green | openRxiv | 19 | needs checking (BY-NC: non-commercial or share-alike terms) |
| @thelwallEvaluatingResearchQuality2024 | 10.48550/arXiv.2408.06752 | cc-by | diamond | Chinese Academy of Sciences | 13 | allowed (attribution required) |
| @tyserAIDrivenReviewSystems2024 | 10.48550/arXiv.2408.10365 | cc-by | green | Cornell University | 15 | allowed (attribution required) |
| @woelfleBenchmarkingHumanAICollaboration2024 | 10.1016/j.jclinepi.2024.111533 | http://creativecommons.org/licenses/by/4.0/ | hybrid | Elsevier BV | 33 | allowed (attribution required) |
| @wrightsonGPTRCTsUsing2025 | 10.1136/bmjopen-2024-088735 | http://creativecommons.org/licenses/by-nc/4.0/ | gold | BMJ | 15 | needs checking (BY-NC: non-commercial or share-alike terms) |
| @wuAutomatedNoveltyEvaluationa | 10.1002/asi.70005 | none found | green | Wiley | 14 | not allowed (no open licence; fair use only) |
| @xuCanLLMsIdentify2025 | 10.48550/arXiv.2507.02694 | cc-by | green | Cornell University | 15 | allowed (attribution required) |
| @zhangDetectingReferenceErrors2024 | 10.48550/arXiv.2411.06101 | none found | green | National Institutes of Health | 13 | needs checking (no licence found; fair use only) |
| @zhangReviewingScientificPapers2025a | 10.48550/arXiv.2505.23824 | cc-by-sa | green | Cornell University | 16 | needs checking (CC BY-SA terms) |
| @zhouLLMReliableReviewer2024 | 10.63317/48d359hjdvog | cc-by-nc | hybrid | European Language Resources Association (ELRA) and ICCL | 14 | needs checking (CC BY-NC terms) |

Summary: 13 papers carry a CC BY licence (allowed with attribution), 10 need checking (non-commercial, share-alike, or no licence found), 4 have no open licence at all and are access-restricted ("closed" or "bronze").

How the last column was decided. CC BY allows copying and adaptation with credit, so republishing is clearly allowed as long as each page credits the paper. CC BY-NC allows non-commercial use only, so it depends on whether the site counts as non-commercial. CC BY-SA requires the republished material to be shared under the same licence, which may conflict with whatever licence the repository gets. "None found" for a preprint usually means the default arXiv terms apply, which let arXiv distribute the paper but give others no reuse right. "Not allowed" means no open licence was found and the paper is behind a paywall or free-to-read only, so reuse relies on fair use or on asking the publisher.

## Fair use and takedown considerations

- The screenshots are verbatim crops of copyrighted figures and tables. Where there is an open licence, the licence is the basis for reuse. Where there is not, the only basis is fair use (US) or a quotation exception (other countries), and those are judged case by case, not granted automatically.
- Points that usually help a fair-use argument: the use is scholarly commentary and appraisal, each crop is small compared with the whole paper, each is shown next to JP's own analysis, and it does not replace reading the paper. Points that usually hurt: commercial use, reproducing a full table or figure when a short quote would do, and republishing many crops from one paper.
- Reuse of the numbers themselves (facts) is lower risk than reuse of the figure image. Where a paper is "not allowed" above, the lowest-risk fix is to replace the image with a typed table or a short quotation plus a link to the paper.
- Keep a visible attribution (citation and DOI link) next to every crop, and keep a clear way for rights holders to ask for removal. When a request arrives, remove the crop promptly first, then discuss.
- The repository history keeps removed images unless it is rewritten, so a takedown may also need a history clean-up.

## Decisions only JP can make (placeholders)

- Repository LICENSE: **[JP TO DECIDE: no LICENSE file has been chosen or added. The choice should be checked against the CC BY-SA and CC BY-NC papers above.]**
- Licence for JP's own ratings and appraisals (the review text, tags and scores): **[JP TO DECIDE]**
- Takedown contact address: **[JP TO PROVIDE: no address has been invented. Add one here and on the site.]**
- What to do with papers marked "not allowed" or "needs checking" (keep under fair use, replace by typed tables, or ask the publisher): **[JP TO DECIDE]**
