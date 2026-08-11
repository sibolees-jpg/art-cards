import io,sys
sys.path.insert(0,'.')
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
from findfile import url_of,search
from fetchimg import fetch
REPO='/Users/sli001/Desktop/艺术卡片-发布'
F={1226:['File:韩滉五牛图卷.png','File:Five Oxen.jpg'],
   1227:['File:搗練圖.jpg']+search('Zhang Xuan silk',6)+search('Daolian tu',4)}
for i,cands in F.items():
    done=False
    for t in cands:
        if done: break
        try:
            im=Image.open(io.BytesIO(fetch(url_of(t,2000)))).convert('RGB')
            w,h=im.size
            if w/h>2.0:
                cw=int(h*1.35); x0=int(w*0.15)
                if x0+cw>w: x0=max(0,w-cw)
                im=im.crop((x0,0,min(w,x0+cw),h))
            if min(im.size)<380:
                s=480/min(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
            if max(im.size)>1300:
                s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
            im.save(f'{REPO}/imgs/{i}.webp','WEBP',quality=84)
            print(i,'OK',im.size,t[5:46],flush=True); done=True
        except Exception: pass
    if not done: print(i,'--失败',flush=True)
