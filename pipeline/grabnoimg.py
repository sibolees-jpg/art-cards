# -*- coding: utf-8 -*-
"""给已有文案但缺图的卡补图。图直接写到该卡自己的 id,不新编号。
   抓完必须拼图肉眼核对是不是同一件——自动搜索选错件的概率不低。"""
import json,io,sys
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
from findfile import search,url_of
from fetchimg import fetch
REPO='/Users/sli001/Desktop/艺术卡片-发布'
got=[];miss=[]
for i,zh,q in json.load(open('list_noimg.json')):
    done=False
    w=q.split(); cands=[]
    for k in (len(w),4,3,2):
        if k>len(w): continue
        cands=search(' '.join(w[:k]),8)
        if cands: break
    for t in cands:
        if done: break
        try:
            im=Image.open(io.BytesIO(fetch(url_of(t,1800)))).convert('RGB')
            if min(im.size)<400: continue
            ww,hh=im.size; ar=ww/hh
            if ar>2.6:
                cw=int(hh*1.4); x0=max(0,(ww-cw)//2); im=im.crop((x0,0,min(ww,x0+cw),hh))
            elif ar<0.36:
                ch=int(ww*1.4); y0=int(hh*0.05); im=im.crop((0,y0,ww,min(hh,y0+ch)))
            if max(im.size)>1300:
                s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
            im.save(f'{REPO}/imgs/{i}.webp','WEBP',quality=84)
            got.append([i,zh,t]); done=True
        except Exception: pass
    if not done: miss.append([i,zh])
    print(f'{i}\t{"OK" if done else "--"}\t{zh}',flush=True)
json.dump({'got':got,'miss':miss},open('noimg_result.json','w'),ensure_ascii=False,indent=1)
print('抓到',len(got),'/',len(got)+len(miss))
