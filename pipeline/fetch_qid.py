# -*- coding: utf-8 -*-
"""按 QID 直接抓作品(跳过维基条目名解析)"""
import json,sys,os,urllib.parse,subprocess
SP=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,SP)
from wd import works_of
src=json.load(open(os.path.join(SP,sys.argv[1])))
out={}
for name,qid,n in src:
    try:
        ws=works_of(qid,12)
        out[name]={'qid':qid,'works':ws}
        print(f'{name:<28} {qid:<12} {len(ws)}')
    except Exception as e:
        print(f'{name:<28} {qid:<12} ✗ {e}')
json.dump(out,open(os.path.join(SP,sys.argv[2]),'w'),ensure_ascii=False)
print('saved',sys.argv[2])
