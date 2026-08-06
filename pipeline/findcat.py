#!/usr/bin/env python3
"""搜索 Commons 分类名(别再猜了)"""
import json,sys,urllib.parse,urllib.request,time
UA='ArtCards/3.0 (educational)'
def search_cat(q,n=4):
    u=('https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search'
       '&srnamespace=14&srlimit=%d&srsearch=%s'%(n,urllib.parse.quote(q)))
    try:
        d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=40))
        return [r['title'] for r in d.get('query',{}).get('search',[])]
    except Exception: return []
if __name__=='__main__':
    for q in sys.argv[1:]:
        print(q,'→',search_cat(q))
        time.sleep(0.6)
