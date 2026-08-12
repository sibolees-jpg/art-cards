# -*- coding: utf-8 -*-
"""批量修压扁的长卷。

上一轮几何扫描按 imgs/{id}.webp 找文件,凡是 .jpg 的卡全被跳过——56 张漏网,
几乎全是中国长卷(最扁的《沧洲趣图》900x18,50:1)。

中文标题在 Commons 上对中国古画命中率远高于英文。裁切位置没有定规:
题跋可能在卷首也可能在卷尾,统一取中段,不对的再逐张调。

  python3 scrolls.py <起> <止>    # 处理 flat_all.json 里第 起~止 个
"""
import io,json,os,sys
sys.path.insert(0,'.')
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
from findfile import search,url_of
from fetchimg import fetch

REPO='/Users/sli001/Desktop/艺术卡片-发布'
FRAC=0.45          # 默认取中段偏前

def crop_at(im,frac):
    w,h=im.size
    if w/h>2.0:
        cw=int(h*1.35); x0=int(w*frac)
        if x0+cw>w: x0=max(0,w-cw)
        return im.crop((x0,0,min(w,x0+cw),h))
    if w/h<0.5:
        ch=int(w*1.35); y0=max(0,int(h*frac)-ch//2)
        return im.crop((0,y0,w,min(h,y0+ch)))
    return im

def norm(im):
    if min(im.size)<380:
        s=480/min(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
    if max(im.size)>1300:
        s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
    return im

def main():
    lo,hi=int(sys.argv[1]),int(sys.argv[2])
    ids=json.load(open('/tmp/flat_all.json'))[lo:hi]
    meta={r[0]:r for r in json.load(open('/tmp/allimgs.json'))}
    got={}
    try: got=json.load(open('scrolls_done.json'))
    except Exception: pass
    for i in ids:
        if str(i) in got: continue
        t=meta[i][1]; a=meta[i][2]
        cands=search(t,6) or search(f'{a} {t}',6)
        done=False
        for f in cands:
            if done: break
            try:
                im=Image.open(io.BytesIO(fetch(url_of(f,2200)))).convert('RGB')
                if max(im.size)<900: continue
                im2=norm(crop_at(im,FRAC))
                if min(im2.size)<300: continue
                im2.save(f'{REPO}/imgs/{i}.webp','WEBP',quality=84)
                got[str(i)]={'f':f,'frac':FRAC,'size':list(im2.size)}
                print(f'{i}\tOK\t{t[:14]}\t{f[5:44]}',flush=True); done=True
            except Exception: pass
        if not done: print(f'{i}\t--\t{t[:14]}',flush=True)
        json.dump(got,open('scrolls_done.json','w'),ensure_ascii=False)
    print('累计修好',len(got))

if __name__=='__main__': main()
