import json,subprocess
CATS=[
 ("马远","Category:Ma Yuan"),("李唐","Category:Li Tang"),("梁楷","Category:Liang Kai (painter)"),
 ("郭熙","Category:Guo Xi (painter)"),("黄公望","Category:Huang Gongwang (painter)"),
 ("倪瓒","Category:Ni Zan (painter)"),("王蒙","Category:Wang Meng"),
 ("吴镇","Category:Wu Zhen"),("崔白","Category:Cui Bai (painter)"),
 ("阎立本","Category:Yan Liben (painter)"),("张萱","Category:Zhang Xuan (painter)"),
 ("周昉","Category:Zhou Fang (painter)"),("展子虔","Category:Zhan Ziqian (painter)"),
 ("陈洪绶","Category:Chen Hongshou (painter)"),("恽寿平","Category:Yun Shouping (painter)"),
 ("郎世宁","Category:Giuseppe Castiglione"),("任伯年","Category:Ren Bonian"),
 ("张大千","Category:Zhang Daqian (painter)"),("傅抱石","Category:Fu Baoshi (painter)"),
 ("李可染","Category:Li Keran (painter)"),
 ("文徵明","Category:Wen Zhengming"),("唐寅","Category:Tang Yin"),
 ("仇英","Category:Qiu Ying"),("董其昌","Category:Dong Qichang"),
 ("王翚","Category:Wang Hui"),("王原祁","Category:Wang Yuanqi"),
 ("王时敏","Category:Wang Shimin"),("华嵒","Category:Hua Yan"),
 ("郑燮","Category:Zheng Xie"),("赵之谦","Category:Zhao Zhiqian"),
 ("虚谷","Category:Xugu"),("蓝瑛","Category:Lan Ying"),
 ("徐悲鸿","Category:Xu Beihong"),("林风眠","Category:Lin Fengmian"),
 ("潘天寿","Category:Pan Tianshou"),("石鲁","Category:Shi Lu"),
 ("敦煌","Category:Mogao Caves paintings"),("永乐宫","Category:Yongle Palace"),
 ("宋代绘画","Category:Song dynasty paintings"),("明代绘画","Category:Ming dynasty paintings"),
]
out={}
for zh,cat in CATS:
    f=f'/tmp/c2_{abs(hash(cat))%99999}.json'
    subprocess.run(['python3','commons.py',cat,f,'12'],capture_output=True,text=True)
    try:
        rows=json.load(open(f))
        if rows: out[zh]=rows
        print(f'{zh:<10} {len(rows)}',flush=True)
    except Exception: print(f'{zh:<10} 失败',flush=True)
json.dump(out,open('cnworks2.json','w'),ensure_ascii=False,indent=1)
print('总计:',sum(len(v) for v in out.values()))
