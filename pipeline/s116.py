import io
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
from findfile import search,url_of
from fetchimg import fetch
for t in search('Munch The Scream 1893',8):
    try:
        im=Image.open(io.BytesIO(fetch(url_of(t,1600)))).convert('RGB')
        if min(im.size)<500: continue
        if max(im.size)>1300:
            s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
        im.save('/Users/sli001/Desktop/艺术卡片-发布/imgs/116.webp','WEBP',quality=86)
        print('OK',im.size,t,flush=True); break
    except Exception as e: print('--',type(e).__name__,t[:40],flush=True)
