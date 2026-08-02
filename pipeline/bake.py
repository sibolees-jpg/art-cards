import json,os,re,sys,importlib
SP=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,SP)
CARDS=importlib.import_module(sys.argv[1]).CARDS
REPO='/Users/sli001/Desktop/艺术卡片-发布'
os.chdir(REPO)
jv=lambda v: json.dumps(v,ensure_ascii=False)
recs=[];skipped=[]
for c in CARDS:
    p=f"imgs/{c['id']}.webp"
    if not(os.path.exists(p) and os.path.getsize(p)>8000):
        skipped.append(c['id']); continue
    fields=[('id',c['id']),('img',p),('cr',c['cr']),('cat',c['cat']),('kind','art'),
            ('t',c['t']),('a',c['a']),('y',c['y']),('bg',c['bg']),('how',c['how']),
            ('why',c['why']),('more',c['more'])]
    recs.append('{'+','.join(f"{k}:{jv(v)}" if k!='id' else f"id:{v}" for k,v in fields)+'}')
data=open('data.js',encoding='utf-8').read()
exist=set(int(m) for m in re.findall(r'(?m)^\{id:(\d+)',data))
recs=[r for r in recs if int(re.match(r'\{id:(\d+)',r).group(1)) not in exist]
if not recs: print('无新卡可写'); raise SystemExit
i=data.rstrip().rfind('];'); head=data[:i].rstrip()
if not head.endswith(','): head+=','
open('data.js','w',encoding='utf-8').write(head+'\n'+',\n'.join(recs)+'\n];\n')
print('写入新卡',len(recs),'张;因无图跳过',skipped)
