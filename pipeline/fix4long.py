# -*- coding: utf-8 -*-
"""再修 4 张漏网的超扁长卷。《自叙帖》1280x26 是全库最扁的一张,几乎只剩一条线。"""
import io,sys
sys.path.insert(0,'.'); sys.setrecursionlimit(20000)
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
from findfile import url_of,search
from fetchimg import fetch
REPO='/Users/sli001/Desktop/艺术卡片-发布'
F={561:['File:唐懷素自敘帖 卷.png','File:Huaisu - Autobiography.jpg'],
   562:['File:Songhuizong9.jpg'],
   563:['File:Zhao Mengfu-Autumn Colors on the Que and Hua Mountains.jpg','File:鵲華秋色圖.jpg'],
   566:['File:Li Gonglin-Five Horses.jpg','File:五马图.jpg']}
# 搜不到的用关键词兜底
Q={563:'Autumn Colors Que Hua Mountains',566:'Five Horses Li Gonglin'}
for i,cands in F.items():
    if i in Q: cands=cands+search(Q[i],6)
    done=False
    for t in cands:
        if done: break
        try:
            im=Image.open(io.BytesIO(fetch(url_of(t,2000)))).convert('RGB')
            w,h=im.size
            if w/h>2.0:
                cw=int(h*1.35); x0=int(w*0.18)
                if x0+cw>w: x0=max(0,w-cw)
                im=im.crop((x0,0,min(w,x0+cw),h))
            if min(im.size)<380:
                s=480/min(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
            if max(im.size)>1300:
                s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
            im.save(f'{REPO}/imgs/{i}.webp','WEBP',quality=84)
            print(i,'OK',im.size,t[5:50],flush=True); done=True
        except Exception as e: pass
    if not done: print(i,'--失败',flush=True)
