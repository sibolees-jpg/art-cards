# -*- coding: utf-8 -*-
"""手工指定文件与裁切位置的长卷修复——自动选段挑不准的那几张走这条。

「画意分」会被宣纸的米黄底色骗到:题跋纸底饱和度也高,所以《兰亭修禊图》
《秋郊饮马图》都挑中了题字段。这几张只能看图定位置。
"""
import io,json,sys
sys.path.insert(0,'.')
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
from findfile import url_of
from fetchimg import fetch

REPO='/Users/sli001/Desktop/艺术卡片-发布'
# id: (Commons 文件, 取段位置)
JOBS={
 5319:('File:文徵明兰亭修褉图卷.png',0.02),
 1575:('File:Zhao Mengfu. Horse Herding in Autumn Countryside 1312 23,6х59см, Palace Museum, Beijing.jpg',0.92),
 1359:('File:The Calligraphy Model Boyuan by Wang Xun.jpg',0.02),
}

def main():
    done=json.load(open('scrolls_done.json'))
    for i,(f,fr) in JOBS.items():
        try:
            im=Image.open(io.BytesIO(fetch(url_of(f,2200)))).convert('RGB')
            w,h=im.size
            if w/h>2.0:
                cw=int(h*1.35); x0=int(w*fr)
                if x0+cw>w: x0=max(0,w-cw)
                im=im.crop((x0,0,min(w,x0+cw),h))
            if min(im.size)<380:
                s=480/min(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
            if max(im.size)>1300:
                s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
            im.save(f'{REPO}/imgs/{i}.webp','WEBP',quality=84)
            done[str(i)]={'f':f,'frac':fr,'size':list(im.size),'manual':True}
            print(i,'OK',im.size,flush=True)
        except Exception as e:
            print(i,'--',type(e).__name__,str(e)[:40],flush=True)
    json.dump(done,open('scrolls_done.json','w'),ensure_ascii=False)

if __name__=='__main__': main()
