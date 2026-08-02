import json,sys,os,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from wd import works_of
# 已解析出的 QID(从日志复原,避免重跑解析)
Q={"丢勒":"Q5580","小汉斯·荷尔拜因":"Q48319","克拉纳赫":"Q191748","阿尔特多费":"Q153746",
"格吕内瓦尔德":"Q154338","博斯":"Q130531","老勃鲁盖尔":"Q43270","范艾克":"Q102272",
"康平":"Q80442","梅姆林":"Q106851","博茨":"Q313561"}
out={}
for zh,q in Q.items():
    ws=works_of(q,12); out[zh]={"qid":q,"works":ws}
    print(zh,len(ws),flush=True); time.sleep(1)
json.dump(out,open("works1a.json","w"),ensure_ascii=False,indent=1)
print("saved works1a.json")
