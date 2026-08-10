# -*- coding: utf-8 -*-
"""书封第二轮:Open Library 的 q= 把书名和作者混在一起搜命中率低,
   改成 title= / author= 分开传,先精确后放宽。

用法: python3 grabcov2.py <清单.json> <输出.json>
清单格式: [[id,"English Title","Author"], ...]
"""
import json,io,sys,time,urllib.parse,urllib.request
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
UA={'User-Agent':'art-cards/1.0 (educational contact: sibo.lees@gmail.com)'}
REPO='/Users/sli001/Desktop/艺术卡片-发布'

def ol(tries=3,**kw):
    kw.setdefault('limit','6'); kw.setdefault('fields','title,author_name,cover_i')
    u='https://openlibrary.org/search.json?'+urllib.parse.urlencode(kw)
    for k in range(tries):
        try:
            d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40))
            return [x for x in d.get('docs',[]) if x.get('cover_i')]
        except Exception:
            time.sleep(1.5*(k+1))
    return []

def save(cid,i):
    u=f'https://covers.openlibrary.org/b/id/{cid}-L.jpg'
    raw=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40).read()
    im=Image.open(io.BytesIO(raw)).convert('RGB')
    if min(im.size)<180: raise ValueError('placeholder')   # OL 缺封面时返回 1x1 或小占位
    if max(im.size)>1100:
        s=1100/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
    im.save(f'{REPO}/imgs/{i}.webp','WEBP',quality=84)
    return im.size

def main():
    got=[];miss=[]
    for row in json.load(open(sys.argv[1])):
        i,title=row[0],row[1]; author=row[2] if len(row)>2 else ''
        cands=[]
        if author: cands=ol(title=title,author=author)
        if not cands: cands=ol(title=title)
        if not cands: cands=ol(q=f'{title} {author}'.strip())
        done=False
        for d in cands:
            try:
                sz=save(d['cover_i'],i)
                got.append([i,title,d.get('title','')[:46],d['cover_i'],list(sz)]); done=True; break
            except Exception: pass
        if not done: miss.append([i,title,author])
        print(f'{i}\t{"OK" if done else "--"}\t{title[:40]}',flush=True)
    json.dump({'got':got,'miss':miss},open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
    print('抓到',len(got),'/',len(got)+len(miss))

if __name__=='__main__': main()
