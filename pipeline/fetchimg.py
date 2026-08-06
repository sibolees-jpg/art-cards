# -*- coding: utf-8 -*-
"""Commons 取图的公用函数。抽出来是因为 cndl.py 顶层就是下载循环,import 会误触发。"""
import urllib.request,urllib.parse,http.client
UA={'User-Agent':'art-cards/1.0 (educational contact: sibo.lees@gmail.com)'}

def fetch(url,tries=3):
    """Commons 大图常在末尾几 KB 处断流(IncompleteRead),截断的 JPEG 其实能用;
       URL 里的非 ASCII 字符必须先 quote,否则 urllib 抛 UnicodeEncodeError。
       这两个坑之前每批都在悄悄吞素材(中国批 478 件只下来 141)。"""
    p=urllib.parse.urlsplit(url)
    url=urllib.parse.urlunsplit((p.scheme,p.netloc,urllib.parse.quote(p.path),
                                 urllib.parse.quote(p.query,safe='=&'),''))
    last=None
    for _ in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=90).read()
        except http.client.IncompleteRead as e:
            if len(e.partial)>60000: return e.partial   # 够解码就用残缺数据
            last=e
        except Exception as e:
            last=e
    raise last
