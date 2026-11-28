"""Offline tests for scripts/methods_table_check.py: a synthetic table, the real Woelfle Table 1 (PDF page 3) and Sarol Table 4 (PDF page 6), a vault page, a prose check.
MinerU runs once per page in the table-parsers virtual environment and is cached; with the cache present the tests need no model. Run: python3 tests/test_methods_table_check.py"""
import json, os, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import fitz
import methods_table_check as M, pdf_pages as pp
bad = 0
def check(name, cond, detail=''):
    global bad
    if not cond: bad += 1; print('MISMATCH', name, detail)
def kinds(rec): return {(c['row'], c['col']): c['result'] for c in rec['cells']}
def cell(rec, r, c): return next(x for x in rec['cells'] if x['row'] == r and x['col'] == c)

# ---- synthetic table (ruled grid drawn with PyMuPDF; read by PyMuPDF only)
def synth_pdf(path):
    doc = fitz.open(); pg = doc.new_page(width=612, height=792); pg.insert_text((72, 60), 'Table 1. Accuracy of three models.', fontsize=10)
    vals = [['Model', 'Accuracy', 'CI'], ['Alpha', '0.90', '(0.88-0.93)'], ['Beta', '63%', '(60%-66%)'], ['Gamma', '1,000', '(900-1,100)']]
    for r in range(4):
        for c in range(3):
            pg.draw_rect(fitz.Rect(72 + c * 100, 80 + r * 22, 72 + (c + 1) * 100, 80 + (r + 1) * 22), color=(0, 0, 0), width=0.6)
            pg.insert_text((72 + c * 100 + 4, 80 + r * 22 + 15), vals[r][c], fontsize=8)
    doc.save(path)
tmp = Path(tempfile.mkdtemp()); sp = tmp / 'synth.pdf'; synth_pdf(str(sp))
good = [['Model', 'Accuracy', 'CI'], ['Alpha', '0.90', '(0.88-0.93)'], ['Beta', '63%', '(60%-66%)'], ['Gamma', '1,000', '(900-1,100)']]
r = M.check_table(good, sp, 1, parsers=('pymupdf',), table_no='1')
check('synthetic: correct copy is fully matched', r['summary']['matched'] == r['summary']['cells'] == 12, r['summary'])
fmt = [['Model', 'Accuracy', 'CI'], ['Alpha', '.9', '(0.88–0.93)'], ['Beta', '63 %', '(60%–66%)'], ['Gamma', '1000', '(900–1100)']]
r = M.check_table(fmt, sp, 1, parsers=('pymupdf',))
check('synthetic: other number format is not flagged', not r['summary']['mismatches'] and cell(r, 1, 1)['result'] == 'number_format', r['summary'])
check('synthetic: en dash against hyphen is match_after_repair', cell(r, 1, 2)['result'] == 'match_after_repair')
planted = [['Model', 'Accuracy', 'CI'], ['Alpha', '0.91', '(0.88-0.93)'], ['Beta', '63%', '(60%-66%)'], ['Gamma', '1,000', '(900-1,100)']]
r = M.check_table(planted, sp, 1, parsers=('pymupdf',))
m = r['summary']['mismatches']
check('synthetic: one changed digit is caught', len(m) == 1 and m[0]['result'] == 'text_differs' and m[0]['copy'] == '0.91' and m[0]['source'] == '0.90', m)
reord = [good[0], good[3], good[1], good[2]]
r = M.check_table(reord, sp, 1, parsers=('pymupdf',)); check('synthetic: reordered rows match', not r['summary']['mismatches'], r['summary'])
extra = good + [['Delta', '0.50', '(0.4-0.6)']]
r = M.check_table(extra, sp, 1, parsers=('pymupdf',)); check('synthetic: extra row reported', {x['result'] for x in r['summary']['mismatches']} == {'extra_in_copy'} and len(r['summary']['mismatches']) == 3, r['summary'])
miss = [['Model', 'Accuracy', 'CI'], ['Alpha', '0.90', '(0.88-0.93)', 'new column'], ['Beta', '63%', '(60%-66%)'], ['Gamma', '1,000', '(900-1,100)']]
r = M.check_table(miss, sp, 1, parsers=('pymupdf',)); check('synthetic: extra cell with no source cell is missing_in_source', cell(r, 1, 3)['result'] == 'missing_in_source', r['summary'])
split = [['Model', 'Accuracy', 'CI low', 'CI high'], ['Alpha', '0.90', '(0.88', '0.93)'], ['Beta', '63%', '(60%', '66%)'], ['Gamma', '1,000', '(900', '1,100)']]
r = M.check_table(split, sp, 1, parsers=('pymupdf',)); check('synthetic: a split cell is matched', cell(r, 1, 2)['result'] == 'match_split_or_joined_cells' or cell(r, 1, 2)['result'] in M.MATCHED, r['summary'])
r2 = M.check_table(good, sp, None, parsers=('pymupdf',), table_no='1'); check('synthetic: page located from the caption', r2['source']['pdf_page'] == 1 and r2['source']['page_source'] in ('caption', 'overlap'))
check('record: no absolute home path and a sha256', str(Path.home()) not in json.dumps(r2) and len(r2['source']['sha256']) == 64)
out = tmp / 'out'; r3 = M.check_table(good, sp, 1, parsers=('pymupdf',), out_dir=out)
check('record: JSON and crop written, relative or file-name paths', (out / Path(r3['crop']).name).exists() and (out / Path(r3['record']).name).exists() and not str(r3['crop']).startswith('/Users'))
pr = M.check_prose_numbers('Alpha reached 0.90 and Gamma 1,000 but Beta 77.', sp, 1); check('prose: numbers found and not found', pr['not_found'] == ['77'] and pr['found'] == 2, pr)

