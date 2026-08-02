import json,sys,os,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from wd import works_of
Q=json.load(open(sys.argv[1]))
out=json.load(open(sys.argv[2])) if os.path.exists(sys.argv[2]) else {}
for zh,q in Q.items():
    if zh in out and out[zh].get("works"): continue
    ws=works_of(q,12); out[zh]={"qid":q,"works":ws}
    print(zh,len(ws),flush=True)
    json.dump(out,open(sys.argv[2],"w"),ensure_ascii=False,indent=1)   # 每次都存,防中断丢失
    time.sleep(1)
print("done",len(out))
