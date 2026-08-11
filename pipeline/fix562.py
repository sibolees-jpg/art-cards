import io,sys
sys.path.insert(0,'.')
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
from findfile import url_of,search
from fetchimg import fetch
REPO='/Users/sli001/Desktop/艺术卡片-发布'
cands=['File:Songhuizong10.jpg','File:Songhuizong8.jpg']+search('Emperor Huizong slender gold calligraphy',6)
for t in cands:
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
        im.save('/tmp/c562.webp','WEBP',quality=84)
        print('OK',im.size,t[5:60],flush=True)
    except Exception as e: print('--',t[5:40],type(e).__name__,flush=True)
