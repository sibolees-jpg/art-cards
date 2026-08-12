# -*- coding: utf-8 -*-
"""长卷裁画心:在多个位置里自动挑最像「画」的一段。

固定取某个百分比总有一半落在题跋上。题跋是白纸黑字——饱和度低、色调集中;
画心有绢色、矿物色和灰阶层次。按这个差别打分选段,比猜位置靠谱。

书法作品(帖/序/赋/书谱/千字文)例外:那些本来就是字,取哪段都行。

  python3 scrolls2.py <id> [<id>...]
"""
import io,json,os,sys,re
sys.path.insert(0,'.')
from PIL import Image,ImageFile,ImageStat
ImageFile.LOAD_TRUNCATED_IMAGES=True
from findfile import search,url_of
from fetchimg import fetch

REPO='/Users/sli001/Desktop/艺术卡片-发布'
CALLIG=re.compile(r'帖|书谱|書譜|序$|赋|賦|千字文|自叙|自敘')

def painty(im):
    """越像画分越高:彩色像素占比 + 中间调占比。题跋是白底黑字,两项都低。"""
    s=im.convert('RGB').resize((80,80))
    px=list(s.getdata())
    col=sum(1 for r,g,b in px if max(r,g,b)-min(r,g,b)>28)
    mid=sum(1 for r,g,b in px if 60<(r+g+b)/3<205)
    return col/6400*1.4 + mid/6400

def crop_at(im,frac):
    w,h=im.size
    if w/h>2.0:
        cw=int(h*1.35); x0=int(w*frac)
        if x0+cw>w: x0=max(0,w-cw)
        return im.crop((x0,0,min(w,x0+cw),h))
    if w/h<0.5:
        ch=int(w*1.35); y0=max(0,int(h*frac)-ch//2)
        return im.crop((0,y0,w,min(h,y0+ch)))
    return im

def norm(im):
    if min(im.size)<380:
        s=480/min(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
    if max(im.size)>1300:
        s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
    return im

def main():
    ids=[int(x) for x in sys.argv[1:]]
    meta={r[0]:r for r in json.load(open('/tmp/allimgs.json'))}
    done={}
    try: done=json.load(open('scrolls_done.json'))
    except Exception: pass
    for i in ids:
        t=meta[i][1]; a=meta[i][2]
        src=done.get(str(i),{}).get('f')
        cands=[src] if src else (search(t,6) or search(f'{a} {t}',6))
        best=None
        for f in cands:
            if not f: continue
            try:
                im=Image.open(io.BytesIO(fetch(url_of(f,2200)))).convert('RGB')
                if max(im.size)<900: continue
                if CALLIG.search(t):
                    cand=[(1.0,0.45,norm(crop_at(im,0.45)))]
                else:
                    cand=[]
                    for fr in (0.12,0.28,0.45,0.62,0.78):
                        c=norm(crop_at(im,fr))
                        if min(c.size)<300: continue
                        cand.append((painty(c),fr,c))
                if not cand: continue
                cand.sort(key=lambda x:-x[0])
                sc,fr,c=cand[0]
                if best is None or sc>best[0]: best=(sc,fr,c,f)
            except Exception: pass
        if best:
            sc,fr,c,f=best
            c.save(f'{REPO}/imgs/{i}.webp','WEBP',quality=84)
            done[str(i)]={'f':f,'frac':fr,'size':list(c.size),'score':round(sc,3)}
            print(f'{i}\tOK\t{t[:14]}\tfrac={fr}\t画意分={sc:.2f}',flush=True)
        else:
            print(f'{i}\t--\t{t[:14]}',flush=True)
        json.dump(done,open('scrolls_done.json','w'),ensure_ascii=False)
    print('累计',len(done))

if __name__=='__main__': main()
