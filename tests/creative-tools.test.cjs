const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const source=fs.existsSync('creative-tools.js')?require('../creative-tools.js'):{};
test('wheel uses only the profile visible candidates, with the exact displayed questions',()=>{
 assert.equal(typeof source.poolsFromAttributes,'function');
 const a={material:[{k:'纸',s:2}],method:[{k:'重复',s:1}],mood:[{k:'荒诞感',s:1}]};
 const q=[{k:'秩序与荒诞',text:'规则为何荒诞?'}];
 const p=source.poolsFromAttributes(a,q);
 assert.deepEqual(p.material,[{k:'纸',s:2}]);
 assert.deepEqual(p.method,a.method); assert.deepEqual(p.mood,a.mood);
 assert.deepEqual(p.question,q);
 assert.deepEqual(source.poolsFromAttributes({material:[],method:[],mood:[]},[]),{material:[],method:[],question:[],mood:[]});
});
test('locked ring stays unchanged; spinning one ring changes no other selection',()=>{
 assert.equal(typeof source.spinSelection,'function');
 const pools={material:[{k:'纸'},{k:'石'}],method:[{k:'重复'},{k:'拼贴'}],question:[],mood:[{k:'寂静'}]};
 const state={selected:{material:'纸',method:'重复',mood:'寂静'},locked:{material:true}};
 const next=source.spinSelection(pools,state,undefined,()=>0.99);
 assert.equal(next.material,'纸');assert.equal(next.method,'拼贴');assert.equal(next.mood,'寂静');assert.equal(next.question,null);
 assert.equal(state.selected.method,'重复');
 const single=source.spinSelection(pools,{...state,locked:{}},'material',()=>0.99);
 assert.equal(single.material,'石');assert.equal(single.method,'重复');
});
test('mood attribution uses only liked works and doubles favourite weight',()=>{
 const html=fs.readFileSync('index.html','utf8');
 const attrs=html.slice(html.indexOf('const ATTR ='),html.indexOf('/* ============ 个人(信息'));
 const context={CreativeTools:source,WORKS:[{id:1,bg:'孤独与寂寞',how:'静坐',why:'沉默',cat:'行为',t:'独处'},{id:2,bg:'欢乐',how:'游戏',why:'快乐',cat:'行为',t:'欢庆'}],lib:new Set([1]),favs:new Set([1])};
 vm.createContext(context);vm.runInContext(attrs,context);
 const a=vm.runInContext('computeAttr()',context);
 assert.ok(Array.isArray(a.mood),'profile must include mood');
 assert.ok(a.mood.some(x=>x.k==='孤独感'&&x.s===2));
 assert.ok(!a.mood.some(x=>x.k==='欢愉感'));
 context.lib.clear();assert.equal(vm.runInContext('computeAttr().mood.length',context),0);
});
