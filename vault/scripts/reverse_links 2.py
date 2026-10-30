"""Add reverse links across the discourse graph.

For each EVD:
  - `## Caveats` — every CVT whose `appliesTo` lists this EVD.
  - `## Supports Claim(s)` — every CLM whose `Papers` block contains this EVD's citekey.

For each CLM:
  - `### Supporting Evidence` — every EVD whose source citekey appears in the CLM's
    `Papers` block.

Idempotent: if the section already exists, it is regenerated (so re-running
keeps it in sync).
"""
import re
from pathlib import Path
from collections import defaultdict

VAULT = Path('/Users/ppatel/Documents/living-synthesis')


def evd_filename_to_stem(name: str) -> str:
    return name[:-3] if name.endswith('.md') else name


def evd_stem_to_citekey(stem: str) -> str | None:
    m = re.search(r'@([a-zA-Z][a-zA-Z0-9-]+)$', stem)
    return m.group(1) if m else None


def parse_appliesTo(text: str) -> list[str]:
    """Return list of EVD stems referenced in CVT's appliesTo block."""
    m = re.search(r'^appliesTo:\s*\n((?:^\s*-\s*"\[\[.*?\]\]"\s*\n?)+)', text, re.MULTILINE)
    if not m:
        return []
    return re.findall(r'\[\[(EVD[^\]]+)\]\]', m.group(1))


def parse_clm_papers(text: str) -> list[str]:
    """Return list of citekeys from CLM's Papers block."""
    m = re.search(r'> \[!info\] Papers\s*\n((?:>\s*\[\[@.*?\]\]\s*\n?)+)', text)
    if not m:
        return []
    keys = []
    seen = set()
    for refm in re.finditer(r'@([a-zA-Z][a-zA-Z0-9-]+)\b', m.group(1)):
        if refm.group(1) not in seen:
            seen.add(refm.group(1))
            keys.append(refm.group(1))
    return keys


def insert_or_replace_section(text: str, section_header: str, body: str) -> str:
    """Replace section_header + its body, or append at end if not present."""
    pattern = rf'^({re.escape(section_header)}\s*\n)(.*?)(?=^##\s|\Z)'
    if re.search(pattern, text, re.MULTILINE | re.DOTALL):
        return re.sub(pattern, section_header + '\n' + body + '\n', text, count=1, flags=re.MULTILINE | re.DOTALL)
    # Append at end with separator
    if not text.endswith('\n'):
        text += '\n'
    return text + '\n' + section_header + '\n' + body + '\n'


def main():
    # 1) Build mappings
    cvt_to_evds = {}  # cvt_filename → list[evd_stem]
    evd_to_cvts = defaultdict(list)  # evd_stem → list[cvt_stem]
    for f in sorted((VAULT / 'caveats').glob('CVT*.md')):
        text = f.read_text()
        evd_stems = parse_appliesTo(text)
        cvt_stem = f.stem
        for evd_stem in evd_stems:
            evd_to_cvts[evd_stem].append(cvt_stem)
        cvt_to_evds[f.name] = evd_stems

    clm_to_papers = {}  # clm_filename → list[citekey]
    paper_to_clms = defaultdict(list)  # citekey → list[clm_stem]
    for f in sorted((VAULT / 'claims').glob('CLM*.md')):
        text = f.read_text()
        papers = parse_clm_papers(text)
        clm_to_papers[f.name] = papers
        for p in papers:
            paper_to_clms[p].append(f.stem)

    # 2) Process EVDs: add ## Caveats and ## Supports Claim(s)
    evd_count = 0
    for f in sorted((VAULT / 'evidence').glob('EVD*.md')):
        text = f.read_text()
        stem = f.stem
        citekey = evd_stem_to_citekey(stem)
        if not citekey:
            continue
        # Caveats
        related_cvts = sorted(evd_to_cvts.get(stem, []))
        if related_cvts:
            cvt_lines = '\n'.join(f'- [[{cvt}]]' for cvt in related_cvts)
            caveats_body = f'> [!info] Caveats applying to this evidence\n\n{cvt_lines}'
        else:
            caveats_body = '> [!info] No caveats currently linked to this evidence.'
        text = insert_or_replace_section(text, '## Caveats', caveats_body)
        # Supports Claim(s)
        related_clms = sorted(paper_to_clms.get(citekey, []))
        if related_clms:
            clm_lines = '\n'.join(f'- [[{clm}]]' for clm in related_clms)
            claims_body = f'> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)\n\n{clm_lines}'
        else:
            claims_body = '> [!info] No claims currently linked to this evidence.'
        text = insert_or_replace_section(text, '## Supports Claim(s)', claims_body)
        f.write_text(text)
        evd_count += 1

    # 3) Process CLMs: add ### Supporting Evidence
    # Build paper → list[evd_stem]
    paper_to_evds = defaultdict(list)
    for f in (VAULT / 'evidence').glob('EVD*.md'):
        ck = evd_stem_to_citekey(f.stem)
        if ck:
            paper_to_evds[ck].append(f.stem)

    clm_count = 0
    for f in sorted((VAULT / 'claims').glob('CLM*.md')):
        text = f.read_text()
        papers = parse_clm_papers(text)
        if not papers:
            continue
        evd_stems = []
        for p in papers:
            evd_stems.extend(paper_to_evds.get(p, []))
        evd_stems = sorted(set(evd_stems))
        if evd_stems:
            evd_lines = '\n'.join(f'- [[{e}]]' for e in evd_stems)
            body = f'> [!info] EVDs from the cited papers (auto-derived; not all may directly support the claim — verify before citing)\n\n{evd_lines}'
        else:
            body = '> [!info] No supporting evidence currently linked.'
        # Insert as a ### subsection at the end of the file (or after Snippet section)
        # Use the same insert/replace, but with ### header
        text = insert_or_replace_section(text, '### Supporting Evidence', body)
        f.write_text(text)
        clm_count += 1

    print(f'Updated {evd_count} EVDs with reverse links.')
    print(f'Updated {clm_count} CLMs with reverse links.')


if __name__ == '__main__':
    main()
