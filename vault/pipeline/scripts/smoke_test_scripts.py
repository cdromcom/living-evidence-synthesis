#!/usr/bin/env python3
"""Smoke-test every script in pipeline/scripts on a THROWAWAY copy of the vault (the real vault is never touched).
For each script: exit code, seconds, files it changed in the copy, last output line. Writes a markdown table.
  python3 smoke_test_scripts.py --copy DIR --out report.md [--only name]
DIR must hold a copy of the vault (the PDF folder may be a symlink); set up by the caller. Network scripts run for real (cents at most)."""
import argparse, hashlib, os, subprocess, sys, time
from pathlib import Path
ap = argparse.ArgumentParser(); ap.add_argument('--copy', required=True); ap.add_argument('--out', required=True); ap.add_argument('--only'); ap.add_argument('--graph', default='')
a = ap.parse_args(); C = Path(a.copy).resolve(); HERE = Path(__file__).resolve().parent
PDF = next(iter(sorted((C / 'sysrev/dgraph/source/pdfs').glob('Akyon*.pdf'))), None); CK = '@akyonEvaluatingCapabilitiesGenerative2024'
SCR = C / 'pipeline/scripts'; PROV = SCR / 'provenance'; OUT = C / '_smoke_out'; OUT.mkdir(exist_ok=True)
(OUT / 'q.json').write_text('[{"label":"t","page":9,"opening":"we relied on the expertise","closing":"epidemiology expert doctor"}]')
T = [('add_tldr_callouts.py', []), ('build_dgraph.py', []), ('count_evds_per_subtask.py', []), ('cvt_screenshot_pipeline.py', []), ('find_redundancies.py', []),
     ('link_eps_to_ques.py', []), ('readability_pass.py', []), ('reverse_links.py', []), ('verbatim_audit.py', []),
     ('quote_pipeline.py', []), ('extract_quotes.py', [str(PDF), str(OUT / 'crops'), CK, str(OUT / 'q.json')]),
     ('check_quality_signals.py', []), ('audit_signal_quotes.py', ['--only', CK, '--outdir', str(OUT)]),
     ('signals_decision_models.py', ['--only', CK, '--limit', '1', '--out', str(OUT / 'dm.jsonl')]),
     ('signals_to_gsheet.py', ['--only', CK, '--out', str(OUT / 'review.xlsx')]),
     ('vault_to_gsheet.py', ['--out', str(OUT / 'mirror.xlsx')] + (['--graph', a.graph] if a.graph else [])),
     ('pdf_pages.py', ['map', str(PDF)]), ('pdf_pages.py', ['find', str(PDF), 'we relied on the expertise of an experienced medical professor']),
     ('pdf_pages.py', ['crop', str(PDF), 'we relied on the expertise of an experienced medical professor', str(OUT / 'c.png')]), ('pdf_pages.py', ['links', str(PDF)]),
     ('keyword_freq_check.py', []), ('pangram_check.py', []),
     ('provenance/openalex.py', ['10.2196/59258']), ('provenance/doaj.py', ['2291-9694']), ('provenance/opencitations.py', ['10.2196/59258']),
     ('provenance/pubpeer.py', ['10.2196/59258']), ('provenance/howfairis_check.py', ['https://github.com/fair-software/howfairis']),
     ('provenance/fair_checker.py', ['https://osf.io/']), ('provenance/run_provenance.py', ['--doi', '10.2196/59258'])]
def snap():
    d = {}
    for p in C.rglob('*'):
        if p.is_file() and not p.is_symlink() and '_smoke_out' not in p.parts and 'pdfs' not in p.parts and '__pycache__' not in p.parts:
            d[str(p.relative_to(C))] = hashlib.md5(p.read_bytes()).hexdigest()
    return d
rows = []
for name, args in T:
    if a.only and a.only not in name: continue
    before = snap(); t0 = time.time(); env = dict(os.environ, LIVES_VAULT=str(C))
    try:
        p = subprocess.run([sys.executable, str(SCR / name)] + args, capture_output=True, text=True, timeout=300, env=env, cwd=str(SCR / Path(name).parent)); rc = p.returncode
        tail = ((p.stdout.strip() or p.stderr.strip()).splitlines() or [''])[-1][:110]
    except subprocess.TimeoutExpired: rc, tail = 'timeout', '>300 s'
    after = snap(); ch = sorted(k for k in after if before.get(k) != after[k])
    rows.append((name + ' ' + (args[0] if args and not args[0].startswith(('-', '/')) and name == 'pdf_pages.py' else ''), rc, round(time.time() - t0, 1), len(ch), tail.replace('|', '/')))
    print(rows[-1], flush=True)
md = ['# Script smoke tests', '', 'Run on a throwaway copy of the vault; the real vault was not touched. Exit code 0 = ran without error. "Changed" = files the script modified in the copy.', '',
      '| Script | Exit | Seconds | Changed | Last output line |', '|---|---|---|---|---|'] + [f'| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |' for r in rows]
Path(a.out).write_text('\n'.join(md) + '\n'); print('wrote', a.out)
