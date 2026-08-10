# -*- coding: utf-8 -*-
"""按英文书名从 Open Library 抓封面。中文书名在 OL 上几乎搜不到,必须走英译名。
   用法: python3 grabcov.py book_en1.json out1.json"""
import json,io,sys,urllib.request
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
sys.path.insert(0,'.')
from bookcov import search_ol,cover
UA={'User-Agent':'art-cards/1.0 (educational contact: sibo.lees@gmail.com)'}
REPO='/Users/sli001/Desktop/艺术卡片-发布'

got=[];miss=[]
for i,q in json.load(open(sys.argv[1])):
    done=False
    for d in search_ol(q):
        if done or not d.get('cover_i'): continue
        try:
            raw=urllib.request.urlopen(urllib.request.Request(cover(d['cover_i']),headers=UA),timeout=40).read()
            im=Image.open(io.BytesIO(raw)).convert('RGB')
            if min(im.size)<180: continue          # OL 的占位图很小
            if max(im.size)>1100:
                s=1100/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
            im.save(f'{REPO}/imgs/{i}.webp','WEBP',quality=84)
            got.append([i,q,d.get('title','')[:50],d['cover_i']]); done=True
        except Exception: pass
    if not done: miss.append([i,q])
    print(f'{i}\t{"OK" if done else "--"}\t{q[:44]}',flush=True)
json.dump({'got':got,'miss':miss},open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
print('抓到',len(got),'/',len(got)+len(miss))
