# -*- coding: utf-8 -*-
"""按作品名点名抓图——分类通道对古代题材几乎全是游客现场照,这条通道命中率高得多。

用法:  python3 named.py <清单.json> <起始id> <输出pick.json>
清单格式: [["中文名","commons search keywords"], ...]

起始 id 一律先跑 nextid.py 取,不要凭记忆接号。
"""
import json,io,sys
from PIL import Image
from findfile import search,url_of
from fetchimg import fetch

REPO='/Users/sli001/Desktop/艺术卡片-发布'

def grab(works,nid,outfile,minside=420):
    out=[]
    for zh,q in works:
        got=False
        # Commons 的 search 是 AND 语义,词一多就 0 命中——逐级砍短再试
        w=q.split(); cands=[]
        for k in (len(w),4,3,2):
            if k>len(w): continue
            cands=search(' '.join(w[:k]),8)
            if cands: break
        for t in cands:
            if got: break
            try:
                d=fetch(url_of(t))
                im=Image.open(io.BytesIO(d)).convert('RGB')
                if min(im.size)<minside: continue
                if max(im.size)>1300:
                    s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
                im.save(f'{REPO}/imgs/{nid}.webp','WEBP',quality=84)
                out.append({'id':nid,'zh':zh,'file':t}); nid+=1; got=True
            except Exception:
                pass
        print(f'{zh:<16} {"OK" if got else "--"}',flush=True)
    json.dump(out,open(outfile,'w'),ensure_ascii=False,indent=1)
    print('抓到:',len(out),'/',len(works))
    return out

if __name__=='__main__':
    works=json.load(open(sys.argv[1]))
    grab(works,int(sys.argv[2]),sys.argv[3])
