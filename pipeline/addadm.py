import json,sys
sys.path.insert(0,'.'); sys.setrecursionlimit(30000)
from adm1 import geoshape,rings_of,area,dp
ADD={'美国':{'加利福尼亚州':'Q99','華盛頓哥倫比亞特區':'Q61','印第安纳州':'Q1415',
             '北卡罗来纳州':'Q1454','南卡罗来纳州':'Q1456','田纳西州':'Q1509',
             '威斯康星州':'Q1537','夏威夷州':'Q782','新罕布什尔州':'Q759'},
     '日本':{'石川縣':'Q127513','沖繩縣':'Q766445'},
     '比利时':{'瓦隆大区':'Q234'},
     '意大利':{'西西里':'Q1460','撒丁岛':'Q1462','特伦蒂诺-上阿迪杰':'Q1237',
               '弗留利-威尼斯朱利亚':'Q1250','瓦莱达奥斯塔':'Q1222','卡拉布里亚':'Q1458'}}
raw=json.load(open('admin1_raw.json'))
for cn,units in ADD.items():
    have={u['n'] for u in raw.get(cn,[])}
    for n,q in units.items():
        if n in have: continue
        try:
            d=geoshape(q); rings=[]
            for f in d.get('features',[]): rings+=rings_of(f['geometry'])
            rings.sort(key=area,reverse=True)
            keep=[r for r in rings[:3] if area(r)>=area(rings[0])*0.05]
            simp=[]
            for r in keep:
                pts=[[round(x,2),round(y,2)] for x,y in dp([tuple(p) for p in r],0.12)]
                if len(pts)>=4: simp.append(pts)
            if simp: raw[cn].append({'n':n,'r':simp}); print(cn,n,'OK',flush=True)
            else: print(cn,n,'-- too small',flush=True)
        except Exception as e: print(cn,n,'--',type(e).__name__,flush=True)
    json.dump(raw,open('admin1_raw.json','w'),ensure_ascii=False)
print('合计',sum(len(v) for v in raw.values()))