# ---- real tables (MinerU result cached; PyMuPDF as fallback)
wo = pp.resolve_pdf('@woelfleBenchmarkingHumanAICollaboration2024'); sa = pp.resolve_pdf('@sarolAssessingCitationIntegrity2024')
W = [['Company: LLM name (exact version identifier)', 'Context length, n tokens (words)', 'Time of queries and API used', 'Median cost (IQR) and response time per publication'],
     ['Anthropic: Claude-3-Opus (claude-3-opus-20240229)', '200k (~150k)', 'April 2024 via Anthropic', '$ 0.40 (0.14-0.78) ~1-2 mins'],
     ['Anthropic: Claude-2 (claude-2.0)', '100k (~75k)', 'September 2023 via OpenRouter', '$ 0.19 (0.09-0.81) ~1 minute'],
     ['OpenAI: GPT-4 (gpt-4-32k-0613)', '32k (~24k)', 'September 2023 via OpenRouter', '$ 1.15 (0.65-1.98) ~2 mins'],
     ['OpenAI: GPT-3.5 (gpt-3.5-turbo-16k-0613)', '16k (~12k)', 'August 7, 2023 via OpenAI', '$ 0.06 (0.03-0.10) ~10 s'],
     ['Mistral AI: Mixtral-8x22B (Mixtral-8x22b-instruct-v0.1)', '64k (~48k)', 'April 2024 via OpenRouter', '$ 0.012 (0.010-0.017) ~1-2 mins']]
r = M.check_table(W, wo, 3, table_no='1'); s = r['summary']
check('Woelfle Table 1: correct copy fully matched', s['matched'] == s['cells'] == 24, s)
check('Woelfle Table 1: a cell where MinerU misreads OpenAI is supplied by PyMuPDF', cell(r, 4, 2)['parser'] == 'pymupdf' and cell(r, 4, 2)['result'] in ('exact', 'match_after_repair'), cell(r, 4, 2))
check('Woelfle Table 1: the bar-for-tilde repair is recorded', any('bar_for_tilde' in c.get('repair_rules', []) for c in r['cells']))
Wp = [row[:] for row in W]; Wp[1][3] = '$ 0.44 (0.14-0.78) ~1-2 mins'
r = M.check_table(Wp, wo, 3, table_no='1'); m = r['summary']['mismatches']
check('Woelfle Table 1: one digit changed (0.40 to 0.44) is caught', len(m) == 1 and m[0]['row'] == 1 and m[0]['col'] == 3 and m[0]['result'] == 'text_differs' and '0.40' in m[0]['source'], m)
Wf = [row[:] for row in W]; Wf[1][3] = '$0.4 (0.14–0.78) ~1–2 mins'; Wf[5][3] = '$ 0.012 (.010–.017) ~1-2 mins'
r = M.check_table(Wf, wo, 3, table_no='1'); check('Woelfle Table 1: same values in another format are not flagged', not r['summary']['mismatches'] and cell(r, 1, 3)['result'] in ('number_format', 'match_after_repair'), r['summary'])
S = [['Evidence input', 'Label', 'F1', 'Micro/Macro-F1'], ['MultiVerS models', '', '', ''], ['Title+abstract', 'ACC', '0.69', ''], ['', 'N_ACC', '0.38', '0.56/0.43'], ['', 'IRR', '0.20', ''],
     ['Top 5 sentences', 'ACC', '0.69', ''], ['', 'N_ACC', '**0.43**', '0.58/0.50'], ['', 'IRR', '0.37', ''], ['Top 10 sentences', 'ACC', '0.67', ''], ['', 'N_ACC', '0.41', '0.56/0.48'], ['', 'IRR', '0.36', ''],
     ['Top 20 sentences', 'ACC', '0.69', ''], ['', 'N_ACC', '**0.43**', '0.59/0.52'], ['', 'IRR', '0.42', ''], ['Top 20 sentences + annotated evidence', 'ACC', '0.69', ''], ['', 'N_ACC', '**0.43**', '0.58/0.50'], ['', 'IRR', '0.38', ''],
     ['Oracle (gold citation + gold evidence)', 'ACC', '0.80', ''], ['', 'N_ACC', '0.57', '0.75/0.78'], ['', 'IRR', '0.96', ''], ['Oracle (gold evidence)', 'ACC', '0.79', ''], ['', 'N_ACC', '0.52', '0.73/0.75'], ['', 'IRR', '0.93', '']]
