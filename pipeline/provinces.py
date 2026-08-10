# -*- coding: utf-8 -*-
"""抓中国 34 个省级行政区的边界,简化后写成 provinces.js。

数据源是 Wikimedia 的 geoshape 服务(按 Wikidata QID 取 GeoJSON)。
原始点数上千,卡片地图用不着那么细——用 Douglas-Peucker 简化到每省几十个点,
和 regions.js 的国家边界一个量级,不然 canvas 每帧重绘会卡。
"""
import json,io,math,urllib.request,http.client

UA={'User-Agent':'art-cards/1.0 (educational contact: sibo.lees@gmail.com)'}

QID={
 '北京':'Q956','天津':'Q11736','河北':'Q21208','山西':'Q46913','内蒙古':'Q41079',
 '辽宁':'Q43934','吉林':'Q45208','黑龙江':'Q19206','上海':'Q8686','江苏':'Q16963',
 '浙江':'Q16967','安徽':'Q40956','福建':'Q41705','江西':'Q57052','山东':'Q43407',
 '河南':'Q43684','湖北':'Q46862','湖南':'Q45761','广东':'Q15175','广西':'Q15176',
 '海南':'Q42200','重庆':'Q11725','四川':'Q19770','贵州':'Q47097','云南':'Q43194',
 '西藏':'Q17269','陕西':'Q47974','甘肃':'Q42392','青海':'Q45833','宁夏':'Q57448',
 '新疆':'Q34800','台湾':'Q57251','香港':'Q8646','澳门':'Q14773',
}

def fetch(url,tries=6):
    """JSON 不能像图片那样用残缺数据兜底——截断的 JSON 直接解析失败,只能重试。"""
    import time
    last=None
    for k in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=120).read()
        except Exception as e:
            last=e; time.sleep(1.5*(k+1))
    raise last

def perp(p,a,b):
    (x,y),(x1,y1),(x2,y2)=p,a,b
    dx,dy=x2-x1,y2-y1
    if dx==0 and dy==0: return math.hypot(x-x1,y-y1)
    t=max(0,min(1,((x-x1)*dx+(y-y1)*dy)/(dx*dx+dy*dy)))
    return math.hypot(x-(x1+t*dx), y-(y1+t*dy))

def dp(pts,eps):
    """Douglas-Peucker;递归版对上千点的环够用"""
    if len(pts)<3: return pts
    dmax,idx=0,0
    for i in range(1,len(pts)-1):
        d=perp(pts[i],pts[0],pts[-1])
        if d>dmax: dmax,idx=d,i
    if dmax>eps:
        return dp(pts[:idx+1],eps)[:-1]+dp(pts[idx:],eps)
    return [pts[0],pts[-1]]

def rings_of(geom):
    t=geom['type']; c=geom['coordinates']
    if t=='Polygon': return [c[0]]
    if t=='MultiPolygon': return [p[0] for p in c]
    return []

def area(ring):
    s=0
    for i in range(len(ring)):
        x1,y1=ring[i]; x2,y2=ring[(i+1)%len(ring)]
        s+=x1*y2-x2*y1
    return abs(s)/2

def main():
    out=[]
    SMALL={'澳门','香港','上海','北京','天津','海南','台湾'}
    for name,qid in QID.items():
        EPS=0.012 if name in SMALL else 0.08
        try:
            d=json.loads(fetch(f'https://maps.wikimedia.org/geoshape?getgeojson=1&ids={qid}'))
            rings=[]
            for f in d.get('features',[]):
                rings+=rings_of(f['geometry'])
            if not rings: raise ValueError('no rings')
            rings.sort(key=area,reverse=True)
            keep=[r for r in rings[:6] if area(r)>=area(rings[0])*0.01]  # 丢掉零碎小岛
            simp=[]
            for r in keep:
                pts=[[round(x,2),round(y,2)] for x,y in dp([tuple(p) for p in r],EPS)]
                if len(pts)>=4: simp.append(pts)
            if not simp: raise ValueError('simplified away')
            out.append({'n':name,'r':simp})
            print(f'{name:<5} 环{len(simp)} 点{sum(len(r) for r in simp)}',flush=True)
        except Exception as e:
            print(f'{name:<5} ERR {type(e).__name__} {str(e)[:40]}',flush=True)
    js='const PROVINCES='+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\nwindow.PROVINCES=PROVINCES;\n'
    open('/Users/sli001/Desktop/艺术卡片-发布/provinces.js','w',encoding='utf-8').write(js)
    print('写出 provinces.js |',len(out),'个省级区 |',len(js)//1024,'KB')

if __name__=='__main__': main()
