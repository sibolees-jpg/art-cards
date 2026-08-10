# -*- coding: utf-8 -*-
"""按图片哈希去重——比标题匹配可靠。

上一轮按「同标题同作者」合并后仍剩 246 组重复,原因是译名不同:
「凡·戴克/凡·代克」「哈默肖伊/哈默修伊/哈默斯霍伊」「马克/麦克」。
图片内容完全相同(md5 一致)才是同一件作品的硬证据。

同一组内图已相同,所以不需要换图,只保留文案最详细的那张。

用法: python3 dedupe_hash.py [--apply]
"""
import json,os,re,sys

REPO='/Users/sli001/Desktop/艺术卡片-发布'
APPLY='--apply' in sys.argv

def main():
    groups=json.load(open('/tmp/dup_same.json'))
    full={r[0]:r for r in json.load(open('/tmp/full2.json'))}
    txt=json.load(open('/tmp/txtlen.json'))       # id -> 文案总字数

    plan=[]
    for files,cards in groups:
        ids=[c[0] for c in cards]
        keep=max(ids,key=lambda i:txt.get(str(i),0))
        plan.append({'keep':keep,'drop':[i for i in ids if i!=keep],
                     't':next(c[3] for c in cards if c[0]==keep)})
    drop=[i for p in plan for i in p['drop']]
    print(f'重复组 {len(plan)} | 将删卡 {len(drop)}')
    for p in plan[:10]: print(f'  保留 {p["keep"]} 「{p["t"]}」 删 {p["drop"]}')
    if not APPLY:
        json.dump(plan,open('dedupe_hash_plan.json','w'),ensure_ascii=False,indent=1)
        print('\n(dry-run;加 --apply 才写入)'); return

    s=open(f'{REPO}/data.js',encoding='utf-8').read()
    n=0
    for i in drop:
        m=re.search(r'\n\{id:%d,.*?\},(?=\n)'%i,s,re.S) or re.search(r'\{id:%d,.*?\},'%i,s,re.S)
        if m: s=s[:m.start()]+s[m.end():]; n+=1
    open(f'{REPO}/data.js','w',encoding='utf-8').write(s)
    print('已删卡',n)

if __name__=='__main__': main()
