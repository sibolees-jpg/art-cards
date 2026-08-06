#!/usr/bin/env python3
"""从 Commons 分类直抓图片(中国古画等 Wikidata 结构数据薄的门类用这条路)。
用法: python3 commons.py "Category:Paintings by Shen Zhou" out.json [上限]"""
import json,sys,urllib.parse,urllib.request,time
UA='ArtCards/3.0 (educational, non-commercial)'
def api(params):
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)
    for k in range(3):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=45))
        except Exception: time.sleep(3*(k+1))
    return {}
def _members(cat,typ):
    out=[];cont=None
    while True:
        p={'action':'query','format':'json','list':'categorymembers','cmtitle':cat,
           'cmtype':typ,'cmlimit':'100'}
        if cont: p['cmcontinue']=cont
        d=api(p)
        for m in d.get('query',{}).get('categorymembers',[]): out.append(m['title'])
        cont=d.get('continue',{}).get('cmcontinue')
        if not cont: break
    return out
def files_in(cat,limit=60,depth=2):
    """递归下探子分类——中国画的图常常埋在「作品名」子分类里"""
    seen=set(); out=[]; queue=[(cat,0)]
    while queue and len(out)<limit:
        c,d=queue.pop(0)
        if c in seen: continue
        seen.add(c)
        for f in _members(c,'file'):
            if f not in out: out.append(f)
            if len(out)>=limit: break
        if d<depth:
            for sub in _members(c,'subcat')[:12]: queue.append((sub,d+1))
    return out[:limit]
def info(titles):
    """批量取图片 URL 与尺寸"""
    res={}
    for i in range(0,len(titles),20):
        chunk=titles[i:i+20]
        d=api({'action':'query','format':'json','prop':'imageinfo',
               'iiprop':'url|size','iiurlwidth':'1400','titles':'|'.join(chunk)})
        for _,pg in d.get('query',{}).get('pages',{}).items():
            for ii in pg.get('imageinfo',[]):
                res[pg['title']]={'url':ii.get('thumburl') or ii.get('url'),
                                  'w':ii.get('width'),'h':ii.get('height')}
        time.sleep(0.5)
    return res
if __name__=='__main__':
    cat=sys.argv[1]; out=sys.argv[2]; lim=int(sys.argv[3]) if len(sys.argv)>3 else 40
    ts=files_in(cat,lim)
    inf=info(ts)
    rows=[{'title':t.replace('File:',''),**inf.get(t,{})} for t in ts if t in inf]
    json.dump(rows,open(out,'w'),ensure_ascii=False,indent=1)
    print(f'{cat} → {len(rows)} 件')
