import os
import json,re,sys,os
from opencc import OpenCC
cc=OpenCC('t2s')
SP=os.path.dirname(os.path.abspath(__file__))
REPO='/Users/sli001/Desktop/艺术卡片-发布'
srcs=sys.argv[1].split(',')          # works1.json,works1b.json
start=int(sys.argv[2]); N=int(sys.argv[3]); outf=sys.argv[4]
PER=int(sys.argv[5]) if len(sys.argv)>5 else 6
LO,HI=(int(os.environ.get("AC_LINKS_LO",2)), int(os.environ.get("AC_LINKS_HI",9)))
s=open(f'{REPO}/data.js').read()
titles={cc.convert(t) for t in re.findall(r'(?<![A-Za-z])t:"([^"]+)"',s)}
clean=lambda t: re.sub(r'[\s·:：,，。、_\-—]','',re.sub(r'[（(【\[].*?[）)】\]]','',t))
libset={clean(t) for t in titles}; libsort={''.join(sorted(clean(t))) for t in titles}
used=set()
if os.path.exists(f'{SP}/used_qids.json'):
    used|=set(json.load(open(f'{SP}/used_qids.json')))   # 持久账本:所有历史批次的 qid
for f in os.listdir(SP):
    if f.startswith('pick') and f.endswith('.json'):
        try: used|={x['qid'] for x in json.load(open(f'{SP}/{f}'))}
        except Exception: pass
EN2ZH={'psyche':'穿衣镜','mirror':'镜','lorient':'洛里昂','sunflower':'向日葵','loge':'包厢',
'toilette':'梳妆','blanchisseuse':'洗衣','equestrienne':'女骑手','hangover':'宿醉',
'death and the maiden':'死神与少女','dead city':'死城','the family':'家庭','embrace':'拥抱',
'hermits':'隐士','composition':'构成','on white':'白之上','yellow-red-blue':'黄·红·蓝',
'senecio':'塞内西奥','sumpflegende':'沼泽传说','villa r':'别墅','ashes':'灰烬','evolution':'进化',
'flooding':'洪水','chestnut':'栗树','gravelines':'格拉沃利讷','courbevoie':'库尔伯瓦',
'broadway':'百老汇','red, yellow':'红黄蓝','mother and sister':'母亲与姐姐'}
pool=[]
for src in srcs:
    j=json.load(open(f'{SP}/{src}'))
    for a,d in j.items():
        for w in d['works']:
            if w['qid'] in used: continue
            if not (LO<=w['links']<=HI): continue
            t=clean(cc.convert(w['t']))
            if not t or re.match(r'^Q\d+$',t): continue
            if t in libset or ''.join(sorted(t)) in libsort: continue
            # 跨语言:英文标题里的关键词若命中库内中文标题,判为重复
            tl=w['t'].lower()
            hit=False
            for en,zh in EN2ZH.items():
                if en in tl and any(zh in x for x in libset):
                    hit=True; break
            if hit: continue
            pool.append({'a':a,**w})
pool.sort(key=lambda x:(x['a'],-x['links']))
per={};sel=[]
for w in pool:
    if per.get(w['a'],0)>=PER: continue
    per[w['a']]=per.get(w['a'],0)+1; sel.append(w)
    if len(sel)>=N: break
out=[{'id':start+n,'zh':w['t'][:26],'qid':w['qid'],'img':w['img'],'y':w['y'],'loc':w['loc'],'a':w['a']} for n,w in enumerate(sel)]
json.dump(out,open(f'{SP}/{outf}','w'),ensure_ascii=False,indent=1)
print('候选池',len(pool),'| 选出',len(out),'来自',len(per),'位')
for x in out: print(f"{x['id']} {x['a']:<14} {x['zh'][:30]} | {x['y']}")
