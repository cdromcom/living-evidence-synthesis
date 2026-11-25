## Page structure

1. **Make verification the primary flow.** Give readers a short, explicit path from any claim to the relevant evidence and back: “Check this claim,” “Open source at page 7,” “Back to claim.” Label evidence as supporting, qualifying, or contradicting the claim—not just “related.” Give quotes and assessments stable, shareable anchors. Keep the decisive caveat next to the finding in every layout and in print.

2. **Show what could change the reader’s judgment.** Default to one row per quality domain, with consequential concerns and disagreements visible. Expand each row into individual checks, their rationale, and supporting passages. Distinguish “not reported in the paper,” “not assessed,” and “not applicable.” When judges disagree, show what they disagree about and whether a human resolved it; don’t turn agreement into a confidence score.

3. **Give each page type a job.** Claims should explain the synthesis, Evidence should enable verification, and Sources should index what was extracted. In search, show plain-language types and a matching excerpt, not just titles and IDs. Keep browse-by-type links for readers who don’t know what to search for. Defer the reviewer inbox until you observe a recurring triage task. Make the AI-use byline link to the page’s disclosure rather than duplicating it; don’t open the table on hover.

## Color

4. **Separate classification from judgment.** Reserve categorical colors for page types. Use quiet, mostly neutral quality rows and reserve emphasis for concerns that matter. Use underlines for inline links and distinguish visited links so readers can track what they’ve checked. Test actual text, borders, icons, and focus states on tinted surfaces in both themes; a colorblind-safe palette does not guarantee contrast.

## Typography

5. **Set evidence quotes for reading, not coding.** Use the body face for quotations and reserve mono for IDs and versions. Distinguish verbatim text from editorial interpretation with a clear label and spacing. Keep the source locator legible: show the printed page and, when different, the PDF page number. A reader should be able to find the passage without opening the image.

## Layout and spacing

6. **Let the article win when space is tight.** Resolve the breakpoint ambiguity: keep only one rail at intermediate widths and name which one. I’d keep the contents rail and move supporting links into the article at relevant points. At narrow widths, put a compact “On this page” control before the article; never move the decisive caveat into a rail. Verify the layout at 400% zoom. For wide comparison tables, label the scroll region and make it obvious that more columns exist.

## Visuals

7. **Make the screenshot a verification aid, not the hero.** Lead with selectable text and a source link; show a lightweight crop with enough surrounding text to check context. Offer the full page on demand. Don’t duplicate the adjacent quote in alt text; describe what the image adds, such as where the highlighted passage appears. Confirm reproduction rights and provide a source link when a screenshot can’t be shown.

## Animation

8. **Keep feedback immediate and motion optional.** Don’t animate the focus ring or delay the appearance of search results. Keep the graph still until the reader chooses to explore it; stop it settling again on selection so nodes remain trackable. Show a loading state for the full-page image instead of leaving a blank viewer.

## Accessibility

9. **Specify focus as a sequence, not a ring.** On new-page navigation, focus the heading; for fragment links, focus the destination; on Back, restore the reader’s prior position when possible. Return focus to the opener after search or zoom closes, and ensure sticky UI never covers the focused item. Drop the resize handle unless it serves a real task; if retained, provide keyboard controls and a reset.

10. **Test equivalent tasks, not equivalent gestures.** The graph list must let readers find a node, inspect labeled relationships, and follow them without touching the canvas. Test the entire claim-to-source journey with keyboard and screen readers, including dismissing zoom and returning to the same quote. Axe won’t catch a lost reading position or an unhelpful result announcement.

## Build

11. **Ship one complete verification path before scaling.** Build a claim, evidence page, and source as a vertical slice. Test it with reviewers on a phone and a throttled connection. Keep article content and evidence links usable without JavaScript; load the search index when search opens, and the graph and full-page images on demand. Set a first-load budget and enforce it in CI.

12. **Make release checks about evidence integrity.** In addition to snapshots, validate typed relationships, reciprocal links where expected, quote locators, disclosure fields, and redirects for changed URLs. Start these checks in phase one. Assign a human owner to approve accessibility and source-verification acceptance criteria; model review and a token budget don’t cover that work.