import io,sys
sys.path.insert(0,'.')
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
from findfile import url_of
from fetchimg import fetch
# 《五牛图》卷首是印章与题跋,画心要往后取七成才见牛
im=Image.open(io.BytesIO(fetch(url_of('File:Five Oxen.jpg',2200)))).convert('RGB')
w,h=im.size
cw=int(h*1.35); x0=int(w*0.72)
if x0+cw>w: x0=max(0,w-cw)
im=im.crop((x0,0,min(w,x0+cw),h))
if min(im.size)<380:
    s=480/min(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
if max(im.size)>1300:
    s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
im.save('/Users/sli001/Desktop/艺术卡片-发布/imgs/1226.webp','WEBP',quality=84)
print('1226 OK',im.size)
