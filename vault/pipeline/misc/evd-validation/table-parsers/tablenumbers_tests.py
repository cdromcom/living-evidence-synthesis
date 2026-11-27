"""Offline tests for table_numbers (vault_table_numbers_block.py), docx_tables (vault_docx_tables_block.py) and derotate_page (derotate.py). Run: python3 tablenumbers_tests.py"""
import os, sys, tempfile
here=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,here)
import tablenumbers as TN
import pymupdf
bad=0
def check(name,cond):
    global bad
    if not cond: bad+=1; print('MISMATCH',name)
ns=TN._number_set
check('commas and zeros normalised', ns('1,000 items, 0.90 and 007')=={'1000','0.9','7'})
check('minus kept with and without sign', {'-0.05','0.05'}<=ns('(-0.05 to 0.12)') and '0.12' in ns('(-0.05 to 0.12)'))
check('range hyphen is not a sign', ns('scale of 0-5')=={'0','5'})
check('percent and plus-minus ignored', ns('2.95 ± 1.19 (63%)')=={'2.95','1.19','63'})
check('numbers glued to words are not numbers', ns('ChatGPT4o Recall@5')=={'5'})
# synthetic page: caption, a ruled table, a footnote below, a body paragraph that mentions a table
doc=pymupdf.open(); pg=doc.new_page(width=612,height=792)
pg.insert_text((72,60),'Table 1. Accuracy on 1,000 items (scale 0-5).',fontsize=10)
x0,y0=72,80
for r in range(3):
    for c in range(3):
        pg.draw_rect(pymupdf.Rect(x0+c*90,y0+r*20,x0+(c+1)*90,y0+(r+1)*20),color=(0,0,0),width=0.6)
vals=[['Model','A','B'],['Top 5 sentences','0.91','$ 1.15 ~2 mins'],['x','0.5','0.6']]
for r in range(3):
    for c in range(3): pg.insert_text((x0+c*90+3,y0+r*20+14),vals[r][c][:14],fontsize=6)
pg.insert_text((72,150),'a Rater 1 only, n = 42.',fontsize=8)
pg.insert_text((72,190),'Table 2 shows that 77 of 99 papers were read by the second author in the long run of the study.',fontsize=10)
page=doc[0]
txt=TN.caption_footnote_text(page); tn=TN.table_numbers(page)
check('caption found', any(t.startswith('Table 1.') for t in txt))
check('footnote with letter marker found', any(t.startswith('a Rater') for t in txt))
check('body sentence about a table not taken', not any('77 of 99' in t for t in txt))
check('caption number in set', '1000' in tn and '0' in tn and '5' in tn)
check('footnote number in set', '42' in tn)
check('mixed text cell number in set', '1.15' in tn and '2' in tn)
check('label cell number in set', '5' in tn)
check('body number not in set', '77' not in tn and '99' not in tn)
# docx
import docx
d=docx.Document(); t=d.add_table(rows=3,cols=3)
t.cell(0,0).merge(t.cell(0,2)); t.cell(0,0).text='Header 0.37e0.44'
t.cell(1,0).merge(t.cell(2,0)); t.cell(1,0).text='Row'
t.cell(1,1).text='1.5a'; t.cell(1,2).text='2'; t.cell(2,1).text='3'; t.cell(2,2).text='4'
inner=t.cell(2,2).add_table(rows=1,cols=2); inner.cell(0,0).text='n1'; inner.cell(0,1).text='n2'
fn=os.path.join(tempfile.mkdtemp(),'t.docx'); d.save(fn)
from tablelib import repair_cell_text
exec(open(os.path.join(here,'vault_docx_tables_block.py')).read())
tabs=docx_tables(fn)
check('docx: outer and nested table returned', len(tabs)==2)
check('docx: horizontal merge repeated', tabs[0][0]==['Header 0.37–0.44']*3)
check('docx: vertical merge repeated', tabs[0][1][0]=='Row' and tabs[0][2][0]=='Row')
check('docx: repaired text', tabs[0][1][1]=='1.5')
check('docx: nested table kept apart', tabs[1]==[['n1','n2']])
# derotate
from derotate import derotate_page, text_angle
src=pymupdf.open(); p=src.new_page(width=612,height=792); p.insert_text((72,100),'Table 1. Hello world, this is a test line.',fontsize=11)
for deg in (0,90,180,270):
    s2=pymupdf.open(); s2.insert_pdf(src); s2[0].set_rotation(deg)
    up,info=derotate_page(s2[0]); check(f'derotate rotation {deg}',up.rotation==0 and info['method']=='text-direction')
s3=pymupdf.open(); q=s3.new_page(width=792,height=612); q.show_pdf_page(q.rect,src,0,rotate=90)
up,info=derotate_page(s3[0]); check('derotate sideways content', info['flattened'] and up.rotation==0 and text_angle(up)[0]==0)
for deg in (90,180,270):
    s4=pymupdf.open(); q=s4.new_page(width=612,height=792); q.show_pdf_page(q.rect,src,0,rotate=deg)
    up,info=derotate_page(s4[0]); check(f'derotate content turned {deg}',text_angle(up)[0]==0 and up.rotation==0 and 'Hello world' in up.get_text())
b=pymupdf.open(); b.new_page(); up,info=derotate_page(b[0]); check('derotate page without text',info['method']=='no-text-layer')
print('tablenumbers_tests: mismatches',bad); sys.exit(1 if bad else 0)
