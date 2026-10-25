const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--no-sandbox']});const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const [d,o] of [['spray','todohome_pulverizador_portada.jpg'],['botes','todohome_botes_portada.jpg']]){
await p.goto('file://'+require('path').resolve(d)+'/portada.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.screenshot({path:o,type:'jpeg',quality:93});}
await b.close()})();
