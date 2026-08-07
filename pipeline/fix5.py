import json,io
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
from findfile import url_of
from fetchimg import fetch
from fixlong import crop_piece
REPO='/Users/sli001/Desktop/艺术卡片-发布'
F={1532:'File:卫贤高士图卷.jpg',4540:'File:吴昌硕紫藤图轴.png',
   5116:'File:吴昌硕 桃实图轴.jpg',5313:'File:王蒙夏日山居图轴.jpg',903:'File:郑燮 墨竹轴.jpg'}
for i,t in F.items():
    try:
        im=Image.open(io.BytesIO(fetch(url_of(t,1800)))).convert('RGB')
        im=crop_piece(im)
        if min(im.size)<380:
            s=480/min(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
        if max(im.size)>1300:
            s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
        im.save(f'{REPO}/imgs/{i}.webp','WEBP',quality=84)
        print(i,'OK',im.size,flush=True)
    except Exception as e: print(i,'--',type(e).__name__,str(e)[:50],flush=True)
