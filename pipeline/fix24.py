# -*- coding: utf-8 -*-
"""修 id>=6000 里 24 张几何异常的图:超宽长卷/超高立轴取画心局部,过小的重抓大图。

注意有些作品的真实比例就是极扁——荷尔拜因《墓中基督》原作 30.5x200cm、
屏风、手卷都是。对这些裁局部是为了卡面看得清,不是纠正比例,more 要注明。
"""
import json,io,os,sys
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
from findfile import search,url_of
from fetchimg import fetch

REPO='/Users/sli001/Desktop/艺术卡片-发布'

# id: (是否需要裁局部, 搜索词)  —— 中国古画一律用中文名,英文命中率太低
W={
 6367:(1,'Holbein Dead Christ Tomb Basel'),
 6564:(0,'Vrubel Demon Downcast'),
 6628:(1,'伊藤若冲 象と鯨図屏風'),
 6631:(1,'円山応挙 幽霊図'),
 8121:(1,'Van der Helst Banquet Civic Guard'),
 8593:(0,'Giovanni Fattori La Rotonda Palmieri'),
 8596:(0,'Giovanni Fattori Maremma herdsmen cattle'),
 8626:(1,'Fortuny Battle Tetuan'),
 8956:(1,'Max Klinger Die Blutezeit Griechenlands'),
 9340:(1,'Heemskerck Adam Eve painting'),
 9550:(1,'仇英 漢宮春曉圖'),
 9565:(1,'恽寿平 王翚 山水卷'),
 9596:(0,'夏圭 溪山清遠圖'),
 9598:(1,'张择端 清明易简图'),
 9600:(1,'李唐 濠梁秋水圖'),
 9605:(1,'牧谿 漁村夕照'),
 9606:(1,'牧谿 瀟湘八景'),
 9612:(0,'赵佶 夏景山水'),
 9614:(1,'赵孟頫 人騎圖'),
 9621:(0,'马远 风雨山水'),
 9627:(1,'顾恺之 列女仁智圖'),
 10314:(0,'Henri met de Bles landscape parable sower'),
 10529:(0,'Maki Four World Trade Center'),
 10697:(0,'Emil Nolde Abschied painting'),
}

def crop(im,do):
    w,h=im.size; ar=w/h
    if not do: return im
    if ar>2.0:
        cw=int(h*1.35); x0=int(w*0.18)          # 长卷画心多在卷首之后、题跋之前
        if x0+cw>w: x0=max(0,w-cw)
        return im.crop((x0,0,min(w,x0+cw),h))
    if ar<0.5:
        ch=int(w*1.35); y0=max(0,(h-ch)//2)
        return im.crop((0,y0,w,min(h,y0+ch)))
    return im

def main():
    got=[];miss=[]
    for i,(docrop,q) in W.items():
        cur=0
        p=f'{REPO}/imgs/{i}.webp'
        if os.path.exists(p):
            ww,hh=Image.open(p).size; cur=ww*hh
        done=False
        ws=q.split(); cands=[]
        for k in (len(ws),4,3,2):
            if k>len(ws): continue
            cands=search(' '.join(ws[:k]),8)
            if cands: break
        for t in cands:
            if done: break
            try:
                im=Image.open(io.BytesIO(fetch(url_of(t,2000)))).convert('RGB')
                im=crop(im,docrop)
                if min(im.size)<380: continue
                if max(im.size)>1300:
                    s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
                if im.size[0]*im.size[1] <= cur*1.05: continue   # 没比原图更好就不换
                im.save(p,'WEBP',quality=84)
                got.append([i,t,list(im.size)]); done=True
            except Exception: pass
        if not done: miss.append(i)
        print(f'{i}\t{"OK" if done else "--"}\t{q}',flush=True)
    json.dump({'got':got,'miss':miss},open('fix24_result.json','w'),ensure_ascii=False,indent=1)
    print('修好',len(got),'| 未修',miss)

if __name__=='__main__': main()
