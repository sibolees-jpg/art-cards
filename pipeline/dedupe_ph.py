# -*- coding: utf-8 -*-
"""按感知哈希合并重复卡。

md5 只抓得到「同一个文件」。同一件作品被重新编码/重新裁切后 md5 就不同了,
但 pHash 仍能认出来——这轮挖出的 300 多对就是这么漏网的,而且作者译名五花八门
(籍里柯/热里科、希施金/希什金、凡·戴克/凡·代克),按标题+作者匹配也抓不到。

同一组内保留文案最详细的一张,其余删掉。

用法: python3 dedupe_ph.py [--apply]
"""
import json,re,sys,collections

REPO='/Users/sli001/Desktop/艺术卡片-发布'
APPLY='--apply' in sys.argv

# 图相同但确属不同作品——图归其中一方,另一方去图(逐张看过图定的)
STRIP=[4339,   # 图是拉斐尔的《美惠三女神》,不是鲁本斯的
       5311,   # 《渔父图》图归吴镇那张
       4523,   # 《墨梅图》图归王冕那张
       1555,   # 图是巴塞罗那椅,不是凳
       8068]   # 图是卡萨特《母与子》,不是《的里雅斯特港》

# music/film 的关联不是重复,别合并:乐章之于全曲、配乐之于电影、同一歌手的两首歌
KEEP_PAIRS={(1419,5453),(1461,4674),(1641,4851),(197,5016),(1957,5216),(1878,5552),
            (201,3806),(435,598),(644,4859),(791,931),(843,991),(4671,4678)}

def main():
    pairs=json.load(open('phash_pairs.json'))
    txt=json.load(open('/tmp/txtlen.json'))
    full={r[0]:r for r in json.load(open('/tmp/full2.json'))}

    def nt(s): return re.sub(r'[·・\s()（）《》]','',str(s or ''))
    def jac(a,b):
        A,B=set(nt(a)),set(nt(b))
        return len(A&B)/max(1,len(A|B))

    # 并查集:标题相近且图几乎一样 -> 同一件作品
    par={}
    def find(x):
        par.setdefault(x,x)
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    def uni(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: par[ra]=rb

    for p in pairs:
        ia,ib=p['a'][0],p['b'][0]
        if (ia,ib) in KEEP_PAIRS or (ib,ia) in KEEP_PAIRS: continue
        if ia in STRIP or ib in STRIP: continue
        if p['a'][1]!=p['b'][1]: continue            # 跨门类不合并
        if jac(p['a'][2],p['b'][2])<0.45: continue   # 标题差太远,可能是共用图的错配
        uni(ia,ib)

    groups=collections.defaultdict(list)
    for x in par: groups[find(x)].append(x)
    groups=[sorted(v) for v in groups.values() if len(v)>1]

    plan=[]
    for g in groups:
        keep=max(g,key=lambda i:txt.get(str(i),0))
        plan.append({'keep':keep,'drop':[i for i in g if i!=keep],
                     't':full[keep][1] if keep in full else ''})
    drop=[i for p in plan for i in p['drop']]
    print(f'合并组 {len(plan)} | 删卡 {len(drop)} | 另去图 {len(STRIP)} 张')
    for p in plan[:12]: print(f"  保留 {p['keep']} 「{p['t']}」 删 {p['drop']}")
    if not APPLY:
        json.dump(plan,open('dedupe_ph_plan.json','w'),ensure_ascii=False,indent=1)
        print('\n(dry-run;加 --apply 才写入)'); return

    s=open(f'{REPO}/data.js',encoding='utf-8').read()
    n=0
    for i in drop:
        m=re.search(r'\n\{id:%d,.*?\},(?=\n)'%i,s,re.S) or re.search(r'\{id:%d,.*?\},'%i,s,re.S)
        if m: s=s[:m.start()]+s[m.end():]; n+=1
    k=0
    for i in STRIP:
        m=re.search(r'\{id:%d,'%i,s)
        if not m: continue
        end=s.index('}',m.start()); seg=s[m.start():end]
        seg2=re.sub(r'cr:"[^"]*",','',re.sub(r'img:"[^"]*",','',seg))
        if seg2!=seg: s=s[:m.start()]+seg2+s[end:]; k+=1
    open(f'{REPO}/data.js','w',encoding='utf-8').write(s)
    print(f'已删卡 {n} | 已去图 {k}')

if __name__=='__main__': main()
