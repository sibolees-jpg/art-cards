import json,sys,time
sys.path.insert(0,'.'); sys.setrecursionlimit(30000)
from adm1 import geoshape,rings_of,area,dp
ADD=[('伊朗','德黑蘭省','Q590866',0.08),('墨西哥','墨西哥城','Q1489',0.03),
     ('瑞士','巴塞尔城市州','Q12172',0.02),('日本','大阪府','Q123376',0.05)]
raw=json.load(open('admin1_raw.json'))
for cn,n,q,eps in ADD:
    if any(u['n']==n for u in raw.get(cn,[])): print(cn,n,'已有'); continue
    ok=False
    for k in range(5):
        try:
            d=geoshape(q,tries=2); rings=[]
            for f in d.get('features',[]): rings+=rings_of(f['geometry'])
            rings.sort(key=area,reverse=True)
            keep=[r for r in rings[:3] if area(r)>=area(rings[0])*0.05]
            simp=[[[round(x,2),round(y,2)] for x,y in dp([tuple(p) for p in r],eps)] for r in keep]
            simp=[p for p in simp if len(p)>=4]
            if simp: raw[cn].append({'n':n,'r':simp}); print(cn,n,'OK',sum(len(x) for x in simp),flush=True); ok=True; break
        except Exception: time.sleep(3*(k+1))
    if not ok: print(cn,n,'--失败',flush=True)
json.dump(raw,open('admin1_raw.json','w'),ensure_ascii=False)
print('合计',sum(len(v) for v in raw.values()))
