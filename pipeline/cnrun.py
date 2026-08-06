import json,sys,subprocess,os
CATS=[
 ("马远","Category:Ma Yuan (painter)"),("夏圭","Category:Xia Gui"),
 ("李唐","Category:Li Tang (painter)"),("梁楷","Category:Liang Kai"),
 ("牧谿","Category:Muqi"),("范宽","Category:Fan Kuan"),
 ("郭熙","Category:Guo Xi"),("李成","Category:Li Cheng"),
 ("董源","Category:Dong Yuan"),("巨然","Category:Juran"),
 ("赵孟頫","Category:Zhao Mengfu"),("黄公望","Category:Huang Gongwang"),
 ("倪瓒","Category:Ni Zan"),("王蒙","Category:Wang Meng (painter)"),
 ("吴镇","Category:Wu Zhen (painter)"),("钱选","Category:Qian Xuan"),
 ("宋徽宗","Category:Emperor Huizong of Song"),("张择端","Category:Zhang Zeduan"),
 ("崔白","Category:Cui Bai"),("阎立本","Category:Yan Liben"),
 ("张萱","Category:Zhang Xuan"),("周昉","Category:Zhou Fang"),
 ("韩滉","Category:Han Huang"),("韩干","Category:Han Gan"),
 ("顾恺之","Category:Gu Kaizhi"),("展子虔","Category:Zhan Ziqian"),
 ("徐渭","Category:Xu Wei"),("陈洪绶","Category:Chen Hongshou"),
 ("八大山人","Category:Bada Shanren"),("石涛","Category:Shitao"),
 ("恽寿平","Category:Yun Shouping"),("金农","Category:Jin Nong"),
 ("郎世宁","Category:Giuseppe Castiglione (painter)"),("任伯年","Category:Ren Yi"),
 ("吴昌硕","Category:Wu Changshuo"),("齐白石","Category:Qi Baishi"),
 ("张大千","Category:Zhang Daqian"),("傅抱石","Category:Fu Baoshi"),
 ("李可染","Category:Li Keran"),("黄宾虹","Category:Huang Binhong"),
]
out={}
for zh,cat in CATS:
    f=f'/tmp/cn_{abs(hash(cat))%99999}.json'
    r=subprocess.run(['python3','commons.py',cat,f,'12'],capture_output=True,text=True)
    try:
        rows=json.load(open(f))
        out[zh]=rows
        print(f'{zh:<10} {len(rows)}',flush=True)
    except Exception as e:
        print(f'{zh:<10} 失败',flush=True)
json.dump(out,open('cnworks.json','w'),ensure_ascii=False,indent=1)
print('总计:',sum(len(v) for v in out.values()))
