#!/usr/bin/env python3
"""Code Quality via howfairis (fair-software.eu, 5 criteria). Only github.com and gitlab.com repositories. howfairis pins an old click, so it
lives in its own virtual environment: python3 -m venv ~/.cache/lives-bench/venv-howfairis && ~/.cache/lives-bench/venv-howfairis/bin/pip install howfairis
Set HOWFAIRIS_PYTHON to use another interpreter. A GitHub token (env GITHUB_API_TOKEN, else `gh auth token`) avoids the 60-requests-an-hour limit.
  python3 howfairis_check.py https://github.com/owner/repo"""
import json, os, subprocess, sys
from pathlib import Path
PY = os.environ.get('HOWFAIRIS_PYTHON') or str(Path.home() / '.cache/lives-bench/venv-howfairis/bin/python')
CODE = ("import json,sys\nfrom howfairis import Checker, Repo\nc=Checker(Repo(sys.argv[1]),is_quiet=True).check_five_recommendations()\n"
        "print(json.dumps({k:bool(getattr(c,k)) for k in ('repository','license','registry','citation','checklist')}))")


def check(url: str) -> dict:
    if not any(h in url for h in ('github.com', 'gitlab.com')): return {'top/code-quality-fair': None, 'skipped': 'host not supported by howfairis (github.com and gitlab.com only)'}
    env = dict(os.environ)
    if 'GITHUB_API_TOKEN' not in env:
        t = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True).stdout.strip()
        if t: env['GITHUB_API_TOKEN'] = t
    p = subprocess.run([PY, '-c', CODE, url], capture_output=True, text=True, env=env, timeout=180)
    if p.returncode: return {'top/code-quality-fair': None, 'error': (p.stderr.strip().splitlines() or ['failed'])[-1][:200]}
    r = json.loads(p.stdout.strip().splitlines()[-1])
    return {'url': url, 'criteria': r, 'top/code-quality-fair': sum(r.values()), 'license_found': r['license']}


if __name__ == '__main__':
    print(json.dumps(check(sys.argv[1]), indent=1))