r = M.check_table(S, sa, 6, table_no='4'); s = r['summary']
check('Sarol Table 4: correct copy has no mismatch', not s['mismatches'], s['mismatches'][:5])
Sp = [row[:] for row in S]; Sp[12][2] = '0.44'
r = M.check_table(Sp, sa, 6, table_no='4'); m = r['summary']['mismatches']
check('Sarol Table 4: one digit changed (Top 20, N_ACC 0.43 to 0.44) is caught', len(m) == 1 and m[0]['copy'] == '0.44' and m[0]['source'] and '0.43' in m[0]['source'], m)
Sf = [row[:] for row in S]; Sf[3][2] = '.38'; Sf[18][3] = '0.75 / 0.78'
r = M.check_table(Sf, sa, 6, table_no='4'); check('Sarol Table 4: other formatting is not flagged', not r['summary']['mismatches'], r['summary']['mismatches'][:3])
t = time = __import__('time').time(); r = M.check_table(S, sa, 6, table_no='4'); check('cached MinerU result makes a rerun free', r['parsers']['mineru']['status'] == 'cached' and r['parsers']['mineru']['seconds'] == 0)


# ---- Woelfle Table 2 (PDF page 5): en dash stored as the letter e in the text layer, MinerU spacing differs
T2 = [['Rater', "Cohen's kappa (95% CI)", 'Agreement (%, 95% CI)', "Cohen's kappa (95% CI)", 'Agreement (%, 95% CI)'],
      ['PRISMA (27 items \u00d7 112 publications = up to 3024 ratings)', '', '', '', ''],
      ['(1) Human Rater 1', '0.81 (0.78\u20130.83)', '2686/3024 (89%, 87%\u201390%)', '0.84 (0.80\u20130.88)', '2384/2619 (91%, 89%\u201393%)'],
      ['(2) Claude-3-Opus', '0.51 (0.47\u20130.55)', '2073/2943 (70%, 68%\u201372%)', '0.68 (0.64\u20130.71)', '2318/2889 (80%, 78%\u201382%)'],
      ['(2) GPT-3.5', '0.40 (0.37\u20130.44)', '1868/2943 (63%, 62%\u201366%)', '0.90 (0.87\u20130.93)', '2762/2943 (94%, 92%\u201396%)']]
r = M.check_table(T2, wo, 5, table_no='2'); s = r['summary']
check('Woelfle Table 2: correct copy has no mismatch', not s['mismatches'], s['mismatches'][:4])
check('Woelfle Table 2: a repaired source cell is match_after_repair', any(c['result'] == 'match_after_repair' for c in r['cells']), s['by_result'])
T2p = [row[:] for row in T2]; T2p[4][1] = '0.41 (0.37\u20130.44)'
r = M.check_table(T2p, wo, 5, table_no='2'); m = r['summary']['mismatches']
check('Woelfle Table 2: one digit changed (kappa 0.40 to 0.41) is caught', len(m) == 1 and m[0]['copy'].startswith('0.41') and '0.40' in m[0]['source'], m)

# ---- a vault page
page = tmp / 'EVD - test.md'
md = lambda rows: '\n'.join('| ' + ' | '.join(x) + ' |' for x in ([rows[0], ['---'] * len(rows[0])] + rows[1:]))
page.write_text('## Source\n\n[[source/@woelfleBenchmarkingHumanAICollaboration2024]]\n\nTable 1 (PDF p. 3):\n\n' + md(Wp) + '\n\nA table with no citation:\n\n| a | b |\n| --- | --- |\n| 1 | 2 |\n', encoding='utf-8')
vr = M.check_vault_page(page, out_dir=tmp / 'vault_out')
check('vault page: cited table checked, uncited table skipped', len(vr['tables']) == 1 and len(vr['skipped']) == 1 and vr['tables'][0]['source']['pdf_page'] == 3, vr['skipped'])
check('vault page: the planted change is reported', len(vr['tables'][0]['summary']['mismatches']) == 1)
print('methods_table_check tests: mismatches', bad)
def run(): return bad
if __name__ == '__main__': sys.exit(1 if bad else 0)
