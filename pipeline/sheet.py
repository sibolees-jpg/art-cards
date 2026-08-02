from PIL import Image,ImageDraw,ImageFont
import os
REPO='/Users/sli001/Desktop/艺术卡片-发布'
def make(items,out,cols=6,cell=(232,196)):
    rows=(len(items)+cols-1)//cols
    W,H=cols*cell[0],rows*(cell[1]+24)
    cv=Image.new('RGB',(W,H),(24,24,24)); d=ImageDraw.Draw(cv)
    try: f=ImageFont.truetype('/System/Library/Fonts/PingFang.ttc',11)
    except Exception: f=ImageFont.load_default()
    for n,(i,zh) in enumerate(items):
        cx,cy=(n%cols)*cell[0],(n//cols)*(cell[1]+24)
        p=f'{REPO}/imgs/{i}.webp'
        if os.path.exists(p):
            try:
                im=Image.open(p).convert('RGB'); im.thumbnail((cell[0]-12,cell[1]-12))
                cv.paste(im,(cx+6,cy+6))
            except Exception: d.text((cx+8,cy+80),'坏图',fill=(255,60,60),font=f)
        else: d.text((cx+8,cy+80),'缺图',fill=(255,60,60),font=f)
        d.text((cx+6,cy+cell[1]+4),f'{i} {zh[:15]}',fill=(255,215,122),font=f)
    cv.save(out); print(out,cv.size,f'{len(items)}格')
