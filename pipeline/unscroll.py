# -*- coding: utf-8 -*-
"""回滚被误裁的 film/music 卡。
   长卷裁切逻辑只该用在中国手卷上——电影海报、专辑封面本来就是宽幅完整图,
   裁中段只会剩下标题的几个字母。"""
import io,json,sys
sys.path.insert(0,'.')
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
from findfile import url_of
from fetchimg import fetch
REPO='/Users/sli001/Desktop/艺术卡片-发布'
done=json.load(open('scrolls_done.json'))
meta={r[0]:r for r in json.load(open('/tmp/allimgs.json'))}
for k in list(done):
    i=int(k)
    if meta[i][3]=='art': continue
    f=done[k]['f']
    try:
        im=Image.open(io.BytesIO(fetch(url_of(f,1600)))).convert('RGB')   # 整幅,不裁
        if max(im.size)>1300:
            s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
        im.save(f'{REPO}/imgs/{i}.webp','WEBP',quality=84)
        print(i,meta[i][1],'整幅',im.size,flush=True)
        del done[k]
    except Exception as e: print(i,'--',type(e).__name__,flush=True)
json.dump(done,open('scrolls_done.json','w'),ensure_ascii=False)
