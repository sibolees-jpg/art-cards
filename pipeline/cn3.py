import json
from commons import files_in
CATS={
 '古罗马雕塑':'Category:Ancient Roman sculptures in the Vatican Museums',
 '庞贝壁画':'Category:Frescos in Pompeii',
 '罗马肖像':'Category:Ancient Roman portrait busts',
 '罗马马赛克':'Category:Ancient Roman mosaics in Italy',
 '希腊化雕塑':'Category:Hellenistic sculptures',
 '罗马石棺':'Category:Ancient Roman sarcophagi',
 '罗马建筑':'Category:Ancient Roman architecture in Rome',
 '罗马银器':'Category:Ancient Roman silver',
 '法尤姆肖像':'Category:Fayum mummy portraits',
 '罗马凯旋门':'Category:Triumphal arches in Italy',
 '罗马神庙':'Category:Ancient Roman temples in Italy',
 '伊特鲁里亚':'Category:Etruscan art',
 '罗马玻璃':'Category:Ancient Roman glass',
 '罗马浮雕':'Category:Ancient Roman reliefs',
}
out={}
for a,c in CATS.items():
    try: fs=files_in(c,limit=14,depth=2)
    except Exception: fs=[]
    out[a]=[{'title':f,'url':'https://commons.wikimedia.org/wiki/Special:FilePath/'+f.replace('File:','').replace(' ','_')+'?width=2000'} for f in fs]
    print(f'{a:<10} {len(out[a])}',flush=True)
json.dump(out,open('romeworks.json','w'),ensure_ascii=False)
