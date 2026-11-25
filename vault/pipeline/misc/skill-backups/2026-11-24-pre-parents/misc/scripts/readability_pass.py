"""Apply readability formatting across all node files.

Three rules:
1. After every `##` or `###` heading, ensure a blank line before the body.
2. Inside blockquotes, between any non-empty `> ...` line and a following
   `> ![[...]]` embed, insert a `>` separator (in-blockquote blank line).
3. Between consecutive `- [[wikilink]]` list items, insert a blank line so
   each link gets its own visual chunk.

Idempotent: collapses any `\n\n\n+` runs to `\n\n`.
"""
import re
from pathlib import Path

VAULT = Path('/Users/ppatel/Documents/living-synthesis')


def fix_readability(text: str) -> str:
    # Preserve YAML frontmatter (don't touch headings inside it)
    fm_end = -1
    if text.startswith('---'):
        m = re.match(r'^---\n(.*?\n)---\n', text, re.DOTALL)
        if m:
            fm_end = m.end()
    head = text[:fm_end] if fm_end > 0 else ''
    body = text[fm_end:] if fm_end > 0 else text

    lines = body.split('\n')
    new_lines = []
    for i, line in enumerate(lines):
        new_lines.append(line)
        nxt = lines[i + 1] if i + 1 < len(lines) else None

        # Rule 1: After ## or ### heading, blank line before body
        if re.match(r'^##+\s', line):
            if nxt is not None and nxt.strip() != '':
                new_lines.append('')

        # Rule 2: Inside blockquote, between non-empty > line and > ![[...]] embed,
        # insert > separator. Don't insert if previous line is already a separator.
        if (line.startswith('>') and line.strip() != '>'
                and nxt is not None and re.match(r'^>\s*!\[\[', nxt)
                and not re.match(r'^>\s*!\[\[', line.strip())):  # current is not also an embed
            new_lines.append('>')

        # Rule 3: Between consecutive list items that are wikilinks, blank line
        if re.match(r'^-\s*\[\[', line) and nxt is not None and re.match(r'^-\s*\[\[', nxt):
            new_lines.append('')

    body = '\n'.join(new_lines)
    # Collapse 3+ consecutive blank lines to 2
    body = re.sub(r'\n{3,}', '\n\n', body)
    return head + body


def main():
    counts = {'evidence': 0, 'claims': 0, 'caveats': 0, 'questions': 0}
    for d in counts:
        for f in (VAULT / d).glob('*.md'):
            if not (f.name.startswith('EVD') or f.name.startswith('CLM')
                    or f.name.startswith('CVT') or f.name.startswith('QUE')):
                continue
            text = f.read_text()
            new = fix_readability(text)
            if new != text:
                f.write_text(new)
                counts[d] += 1
    for d, c in counts.items():
        print(f'{d}: {c} files updated')
    print(f'Total: {sum(counts.values())} files updated')


if __name__ == '__main__':
    main()
