/* 个人属性的创作工具。候选只来自 computeAttr 与当前问题意识。 */
(function(root){
'use strict';
const moods=[
 {k:'孤独感',kw:['孤独','寂寞','独处','孤寂','孑然']},
 {k:'寂静感',kw:['寂静','静默','沉默','宁静','清静','静谧']},
 {k:'忧伤与哀悼',kw:['忧伤','悲伤','悲痛','哀悼','悼念','悲凉','悲叹']},
 {k:'荒诞感',kw:['荒诞','荒谬','滑稽','无意义','戏谑']},
 {k:'梦幻感',kw:['梦幻','梦境','梦游','幻觉','超现实','似曾相识']},
 {k:'危机与压迫',kw:['危机','压迫','恐惧','威胁','窒息','惊恐','不安']},
 {k:'无常与消逝',kw:['无常','消逝','流逝','短暂','转瞬','衰败','凋零']},
 {k:'苍凉感',kw:['苍凉','荒凉','废墟','荒芜','残垣','沧桑']},
 {k:'神秘感',kw:['神秘','谜团','不可知','幽深','未知']},
 {k:'崇高与庄严',kw:['崇高','庄严','肃穆','宏伟','敬畏','神圣']},
 {k:'温暖与亲密',kw:['温暖','温柔','亲密','温馨','抚慰','呵护']},
 {k:'欢愉感',kw:['欢愉','欢乐','快乐','喜悦','欢庆','嬉戏']},
 {k:'天真感',kw:['天真','纯真','童趣','稚拙','童真']},
 {k:'空灵与悠远',kw:['空灵','悠远','幽远','淡远','缥缈','空寂']},
 {k:'混乱与眩晕',kw:['混乱','眩晕','迷乱','眼花缭乱','失序','混沌']},
 {k:'疏离感',kw:['疏离','陌生化','隔阂','冷漠','异化','距离感']}
];
const dimensions=[{key:'material',name:'材料',color:'#9a7c38'},{key:'method',name:'组织方法',color:'#638073'},{key:'question',name:'问题意识',color:'#a86452'},{key:'mood',name:'意境',color:'#7c7194'}];
function poolsFromAttributes(a,questions){return {material:a.material.slice(0,5),method:a.method.slice(0,5),question:questions.slice(0,3),mood:a.mood.slice(0,5)};}
function spinSelection(pools,state,only,random=Math.random){
 const out={...state.selected};
 for(const {key} of dimensions){
  const list=pools[key];
  if(!list.length){out[key]=null;continue;}
  if(!list.some(x=>x.k===out[key]))out[key]=list[0].k;
  if(state.locked[key]||(only&&only!==key))continue;
  const options=list.length>1?list.filter(x=>x.k!==out[key]):list;
  out[key]=options[Math.floor(random()*options.length)].k;
 }
 return out;
}
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const point=(r,d)=>[230+r*Math.cos(d*Math.PI/180),230+r*Math.sin(d*Math.PI/180)];
function sector(inner,outer,start,end){
 const a=point(outer,start),b=point(outer,end),c=point(inner,end),d=point(inner,start),large=end-start>180?1:0;
 return `M${a} A${outer},${outer} 0 ${large} 1 ${b} L${c} A${inner},${inner} 0 ${large} 0 ${d} Z`;
}
function mount(box,{attributes,questions,unlocked,suffix=''}){
 if(box._dispose)box._dispose();
 if(!unlocked){box.innerHTML='<div class="alock"><div class="ico">◉</div><h4>刷完第 1 关即可解锁</h4><p>个人属性形成后，会成为你的创作转盘。</p></div>';return;}
 const pools=poolsFromAttributes(attributes,questions),storageKey='ac_creative'+suffix;
 let saved={};try{saved=JSON.parse(localStorage.getItem(storageKey)||'{}')||{};}catch(_){}
 const state={selected:{},locked:{},combinations:[]};
 for(const {key} of dimensions){state.selected[key]=pools[key].some(x=>x.k===saved.selected?.[key])?saved.selected[key]:(pools[key][0]?.k||null);state.locked[key]=saved.locked?.[key]===true;}
 state.combinations=Array.isArray(saved.combinations)?saved.combinations.filter(c=>c&&dimensions.every(d=>typeof c[d.key]==='string')).slice(0,50):[];
 let busy=false,timer,disposed=false;
 box._dispose=()=>{disposed=true;clearTimeout(timer);};
 const persist=()=>{try{localStorage.setItem(storageKey,JSON.stringify(state));return true;}catch(_){message('本机存储空间不足，暂时无法保存。');return false;}};
 const message=t=>{box.querySelector('.cw-status').textContent=t;};
 const current=()=>Object.fromEntries(dimensions.map(({key})=>{const item=pools[key].find(x=>x.k===state.selected[key]);return [key,item?.text||item?.k||''];}));
 const complete=()=>dimensions.every(d=>pools[d.key].length);
 const ring=(d,i)=>{
  const list=pools[d.key],outer=222-i*44,inner=outer-40,mid=(outer+inner)/2;
  const count=list.length||1,step=360/count;
  let segments='';
  for(let n=0;n<count;n++){
   const angle=-90+n*step,pt=point(mid,angle),item=list[n];
   const shape=count===1?`<circle cx="230" cy="230" r="${mid}" fill="none" stroke="${d.color}" stroke-opacity=".15" stroke-width="40"/>`:`<path d="${sector(inner,outer,angle-step/2+1,angle+step/2-1)}" fill="${d.color}" fill-opacity="${n%2?'.18':'.11'}" stroke="${d.color}" stroke-opacity=".2"/>`;
   segments+=`<g data-choice="${n}">${shape}<text x="${pt[0]}" y="${pt[1]}" transform="rotate(${n*step} ${pt[0]} ${pt[1]})" text-anchor="middle" dominant-baseline="middle" fill="${d.color}">${esc(item?.k||'待积累')}</text></g>`;
  }
  return `<g class="cw-ring" data-ring="${d.key}" role="button" tabindex="0" aria-label="转动${d.name}，左右方向键选择">${segments}</g>`;
 };
 box.innerHTML=`<div class="cw-heading"><div class="cw-eyebrow">把偏好变成创作的起点</div><h3>创作转盘</h3><p>来自你的个人属性 · 拖动圆环，或点一下转动<br>由外至内：材料 / 组织方法 / 问题意识 / 意境</p></div>
 <div class="cw-disc"><svg viewBox="0 0 460 460" aria-label="四层同心创作转盘">${dimensions.map(ring).join('')}<path d="M230 7 L223 19 L237 19 Z" fill="#544936"/><line x1="230" y1="24" x2="230" y2="186" stroke="#544936" stroke-opacity=".35" stroke-dasharray="2 5" pointer-events="none"/><circle cx="230" cy="230" r="39" fill="#f5f3ee"/><text x="230" y="228" text-anchor="middle" class="cw-center">创作</text><text x="230" y="246" text-anchor="middle" class="cw-center-small">四种相遇</text></svg></div>
 <div class="cw-controls">${dimensions.map(d=>`<div class="cw-row" style="--wheel-color:${d.color}"><span class="cw-label">${d.name}</span><span class="cw-value" data-value="${d.key}"></span><button data-spin="${d.key}" aria-label="单独转动${d.name}">↻</button><button data-lock="${d.key}" aria-label="锁定${d.name}" aria-pressed="false">锁定</button></div>`).join('')}</div>
 <div class="cw-actions"><button class="cw-primary" data-all>转动未锁定的圈</button><button data-save>留下这组</button></div><p class="cw-status" role="status" aria-live="polite"></p>
 <p class="cw-note">词项与个人属性同步。问题意识沿用同一组提问；缺少的维度会在继续刷卡后逐渐形成。组合只保存在这台设备。</p>
 <div class="cw-saved"><h4>留下的组合 <span data-count></span></h4><div data-saved></div></div>`;
 const angles={};
 function update(animate=false){
  for(const d of dimensions){
   const list=pools[d.key],index=list.findIndex(x=>x.k===state.selected[d.key]),target=index<0?0:-index*360/list.length;
   const g=box.querySelector(`[data-ring="${d.key}"]`);
   const prev=angles[d.key];
   angles[d.key]=animate&&prev!==undefined?prev+720+((target-prev)%360+360)%360:target;
   g.style.transition=animate?'transform 900ms cubic-bezier(.18,.75,.22,1)':'none';g.style.transform=`rotate(${angles[d.key]}deg)`;
   g.setAttribute('aria-disabled',String(busy||state.locked[d.key]||!list.length));
   g.setAttribute('aria-label',`${d.name}：${state.selected[d.key]||'待积累'}${state.locked[d.key]?'，已锁定':'，左右方向键选择'}`);
   const item=list[index];box.querySelector(`[data-value="${d.key}"]`).textContent=item?.text||item?.k||'尚未形成，继续积累';
   const lock=box.querySelector(`[data-lock="${d.key}"]`);lock.textContent=state.locked[d.key]?'已锁定':'锁定';lock.setAttribute('aria-pressed',String(state.locked[d.key]));lock.disabled=busy||!list.length;
   box.querySelector(`[data-spin="${d.key}"]`).disabled=busy||state.locked[d.key]||list.length<2;
  }
  box.querySelector('[data-all]').disabled=busy||!dimensions.some(d=>!state.locked[d.key]&&pools[d.key].length>1);
  box.querySelector('[data-save]').disabled=busy||!complete();
 }
 function renderSaved(){
  box.querySelector('[data-count]').textContent=state.combinations.length;
  box.querySelector('[data-saved]').innerHTML=state.combinations.length?state.combinations.map((c,i)=>`<article class="cw-combination"><div class="cw-combination-title">组合 ${String(state.combinations.length-i).padStart(2,'0')}<button data-delete="${i}" aria-label="删除组合 ${state.combinations.length-i}">删除</button></div>${dimensions.map(d=>`<p><span>${d.name}</span>${esc(c[d.key])}</p>`).join('')}</article>`).join(''):'<p class="cw-note">遇到有意思的组合，就留下来。</p>';
 }
 function turn(only,chosen){
  if(busy)return;
  if(only&&(state.locked[only]||!pools[only].length))return;
  const previous={...state.selected};
  state.selected=chosen?{...state.selected,[only]:chosen}:spinSelection(pools,state,only);
  busy=true;
  // Animate only rings whose choices actually changed; locked circles never move.
  const oldAngles={...angles};update(true);
  for(const d of dimensions)if(previous[d.key]===state.selected[d.key]){angles[d.key]=oldAngles[d.key];box.querySelector(`[data-ring="${d.key}"]`).style.transform=`rotate(${oldAngles[d.key]}deg)`;}
  persist();message('转动中…');
  timer=setTimeout(()=>{if(disposed)return;busy=false;for(const d of dimensions){const g=box.querySelector(`[data-ring="${d.key}"]`);g.style.transition='none';}update();message(complete()?'新的组合已就位。':'已有的维度已就位，继续刷卡积累其余维度。');},950);
 }
 box.onclick=e=>{
  const b=e.target.closest('button');if(!b||!box.contains(b)||b.disabled)return;
  if(b.hasAttribute('data-all'))turn();
  if(b.dataset.spin)turn(b.dataset.spin);
  if(b.dataset.lock){state.locked[b.dataset.lock]=!state.locked[b.dataset.lock];persist();update();}
  if(b.hasAttribute('data-save')){
   const c=current();if(state.combinations.some(x=>dimensions.every(d=>x[d.key]===c[d.key]))){message('这组已经留下了。');return;}
   if(state.combinations.length>=50){message('已留下 50 组，删除一些后再保存。');return;}
   state.combinations.unshift(c);if(persist()){renderSaved();message('已留下这组。');}else state.combinations.shift();
  }
  if(b.dataset.delete!==undefined){const previous=state.combinations.slice();state.combinations.splice(Number(b.dataset.delete),1);if(persist()){renderSaved();message('已删除该组合。');}else state.combinations=previous;}
 };
 box.querySelectorAll('[data-ring]').forEach(g=>{
  const key=g.dataset.ring;let drag=null;
  const angle=e=>{const rect=g.ownerSVGElement.getBoundingClientRect();return Math.atan2(e.clientY-rect.top-rect.height/2,e.clientX-rect.left-rect.width/2)*180/Math.PI;};
  g.onpointerdown=e=>{if(busy||state.locked[key]||pools[key].length<2)return;drag={last:angle(e),delta:0};g.setPointerCapture(e.pointerId);};
  g.onpointermove=e=>{if(!drag)return;const a=angle(e);drag.delta+=(a-drag.last+540)%360-180;drag.last=a;g.style.transition='none';g.style.transform=`rotate(${angles[key]+drag.delta}deg)`;};
  g.onpointerup=()=>{if(!drag)return;const delta=drag.delta;drag=null;const list=pools[key],idx=list.findIndex(x=>x.k===state.selected[key]);const steps=Math.round(delta/(360/list.length));const target=list[((idx-steps)%list.length+list.length)%list.length].k;turn(key,Math.abs(delta)<8?null:target);};
  g.onpointercancel=()=>{drag=null;update();};
  g.onkeydown=e=>{if(!['ArrowLeft','ArrowRight','Enter',' '].includes(e.key))return;e.preventDefault();if(e.key==='Enter'||e.key===' ')turn(key);else{const list=pools[key];if(!list.length)return;const idx=list.findIndex(x=>x.k===state.selected[key]);turn(key,list[(idx+(e.key==='ArrowRight'?1:-1)+list.length)%list.length].k);}};
 });
 update();renderSaved();if(!attributes.n)message('还没有喜欢的作品，右滑喜欢的卡片来形成个人属性。');
}
const api={moods,poolsFromAttributes,spinSelection,mount};
if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.CreativeTools=api;
})(typeof globalThis!=='undefined'?globalThis:this);
