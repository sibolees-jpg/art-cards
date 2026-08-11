import json,sys,time
sys.path.insert(0,'.'); sys.setrecursionlimit(30000)
from adm1 import geoshape,rings_of,area,dp
RETRY=[('美国','加利福尼亚州','Q99',0.12),('美国','印第安纳州','Q1415',0.12),
       ('美国','南卡罗来纳州','Q1456',0.12),('美国','威斯康星州','Q1537',0.12),
       ('美国','新罕布什尔州','Q759',0.12),('比利时','瓦隆大区','Q234',0.04),
       ('意大利','瓦莱达奥斯塔','Q1222',0.04),('意大利','卡拉布里亚','Q1458',0.08)]
raw=json.load(open('admin1_raw.json'))
for cn,n,q,eps in RETRY:
    if any(u['n']==n for u in raw.get(cn,[])): continue
    ok=False
    for k in range(6):
        try:
            d=geoshape(q,tries=2); rings=[]
            for f in d.get('features',[]): rings+=rings_of(f['geometry'])
            rings.sort(key=area,reverse=True)
            keep=[r for r in rings[:3] if area(r)>=area(rings[0])*0.05]
            simp=[]
            for r in keep:
                pts=[[round(x,2),round(y,2)] for x,y in dp([tuple(p) for p in r],eps)]
                if len(pts)>=4: simp.append(pts)
            if simp:
                raw[cn].append({'n':n,'r':simp}); print(cn,n,'OK',sum(len(x) for x in simp),flush=True); ok=True; break
        except Exception as e:
            time.sleep(3*(k+1))
    if not ok: print(cn,n,'-- 仍失败',flush=True)
    json.dump(raw,open('admin1_raw.json','w'),ensure_ascii=False)
print('合计',sum(len(v) for v in raw.values()))
