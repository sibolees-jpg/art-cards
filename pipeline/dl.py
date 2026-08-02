import json,subprocess,urllib.parse,os,time,sys
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
REPO='/Users/sli001/Desktop/艺术卡片-发布'
SP=os.path.dirname(os.path.abspath(__file__))
UA='ArtCards/3.0 (educational, non-commercial)'
spec=json.load(open(f'{SP}/'+sys.argv[1]))
def thumb(p18,width=1100):
    fname=urllib.parse.unquote(p18.rsplit('/',1)[-1])
    api=('https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo'
         '&iiprop=url|size&iiurlwidth=%d&titles=File:%s'%(width,urllib.parse.quote(fname)))
    for k in range(3):
        r=subprocess.run(['curl','-s','-m','45','-A',UA,api],capture_output=True)
        try: d=json.loads(r.stdout)
        except Exception: d=None
        if d:
            for pg in (d.get('query') or {}).get('pages',{}).values():
                ii=(pg.get('imageinfo') or [{}])[0]
                if ii.get('thumburl'): return ii['thumburl']
        time.sleep(3)
    return None
def valid(p):
    if not(os.path.exists(p) and os.path.getsize(p)>8000): return False
    with open(p,'rb') as f: h=f.read(12)
    return h[:4]==b'RIFF' and h[8:12]==b'WEBP'
ok=[];bad=[]
for b in spec:
    dst=f"{REPO}/imgs/{b['id']}.webp"
    if valid(dst): ok.append(b['id']); continue
    urls=[]
    tu=thumb(b['img'])
    if tu: urls.append(tu)
    urls.append('https://wsrv.nl/?w=1100&url='+urllib.parse.quote(b['img'],safe=''))
    urls.append(b['img'])
    done=False
    for u in urls:
        tmp=f"/tmp/t{b['id']}.img"
        subprocess.run(['curl','-sfL','--retry','2','--retry-all-errors','-m','120','-A','Mozilla/5.0','-o',tmp,u],capture_output=True)
        if os.path.exists(tmp) and os.path.getsize(tmp)>8000:
            try:
                im=Image.open(tmp).convert('RGB')
                w,h=im.size; sc=min(1,1100/max(w,h))
                if sc<1: im=im.resize((int(w*sc),int(h*sc)),Image.LANCZOS)
                im.save(dst,'WEBP',quality=76)
                print('OK',b['id'],b['zh'],'%dKB'%(os.path.getsize(dst)//1024),flush=True)
                ok.append(b['id']); done=True; break
            except Exception: pass
        time.sleep(1)
    if not done:
        bad.append(b['id']); print('FAIL',b['id'],b['zh'],flush=True)
print('成功',len(ok),'失败',len(bad),bad)
