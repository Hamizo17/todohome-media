// node rend.js <dir> [t1,t2,...]  -> frames en <dir>/fr/ o comprobaciones <dir>/chk_t.jpg
const {chromium}=require('playwright');(async()=>{const dir=process.argv[2],only=process.argv[3];
const fs=require('fs');const D=JSON.parse(fs.readFileSync(dir+'/spec.json')).dur;
const b=await chromium.launch({args:['--no-sandbox','--allow-file-access-from-files']});
const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+require('path').resolve(dir)+'/v.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
if(!only)fs.mkdirSync(dir+'/fr',{recursive:true});
const list=only?only.split(',').map(Number):[...Array(Math.round(D*30)).keys()];
for(const i of list){await p.evaluate(t=>seek(t),only?i:i/30);await p.screenshot({path:only?`${dir}/chk_${i}.jpg`:`${dir}/fr/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}
await b.close()})();
