import json,subprocess
CATS=[("马远","Category:Ma Yuan (painter)"),("李唐","Category:Li Tang (painter)"),
 ("梁楷","Category:Liang Kai"),("郭熙","Category:Guo Xi"),("黄公望","Category:Huang Gongwang"),
 ("倪瓒","Category:Ni Zan"),("王蒙","Category:Wang Meng (painter)"),("吴镇","Category:Wu Zhen (painter)"),
 ("崔白","Category:Cui Bai"),("阎立本","Category:Yan Liben"),("张萱","Category:Zhang Xuan"),
 ("周昉","Category:Zhou Fang"),("展子虔","Category:Zhan Ziqian"),("陈洪绶","Category:Chen Hongshou"),
 ("恽寿平","Category:Yun Shouping"),("任伯年","Category:Ren Yi"),("张大千","Category:Zhang Daqian"),
 ("傅抱石","Category:Fu Baoshi"),("李可染","Category:Li Keran"),("文徵明","Category:Wen Zhengming"),
 ("仇英","Category:Qiu Ying"),("董其昌","Category:Dong Qichang"),("王时敏","Category:Wang Shimin"),
 ("华嵒","Category:Hua Yan"),("赵之谦","Category:Zhao Zhiqian"),("虚谷","Category:Xugu"),
 ("蓝瑛","Category:Lan Ying"),("林风眠","Category:Lin Fengmian"),("石鲁","Category:Shi Lu"),
 ("沈周","Category:Shen Zhou"),("王鉴","Category:Wang Jian (painter)"),("石涛","Category:Shitao"),
 ("八大山人","Category:Bada Shanren"),("金农","Category:Jin Nong"),("郑燮","Category:Zheng Xie"),
 ("敦煌壁画","Category:Paintings in the Mogao Caves"),("永乐宫壁画","Category:Yongle Palace murals"),
 ("徐渭","Category:Xu Wei"),("唐寅","Category:Tang Yin"),("王翚","Category:Wang Hui (painter)"),
]
out={}
for zh,cat in CATS:
    f=f'/tmp/c3_{abs(hash(cat))%99999}.json'
    subprocess.run(['python3','commons.py',cat,f,'14'],capture_output=True,text=True)
    try:
        rows=json.load(open(f))
        if rows: out[zh]=rows
        print(f'{zh:<10} {len(rows)}',flush=True)
    except Exception: print(f'{zh:<10} 失败',flush=True)
json.dump(out,open('cnworks3.json','w'),ensure_ascii=False,indent=1)
print('总计:',sum(len(v) for v in out.values()))
