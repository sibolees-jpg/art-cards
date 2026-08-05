#!/usr/bin/env python3
"""开新批次前必跑:打印当前 data.js 的最大 id + 1。
   永远从这个号开始编,不要凭记忆接号——id 复用会覆盖已有图片,造成图文错位。"""
import re,sys
s=open('/Users/sli001/Desktop/艺术卡片-发布/data.js',encoding='utf-8').read()
ids=[int(m) for m in re.findall(r'\bid:(\d+)',s)]
print(f"当前卡数 {len(ids)} | 最大 id {max(ids)} | 下一批从 {max(ids)+1} 开始")
