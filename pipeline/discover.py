# -*- coding: utf-8 -*-
"""从 Wikidata 捞「有多件带图作品」的画家,自动跳过库里已有的作者"""
import json,sys,urllib.parse,urllib.request,re,os
from opencc import OpenCC
cc=OpenCC('t2s')
SP=os.path.dirname(os.path.abspath(__file__))
UA='artcards/1.0 (sibo.lees@gmail.com)'

import subprocess
def sparql(q):
    u='https://query.wikidata.org/sparql?format=json&query='+urllib.parse.quote(q)
    for _ in range(3):
        p=subprocess.run(['curl','-sL','--max-time','240','-A',UA,'-H','Accept: application/sparql-results+json',u],capture_output=True)
        try: return json.loads(p.stdout)['results']['bindings']
        except Exception: pass
    return []

# 库里已有的作者(简体)
data=open(os.path.join(SP,'..','data.js'),encoding='utf-8').read()
have={cc.convert(a) for a in re.findall(r'a:"([^"]+)"',data)}

lo,hi = int(sys.argv[1]), int(sys.argv[2])       # 出生年区间
minw = int(sys.argv[3]) if len(sys.argv)>3 else 6 # 至少几件带图作品
Q="""SELECT ?p ?pLabel (COUNT(DISTINCT ?w) AS ?n) WHERE {
  ?p wdt:P106 wd:Q1028181 ; wdt:P569 ?b .
  FILTER(YEAR(?b) >= %d && YEAR(?b) <= %d)
  ?w wdt:P170 ?p ; wdt:P18 ?img .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "zh,en". }
} GROUP BY ?p ?pLabel HAVING(COUNT(DISTINCT ?w) >= %d) ORDER BY DESC(?n) LIMIT 400""" % (lo,hi,minw)
rows=sparql(Q)
out=[]
for r in rows:
    zh=cc.convert(r['pLabel']['value'])
    if re.match(r'^Q\d+$',zh): continue
    if zh in have: continue
    out.append([zh, r['p']['value'].split('/')[-1], int(r['n']['value'])])
print('候选新作者:',len(out))
json.dump(out,open(os.path.join(SP,sys.argv[4] if len(sys.argv)>4 else 'disc.json'),'w'),ensure_ascii=False)
for x in out[:40]: print(' ',x[0],x[1],x[2])
