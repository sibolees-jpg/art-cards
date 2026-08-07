# -*- coding: utf-8 -*-
"""修长卷/立轴:按整幅比例缩到卡片里,内容会被压成一条几乎不可读。
   重抓原图,裁出有代表性的一段,写回同一个 id 的图片文件。
   卡片文案里的 more 需另行补「此为局部」——bake 不会自动加。"""
import json,io,sys
from PIL import Image
from findfile import search,url_of
from fetchimg import fetch

REPO='/Users/sli001/Desktop/艺术卡片-发布'

# id -> Commons 搜索词。中文作品名在 Commons 上基本搜不到,一律用英文/罗马字。
Q={
 247:'Nymph of the Luo River Gu Kaizhi',
 248:'Bunian Tu Yan Liben emperor',
 251:'Yan Zhenqing Requiem nephew manuscript',
 562:'Emperor Huizong Thousand Character Classic slender gold',
 563:'Zhao Mengfu Autumn Colors Que Hua',
 565:'Court Ladies Adorning Hair Flowers Zhou Fang',
 1356:'Mi Youren Marvelous Views Xiao Xiang',
 1359:'Wang Xun Boyuan letter calligraphy',
 1360:'Wang Xianzhi Mid-Autumn calligraphy',
 1365:'Wu Daozi Devas Sakyamuni handscroll',
 2012:'Li Tang Boyi Shuqi picking ferns',
 2054:'Hu Gui Zhuoxie tu nomads',
 4500:'Zhao Mengfu Elegant Rocks Sparse Trees',
 4501:'Qian Xuan Dwelling Floating Jade Mountains',
 4508:'Wang Meng Taibai Mountain',
 5200:'Li Cheng Luxuriant Forest Distant Peaks',
 5307:'Wang Shen Fishing boats snowy river',
 5317:'Wen Zhengming Zhenshang Zhai studio',
 903:'Zheng Xie ink bamboo hanging scroll',
 1398:'Wang Meng Qingbian Mountains dwelling',
 1532:'Wei Xian Noble Scholar hermit',
 4540:'Wu Changshuo wisteria hanging scroll',
 5116:'Wu Changshuo peaches painting',
 5117:'Yun Shouping peony painting',
 5121:'Stone inscription Mount Tai Li Si seal script',
 5313:'Wang Meng Summer Mountain Dwelling',
}

def crop_piece(im):
    """超宽取中段、超高取中上段,裁成接近 4:3 / 3:4,让内容在卡面上看得清。"""
    w,h=im.size; ar=w/h
    if ar>2.0:
        cw=int(h*1.35); x0=max(0,(w-cw)//2)
        return im.crop((x0,0,min(w,x0+cw),h))
    if ar<0.5:
        ch=int(w*1.35); y0=int(h*0.06)      # 立轴主体多在上部,题跋在下
        return im.crop((0,y0,w,min(h,y0+ch)))
    return im

def main():
    ok=[];miss=[]
    for i,q in Q.items():
        done=False
        w=q.split(); cands=[]
        for k in (len(w),4,3,2):
            if k>len(w): continue
            cands=search(' '.join(w[:k]),8)
            if cands: break
        for t in cands:
            if done: break
            try:
                im=Image.open(io.BytesIO(fetch(url_of(t,2400)))).convert('RGB')
                if max(im.size)<1200: continue          # 原图不够大,裁完更糊
                im=crop_piece(im)
                if min(im.size)<380: continue
                if max(im.size)>1300:
                    s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
                im.save(f'{REPO}/imgs/{i}.webp','WEBP',quality=84)
                ok.append((i,t)); done=True
            except Exception:
                pass
        if not done: miss.append(i)
        print(f'{i}\t{"OK" if done else "--"}\t{q}',flush=True)
    json.dump({'ok':ok,'miss':miss},open('fixlong_result.json','w'),ensure_ascii=False,indent=1)
    print('修好',len(ok),'| 未修',miss)

if __name__=='__main__': main()
