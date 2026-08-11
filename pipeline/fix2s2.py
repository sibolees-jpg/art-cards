import io,sys
sys.path.insert(0,'.')
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
from findfile import url_of
from fetchimg import fetch
REPO='/Users/sli001/Desktop/艺术卡片-发布'
# 题跋在卷首,画心得往后取;英文名版多是画心裁好的
JOBS=[(1226,'File:Five Oxen.jpg',0.55),(1227,'File:Court Ladies Preparing Newly Woven Silk.jpg',0.45)]
for i,t,frac in JOBS:
    try:
        im=Image.open(io.BytesIO(fetch(url_of(t,2200)))).convert('RGB')
        w,h=im.size
        if w/h>2.0:
            cw=int(h*1.35); x0=int(w*frac)
            if x0+cw>w: x0=max(0,w-cw)
            im=im.crop((x0,0,min(w,x0+cw),h))
        if min(im.size)<380:
            s=480/min(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
        if max(im.size)>1300:
            s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
        im.save(f'{REPO}/imgs/{i}.webp','WEBP',quality=84)
        print(i,'OK',im.size,flush=True)
    except Exception as e: print(i,'--',type(e).__name__,flush=True)
