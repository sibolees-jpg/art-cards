const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const {spawn}=require('node:child_process'),assert=require('node:assert/strict');
(async()=>{const server=spawn('python3',['-m','http.server','8843','--bind','127.0.0.1'],{cwd:require('node:path').resolve(__dirname,'..'),stdio:'ignore'});let browser;
try{await new Promise(r=>setTimeout(r,500));browser=await chromium.launch({channel:'chrome',headless:true,args:['--disable-gpu']});const context=await browser.newContext({viewport:{width:1100,height:900}});const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:8843/',{waitUntil:'domcontentloaded'});await page.locator('#sgGateGo').click();await page.waitForTimeout(1200);
await page.locator('#btnLearn').click();assert.equal(await page.locator('#gmapEmpty').isVisible(),true);
await page.evaluate(()=>{localStorage.setItem('ac_lib',JSON.stringify(WORKS.slice(0,100).map(w=>w.id)));localStorage.setItem('ac_favs','[1,2,3]');localStorage.setItem('ac_rounds','1');});
await page.reload({waitUntil:'domcontentloaded'});await page.locator('#btnLearn').click();
assert.equal(await page.locator('[data-ir-axis]').count(),6);
for(const key of ['concern','material','method','mood']){
 await page.locator(`[data-ir-view="${key}"]`).click();
 const state=await page.evaluate(key=>({expected:computeAttr()[key].slice(0,6).map(x=>x.k),got:[...document.querySelectorAll('[data-ir-axis]:not(:disabled) span')].map(x=>x.textContent)}),key);
 assert.deepEqual(state.got,state.expected);
 await page.locator('[data-ir-axis="1"]').click();
 const count=await page.locator('[data-ir-count]').innerText();assert.ok(parseInt(count)>0);
 const expectedIds=await page.evaluate(key=>{const name=document.querySelector('[data-ir-title]').textContent,b=ATTR[key].find(x=>x.k===name);return WORKS.filter(w=>lib.has(w.id)&&b.kw.some(k=>gTextOf(w).includes(k))).map(w=>String(w.id));},key);
 const actual=await page.locator('[data-ir-open]').evaluateAll(es=>es.map(e=>e.dataset.irOpen));assert.deepEqual(actual,expectedIds.slice(0,12));
}
await page.locator('[data-ir-view="concern"]').click();
await page.locator('[data-ir-check]').nth(0).check();await page.locator('[data-ir-check]').nth(1).check();assert.equal(await page.locator('#gAnalyze').isEnabled(),true);
const selected=await page.evaluate(()=>[...gSel]);await page.locator('[data-ir-view="mood"]').click();assert.deepEqual(await page.evaluate(()=>[...gSel]),selected);
await page.locator('#gAnalyze').click();assert.equal(await page.locator('#gResult').isVisible(),true);await page.locator('#grClose').click();
await page.locator('[data-ir-open]').first().click();assert.equal(await page.locator('#detail').isVisible(),true);await page.locator('[data-close="detail"]').click();
await page.locator('#gClearSel').click();assert.equal(await page.evaluate(()=>gSel.size),0);assert.equal(await page.locator('#gAnalyze').isDisabled(),true);
await page.locator('[data-gt="rev"]').click();assert.equal(await page.locator('#gRevView').isVisible(),true);await page.locator('[data-gt="map"]').click();
await page.locator('[data-ir-view="material"]').click();await page.reload({waitUntil:'domcontentloaded'});await page.locator('#btnLearn').click();assert.equal(await page.locator('[data-ir-view="material"]').getAttribute('aria-pressed'),'true');
await page.locator('[data-ir-view="concern"]').click();await page.screenshot({path:'/tmp/radar-desktop.png'});
await page.setViewportSize({width:320,height:740});await page.waitForTimeout(300);
const fits=await page.evaluate(()=>{const root=document.getElementById('interestRadar'),rc=root.getBoundingClientRect();return [...document.querySelectorAll('[data-ir-axis]')].every(b=>{const x=b.getBoundingClientRect();return x.left>=rc.left&&x.right<=rc.right;});});assert.equal(fits,true);
assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
await page.screenshot({path:'/tmp/radar-mobile.png'});
await page.locator('[data-ir-axis="2"]').click();assert.equal(await page.locator('[data-ir-axis="2"]').getAttribute('aria-pressed'),'true');
// Empty view and a profile with one result.
await page.evaluate(()=>{gRadar.destroy();gRadar=InterestRadar.mount(document.getElementById('interestRadar'),{profile:{wsum:2,concern:[],mood:[{k:'孤独感',s:2}]},buckets:ATTR,works:[],favourites:new Set(),getSelected:()=>new Set(),onToggle:()=>{},onOpen:()=>{}});});
assert.equal(await page.locator('.ir-no-axis').isVisible(),true);await page.locator('[data-ir-view="mood"]').click();assert.equal(await page.locator('[data-ir-axis]:disabled').count(),5);assert.match(await page.locator('[data-ir-axis="0"]').innerText(),/100%/);
await page.reload({waitUntil:'domcontentloaded'});await page.locator('#btnLearn').click();await page.evaluate(()=>navigator.serviceWorker.ready);await page.waitForTimeout(1200);await context.setOffline(true);await page.reload({waitUntil:'domcontentloaded'});await page.locator('#btnLearn').click();assert.equal(await page.locator('[data-ir-axis]').count(),6);
assert.deepEqual(errors,[]);console.log('PASS: four profile views, exact evidence lists, selection across views, comparison, detail, review, remembered view, empty/sparse data, 320px labels, offline; zero page errors');
}finally{if(browser)await browser.close();server.kill();}})().catch(e=>{console.error(e);process.exit(1)});
