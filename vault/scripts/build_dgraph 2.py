"""Build DGRAPH.md — a comprehensive nested view of the discourse graph.

Structure:
  # Discourse Graph
  ## Questions and Their Answers
    ### QUE 1
      - CLM A
        - EVD X
          - CVT references
        - EVD Y
      - CLM B
    ### QUE 2
    ...
  ## Unattributed Claims (no matching QUE)
  ## Orphan Evidence (no CLM links)
  ## All Caveats

All node references are Obsidian wikilinks `[[Stem]]`.
"""
import re
from pathlib import Path
from collections import defaultdict

VAULT = Path('/Users/ppatel/Documents/living-synthesis')


def parse_que_supporting_claims(que_path: Path) -> list[tuple[str, list[str]]]:
    """Parse a QUE's nested Supporting Claims section.
    Returns list of (clm_stem, [evd_stems]).
    """
    text = que_path.read_text()
    m = re.search(r'### Supporting Claims \(with their evidence\)\s*\n.+?\n+(.+?)(?=^##\s|\Z)',
                  text, re.MULTILINE | re.DOTALL)
    if not m:
        return []
    body = m.group(1)
    results = []
    current_clm = None
    for line in body.split('\n'):
        clm_m = re.match(r'^-\s*\[\[(CLM[^\]]+)\]\]', line)
        evd_m = re.match(r'^\s+-\s*\[\[(EVD[^\]]+)\]\]', line)
        if clm_m:
            current_clm = (clm_m.group(1), [])
            results.append(current_clm)
        elif evd_m and current_clm is not None:
            current_clm[1].append(evd_m.group(1))
    return results


def parse_clm_supporting_evds(clm_path: Path) -> list[str]:
    text = clm_path.read_text()
    m = re.search(r'### Supporting Evidence\s*\n.+?\n+((?:- \[\[.*?\]\]\s*\n?)+)',
                  text, re.DOTALL)
    if not m:
        return []
    return re.findall(r'\[\[(EVD[^\]]+)\]\]', m.group(1))


def parse_cvt_appliesTo(cvt_path: Path) -> list[str]:
    text = cvt_path.read_text()
    m = re.search(r'^appliesTo:\s*\n((?:^\s*-\s*"\[\[.*?\]\]"\s*\n?)+)', text, re.MULTILINE)
    if not m:
        return []
    return re.findall(r'\[\[(EVD[^\]]+)\]\]', m.group(1))


