const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs');
const path=require('node:path');const source=path.resolve(__dirname,'../interest-radar.js');
const api=fs.existsSync(source)?require(source):{};
test('axes use the profile weighted scores, top six, fixed 100% scale',()=>{
 assert.equal(typeof api.axesFromProfile,'function');
 const rows=Array.from({length:7},(_,i)=>({k:'项'+i,s:9-i}));const a=api.axesFromProfile({wsum:10,concern:rows},'concern');
 assert.equal(a.length,6);assert.equal(a[0].k,'项0');assert.equal(a[0].percent,90);assert.equal(a[5].k,'项5');assert.equal(a[5].percent,40);
});
test('sparse and empty profiles never invent scored categories',()=>{
 assert.equal(typeof api.axesFromProfile,'function');
 const axes=api.axesFromProfile({wsum:2,mood:[{k:'孤独感',s:2}]},'mood');
 assert.equal(axes.length,6);assert.equal(axes[0].percent,100);assert.equal(axes.filter(x=>x.k).length,1);
 assert.ok(api.axesFromProfile({wsum:0,mood:[]},'mood').every(x=>x.percent===0&&!x.k));
});
test('axis drilldown uses the same text fields and keyword matching as profile',()=>{
 assert.equal(typeof api.matchingWorks,'function');
 const works=[{id:1,t:'a',bg:'无',how:'纸张'},{id:2,t:'b',verse:'纸上'},{id:3,t:'纸张'},{id:4,t:'无'}];
 assert.deepEqual(api.matchingWorks(works,{kw:['纸']} ).map(x=>x.id),[1,2,3]);
 assert.deepEqual(api.matchingWorks(works,null),[]);
});
