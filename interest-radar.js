/* 兴趣雷达：复用个人属性的统计，轴下作品复用同一匹配规则。 */
(function(root){
'use strict';
const VIEWS=[{key:'concern',name:'核心关怀',color:'#b3543e'},{key:'material',name:'材料',color:'#9a7c38'},{key:'method',name:'组织方法',color:'#5b7a5e'},{key:'mood',name:'意境',color:'#7a5b8c'}];
const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const textOf=w=>(w.bg||'')+(w.how||'')+(w.why||'')+(w.more||'')+(w.cat||'')+(w.t||'')+(w.verse||'');
function axesFromProfile(profile,key){
 const rows=(profile[key]||[]).slice(0,6);
 return Array.from({length:6},(_,i)=>rows[i]?{k:rows[i].k,s:rows[i].s,percent:profile.wsum?Math.min(100,rows[i].s/profile.wsum*100):0}:{k:null,s:0,percent:0});
}
function matchingWorks(works,bucket){return bucket?works.filter(w=>bucket.kw.some(k=>textOf(w).includes(k))):[];}
function mount(rootEl,{profile,buckets,works,favourites,getSelected,onToggle,onOpen,suffix=''}){
 let view='concern';const storeKey='ac_radar_view'+suffix;
 try{const k=localStorage.getItem(storeKey);if(VIEWS.some(v=>v.key===k))view=k;}catch(_){}
 let axes=[],active=null,shown=12,matches=[],observer,frame;
 rootEl.innerHTML=`<div class="ir-viewbar" role="group" aria-label="分析视角">${VIEWS.map(v=>`<button type="button" data-ir-view="${v.key}" aria-pressed="false">${v.name}</button>`).join('')}</div>
 <div class="ir-layout"><section class="ir-chart-section"><div class="ir-heading"><div class="ir-overline">从收藏里看见你的偏向</div><h3>兴趣雷达</h3><p data-ir-caption></p></div><div class="ir-chart"><svg role="img" aria-label="兴趣雷达，六轴显示当前视角的加权命中比例"></svg><div class="ir-axis-layer"></div></div><div class="ir-no-axis" hidden>这一视角还没有足够的文字线索。<br>继续收藏作品，让它慢慢形成。</div><p class="ir-note">外圈为 100%。比例沿用个人属性：喜欢计 1，爆灯计 2。类别可以重叠，总和不必等于 100%。</p></section>
 <section class="ir-evidence"><div class="ir-evidence-heading"><div><span class="ir-overline">对应作品</span><h4 data-ir-title></h4></div><span data-ir-count></span></div><p class="ir-evidence-note" data-ir-evidence-note></p><div class="ir-works"></div><button class="ir-more" type="button" hidden>再看 12 件</button></section></div>`;
 const $=s=>rootEl.querySelector(s);
 const fmt=n=>Math.round(n)+'%';
 function syncSelection(){const set=getSelected();rootEl.querySelectorAll('[data-ir-check]').forEach(el=>{el.checked=set.has(Number(el.dataset.irCheck));el.closest('.ir-work').classList.toggle('ir-selected',el.checked);});}
 function renderWorks(){
  $('.ir-works').innerHTML=matches.slice(0,shown).map(w=>{
   const thumb=typeof w.img==='string'&&/^imgs\/[\w./-]+$/.test(w.img)?`<img src="${escape(w.img)}" alt="${escape(w.t)}" loading="lazy">`:`<span class="ir-placeholder">${escape(w.cat||'作品')}</span>`;
   return `<article class="ir-work"><button type="button" class="ir-work-open" data-ir-open="${w.id}" aria-label="查看${escape(w.t)}"><span class="ir-thumb">${thumb}</span><span class="ir-work-text"><b>${escape(w.t)}</b><small>${escape(w.a||'作者不详')}${w.y?' · '+escape(w.y):''}</small>${favourites.has(w.id)?'<em>已爆灯</em>':''}</span></button><label class="ir-check"><input type="checkbox" data-ir-check="${w.id}"> 加入比较</label></article>`;
  }).join('');
  rootEl.querySelectorAll('.ir-thumb img').forEach(img=>{img.onerror=()=>{const note=document.createElement('span');note.className='ir-placeholder';note.textContent='暂无图片';img.replaceWith(note);};});
  $('.ir-more').hidden=shown>=matches.length;syncSelection();
 }
 function selectAxis(key,focus=false){
  active=key;shown=12;
  const bucket=(buckets[view]||[]).find(b=>b.k===key);
  matches=matchingWorks(works,bucket);
  $('[data-ir-title]').textContent=key||'等待兴趣浮现';
  $('[data-ir-count]').textContent=key?matches.length+' 件':'';
  $('[data-ir-evidence-note]').textContent=key?'按作品文字线索归纳。点开查看作品，也可以选择多件继续分析共同点。':'这里会显示支持这一项的具体作品。';
  renderWorks();draw();
  if(focus)rootEl.querySelector(`[data-ir-axis="${axes.findIndex(a=>a.k===key)}"]`)?.focus({preventScroll:true});
 }
 function draw(){
  const chart=$('.ir-chart'),width=chart.clientWidth;if(!width)return;
  const radius=Math.max(50,Math.min(140,(width-168)/2)),height=radius*2+150,cx=width/2,cy=height/2;
  chart.style.height=height+'px';
  const svg=chart.querySelector('svg');svg.setAttribute('viewBox',`0 0 ${width} ${height}`);
  const point=(i,r)=>[cx+Math.cos(-Math.PI/2+i*Math.PI/3)*r,cy+Math.sin(-Math.PI/2+i*Math.PI/3)*r];
  const polygon=r=>axes.map((_,i)=>point(i,r).join(',')).join(' ');
  let content='<title>当前收藏的兴趣雷达</title><desc>'+axes.filter(a=>a.k).map(a=>escape(a.k)+' '+fmt(a.percent)).join('，')+'</desc>';
  for(const level of [25,50,75,100])content+=`<polygon points="${polygon(radius*level/100)}" fill="none" stroke="var(--line)" stroke-width="1"/>`;
  axes.forEach((a,i)=>{const p=point(i,radius);content+=`<line x1="${cx}" y1="${cy}" x2="${p[0]}" y2="${p[1]}" stroke="var(--line)"/>`;});
  content+=`<polygon class="ir-shape" points="${axes.map((a,i)=>point(i,radius*a.percent/100).join(',')).join(' ')}" fill="var(--ir-color)" fill-opacity=".16" stroke="var(--ir-color)" stroke-width="2"/>`;
  axes.forEach((a,i)=>{if(!a.k)return;const p=point(i,radius*a.percent/100);content+=`<circle cx="${p[0]}" cy="${p[1]}" r="${active===a.k?5:3}" fill="var(--ir-color)"/>`;});
  content+=`<text x="${cx+5}" y="${cy+14}">0</text><text x="${cx+5}" y="${cy-radius/2+3}">50</text>`;
  svg.innerHTML=content;
  $('.ir-axis-layer').innerHTML=axes.map((a,i)=>{const p=point(i,radius+40);return `<button type="button" data-ir-axis="${i}" style="left:${p[0]}px;top:${p[1]}px" ${a.k?'':'disabled'} aria-pressed="${!!a.k&&active===a.k}"><span>${escape(a.k||'尚未形成')}</span><b>${a.k?fmt(a.percent):'—'}</b></button>`;}).join('');
 }
 function renderView(){
  axes=axesFromProfile(profile,view);const def=VIEWS.find(v=>v.key===view);rootEl.style.setProperty('--ir-color',def.color);
  rootEl.querySelectorAll('[data-ir-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.irView===view)));
  const n=axes.filter(a=>a.k).length;
  $('[data-ir-caption]').textContent=`${def.name} · 当前最突出的 ${n} 项`;
  $('.ir-chart').hidden=!n;$('.ir-no-axis').hidden=!!n;
  selectAxis(axes[0].k);
 }
 rootEl.onclick=e=>{
  const b=e.target.closest('button');if(!b||b.disabled||!rootEl.contains(b))return;
  if(b.dataset.irView){view=b.dataset.irView;try{localStorage.setItem(storeKey,view);}catch(_){}renderView();}
  if(b.dataset.irAxis!==undefined)selectAxis(axes[Number(b.dataset.irAxis)].k,true);
  if(b.dataset.irOpen)onOpen(Number(b.dataset.irOpen));
  if(b.classList.contains('ir-more')){shown+=12;renderWorks();}
 };
 rootEl.onchange=e=>{if(e.target.dataset.irCheck)onToggle(Number(e.target.dataset.irCheck));};
 let lastWidth=-1;
 observer=new ResizeObserver(entries=>{const width=entries[0].contentRect.width;if(width===lastWidth)return;lastWidth=width;cancelAnimationFrame(frame);frame=requestAnimationFrame(draw);});observer.observe($('.ir-chart-section'));
 renderView();
 return {syncSelection,destroy(){observer.disconnect();cancelAnimationFrame(frame);rootEl.onclick=null;rootEl.onchange=null;}};
}
const api={axesFromProfile,matchingWorks,mount};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.InterestRadar=api;
})(typeof globalThis!=='undefined'?globalThis:this);
