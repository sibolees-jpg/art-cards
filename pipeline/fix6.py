# -*- coding: utf-8 -*-
"""长卷取「中段」会裁到题跋——中国长卷的画心多在卷首之后、卷尾题跋之前。
   改从左起 18% 处取段;立轴取正中(诗塘在最上,题款在最下)。"""
import io
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
from findfile import url_of
from fetchimg import fetch
REPO='/Users/sli001/Desktop/艺术卡片-发布'
F={2012:'File:李唐采薇图卷.png',4500:'File:赵孟頫秀石疏林图卷.png',
   1360:'File:王献之行草书中秋帖卷.png',1356:'File:米友仁潇湘奇观图卷.png',
   5307:'File:赵佶雪江归棹图卷.png',5313:'File:王蒙夏日山居图轴.jpg'}
for i,t in F.items():
    try:
        im=Image.open(io.BytesIO(fetch(url_of(t,1800)))).convert('RGB')
        w,h=im.size; ar=w/h
        if ar>2.0:
            cw=int(h*1.35); x0=int(w*0.18)
            if x0+cw>w: x0=max(0,w-cw)
            im=im.crop((x0,0,min(w,x0+cw),h))
        elif ar<0.5:
            ch=int(w*1.35); y0=max(0,(h-ch)//2)
            im=im.crop((0,y0,w,min(h,y0+ch)))
        if min(im.size)<380:
            s=480/min(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
        if max(im.size)>1300:
            s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
        im.save(f'{REPO}/imgs/{i}.webp','WEBP',quality=84)
        print(i,'OK',im.size,flush=True)
    except Exception as e: print(i,'--',type(e).__name__,str(e)[:40],flush=True)
