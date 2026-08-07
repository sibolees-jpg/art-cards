# -*- coding: utf-8 -*-
"""整卷扫描里题跋常比画心长,裁哪一段都可能落在字上。
   改用博物馆发布的画心版(英文名文件多为画心或 detail)。"""
import io
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
from findfile import url_of
from fetchimg import fetch
REPO='/Users/sli001/Desktop/艺术卡片-发布'
F={2012:'File:Li Tang-Boyi and Shuqi.jpg',
   4500:'File:Zhao Meng Fu Elegant Rocks and Sparse Trees.jpg',
   1360:'File:The Calligraphy Model Mid-Autumn by Wang Xianzhi.jpg',
   1356:'File:Mi Youren. The Spectacular Views of the Xiao and Xiang Rivers. detail.jpg',
   5307:'File:Wang Shen. Fishing Boats by a Snowy Bank. (detail).jpg'}
for i,t in F.items():
    try:
        im=Image.open(io.BytesIO(fetch(url_of(t,1800)))).convert('RGB')
        w,h=im.size; ar=w/h
        if ar>2.0:
            cw=int(h*1.35); x0=max(0,(w-cw)//2); im=im.crop((x0,0,min(w,x0+cw),h))
        if min(im.size)<380:
            s=480/min(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
        if max(im.size)>1300:
            s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
        im.save(f'{REPO}/imgs/{i}.webp','WEBP',quality=84)
        print(i,'OK',im.size,flush=True)
    except Exception as e: print(i,'--',type(e).__name__,str(e)[:40],flush=True)
