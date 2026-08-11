# -*- coding: utf-8 -*-
"""感知哈希查近似重复。

md5 只能抓到「同一个文件」,抓不到同一件作品的不同扫描/不同裁切——
那种图文件不同、内容几乎一样,照样是两张卡撞车。
这里用 aHash+dHash 组合(64+64 位),汉明距离小于阈值即判为近似。

用法: python3 phash.py [阈值]   默认 8
"""
import json,os,sys
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True

REPO='/Users/sli001/Desktop/艺术卡片-发布'

def ahash(im):
    g=im.convert('L').resize((8,8),Image.LANCZOS)
    px=list(g.getdata()); avg=sum(px)/64
    return sum(1<<i for i,v in enumerate(px) if v>avg)

def dhash(im):
    g=im.convert('L').resize((9,8),Image.LANCZOS)
    px=list(g.getdata()); bits=0; k=0
    for r in range(8):
        for c in range(8):
            if px[r*9+c]>px[r*9+c+1]: bits|=1<<k
            k+=1
    return bits

def main():
    thr=int(sys.argv[1]) if len(sys.argv)>1 else 8
    fmap=json.load(open('/tmp/fm5.json'))     # 文件名 -> [id,kind,标题]
    sigs=[]
    for f in fmap:
        p=os.path.join(REPO,'imgs',f)
        if not os.path.exists(p): continue
        try:
            im=Image.open(p)
            sigs.append((f,ahash(im),dhash(im)))
        except Exception: pass
    print('已算指纹',len(sigs))

    # 按 aHash 高 16 位分桶,只在桶内两两比,避免 N^2
    buckets={}
    for f,a,d in sigs:
        for shift in (0,16,32,48):
            buckets.setdefault((shift,(a>>shift)&0xFFFF),[]).append((f,a,d))
    seen=set(); pairs=[]
    for key,items in buckets.items():
        if len(items)>60: continue           # 纯色图会挤在一个桶里,跳过
        for i in range(len(items)):
            for j in range(i+1,len(items)):
                f1,a1,d1=items[i]; f2,a2,d2=items[j]
                k=(f1,f2) if f1<f2 else (f2,f1)
                if k in seen: continue
                seen.add(k)
                dist=bin(a1^a2).count('1')+bin(d1^d2).count('1')
                if dist<=thr: pairs.append((dist,f1,f2))
    pairs.sort()
    print(f'近似对(阈值{thr}):',len(pairs))
    out=[]
    for dist,f1,f2 in pairs:
        c1,c2=fmap[f1],fmap[f2]
        out.append({'d':dist,'a':c1,'b':c2,'fa':f1,'fb':f2})
    json.dump(out,open('phash_pairs.json','w'),ensure_ascii=False,indent=1)
    for r in out[:30]:
        print(f"  d={r['d']:<3} {r['a'][1]}#{r['a'][0]} 「{r['a'][2][:14]}」  ≈  {r['b'][1]}#{r['b'][0]} 「{r['b'][2][:14]}」")

if __name__=='__main__': main()
