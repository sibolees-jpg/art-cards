import json,re,sys,os
from opencc import OpenCC
cc=OpenCC('t2s')
SP=os.path.dirname(os.path.abspath(__file__))
REPO='/Users/sli001/Desktop/艺术卡片-发布'
srcs=sys.argv[1].split(',')          # works1.json,works1b.json
start=int(sys.argv[2]); N=int(sys.argv[3]); outf=sys.argv[4]
PER=int(sys.argv[5]) if len(sys.argv)>5 else 6
LO,HI=(2,9)
s=open(f'{REPO}/data.js').read()
titles={cc.convert(t) for t in re.findall(r'(?<![A-Za-z])t:"([^"]+)"',s)}
clean=lambda t: re.sub(r'[\s·:：,，。、_\-—]','',re.sub(r'[（(【\[].*?[）)】\]]','',t))
libset={clean(t) for t in titles}; libsort={''.join(sorted(clean(t))) for t in titles}
used=set()
for f in os.listdir(SP):
    if f.startswith('pick') and f.endswith('.json'):
        try: used|={x['qid'] for x in json.load(open(f'{SP}/{f}'))}
        except Exception: pass
pool=[]
for src in srcs:
    j=json.load(open(f'{SP}/{src}'))
    for a,d in j.items():
        for w in d['works']:
            if w['qid'] in used: continue
            if not (LO<=w['links']<=HI): continue
            t=clean(cc.convert(w['t']))
            if not t or re.match(r'^Q\d+$',t): continue
            if t in libset or ''.join(sorted(t)) in libsort: continue
            pool.append({'a':a,**w})
pool.sort(key=lambda x:(x['a'],-x['links']))
per={};sel=[]
for w in pool:
    if per.get(w['a'],0)>=PER: continue
    per[w['a']]=per.get(w['a'],0)+1; sel.append(w)
    if len(sel)>=N: break
out=[{'id':start+n,'zh':w['t'][:26],'qid':w['qid'],'img':w['img'],'y':w['y'],'loc':w['loc'],'a':w['a']} for n,w in enumerate(sel)]
json.dump(out,open(f'{SP}/{outf}','w'),ensure_ascii=False,indent=1)
print('候选池',len(pool),'| 选出',len(out),'来自',len(per),'位')
for x in out: print(f"{x['id']} {x['a']:<14} {x['zh'][:30]} | {x['y']}")
