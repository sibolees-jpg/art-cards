import json,os,io,re
from PIL import Image
from fetchimg import fetch
REPO='/Users/sli001/Desktop/艺术卡片-发布'
have=set(json.load(open('/tmp/have_cn.json')))
haveT={x.split('|',1)[1] for x in have}
def norm(t):
    t=re.sub(r'\.(jpg|jpeg|png|tif|tiff|webp)$','',t,flags=re.I)
    t=re.sub(r'[_\-–—]+',' ',t)
    return re.sub(r'\s+',' ',t).strip()
src=json.load(open('romeworks.json'))
nid=11600; out=[]; skip=0
for a,rows in src.items():
    n=0
    for r in rows:
        if n>=10: break
        t=norm(r['title'])
        if any(h in t or t in h for h in haveT if len(h)>3): skip+=1; continue
        if not r.get('url'): continue
        f=f'{REPO}/imgs/{nid}.webp'
        try:
            d=fetch(r['url'])
            im=Image.open(io.BytesIO(d)).convert('RGB'); w,h=im.size
            if min(w,h)<380: continue
            rr=w/h
            if rr>=2.6:  cw=int(h*1.45); x0=max(0,(w-cw)//2); im=im.crop((x0,0,min(w,x0+cw),h))
            elif rr<=0.34: ch=int(w*1.5); y0=int(h*0.08); im=im.crop((0,y0,w,min(h,y0+ch)))
            if min(im.size)<340: continue
            if max(im.size)>1300:
                s=1300/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
            im.save(f,'WEBP',quality=82)
            out.append({'id':nid,'a':a,'zh':t,'file':r['title']})
            nid+=1; n+=1
        except Exception:
            pass
    print(f'{a:<10} +{n}',flush=True)
json.dump(out,open('pick86.json','w'),ensure_ascii=False,indent=1)
print('下载:',len(out),'| 因查重跳过:',skip)
