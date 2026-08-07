# -*- coding: utf-8 -*-
"""第二轮修长卷:英文关键词在 Commons 上对中国古画命中率很低,改用中文名。
   每条直接指定文件名,避免搜索选错件——第一轮就出过「天王送子图」抓成菩萨像、
   「太白山图」和「青卞隐居图」抓到同一张的事故。"""
import json,io
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True  # fetch 会用残缺数据兜底,PIL 默认拒收
from findfile import url_of
from fetchimg import fetch
from fixlong import crop_piece

REPO='/Users/sli001/Desktop/艺术卡片-发布'

F={
 251:'File:Yan Zhenqing - Draft of a Requiem to My Nephew.jpg',
 565:'File:唐周昉簪花仕女图.jpg',
 2054:'File:胡瓌卓歇图卷.png',
 2012:'File:李唐采薇图卷.png',
 4500:'File:赵孟頫秀石疏林图卷.png',
 1360:'File:王献之行草书中秋帖卷.png',
 1356:'File:米友仁潇湘奇观图卷.png',
 4501:'File:钱选 浮玉山居图卷.jpg',
 5200:'File:Li Cheng, Luxuriant Forest among Distant Peaks.jpg',
 5307:'File:赵佶雪江归棹图卷.png',
 1532:'File:卫贤高士图卷.jpg',
 4540:'File:吴昌硕紫藤图轴.png',
 5116:'File:吴昌硕 桃实图轴.jpg',
 5313:'File:王蒙夏日山居图轴.jpg',
 903:'File:郑燮 墨竹轴.jpg',
}

def main():
    ok=[];miss=[]
    for i,t in F.items():
        try:
            im=Image.open(io.BytesIO(fetch(url_of(t,2400)))).convert('RGB')
            if max(im.size)<1000: raise ValueError('too small')
            im=crop_piece(im)
            if min(im.size)<380:            # 超扁长卷裁出的中段仍不够高,放大补足
                s=480/min(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
            if max(im.size)>1300:
                s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
            im.save(f'{REPO}/imgs/{i}.webp','WEBP',quality=84)
            ok.append(i); print(f'{i}\tOK\t{im.size}',flush=True)
        except Exception as e:
            miss.append(i); print(f'{i}\t--\t{type(e).__name__} {str(e)[:40]}',flush=True)
    json.dump({'ok':ok,'miss':miss},open('fixlong2_result.json','w'))
    print('修好',len(ok),'| 未修',miss)

if __name__=='__main__': main()
