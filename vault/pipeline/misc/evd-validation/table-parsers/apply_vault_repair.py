"""Copies the repair block (vault_repair_block.py, same code as tablelib.py) into pipeline/scripts/pdf_pages.py in place of the old repair_cell_text.
usage: python3 apply_vault_repair.py [path to pdf_pages.py]   (default: the vault copy). Idempotent: markers #BEGIN_REPAIR / #END_REPAIR."""
import sys, os, re
here=os.path.dirname(os.path.abspath(__file__))
target=sys.argv[1] if len(sys.argv)>1 else os.path.join(here,'..','..','..','scripts','pdf_pages.py')
blk=open(os.path.join(here,'vault_repair_block.py')).read()
v=open(target).read()
new='#BEGIN_REPAIR\n'+blk+'#END_REPAIR\n\n\n'
if '#BEGIN_REPAIR' in v:
    a=v.index('#BEGIN_REPAIR'); b=v.index('#END_REPAIR\n')+len('#END_REPAIR\n'); v=v[:a]+new.rstrip('\n')+'\n'+v[b:].lstrip('\n') if False else v[:a]+new+v[b:].lstrip('\n')
else:
    a=v.index('def repair_cell_text(text):'); b=v.index('def table_cells(page):'); v=v[:a]+new+v[b:]
open(target,'w').write(v); print('patched',target)
