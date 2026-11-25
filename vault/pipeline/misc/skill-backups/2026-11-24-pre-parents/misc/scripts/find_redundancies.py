"""Surface candidate redundant/overlapping nodes within each type by Jaccard similarity
of title keyword sets. Threshold tuned per node type since EVD titles are longer + more
specific while QUE/CLM titles are more abstract.
"""
import re
from pathlib import Path
from itertools import combinations

VAULT = Path('/Users/ppatel/Documents/living-synthesis')

STOP = set(("a an and are as at be but by could do does for from has have how if in into is it its like may might must "
            "not of on or our should so than that the their them then there these they this to was we were what when "
            "where which who why will with would you your also another any been being both each few many more most "
            "other own same some such those very what's whats us into upon use using used").split())
DOMAIN_STOP = set("llm llms can does ai".split())
SKIP = STOP | DOMAIN_STOP


def keywords(s: str) -> set[str]:
    s = s.lower()
    s = re.sub(r'[^a-z0-9-]+', ' ', s)
    out = set()
    for w in s.split():
        if len(w) <= 2 or w in SKIP:
            continue
        if w.endswith('s') and len(w) > 4 and not w.endswith('ss'):
            w = w[:-1]
        out.add(w)
    return out


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def evd_citekey(stem: str) -> str | None:
    m = re.search(r'@([a-zA-Z][a-zA-Z0-9-]+)$', stem)
    return m.group(1) if m else None


def find_pairs(files, prefix: str, threshold: float, citekey_aware: bool = False):
    """Return list of (jaccard, fileA, fileB, shared_keywords)."""
    items = []
    for f in files:
        title = f.stem.replace(f'{prefix} - ', '')
        # Strip trailing citekey from EVD titles
        title = re.sub(r' - @[a-zA-Z0-9-]+$', '', title)
        items.append((f.stem, keywords(title), evd_citekey(f.stem)))
    pairs = []
    for (s1, k1, c1), (s2, k2, c2) in combinations(items, 2):
        sim = jaccard(k1, k2)
        if sim >= threshold:
            same_paper = (c1 and c2 and c1 == c2)
            pairs.append((sim, s1, s2, k1 & k2, same_paper))
    pairs.sort(reverse=True)
    return pairs


def main():
    print('=' * 80)
    print('REDUNDANCY CANDIDATES — pairs with Jaccard similarity above threshold')
    print('=' * 80)

    print('\n## QUE pairs (threshold 0.30)\n')
    pairs = find_pairs(sorted((VAULT/'questions').glob('QUE*.md')), 'QUE', 0.30)
    print(f'Found {len(pairs)} candidate pairs:\n')
    for sim, a, b, shared, _ in pairs:
        print(f'[{sim:.2f}] shared: {", ".join(sorted(shared))}')
        print(f'    {a}')
        print(f'    {b}')
        print()

    print('\n## CLM pairs (threshold 0.30)\n')
    pairs = find_pairs(sorted((VAULT/'claims').glob('CLM*.md')), 'CLM', 0.30)
    print(f'Found {len(pairs)} candidate pairs:\n')
    for sim, a, b, shared, _ in pairs:
        print(f'[{sim:.2f}] shared: {", ".join(sorted(shared))}')
        print(f'    {a}')
        print(f'    {b}')
        print()

    print('\n## EVD pairs (threshold 0.40, marking same-paper pairs)\n')
    pairs = find_pairs(sorted((VAULT/'evidence').glob('EVD*.md')), 'EVD', 0.40, citekey_aware=True)
    print(f'Found {len(pairs)} candidate pairs:\n')
    for sim, a, b, shared, same in pairs:
        marker = ' [SAME PAPER]' if same else ''
        print(f'[{sim:.2f}]{marker} shared: {", ".join(sorted(shared))}')
        print(f'    {a}')
        print(f'    {b}')
        print()

    print('\n## CVT pairs (threshold 0.30)\n')
    pairs = find_pairs(sorted((VAULT/'caveats').glob('CVT*.md')), 'CVT', 0.30)
    print(f'Found {len(pairs)} candidate pairs:\n')
    for sim, a, b, shared, _ in pairs:
        print(f'[{sim:.2f}] shared: {", ".join(sorted(shared))}')
        print(f'    {a}')
        print(f'    {b}')
        print()


if __name__ == '__main__':
    main()
