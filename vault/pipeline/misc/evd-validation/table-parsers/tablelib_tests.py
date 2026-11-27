"""Offline unit tests for tablelib.repair_cell_text (and repair_cell_text_notes). Run: python3 tablelib_tests.py  (no network, no model).
The same checks in the style of pipeline/scripts/selftest.py are in RESULTS.md, section 'selftest additions'."""
import os, re, sys
here=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,here)
import tablelib as T
R=T.repair_cell_text; N=T.repair_cell_text_notes
TESTS=[
 # rule 1: en dash stored as the letter e
 ('en dash e between numbers', R('0.37 (0.30e0.44)'), '0.37 (0.30–0.44)'),
 ('en dash e after percent', R('88% (85%e90%)'), '88% (85%–90%)'),
 ('scientific number kept', R('1e-5'), '1e-5'),
 ('word with e untouched', R('Table 1 left (the e1)'), 'Table 1 left (the e1)'),
 # rule 2: single-character substitutions
 ('U+0004 is a minus', R('0.01 (\x040.08 to 0.08)'), '0.01 (−0.08 to 0.08)'),
 ('U+0003 is a times sign', R('27 items \x03 112 publications'), '27 items × 112 publications'),
 ('thorn is plus', R('Titleþabstract'), 'Title+abstract'),
 ('quarter sign is equals', R('P ¼ .095'), 'P = .095'),
 ('private-use digits', R('. %'), '59.9 %'),
 ('soft hyphen removed', R('Effi­cacy'), 'Efficacy'),
 ('ligature expanded', R('ﬁnal ﬂow'), 'final flow'),
 # rule 3
 ('five for equals checked by arithmetic', R('PRISMA (27 items \x03 112 publications 5 up to 3024 ratings)'), 'PRISMA (27 items × 112 publications = up to 3024 ratings)'),
 ('five kept when arithmetic does not hold', R('27 items \x03 112 publications 5 up to 3000 ratings'), '27 items × 112 publications 5 up to 3000 ratings'),
 # rule 4: unreadable script
 ('Khmer marked unreadable, digits kept', R('ដកុ្ត 2/3 313 36'), '[unreadable] 2/3 313 36'),
 ('Khmer note', N('ដក 5')[1], {'unreadable': True}),
 # rule 5: bar for tilde
 ('bar before a number is a tilde', R('200k (|150k)'), '200k (~150k)'),
 ('bar before a number after a space', R('$ 0.40 (0.14-0.78) | 1-2 mins'), '$ 0.40 (0.14-0.78) ~1-2 mins'),
 ('bars around a word kept', R('2. |diff| ↓'), '2. |diff| ↓'),
 # rule 6: powers of ten
 ('flattened power of ten', R('10−3'), '10^−3'),
 ('flattened power of ten after a coefficient', R('5.42 10−15'), '5.42 10^−15'),
 ('range with minus and words kept', R('10−12 years'), '10−12 years'),
 ('hyphen range kept', R('10-12'), '10-12'),
 ('superscript exponent after times sign', R('2 ×10²'), '2 ×10^2'),
 ('superscript negative exponent on a bare 10', R('10⁻³'), '10^-3'),
 # rule 7: footnote letters and superscripts
 ('footnote letter after interval', R('0.90 (0.88e0.93)a'), '0.90 (0.88–0.93)'),
 ('footnote letter note', N('0.90 (0.88–0.93)a')[1], {'footnotes': ['a']}),
 ('footnote letter after percent', R('62%b'), '62%'),
 ('footnote letter after decimal', R('3.1c'), '3.1'),
 ('footnote after fraction with percent', R('1878/1989 (94%, 93%–96%)a'), '1878/1989 (94%, 93%–96%)'),
 ('ordinal indicator as footnote a', N('1878/1989 (94%)ª'), ('1878/1989 (94%)', {'footnotes': ['a']})),
 ('footnote letter with the word to', R('0.04 (\x040.05 to 0.12)b'), '0.04 (−0.05 to 0.12)'),
 ('superscript digit footnote', N('1196/2997 (40%, 37%–44%)²'), ('1196/2997 (40%, 37%–44%)', {'superscripts': ['2']})),
 ('days unit kept', R('3d'), '3d'),
 ('decimal days kept', R('37.5d'), '37.5d'),
 ('row label with digit and letter kept', R('2b'), '2b'),
 ('model name kept', R('ChatGPT4o'), 'ChatGPT4o'),
 ('square unit kept', R('5 cm²'), '5 cm²'),
 ('word cell with trailing letter kept', R('(95% CI)a'), '(95% CI)a'),
 ('star and dagger kept', R('0.5 (0.1)*'), '0.5 (0.1)*'),
 ('plain numbers unchanged', R('0.90 (0.88–0.93)'), '0.90 (0.88–0.93)'),
 ('plus-minus kept', R('2.95 ± 1.19'), '2.95 ± 1.19'),
 ('empty cell', R(''), ''),
 ('whitespace-only change not made on a clean cell', R('a  b'), 'a  b'),
]
def run():
    bad=0
    for name,got,want in TESTS:
        ok=(got==want)
        if not ok: bad+=1; print('MISMATCH',name,'| got',repr(got),'| want',repr(want))
    # the callers' contract: repair_cell_text returns a string
    assert isinstance(R('x'),str)
    # the vault copy must hold the same code
    vault=os.path.normpath(os.path.join(here,'..','..','..','scripts','pdf_pages.py'))
    def block(path):
        s=open(path).read()
        if '#BEGIN_REPAIR' not in s: return None
        return s[s.index('#BEGIN_REPAIR'):s.index('#END_REPAIR')]
    a=block(os.path.join(here,'tablelib.py')); b=block(vault) if os.path.exists(vault) else None
    if b is None: print('NOTE vault pdf_pages.py has no #BEGIN_REPAIR block yet (run apply_vault_repair.py to put the same code there)')
    elif a.split('\n',1)[1]!=b.split('\n',1)[1]: bad+=1; print('MISMATCH tablelib.py and pdf_pages.py repair blocks differ')
    print(f'{len(TESTS)} checks, {bad} mismatches')
    return bad
if __name__=='__main__': sys.exit(1 if run() else 0)
