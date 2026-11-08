const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true,args:['--disable-gpu']});
 const context=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:2});
 const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:8842/',{waitUntil:'domcontentloaded'});
 await page.locator('#sgGateGo').click();await page.waitForTimeout(1200);console.log('signed in');
 if(await page.locator('#sgGateSkip').isVisible())await page.locator('#sgGateSkip').click();await page.locator('#btnPerson').click();await page.locator('[data-tab="creative"]').click();
 assert.match(await page.locator('#pCreative').innerText(),/刷完第 1 关/);
 await page.evaluate(()=>{localStorage.setItem('ac_rounds','1');localStorage.setItem('ac_lib',JSON.stringify(WORKS.slice(0,150).map(w=>w.id)));localStorage.setItem('ac_favs','[1,2,3]');});
 await page.reload({waitUntil:'domcontentloaded'});
 if(await page.locator('#sgGateSkip').isVisible())await page.locator('#sgGateSkip').click();await page.locator('#btnPerson').click();await page.locator('[data-tab="attr"]').click();
 assert.match(await page.locator('#pAttr').innerText(),/意 境/);
 const expected=await page.evaluate(()=>CreativeTools.poolsFromAttributes(computeAttr(),profileQuestions(computeAttr())));
 await page.locator('[data-tab="creative"]').click();
 for(const key of ['material','method','question','mood'])assert.equal(await page.locator(`[data-value="${key}"]`).innerText(),expected[key][0].text||expected[key][0].k);
 await page.screenshot({path:'/tmp/art-wheel-mobile.png'});
 await page.locator('[data-lock="material"]').click();
 const before=await page.locator('[data-value="material"]').innerText();
 const transform=await page.locator('[data-ring="material"]').getAttribute('style');
 await page.locator('[data-all]').click();await page.waitForTimeout(1100);
 assert.equal(await page.locator('[data-value="material"]').innerText(),before);
 assert.equal(await page.locator('[data-ring="material"]').getAttribute('style'),transform);
 await page.locator('[data-save]').click();assert.equal(await page.locator('.cw-combination').count(),1);
 await page.locator('[data-save]').click();assert.equal(await page.locator('.cw-combination').count(),1);
 await page.reload({waitUntil:'domcontentloaded'});if(await page.locator('#sgGateSkip').isVisible())await page.locator('#sgGateSkip').click();await page.locator('#btnPerson').click();await page.locator('[data-tab="creative"]').click();
 assert.equal(await page.locator('.cw-combination').count(),1);
 assert.equal(await page.locator('[data-lock="material"]').getAttribute('aria-pressed'),'true');
 await page.evaluate(()=>{window.originalStorageSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k.startsWith('ac_creative'))throw new Error('quota');return window.originalStorageSet.call(this,k,v);};});
 await page.locator('[data-delete="0"]').click();
 assert.match(await page.locator('.cw-status').innerText(),/存储空间不足/);
 assert.equal(await page.locator('.cw-combination').count(),1);
 await page.evaluate(()=>Storage.prototype.setItem=window.originalStorageSet);
 await page.locator('[data-delete="0"]').click();assert.equal(await page.locator('.cw-combination').count(),0);
 for(const key of ['method','question','mood'])await page.locator(`[data-lock="${key}"]`).click();
 assert.equal(await page.locator('[data-all]').isDisabled(),true);
 await page.locator('[data-lock="method"]').click();
 const methodBefore=await page.locator('[data-value="method"]').innerText();
 await page.locator('[data-ring="method"]').focus();await page.keyboard.press('ArrowRight');await page.waitForTimeout(1100);
 assert.notEqual(await page.locator('[data-value="method"]').innerText(),methodBefore);
 // Drag the unlocked method circle clockwise by about one segment.
 await page.locator('.cw-disc').scrollIntoViewIfNeeded();
 const svgRect=await page.locator('.cw-disc svg').boundingBox();
 const dragBefore=await page.locator('[data-value="method"]').innerText();
 const cx=svgRect.x+svgRect.width/2,cy=svgRect.y+svgRect.height/2,r=158*svgRect.width/460;
 await page.mouse.move(cx+r,cy);await page.mouse.down();
 for(let n=1;n<=10;n++){const a=n*72/10*Math.PI/180;await page.mouse.move(cx+r*Math.cos(a),cy+r*Math.sin(a));}
 await page.mouse.up();await page.waitForTimeout(1100);
 assert.notEqual(await page.locator('[data-value="method"]').innerText(),dragBefore);
 // Selected segment's label lies on the twelve-o'clock pointer after settling.
 for(const key of ['material','method','question','mood']){
  const aligned=await page.evaluate(key=>{const g=document.querySelector(`[data-ring="${key}"]`),s=JSON.parse(localStorage.getItem('ac_creative'));const t=[...g.querySelectorAll('text')].find(t=>t.textContent===s.selected[key]);const p=new DOMPoint(+t.getAttribute('x'),+t.getAttribute('y')).matrixTransform(g.getCTM());const c=new DOMPoint(230,230).matrixTransform(g.ownerSVGElement.getCTM());return Math.abs(p.x-c.x)<1&&p.y<c.y;},key);
  assert.equal(aligned,true);
 }
 // Mode separation.
 await page.evaluate(()=>{localStorage.setItem('ac_mode','visual');localStorage.setItem('ac_rounds_v','1');localStorage.setItem('ac_lib_v','[1]');});
 await page.reload({waitUntil:'domcontentloaded'});if(await page.locator('#sgGateSkip').isVisible())await page.locator('#sgGateSkip').click();await page.locator('#btnPerson').click();await page.locator('[data-tab="creative"]').click();
 assert.equal(await page.locator('.cw-combination').count(),0);
 assert.equal(await page.locator('[data-lock="material"]').getAttribute('aria-pressed'),'false');
 // Empty mood does not fabricate an option.
 await page.evaluate(()=>CreativeTools.mount(document.getElementById('pCreative'),{attributes:{n:1,material:[{k:'纸'}],method:[{k:'重复'}],mood:[]},questions:[],unlocked:true,suffix:'_test'}));
 assert.match(await page.locator('[data-value="mood"]').innerText(),/尚未形成/);
 assert.equal(await page.locator('[data-save]').isDisabled(),true);
 await page.evaluate(()=>localStorage.setItem('ac_mode','all'));
 await page.reload({waitUntil:'domcontentloaded'});if(await page.locator('#sgGateSkip').isVisible())await page.locator('#sgGateSkip').click();await page.locator('#btnPerson').click();await page.locator('[data-tab="creative"]').click();
 await page.setViewportSize({width:320,height:740});
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
 await page.waitForTimeout(300);await page.screenshot({path:'/tmp/art-wheel-small.png'});
 await page.setViewportSize({width:1100,height:900});await page.screenshot({path:'/tmp/art-wheel-desktop.png'});
 await page.evaluate(()=>navigator.serviceWorker.ready);await page.waitForTimeout(2000);
 const cachesList=await page.evaluate(async()=>{const c=await caches.open('ac-v83-shell');return (await c.keys()).map(x=>new URL(x.url).pathname);});
 assert.ok(cachesList.includes('/creative-tools.js'));assert.ok(cachesList.includes('/creative-tools.css'));
 await context.setOffline(true);await page.reload({waitUntil:'domcontentloaded'});if(await page.locator('#sgGateSkip').isVisible())await page.locator('#sgGateSkip').click();await page.locator('#btnPerson').click();await page.locator('[data-tab="creative"]').click();assert.equal(await page.locator('.cw-ring').count(),4);
 assert.deepEqual(errors,[]);
 console.log('PASS: profile parity, locked gate, spin, locks, save/dedup/delete/reload, keyboard, mode isolation, missing mood, 320px layout, offline, no page errors');
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
