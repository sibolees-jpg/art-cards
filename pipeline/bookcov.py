# -*- coding: utf-8 -*-
"""书封走 Open Library:按书名+作者查 ISBN,再取封面。
   Commons 上没有现代书封(有版权),Open Library 的封面 API 是公开可用的。"""
import json,io,sys,urllib.parse,urllib.request
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
UA={'User-Agent':'art-cards/1.0 (educational contact: sibo.lees@gmail.com)'}

def search_ol(title,author='',tries=2):
    q={'q':f'{title} {author}'.strip(),'limit':'5','fields':'title,author_name,cover_i,isbn'}
    u='https://openlibrary.org/search.json?'+urllib.parse.urlencode(q)
    for _ in range(tries):
        try:
            d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))
            return d.get('docs',[])
        except Exception: pass
    return []

def cover(cid,size='L'):
    return f'https://covers.openlibrary.org/b/id/{cid}-{size}.jpg'

if __name__=='__main__':
    for t,a in [('Politics','Aristotle'),('Pride and Prejudice','Jane Austen'),
                ('The Story of Art','Gombrich'),('Being and Nothingness','Sartre')]:
        docs=search_ol(t,a)
        hit=[d for d in docs if d.get('cover_i')]
        print(f'{t:<28}', len(docs),'条 |', hit[0]['cover_i'] if hit else '无封面',
              '|', hit[0]['title'][:40] if hit else '')