def main():
    # Inventory
    que_files = sorted((VAULT / 'questions').glob('QUE*.md'))
    clm_files = sorted((VAULT / 'claims').glob('CLM*.md'))
    evd_files = sorted((VAULT / 'evidence').glob('EVD*.md'))
    cvt_files = sorted((VAULT / 'caveats').glob('CVT*.md'))

    # Build EVD → [CVT stems] mapping
    evd_to_cvts = defaultdict(list)
    for cvt in cvt_files:
        for evd_stem in parse_cvt_appliesTo(cvt):
            evd_to_cvts[evd_stem].append(cvt.stem)

    # Track which CLMs and EVDs are linked from at least one QUE
    linked_clms = set()
    linked_evds = set()

    # Build QUE → [(CLM, [EVDs])] mapping
    que_data = {}
    for que in que_files:
        data = parse_que_supporting_claims(que)
        que_data[que.stem] = data
        for clm_stem, evds in data:
            linked_clms.add(clm_stem)
            for evd in evds:
                linked_evds.add(evd)

    # YAML frontmatter (Obsidian properties)
    from datetime import date
    today = date.today().isoformat()
    # Preserve created date if DGRAPH.md already has one
    out = VAULT / 'DGRAPH.md'
    created_date = today
    if out.exists():
        existing = out.read_text()
        m = re.search(r'^created:\s*(\S+)', existing, re.MULTILINE)
        if m:
            created_date = m.group(1)

    lines = []
    lines.append('---')
    lines.append('author: Claude (Opus 4.7 / Sonnet 4.6)')
    lines.append('page_type: index/discourse-graph')
    lines.append(f'created: {created_date}')
    lines.append(f'updated: {today}')
    lines.append('generated_by: scripts/build_dgraph.py')
    lines.append('prompt_source: "[[prompts/2026-04-27-dgraph-creation]]"')
    lines.append('vault: living-synthesis')
    lines.append('---')
    lines.append('')
    lines.append('# Discourse Graph')
    lines.append('')
    lines.append('Central nested index across the living-synthesis vault. Each node is a clickable [[wikilink]]. Hierarchy: **Question → Claim → Evidence → (Caveats apply to evidence)**.')
    lines.append('')
    lines.append(f'**Inventory.** {len(que_files)} QUE · {len(clm_files)} CLM · {len(evd_files)} EVD · {len(cvt_files)} CVT.')
    lines.append('')
    lines.append('> [!info] How this page is generated')
    lines.append('>')
    lines.append('> Auto-generated from each QUE\'s `### Supporting Claims (with their evidence)` section, each CLM\'s `### Supporting Evidence`, and each CVT\'s `appliesTo`. Re-run `scripts/build_dgraph.py` to regenerate after any structural change to the vault.')
    lines.append('')
    lines.append('> [!tip] How to read this page')
    lines.append('>')
    lines.append('> Click any [[wikilink]] to jump to the underlying node. The hierarchy reflects the discourse-graph rule: every CLM lives under at least one QUE; every EVD lives under at least one CLM and one QUE; every CVT (⚠️) constrains specific EVDs.')
    lines.append('')
    lines.append('> [!caution] Auto-derived links')
    lines.append('>')
    lines.append('> QUE → CLM associations come from keyword overlap with each QUE\'s title; CLM → EVD comes from each CLM\'s `Papers` list overlapping with each EVD\'s source citekey. Both are paper-level overlaps, not statement-level entailments. Verify the link is truly supportive before citing.')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## Questions and their answers')
    lines.append('')
    for que in que_files:
        data = que_data[que.stem]
        lines.append(f'### [[{que.stem}]]')
        lines.append('')
        if not data:
            lines.append('- *No supporting claims linked.*')
            lines.append('')
            continue
        for clm_stem, evds in data:
            lines.append(f'- [[{clm_stem}]]')
            for evd_stem in evds:
                lines.append(f'    - [[{evd_stem}]]')
                cvts = evd_to_cvts.get(evd_stem, [])
                for cvt_stem in cvts:
                    lines.append(f'        - ⚠️ [[{cvt_stem}]]')
            lines.append('')

    # Unattributed CLMs
    unlinked_clms = [c for c in clm_files if c.stem not in linked_clms]
    if unlinked_clms:
        lines.append('---')
        lines.append('')
        lines.append('## Claims not yet attached to any question')
        lines.append('')
        lines.append('*These CLMs exist in the vault but no QUE\'s nested structure currently includes them. Either the CLM has no QUE-relevant topic match, or the QUE→CLM keyword-overlap was too low.*')
        lines.append('')
        for clm in unlinked_clms:
            lines.append(f'- [[{clm.stem}]]')
            evds = parse_clm_supporting_evds(clm)
            for evd_stem in evds:
                lines.append(f'    - [[{evd_stem}]]')
                for cvt_stem in evd_to_cvts.get(evd_stem, []):
                    lines.append(f'        - ⚠️ [[{cvt_stem}]]')
            lines.append('')

    # Orphan EVDs
    all_evd_stems = {e.stem for e in evd_files}
    orphan_evds = sorted(all_evd_stems - linked_evds)
    if orphan_evds:
        # Filter out any that are linked through unattributed CLMs
        linked_via_unlinked_clm = set()
        for clm in unlinked_clms:
            linked_via_unlinked_clm.update(parse_clm_supporting_evds(clm))
        truly_orphan = [e for e in orphan_evds if e not in linked_via_unlinked_clm]
        if truly_orphan:
            lines.append('---')
            lines.append('')
            lines.append('## Evidence not attached to any claim or question')
            lines.append('')
            lines.append('*EVDs that are not currently surfaced through any QUE→CLM→EVD path. They still exist as standalone evidence and may be linked manually.*')
            lines.append('')
            for evd_stem in truly_orphan:
                lines.append(f'- [[{evd_stem}]]')
                for cvt_stem in evd_to_cvts.get(evd_stem, []):
                    lines.append(f'    - ⚠️ [[{cvt_stem}]]')
            lines.append('')

    # All caveats (flat)
    lines.append('---')
    lines.append('')
    lines.append('## All caveats')
    lines.append('')
    lines.append('*Methodological limitations across the vault. Each lists which EVDs it constrains.*')
    lines.append('')
    for cvt in cvt_files:
        evds = parse_cvt_appliesTo(cvt)
        lines.append(f'- ⚠️ [[{cvt.stem}]]')
        for e in evds:
            lines.append(f'    - applies to [[{e}]]')
        if not evds:
            lines.append('    - *No EVDs currently linked.*')
        lines.append('')

    # Footer
    lines.append('---')
    lines.append('')
    lines.append(f'*Generated {today} from the vault\'s current state. See `[[prompts/2026-04-27-dgraph-creation]]` for the originating prompt and `History.md` for the change log.*')
    lines.append('')

    out.write_text('\n'.join(lines))
    print(f'Wrote {out}')
    print(f'  {len(que_files)} questions')
    print(f'  {len(linked_clms)} attached CLMs, {len(unlinked_clms)} unattached CLMs')
    print(f'  {len(linked_evds)} attached EVDs, {len(orphan_evds)} orphans')
    print(f'  {len(cvt_files)} caveats')


if __name__ == '__main__':
    main()
