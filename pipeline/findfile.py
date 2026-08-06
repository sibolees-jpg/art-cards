"""按关键词在 Commons 搜文件名——比猜分类可靠得多。
   猜分类的老路对古罗马这类题材几乎全是游客现场照,这个通道按作品名直取。
   用法: python3 findfile.py "Laocoon Vatican" 5"""
import sys,json,time,urllib.request,urllib.parse
UA={'User-Agent':'art-cards/1.0 (educational contact: sibo.lees@gmail.com)'}

def search(q,n=6,tries=3):
    """Commons 的 search API 会偶发 RemoteDisconnected,一次失败不代表没结果。"""
    p={'action':'query','format':'json','list':'search','srsearch':f'filetype:bitmap {q}',
       'srnamespace':'6','srlimit':str(n)}
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(p)
    for i in range(tries):
        try:
            d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40))
            return [r['title'] for r in d.get('query',{}).get('search',[])]
        except Exception:
            if i==tries-1: return []
            time.sleep(2*(i+1))
    return []

def url_of(title,width=1600):
    return ('https://commons.wikimedia.org/wiki/Special:FilePath/'
            +title.replace('File:','').replace(' ','_')+f'?width={width}')

if __name__=='__main__':
    for t in search(sys.argv[1], int(sys.argv[2]) if len(sys.argv)>2 else 6): print(t)
