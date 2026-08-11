# -*- coding: utf-8 -*-
"""图文核对流水线:生成雪碧图供肉眼审,并记录进度。

程序能查的(破图/重复/几何/字段)都清零了,剩下「这张图是不是这件作品」只能看。
量大且跨会话,所以进度写进 audit_state.json,下次从断点接着来。

  python3 audit.py sheets        # 生成全部待审雪碧图
  python3 audit.py next [n]      # 打印接下来 n 张待审的雪碧图路径
  python3 audit.py done <批号>… # 标记这些批已审完
  python3 audit.py bad <id>…    # 记下判定为图文不符的卡
  python3 audit.py stat          # 进度
"""
import json,os,sys
from PIL import Image,ImageDraw,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True

REPO='/Users/sli001/Desktop/艺术卡片-发布'
STATE=os.path.join(REPO,'pipeline','audit_state.json')
OUT='/tmp/audit2'
PER=40

def load():
    try: return json.load(open(STATE))
    except Exception: return {'done':[],'bad':[],'note':{}}

def save(s): json.dump(s,open(STATE,'w'),ensure_ascii=False,indent=1)

def rows():
    """待审:有图的 art 卡(美育案例除外),按 id 排"""
    r=[x for x in json.load(open('/tmp/auditsrc.json'))]
    r.sort(key=lambda x:x[0])
    return r

def sheets():
    os.makedirs(OUT,exist_ok=True)
    rs=rows(); n=0
    for b in range(0,len(rs),PER):
        chunk=rs[b:b+PER]
        cols=8; cw,ch=232,246
        im=Image.new('RGB',(cols*cw,((len(chunk)+cols-1)//cols)*ch),(24,24,24))
        d=ImageDraw.Draw(im)
        for k,(i,t,a,cat,p) in enumerate(chunk):
            fp=os.path.join(REPO,p)
            x,y=(k%cols)*cw+4,(k//cols)*ch+4
            try:
                th=Image.open(fp).convert('RGB'); th.thumbnail((cw-12,ch-58))
                im.paste(th,(x,y))
            except Exception:
                d.text((x+6,y+6),'缺图',fill=(220,80,80))
            d.text((x,y+ch-50),f'{i} {t[:15]}',fill=(228,192,104))
            d.text((x,y+ch-36),f'{(a or "")[:18]}',fill=(150,150,150))
        im.save(f'{OUT}/s{b//PER:03d}.png'); n+=1
    print(f'{len(rs)} 张卡 -> {n} 张雪碧图,在 {OUT}/')

def main():
    cmd=sys.argv[1] if len(sys.argv)>1 else 'stat'
    s=load(); rs=rows(); tot=(len(rs)+PER-1)//PER
    if cmd=='sheets': sheets()
    elif cmd=='next':
        k=int(sys.argv[2]) if len(sys.argv)>2 else 5
        todo=[i for i in range(tot) if i not in s['done']][:k]
        for i in todo:
            lo=i*PER; hi=min(lo+PER,len(rs))
            print(f'{OUT}/s{i:03d}.png  批{i}  id {rs[lo][0]}–{rs[hi-1][0]}')
    elif cmd=='done':
        for x in sys.argv[2:]:
            b=int(x)
            if b not in s['done']: s['done'].append(b)
        s['done'].sort(); save(s); print('已审',len(s['done']),'/',tot,'批')
    elif cmd=='bad':
        for x in sys.argv[2:]:
            i=int(x)
            if i not in s['bad']: s['bad'].append(i)
        save(s); print('问题卡累计',len(s['bad']))
    else:
        print(f'待审 {len(rs)} 张卡 / {tot} 批 | 已审 {len(s["done"])} 批 '
              f'({len(s["done"])*PER} 张,{len(s["done"])*100//max(1,tot)}%) | 记下问题卡 {len(s["bad"])}')

if __name__=='__main__': main()
