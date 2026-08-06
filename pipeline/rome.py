# -*- coding: utf-8 -*-
"""古罗马与希腊化名作:点名抓图。
   《艺术的故事》第4章此前只有 5 张可用卡,分类通道抓来的全是游客现场照,改走这条。"""
import json,io,os,sys
from PIL import Image
from findfile import search,url_of
from fetchimg import fetch

REPO='/Users/sli001/Desktop/艺术卡片-发布'
WORKS=[
 ('拉奥孔','Laocoon and his sons group Vatican marble'),
 ('萨莫色雷斯的胜利女神','Nike of Samothrace Louvre'),
 ('米洛的维纳斯','Venus de Milo Louvre'),
 ('垂死的高卢人','Dying Gaul Capitoline Museums'),
 ('法尔内塞的公牛','Farnese Bull Naples'),
 ('法尔内塞的赫拉克勒斯','Farnese Hercules Naples'),
 ('贝尔维德尔的阿波罗','Apollo Belvedere Vatican'),
 ('贝尔维德尔的躯干','Belvedere Torso Vatican'),
 ('沉睡的阿里阿德涅','Sleeping Ariadne Vatican'),
 ('拳击手','Boxer of Quirinal bronze Rome'),
 ('第一门的奥古斯都','Augustus of Prima Porta statue'),
 ('马可·奥勒留骑马像','Equestrian statue of Marcus Aurelius Capitoline'),
 ('和平祭坛','Ara Pacis Augustae relief procession'),
 ('图拉真柱','Trajan Column relief detail'),
 ('提图斯凯旋门浮雕','Arch of Titus relief menorah'),
 ('君士坦丁凯旋门','Arch of Constantine Rome full'),
 ('万神殿内部','Pantheon Rome interior dome oculus'),
 ('大斗兽场','Colosseum Rome exterior'),
 ('加尔水道桥','Pont du Gard aqueduct'),
 ('亚历山大马赛克','Alexander Mosaic Naples Pompeii'),
 ('神秘别墅壁画','Villa of the Mysteries fresco Pompeii'),
 ('面包师夫妇像','Terentius Neo baker portrait Pompeii fresco'),
 ('利维娅别墅花园壁画','Villa of Livia garden fresco Prima Porta'),
 ('四帝共治像','Portrait of the Four Tetrarchs Venice'),
 ('君士坦丁巨像头部','Colossus of Constantine head Capitoline'),
 ('卡拉卡拉胸像','Bust of Caracalla marble portrait'),
 ('维斯帕先胸像','Bust of Vespasian marble portrait'),
 ('波特兰花瓶','Portland Vase British Museum'),
 ('奥古斯都宝石浮雕','Gemma Augustea Vienna cameo'),
 ('伊特鲁里亚夫妇石棺','Sarcophagus of the Spouses Etruscan Villa Giulia'),
 ('卡皮托利尼的母狼','Capitoline Wolf bronze'),
 ('阿波罗·维爱','Apollo of Veii Etruscan terracotta'),
]

def main():
    nid=int(sys.argv[1]); out=[]
    for zh,q in WORKS:
        got=False
        # Commons 的 search 是 AND 语义,词一多就 0 命中——逐级砍短再试
        w=q.split()
        cands=[]
        for k in (len(w),4,3,2):
            if k>len(w): continue
            cands=search(' '.join(w[:k]),8)
            if cands: break
        for t in cands:
            if got: break
            try:
                d=fetch(url_of(t))
                im=Image.open(io.BytesIO(d)).convert('RGB'); w,h=im.size
                if min(w,h)<420: continue
                if max(im.size)>1300:
                    s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
                im.save(f'{REPO}/imgs/{nid}.webp','WEBP',quality=84)
                out.append({'id':nid,'zh':zh,'file':t}); nid+=1; got=True
            except Exception:
                pass
        print(f'{zh:<14} {"OK" if got else "--"}',flush=True)
    json.dump(out,open('pick87.json','w'),ensure_ascii=False,indent=1)
    print('抓到:',len(out),'/',len(WORKS))

if __name__=='__main__': main()
