# -*- coding: utf-8 -*-
"""合并同标题同作者的重复卡。

早期卡文案写得细,后期管线抓的图更清——所以不是简单删一张,
而是「保文案好的那张,把更清的图搬过去」,再删掉其余。

用法:  python3 dedupe.py           # dry-run,只打印计划
       python3 dedupe.py --apply   # 实际执行
"""
import json,os,re,sys,shutil,collections
from PIL import Image

REPO='/Users/sli001/Desktop/艺术卡片-发布'
APPLY='--apply' in sys.argv

def norm_t(x): return re.sub(r'[·・\s()（）]','',str(x or ''))
def norm_a(x): return re.sub(r'[·・\s]','',str(x or ''))

def load():
    rows=json.load(open('/tmp/full.json'))
    imgp={int(i):p for i,p in json.load(open('/tmp/imgmap.json'))}
    return {r[0]:r for r in rows}, imgp

def px(p):
    try:
        w,h=Image.open(os.path.join(REPO,p)).size; return w*h
    except Exception: return 0

def main():
    m,imgp=load()
    key=collections.defaultdict(list)
    for r in m.values():
        if r[4]!='art': continue
        key[(norm_t(r[1]),norm_a(r[2]))].append(r[0])
    dup={k:v for k,v in key.items() if len(v)>1}

    plan=[]
    for k,v in dup.items():
        keep=max(v,key=lambda i:sum(len(str(x)) for x in m[i][6:10]))   # 文案最详细
        best=max(v,key=lambda i:px(imgp.get(i,'')))                     # 图最清
        swap = best!=keep and px(imgp.get(best,''))>px(imgp.get(keep,''))*1.15
        plan.append({'keep':keep,'drop':[i for i in v if i!=keep],
                     'swap_img_from':best if swap else None,'t':m[keep][1]})
    print(f'重复组 {len(plan)} | 将删卡 {sum(len(p["drop"]) for p in plan)} | 需换图 {sum(1 for p in plan if p["swap_img_from"])}')
    for p in plan[:10]:
        print(f'  保留 {p["keep"]} 「{p["t"]}」 删 {p["drop"]}' + (f' 换图自 {p["swap_img_from"]}' if p['swap_img_from'] else ''))
    if not APPLY:
        print('\n(dry-run;加 --apply 才会写入)')
        json.dump(plan,open('dedupe_plan.json','w'),ensure_ascii=False,indent=1)
        return

    s=open(f'{REPO}/data.js',encoding='utf-8').read()
    swapped=deleted=0
    for p in plan:
        k=p['keep']
        if p['swap_img_from']:
            src=imgp[p['swap_img_from']]; ext=src.rsplit('.',1)[-1]
            dst=f'imgs/{k}.{ext}'
            if os.path.abspath(os.path.join(REPO,src))!=os.path.abspath(os.path.join(REPO,dst)):
                shutil.copy(os.path.join(REPO,src),os.path.join(REPO,dst))
            # 换掉保留卡的 img 路径
            mm=re.search(r'(\{id:%d,.*?img:")([^"]*)(")'%k,s,re.S)
            if mm and mm.start()<s.index('}',mm.start()):
                s=s[:mm.start(2)]+dst+s[mm.end(2):]
                swapped+=1
        for d in p['drop']:
            mm=re.search(r'\n\{id:%d,.*?\},(?=\n)'%d,s,re.S) or re.search(r'\{id:%d,.*?\},'%d,s,re.S)
            if mm: s=s[:mm.start()]+s[mm.end():]; deleted+=1
    open(f'{REPO}/data.js','w',encoding='utf-8').write(s)
    print(f'已换图 {swapped} | 已删卡 {deleted}')

if __name__=='__main__': main()
