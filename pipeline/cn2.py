import json,sys
from commons import files_in
CATS={
 '倪瓒':'Category:Ni Zan','王蒙':'Category:Wang Mêng','崔白':"Category:Ts'ui Po",
 '陈洪绶':'Category:Chen Hongshou (painter)','李唐':'Category:Li Tang','吴镇':'Category:Wu Zhen',
 '阎立本':'Category:Yan Liben','张萱':'Category:Zhang Xuan (Tang dynasty)','周昉':'Category:Zhou Fang (painter)',
 '任伯年':'Category:Ren Bonian','文徵明':'Category:Wen Zhengming','唐寅':'Category:Tang Yin',
 '米芾':'Category:Mi Fu','王翚':'Category:Wang Hui (painter)','龚贤':'Category:Gong Xian',
 '髡残':'Category:Kuncan','弘仁':'Category:Hongren','华嵒':'Category:Hua Yan (painter)',
 '虚谷':'Category:Xugu','苏轼':'Category:Su Shi','王时敏':'Category:Wang Shimin',
 '吴历':'Category:Wu Li','李公麟':'Category:Li Gonglin','马和之':'Category:Ma Hezhi',
 '文同':'Category:Wen Tong','赵伯驹':'Category:Zhao Boju','王希孟':'Category:Wang Ximeng',
 '倪元璐':'Category:Ni Yuanlu','王铎':'Category:Wang Duo (calligrapher)','傅山':'Category:Fu Shan',
 '祝允明':'Category:Zhu Yunming','董邦达':'Category:Dong Bangda','蒋廷锡':'Category:Jiang Tingxi',
}
out={}
for a,c in CATS.items():
    try:
        fs=files_in(c,limit=12,depth=2)
    except Exception:
        fs=[]
    rows=[{'title':f,'url':'https://commons.wikimedia.org/wiki/Special:FilePath/'+f.replace('File:','').replace(' ','_')+'?width=2400'} for f in fs]
    out[a]=rows
    print(f'{a:<8} {len(rows)}',flush=True)
json.dump(out,open('cnworks4.json','w'),ensure_ascii=False)
