# -*- coding: utf-8 -*-
"""补 6 个断流的省。响应总在 13570 字节处截断,重试无效——改用 gzip,
   压缩后体积落在阈值内就能完整传完。"""
import json,gzip,io,sys,math,urllib.request,time
sys.setrecursionlimit(20000)
exec(open('provinces.py').read().split('def main()')[0])   # 复用 perp/dp/rings_of/area

UA2={'User-Agent':'art-cards/1.0 (educational contact: sibo.lees@gmail.com)',
     'Accept-Encoding':'gzip'}
REST={'山西':'Q46913','内蒙古':'Q41079','广东':'Q15175','甘肃':'Q42392',
      '台湾':'Q22502','香港':'Q8646'}

def get(qid,tries=5):
    u=f'https://maps.wikimedia.org/geoshape?getgeojson=1&ids={qid}'
    last=None
    for k in range(tries):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers=UA2),timeout=120)
            raw=r.read()
            if r.headers.get('Content-Encoding')=='gzip':
                raw=gzip.decompress(raw)
            return json.loads(raw)
        except Exception as e:
            last=e; time.sleep(2*(k+1))
    raise last

add=[]
for name,qid in REST.items():
    try:
        d=get(qid); rings=[]
        for f in d.get('features',[]): rings+=rings_of(f['geometry'])
        if not rings: raise ValueError('no rings')
        rings.sort(key=area,reverse=True)
        keep=[r for r in rings[:6] if area(r)>=area(rings[0])*0.01]
        eps=0.012 if name in ('香港','台湾') else 0.08
        simp=[]
        for r in keep:
            pts=[[round(x,2),round(y,2)] for x,y in dp([tuple(p) for p in r],eps)]
            if len(pts)>=4: simp.append(pts)
        if not simp: raise ValueError('simplified away')
        add.append({'n':name,'r':simp})
        print(f'{name:<5} 环{len(simp)} 点{sum(len(r) for r in simp)}',flush=True)
    except Exception as e:
        print(f'{name:<5} ERR {type(e).__name__} {str(e)[:44]}',flush=True)

P='/Users/sli001/Desktop/艺术卡片-发布/provinces.js'
cur=json.loads(open(P,encoding='utf-8').read().split('const PROVINCES=',1)[1].rsplit(';\nwindow',1)[0])
have={o['n'] for o in cur}
cur+= [a for a in add if a['n'] not in have]
js='const PROVINCES='+json.dumps(cur,ensure_ascii=False,separators=(',',':'))+';\nwindow.PROVINCES=PROVINCES;\n'
open(P,'w',encoding='utf-8').write(js)
print('provinces.js 现有',len(cur),'个省级区 |',len(js)//1024,'KB')
