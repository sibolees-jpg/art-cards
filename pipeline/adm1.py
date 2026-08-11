# -*- coding: utf-8 -*-
"""抓各国一级行政区(州/省/大区)边界,写成 admin1.js。

省份那套只做了中国,这里推广到其余有藏品的国家。
QID 用 Wikidata SPARQL 一次查出(P150 = contains administrative territorial entity),
边界仍走 Wikimedia geoshape。区划数量是中国的十倍,所以简化阈值放大、只留主环,
否则 JS 体积会拖慢首屏。
"""
import json,gzip,math,sys,time,urllib.parse,urllib.request

UA={'User-Agent':'art-cards/1.0 (educational contact: sibo.lees@gmail.com)'}
UAZ=dict(UA); UAZ['Accept-Encoding']='gzip'

# 国家中文名 -> (Wikidata QID, 一级行政区的类型 QID)
COUNTRIES={
 '美国':('Q30','Q35657'),          # state of the United States
 '德国':('Q183','Q1221156'),       # state of Germany
 '法国':('Q142','Q36784'),         # region of France
 '英国':('Q145','Q3336843'),       # constituent country of the UK
 '意大利':('Q38','Q16110'),        # region of Italy
 '瑞士':('Q39','Q23058'),          # canton of Switzerland
 '日本':('Q17','Q50337'),          # prefecture of Japan
 '荷兰':('Q55','Q134390'),         # province of the Netherlands
 '西班牙':('Q29','Q10742'),        # autonomous community
 '印度':('Q668','Q131541'),        # state of India
 '澳大利亚':('Q408','Q5852411'),   # state of Australia
 '加拿大':('Q16','Q11828004'),     # province of Canada
 '巴西':('Q155','Q485258'),        # state of Brazil
 '波兰':('Q36','Q150093'),         # voivodeship
 '比利时':('Q31','Q208500'),        # province of Belgium
 '丹麦':('Q35','Q1970725'),        # region of Denmark
 '挪威':('Q20','Q192287'),         # county of Norway
 '伊朗':('Q794','Q127602'),        # province of Iran
 '俄罗斯':('Q159','Q41162'),       # federal subject
 '墨西哥':('Q96','Q1080418'),      # state of Mexico
}

def sparql(q,tries=4):
    u='https://query.wikidata.org/sparql?'+urllib.parse.urlencode({'query':q,'format':'json'})
    last=None
    for k in range(tries):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers=UAZ),timeout=90)
            raw=r.read()
            if r.headers.get('Content-Encoding')=='gzip': raw=gzip.decompress(raw)
            return json.loads(raw)['results']['bindings']
        except Exception as e:
            last=e; time.sleep(3*(k+1))
    raise last

def adm1_of(country_qid,type_qid=None):
    """优先按类型查(结果更干净);类型 QID 猜不准的国家退回 P150 反查下辖行政区。
       丹麦/挪威/比利时按类型查都返回 0,就是这么发现的。"""
    if type_qid:
        rows=sparql(f'''SELECT ?x ?xLabel WHERE {{
  ?x wdt:P31 wd:{type_qid}; wdt:P17 wd:{country_qid}.
  FILTER NOT EXISTS {{ ?x wdt:P576 ?end }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "zh,en". }} }}''')
        if rows:
            return [(r['x']['value'].rsplit('/',1)[-1], r['xLabel']['value']) for r in rows]
    rows=sparql(f'''SELECT ?x ?xLabel WHERE {{
  wd:{country_qid} wdt:P150 ?x .
  FILTER NOT EXISTS {{ ?x wdt:P576 ?e }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "zh,en". }} }}''')
    return [(r['x']['value'].rsplit('/',1)[-1], r['xLabel']['value']) for r in rows]

def geoshape(qid,tries=4):
    u=f'https://maps.wikimedia.org/geoshape?getgeojson=1&ids={qid}'
    last=None
    for k in range(tries):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers=UAZ),timeout=120)
            raw=r.read()
            if r.headers.get('Content-Encoding')=='gzip': raw=gzip.decompress(raw)
            return json.loads(raw)
        except Exception as e:
            last=e; time.sleep(2*(k+1))
    raise last

def perp(p,a,b):
    (x,y),(x1,y1),(x2,y2)=p,a,b
    dx,dy=x2-x1,y2-y1
    if dx==0 and dy==0: return math.hypot(x-x1,y-y1)
    t=max(0,min(1,((x-x1)*dx+(y-y1)*dy)/(dx*dx+dy*dy)))
    return math.hypot(x-(x1+t*dx), y-(y1+t*dy))

def dp(pts,eps):
    if len(pts)<3: return pts
    dmax,idx=0,0
    for i in range(1,len(pts)-1):
        d=perp(pts[i],pts[0],pts[-1])
        if d>dmax: dmax,idx=d,i
    if dmax>eps: return dp(pts[:idx+1],eps)[:-1]+dp(pts[idx:],eps)
    return [pts[0],pts[-1]]

def rings_of(g):
    t,c=g['type'],g['coordinates']
    if t=='Polygon': return [c[0]]
    if t=='MultiPolygon': return [p[0] for p in c]
    return []

def area(r):
    s=0
    for i in range(len(r)):
        x1,y1=r[i]; x2,y2=r[(i+1)%len(r)]
        s+=x1*y2-x2*y1
    return abs(s)/2

def main():
    sys.setrecursionlimit(30000)
    only=sys.argv[1:] or list(COUNTRIES)
    out={}
    P='/Users/sli001/Desktop/艺术卡片-发布/pipeline/admin1_raw.json'
    try: out=json.load(open(P))
    except Exception: pass
    for cn in only:
        if cn in out: print(f'{cn} 已有 {len(out[cn])} 个,跳过'); continue
        cq,tq=COUNTRIES[cn]
        try: units=adm1_of(cq,tq)
        except Exception as e:
            print(f'{cn} SPARQL 失败 {type(e).__name__}'); continue
        print(f'== {cn}: {len(units)} 个一级行政区',flush=True)
        got=[]
        for qid,name in units:
            try:
                d=geoshape(qid); rings=[]
                for f in d.get('features',[]): rings+=rings_of(f['geometry'])
                if not rings: raise ValueError('no rings')
                rings.sort(key=area,reverse=True)
                keep=[r for r in rings[:3] if area(r)>=area(rings[0])*0.05]
                simp=[]
                for r in keep:
                    pts=[[round(x,2),round(y,2)] for x,y in dp([tuple(p) for p in r],0.12)]
                    if len(pts)>=4: simp.append(pts)
                if not simp: raise ValueError('too small')
                got.append({'n':name,'r':simp})
            except Exception as e:
                print(f'   {name} -- {type(e).__name__}',flush=True)
        out[cn]=got
        print(f'{cn} 抓到 {len(got)}/{len(units)}',flush=True)
        json.dump(out,open(P,'w'),ensure_ascii=False)
    print('合计',sum(len(v) for v in out.values()),'个区划')

if __name__=='__main__': main()
