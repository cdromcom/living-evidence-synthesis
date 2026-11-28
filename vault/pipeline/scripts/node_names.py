#!/usr/bin/env python3
"""One place for the vault file name and the wikilink of a discourse-graph node (JP, 2026-11-27). write_src.py uses it for the links on SRC pages; the writer that puts drafted nodes into the vault
must import node_stem() for the file name, so that a link on an SRC page and the node file always agree.
  node_stem(node)   'EVD - <title>' shortened so that the path sysrev/dgraph/<folder>/<stem>.md stays at 150 characters or less (Skill-references.md, Naming Conventions)
  node_link(node)   [[sysrev/dgraph/<folder>/<stem>|<TYPE> <id> - <full title>]]  (the vault's own form is [[<short filename>|<PREFIX> - <full title>]]; the draft id is added so a reader can tell which node is meant)
A node is the dict of the drafts file: id, type (EVD, QUE, CLM, CVT) and statement, title or limitation."""
import re
FOLDER = {'EVD': 'evidence', 'QUE': 'questions', 'CLM': 'claims', 'CVT': 'caveats'}
MAX_PATH = 150


def node_title(n):
    return n.get('statement') or n.get('title') or n.get('limitation') or n['id']


def clean(t):
    return ' '.join(re.sub(r'[\\/:*?"<>|#^\[\]]', '', t).split())


def node_stem(n):
    typ = n['type']; room = MAX_PATH - len(f'sysrev/dgraph/{FOLDER[typ]}/') - len('.md') - len(f'{typ} - ')
    t = clean(node_title(n))
    if len(t) > room: t = t[:room].rsplit(' ', 1)[0]
    return f"{typ} - {t.rstrip('.,;: ')}"


def node_link(n):
    typ = n['type']; return f"[[sysrev/dgraph/{FOLDER[typ]}/{node_stem(n)}|{typ} {n['id']} - {clean(node_title(n))}]]"
