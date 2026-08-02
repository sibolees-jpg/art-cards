import json,sys,os,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from wd import works_of,qid_of
names=json.load(open(sys.argv[1]))     # [[中文名, 英文维基条目名], ...]
out={}
for zh,en in names:
    q=qid_of(en)
    if not q: print('解析失败',zh,en,flush=True); continue
    ws=works_of(q,12)
    out[zh]={"qid":q,"works":ws}
    print(f'{zh:<14}{q:<12}{len(ws)}',flush=True)
    time.sleep(1.5)
json.dump(out,open(sys.argv[2],"w"),ensure_ascii=False,indent=1)
print("saved",sys.argv[2])
