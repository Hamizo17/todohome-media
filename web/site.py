import os, sys, html, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import PRODUCTS, CATS, amazon_url
from photos import AMAZON_IMG
from guides_data import GUIDES, GUIDE_ALT
OUT = os.environ.get("OUT", "public/")
BASE = "https://todohome-es.vercel.app"
EMAIL = "todo.hme@gmail.com"
DISCLOSURE = "Como Afiliado de Amazon, TODOHOME obtiene ingresos por las compras adscritas que cumplen los requisitos aplicables."
TIKTOK, INSTA, PIN = "https://www.tiktok.com/@todo.home", "https://www.instagram.com/todohome/", "https://www.pinterest.es/todohome/"
e = html.escape
BYSLUG = {p["slug"]: p for p in PRODUCTS}
HERO = ["robot-friegasuelos-cecotec", "tostadora-philips", "perchero-vasagle"]
CAT_IMG = {"cocina": "tostadora-philips", "limpieza": "robot-friegasuelos-cecotec", "hogar": "perchero-vasagle"}
CAT_TXT = {"cocina": "Cocina más rápido y con menos aceite.",
           "limpieza": "Limpia en la mitad de tiempo y sin esfuerzo.",
           "hogar": "Orden, confort y calor para tu casa."}

def pic(i, w, h):
    if os.environ.get("PREVIEW"):  # vista previa local sin red
        return f"img/{i}.jpg"
    return f"https://picsum.photos/id/{i}/{w}/{h}"

PHOTOS = {999: "Annie Spratt", 292: "Webvilla", 625: "Breather"}  # Unsplash, servidas por picsum.photos

ICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#1A1C1E"/>'
        '<path d="M15 31 32 16l17 15h-4v17H19V31z" fill="#FFFFFF"/><rect x="28" y="37" width="8" height="11" rx="2" fill="#FF5310"/></svg>')
MARK = ('<svg class="mark" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14"/>'
        '<path d="M15 31 32 16l17 15h-4v17H19V31z" fill="#FFFFFF"/><rect x="28" y="37" width="8" height="11" rx="2" fill="#FF5310"/></svg>')

def ico(d):
    return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{d}</svg>'
I_SEARCH = ico('<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>')
I_CART = ico('<path d="M3 4h2l2.4 11h11l2-8H6.2"/><circle cx="9" cy="19.5" r="1.5"/><circle cx="17" cy="19.5" r="1.5"/>')
I_LOCK = ico('<rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>')
I_TRUCK = ico('<path d="M2 6h12v10H2zM14 9h4l3 3v4h-7"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>')
I_BACK = ico('<path d="M4 12a8 8 0 1 0 2.3-5.7"/><path d="M4 4v4h4"/>')
I_CHECK = ico('<path d="m5 12 4 4 10-10"/>')
I_ARROW = ico('<path d="M5 12h14M13 6l6 6-6 6"/>')
TRUST = [(I_LOCK, "Pago seguro", "Compras en Amazon, con su protección al comprador."),
         (I_TRUCK, "Envío rápido", "Lo envía Amazon. Muchos productos con Prime."),
         (I_BACK, "Devoluciones fáciles", "Las gestiona Amazon según sus condiciones."),
         (I_CHECK, "Elegidos a mano", "Solo productos prácticos para el día a día, sin relleno.")]

CSS = """
@font-face{font-family:"Archivo";src:url("fonts/archivo.woff2") format("woff2-variations"),url("fonts/archivo.woff2") format("woff2");font-weight:100 900;font-stretch:62% 125%;font-display:swap}
:root{
  --bg:#FFFFFF; --soft:#F5F5F2; --tile:#EEEEEA; --ink:#141414; --ink-2:#45454A; --steel:#77777C; --line:#E7E7E2;
  --hot:#FF5310; --hot-2:#E54400; --amber:#FF9A1F; --hot-soft:#FFF0E8;
  --grad:linear-gradient(155deg,#FF3D00 0%,#FF6A13 42%,#FF9C2A 100%);
  --font:"Archivo",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --fs-small:.875rem; --fs-body:1rem; --fs-lead:clamp(1.0625rem,1rem + .35vw,1.25rem);
  --fs-h3:clamp(1.0625rem,1rem + .25vw,1.1875rem); --fs-h2:clamp(1.75rem,1.3rem + 1.7vw,2.75rem);
  --fs-display:clamp(2.5rem,1.3rem + 4.2vw,5rem);
  --m:clamp(16px,4vw,48px); --max:1320px; --r:22px; --r-s:14px;
  --ease-out:cubic-bezier(.22,1,.36,1); --t-fast:160ms; --t-med:320ms;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:90px;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:400 var(--fs-body)/1.55 var(--font);-webkit-font-smoothing:antialiased}
::selection{background:var(--hot);color:#fff}
img{display:block;max-width:100%;height:auto}
a{color:inherit;text-underline-offset:.22em}
h1,h2,h3{margin:0;font-weight:800;letter-spacing:-.035em;line-height:1.02;text-wrap:balance}
p{margin:0;text-wrap:pretty}
:focus-visible{outline:3px solid var(--hot);outline-offset:3px;border-radius:8px}
.wrap{width:min(100% - 2*var(--m),var(--max));margin-inline:auto}
.num-t{font-variant-numeric:tabular-nums}
.ico{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;flex:none}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:.8125rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase}

.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:52px;padding:0 26px;border-radius:999px;border:0;background:var(--ink);color:#fff;font:inherit;font-weight:700;text-decoration:none;cursor:pointer;transition:background var(--t-fast),color var(--t-fast),transform var(--t-fast) var(--ease-out)}
.btn:hover{background:var(--hot)}
.btn:active{transform:scale(.97)}
.btn .ico{width:18px;height:18px}
.btn.hot{background:var(--hot)}.btn.hot:hover{background:var(--hot-2)}
.btn.white{background:#fff;color:var(--ink)}.btn.white:hover{background:var(--ink);color:#fff}
.btn.line{background:transparent;color:#fff;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.7)}.btn.line:hover{background:#fff;color:var(--ink)}
.btn.ghost{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1.5px var(--ink)}.btn.ghost:hover{background:var(--ink);color:#fff}

/* barra superior y cabecera */
.topbar{background:var(--ink);color:#fff;font-size:.8125rem;font-weight:500;text-align:center;padding:9px 16px;letter-spacing:.01em}
.topbar b{color:var(--amber);font-weight:700}
.hdr{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.92);-webkit-backdrop-filter:saturate(1.6) blur(14px);backdrop-filter:saturate(1.6) blur(14px);box-shadow:0 1px 0 var(--line)}
.hdr .in{display:flex;align-items:center;gap:22px;padding-block:12px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-stretch:118%;letter-spacing:-.01em;text-decoration:none;font-size:1.125rem}
.mark{width:36px;height:36px;fill:var(--ink)}
.hdr nav{display:flex;gap:4px;background:var(--soft);border-radius:999px;padding:5px;margin-inline:auto;box-shadow:inset 0 0 0 1px var(--line)}
.hdr nav a{text-decoration:none;white-space:nowrap;font-weight:600;font-size:.9375rem;padding:8px 16px;border-radius:999px;transition:background var(--t-fast),color var(--t-fast)}
.hdr nav a:hover{background:var(--ink);color:#fff}
.search{width:min(300px,30vw);display:flex;align-items:center;gap:10px;background:var(--soft);border-radius:999px;padding:0 16px;min-height:44px;box-shadow:inset 0 0 0 1px var(--line)}
.search:focus-within{box-shadow:inset 0 0 0 2px var(--hot)}
.search .ico{color:var(--steel);width:19px;height:19px}
.search input{all:unset;flex:1;font-size:.9375rem;min-width:0}
.search input::placeholder{color:var(--steel)}
.cart{display:inline-flex;align-items:center;gap:8px;font-weight:700;text-decoration:none;min-height:44px;padding:0 18px;border-radius:999px;background:var(--hot);color:#fff;white-space:nowrap;transition:background var(--t-fast)}
.cart:hover{background:var(--ink)}
.cart .ico{width:19px;height:19px}

/* portada: panel naranja con producto protagonista */
.hero{padding-top:clamp(12px,2vw,24px)}
.stage{position:relative;overflow:hidden;border-radius:clamp(22px,3vw,36px);background:var(--grad);color:#fff;isolation:isolate}
.stage::before{content:"";position:absolute;inset:auto -10% -40% 30%;height:80%;background:radial-gradient(closest-side,rgba(255,214,140,.55),transparent);z-index:-1}
.stage .glass{margin:clamp(14px,2.4vw,34px);border-radius:clamp(18px,2.4vw,28px);background:rgba(60,22,4,.26);box-shadow:inset 0 0 0 1px rgba(255,255,255,.16),0 30px 80px rgba(90,25,0,.25);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);padding:clamp(22px,3.4vw,52px);display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr) minmax(0,.62fr);gap:clamp(20px,3vw,48px);align-items:center;min-height:min(78vh,640px)}
.stage .eyebrow{background:rgba(255,255,255,.16);padding:7px 14px;border-radius:999px}
.stage h1{font-size:var(--fs-display);margin-top:18px;max-width:9ch}
.stage .sub{font-size:var(--fs-lead);color:rgba(255,255,255,.86);max-width:36ch;margin-top:18px}
.stage .ctas{display:flex;flex-wrap:wrap;gap:12px;margin-top:30px}
.stage .ticks{list-style:none;padding:0;margin:28px 0 0;display:flex;flex-wrap:wrap;gap:8px 18px;font-size:.8125rem;font-weight:600;color:rgba(255,255,255,.9)}
.stage .ticks li{display:flex;align-items:center;gap:6px}
.stage .ticks .ico{width:16px;height:16px}
.show{position:relative;aspect-ratio:4/5;border-radius:clamp(18px,2vw,26px);overflow:hidden;box-shadow:0 40px 80px rgba(70,20,0,.4),0 0 0 6px rgba(255,255,255,.14);transform:rotate(-2deg);transition:transform var(--t-med) var(--ease-out)}
.show:hover{transform:rotate(0) scale(1.01)}
.show img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .6s var(--ease-out),transform 1.2s var(--ease-out);transform:scale(1.06)}
.show img.on{opacity:1;transform:scale(1)}
.side{display:grid;gap:18px;align-content:center}
.side .lbl{font-size:.8125rem;font-weight:600;color:rgba(255,255,255,.75)}
.side .nm{font-size:clamp(1.25rem,1rem + .8vw,1.625rem);font-weight:800;letter-spacing:-.02em;line-height:1.1}
.side .pz{font-size:clamp(1.5rem,1.1rem + 1.2vw,2.25rem);font-weight:800;letter-spacing:-.03em;line-height:1}
.side .pz small{display:block;font-size:.8125rem;font-weight:500;letter-spacing:0;color:rgba(255,255,255,.75);margin-top:6px}
.dots{display:flex;gap:10px}
.dots button{all:unset;cursor:pointer;width:54px;height:54px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 2px rgba(255,255,255,.35);transition:box-shadow var(--t-fast),transform var(--t-fast) var(--ease-out)}
.dots button img{width:100%;height:100%;object-fit:cover}
.dots button:hover{transform:translateY(-2px)}
.dots button[aria-pressed="true"]{box-shadow:0 0 0 3px #fff}
.dots button:focus-visible{outline:3px solid #fff;outline-offset:3px}
.side .btn{justify-self:start}

/* confianza */
.trust ul{list-style:none;margin:0;padding:clamp(22px,3vw,34px) 0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px}
.trust li{display:grid;grid-template-columns:auto 1fr;gap:2px 14px;align-items:center}
.trust .ico{width:24px;height:24px;color:var(--hot);grid-row:1/3;padding:12px;box-sizing:content-box;background:var(--hot-soft);border-radius:50%}
.trust strong{font-weight:700}
.trust span{font-size:var(--fs-small);color:var(--steel);line-height:1.4}

/* secciones */
.sec{padding-block:clamp(48px,6vw,96px)}
.sec-h{display:flex;justify-content:space-between;align-items:end;gap:20px;margin-bottom:30px;flex-wrap:wrap}
.sec-h h2{font-size:var(--fs-h2)}
.sec-h p{color:var(--steel);margin-top:8px}
.sec-h a{font-weight:700;white-space:nowrap;display:inline-flex;align-items:center;gap:6px;text-decoration:none}
.sec-h a:hover{color:var(--hot)}
.sec-h a .ico{width:18px;height:18px}

/* categorías */
.cats{display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:18px}
.cat{position:relative;display:block;border-radius:var(--r);overflow:hidden;background:var(--tile);min-height:340px;text-decoration:none;color:#fff}
.cat img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .8s var(--ease-out)}
.cat:hover img{transform:scale(1.05)}
.cat::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 35%,rgba(20,8,0,.78))}
.cat div{position:absolute;left:24px;right:24px;bottom:22px;z-index:1;display:grid;grid-template-columns:1fr auto;gap:4px 14px;align-items:end}
.cat h3{font-size:clamp(1.75rem,1.3rem + 1.4vw,2.5rem);text-transform:uppercase}
.cat p{font-size:var(--fs-small);opacity:.9;grid-column:1}
.cat .go{grid-column:2;grid-row:1/3;display:grid;place-items:center;width:50px;height:50px;border-radius:50%;background:var(--hot);transition:transform var(--t-fast) var(--ease-out)}
.cat:hover .go{transform:rotate(-45deg)}
.cat .go .ico{width:20px;height:20px}
.cat .n{position:absolute;top:18px;left:18px;z-index:1;font-size:.8125rem;font-weight:700;background:#fff;color:var(--ink);padding:6px 12px;border-radius:999px}

/* productos */
.shop-tools{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:6px}
.chip{all:unset;cursor:pointer;padding:10px 18px;border-radius:999px;background:var(--soft);font-weight:600;font-size:var(--fs-small);box-shadow:inset 0 0 0 1px var(--line);transition:background var(--t-fast),color var(--t-fast)}
.chip:hover{background:var(--tile)}
.chip[aria-pressed="true"]{background:var(--ink);color:#fff;box-shadow:none}
.chip:focus-visible{outline:3px solid var(--hot);outline-offset:2px}
.group{margin-top:38px}
.group > h3{font-size:clamp(1.375rem,1.15rem + .7vw,1.75rem);margin-bottom:18px;display:flex;align-items:baseline;gap:10px}
.group > h3 span{font-size:var(--fs-small);font-weight:600;color:var(--steel);letter-spacing:0}
.grid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:28px 20px}
.card{display:flex;flex-direction:column}
.card .ph{position:relative;display:block;aspect-ratio:4/5;background:var(--tile);border-radius:var(--r);overflow:hidden}
.card .ph img{width:100%;height:100%;object-fit:cover;transition:transform .8s var(--ease-out)}
.card:hover .ph img{transform:scale(1.05)}
.card .ct{position:absolute;top:12px;left:12px;font-size:.75rem;font-weight:700;background:#fff;padding:5px 11px;border-radius:999px}
.card .bd{padding:14px 2px 0;display:flex;flex-direction:column;gap:6px;flex:1}
.card h3{font-size:var(--fs-h3);font-weight:700;letter-spacing:-.015em;line-height:1.2}
.card h3 a{text-decoration:none}.card h3 a:hover{color:var(--hot)}
.card .sh{font-size:var(--fs-small);color:var(--steel);line-height:1.45}
.card .row{margin-top:auto;padding-top:10px;display:flex;align-items:center;justify-content:space-between;gap:10px}
.card .pr{font-size:.9375rem;font-weight:700}
.card .pr small{display:block;font-size:.75rem;font-weight:500;color:var(--steel)}
.card .btn{min-height:44px;padding:0 18px;font-size:var(--fs-small)}
.anc{display:block;position:relative;top:-90px}
.shop{margin-top:26px}
.empty{display:none;padding:40px;text-align:center;color:var(--steel);background:var(--soft);border-radius:var(--r);margin-top:24px}

/* cómo comprar */
.how .box{background:var(--ink);color:#fff;border-radius:clamp(22px,3vw,36px);padding:clamp(28px,5vw,64px)}
.how .sec-h p{color:#A9A9AE}
.steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;counter-reset:s}
.steps li{background:rgba(255,255,255,.06);border-radius:var(--r);padding:28px;counter-increment:s;box-shadow:inset 0 0 0 1px rgba(255,255,255,.08)}
.steps li::before{content:"0" counter(s);display:block;font-size:3rem;font-weight:800;letter-spacing:-.04em;line-height:1;margin-bottom:18px;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.steps h3{font-size:1.25rem}
.steps p{color:#BDBDC2;margin-top:8px;font-size:var(--fs-small)}

/* guías */
.blog{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;list-style:none;margin:0;padding:0}
.blog a{display:block;text-decoration:none}
.blog img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:var(--r);background:var(--tile);transition:transform .8s var(--ease-out)}
.blog a:hover img{transform:scale(1.02)}
.blog h3{font-size:1.25rem;margin-top:16px}
.blog p{font-size:var(--fs-small);color:var(--steel);margin-top:6px}
.blog a:hover h3{color:var(--hot)}

/* redes */
.social .box{position:relative;overflow:hidden;display:grid;grid-template-columns:minmax(0,1.3fr) auto;gap:24px;align-items:center;background:var(--grad);color:#fff;border-radius:clamp(22px,3vw,36px);padding:clamp(28px,5vw,64px)}
.social h2{font-size:var(--fs-h2)}
.social p{color:rgba(255,255,255,.88);margin-top:10px}
.social .btns{display:flex;gap:12px;flex-wrap:wrap}

/* ficha de producto */
.crumbs{font-size:var(--fs-small);color:var(--steel);padding-top:22px}
.crumbs a{text-decoration:none}.crumbs a:hover{color:var(--hot)}
.pdp{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:clamp(24px,4vw,64px);padding-block:22px clamp(40px,5vw,72px);align-items:start}
.gal{display:grid;grid-template-columns:84px minmax(0,1fr);gap:14px}
.gal .th{display:grid;gap:12px;align-content:start}
.gal .th button{all:unset;cursor:pointer;aspect-ratio:1;border-radius:var(--r-s);overflow:hidden;background:var(--tile);box-shadow:0 0 0 1px var(--line);transition:box-shadow var(--t-fast)}
.gal .th button[aria-pressed="true"]{box-shadow:0 0 0 2px var(--ink)}
.gal .th button:focus-visible{outline:3px solid var(--hot);outline-offset:2px}
.gal .th img{width:100%;height:100%;object-fit:cover}
.gal .main{position:relative;border-radius:var(--r);overflow:hidden;background:var(--tile);aspect-ratio:4/5}
.gal .main img{width:100%;height:100%;object-fit:cover}
.gal.one{grid-template-columns:1fr}.gal.one .th{display:none}
.pdp .note{font-size:.8125rem;color:var(--steel);margin-top:12px}
.pdp .tags{display:flex;gap:8px;flex-wrap:wrap}
.pdp .tags span{font-size:.75rem;font-weight:700;padding:6px 12px;border-radius:999px;background:var(--soft);box-shadow:inset 0 0 0 1px var(--line)}
.pdp .tags span.hot{background:var(--hot-soft);color:var(--hot-2);box-shadow:none}
.pdp h1{font-size:clamp(2rem,1.4rem + 2vw,3.25rem);margin-top:14px}
.pdp .sh{font-size:var(--fs-lead);color:var(--ink-2);margin-top:14px}
.pdp .pr{font-size:1.75rem;font-weight:800;letter-spacing:-.03em;margin-top:22px}
.pdp .pr small{display:block;font-size:var(--fs-small);font-weight:500;letter-spacing:0;color:var(--steel);margin-top:4px}
.pdp .buy{display:flex;gap:10px;margin-top:22px}
.pdp .buy .btn{flex:1;min-height:58px;font-size:1.0625rem}
.pdp .tr{list-style:none;padding:0;margin:20px 0 0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;font-size:.8125rem;color:var(--ink-2)}
.pdp .tr li{display:grid;gap:6px;justify-items:start;background:var(--soft);border-radius:var(--r-s);padding:14px;line-height:1.35}
.pdp .tr .ico{width:22px;height:22px;color:var(--hot)}
.tabs{margin-top:30px;box-shadow:inset 0 -1px 0 var(--line);display:flex;gap:24px;overflow-x:auto}
.tabs button{all:unset;cursor:pointer;padding:12px 0;font-weight:700;color:var(--steel);box-shadow:inset 0 -2px 0 transparent;white-space:nowrap}
.tabs button[aria-selected="true"]{color:var(--ink);box-shadow:inset 0 -2px 0 var(--ink)}
.tabs button:focus-visible{outline:3px solid var(--hot);outline-offset:2px}
.pane{padding-top:18px;color:var(--ink-2);max-width:62ch}
.pane[hidden]{display:none}
.pane ul{list-style:none;padding:0;margin:0;display:grid;gap:10px}
.pane li{display:flex;gap:10px;align-items:flex-start}
.pane li .ico{color:var(--hot);width:20px;height:20px;margin-top:2px}

/* pie */
footer{background:var(--ink);color:#fff;padding-block:64px 32px;font-size:var(--fs-small);margin-top:clamp(48px,6vw,96px)}
footer .mark{fill:#fff}
footer .mark path{fill:var(--ink)}
.cols{display:grid;grid-template-columns:1.4fr repeat(3,minmax(0,1fr));gap:32px}
.cols ul{list-style:none;margin:0;padding:0;display:grid;gap:9px;align-content:start;color:#A9A9AE}
.cols li:first-child{color:#fff;font-weight:700}
.cols a{text-decoration:none}.cols a:hover{color:var(--amber)}
.cols .about{color:#A9A9AE;display:grid;gap:16px;align-content:start;max-width:36ch}
.cols .about .brand{color:#fff}
.legal{margin-top:44px;padding-top:22px;box-shadow:inset 0 1px 0 rgba(255,255,255,.12);display:grid;gap:6px;color:#8E8E93}
.legal p{max-width:90ch}

/* páginas interiores */
.doc{padding-block:clamp(24px,4vw,48px);max-width:820px}
.doc h1{font-size:var(--fs-h2);margin-bottom:16px}
.doc h2{font-size:1.25rem;margin:36px 0 10px}
.doc p,.doc li{max-width:68ch;color:var(--ink-2)}
.doc .lead{font-size:var(--fs-lead);color:var(--steel)}
.doc ul{padding-left:20px;display:grid;gap:8px}
.doc .grid{grid-template-columns:repeat(3,minmax(0,1fr));margin-top:16px;padding-left:0}
.doc .grid li{color:inherit}
.back{display:inline-block;margin-top:32px;font-weight:700}

@media (prefers-reduced-motion:reduce){*,*::before,*::after{transition-duration:1ms!important;animation-duration:1ms!important}}
@media (max-width:1180px){
  .search{display:none}
  .stage .glass{grid-template-columns:minmax(0,1fr) minmax(0,.9fr)}
  .side{grid-column:1/-1;grid-template-columns:auto auto 1fr auto;align-items:center;gap:14px 24px}
  .side .dots{justify-self:end}
  .grid{grid-template-columns:repeat(3,minmax(0,1fr))}
  .trust ul{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:860px){
  .hdr nav{display:none}
  .cart{margin-left:auto}
  .stage .glass{grid-template-columns:1fr;min-height:0}
  .show{aspect-ratio:1/1;transform:none;order:-1}
  .side{grid-template-columns:1fr;grid-column:auto;gap:14px}
  .side .pz{font-size:1.25rem;display:flex;align-items:baseline;gap:10px}
  .side .pz small{margin:0}
  .side .dots{justify-self:start}
  .side .lbl{display:none}
  .side .btn{grid-column:1/-1;justify-self:stretch}
  .cats{grid-template-columns:1fr;gap:12px}
  .cat{min-height:220px}
  .grid,.doc .grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:22px 12px}
  .card .sh{display:none}
  .card .row{flex-direction:column;align-items:stretch}
  .card .btn{padding:0 10px}
  .trust ul{grid-template-columns:1fr;gap:14px}
  .steps,.blog{grid-template-columns:1fr}
  .social .box{grid-template-columns:1fr}
  .social .btns .btn{flex:1}
  .pdp{grid-template-columns:1fr}
  .gal{grid-template-columns:1fr}
  .gal .th{grid-template-columns:repeat(4,64px);order:2}
  .pdp .tr{grid-template-columns:1fr}
  .cols{grid-template-columns:1fr 1fr}
  .cols .about{grid-column:1/3}
}
"""

def head(title, desc, path, prefix):
    url = BASE + "/" + path.replace("index.html", "")
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website">
<meta name="theme-color" content="#1A1C1E"><link rel="icon" href="{prefix}todohome-icono.svg" type="image/svg+xml">
<link rel="preload" href="{prefix}fonts/archivo.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="{prefix}styles.css">
</head><body>"""

def header(prefix):
    links = "".join(f'<a href="{prefix}index.html#{k}">{v}</a>' for k, v in CATS.items())
    return f"""<p class="topbar">Compra segura en Amazon · <b>Envío rápido</b> y devoluciones gestionadas por Amazon</p>
<header class="hdr"><div class="wrap in"><a class="brand" href="{prefix}index.html" aria-label="TODOHOME, inicio">{MARK}<span>TODOHOME</span></a>
<nav aria-label="Categorías">{links}<a href="{prefix}index.html#guias">Ideas</a></nav>
<form class="search" role="search" action="{prefix}index.html#productos">{I_SEARCH}<input type="search" name="q" id="q" placeholder="Buscar productos" aria-label="Buscar productos"></form>
<a class="cart" href="{prefix}index.html#productos">{I_CART}<span>Tienda</span></a></div></header>"""

def footer(prefix):
    credits = ", ".join(sorted(PHOTOS.values()))
    cats = "".join(f'<li><a href="{prefix}index.html#{k}">{v}</a></li>' for k, v in CATS.items())
    return f"""<footer><div class="wrap"><div class="cols">
<div class="about"><a class="brand" href="{prefix}index.html">{MARK}<span>TODOHOME</span></a><p>Tienda online de productos para el hogar y la cocina. Elegimos lo mejor y lo compras con la seguridad de Amazon.</p></div>
<ul><li>Tienda</li>{cats}<li><a href="{prefix}index.html#productos">Todos los productos</a></li></ul>
<ul><li>Ayuda</li><li><a href="{prefix}index.html#como-comprar">Cómo comprar</a></li><li><a href="{prefix}index.html#guias">Ideas y guías</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul>
<ul><li>Síguenos</li><li><a href="{TIKTOK}" rel="noopener" target="_blank">TikTok</a></li><li><a href="{INSTA}" rel="noopener" target="_blank">Instagram</a></li><li><a href="{PIN}" rel="noopener" target="_blank">Pinterest</a></li><li><a href="{prefix}aviso-legal.html">Aviso legal</a></li><li><a href="{prefix}privacidad.html">Privacidad y cookies</a></li></ul>
</div><div class="legal"><p>{DISCLOSURE} La compra, el pago, el envío y las devoluciones se hacen en Amazon. Precios orientativos: el precio final es el que marca Amazon.</p><p>Fotos de producto de Pexels (licencia libre), que muestran el tipo de producto; el modelo de Amazon puede variar. Fotos de ambiente de {e(credits)} en Unsplash · © 2026 TODOHOME</p></div></div></footer>"""

SEARCH_JS = """<script>
(function(){
var q=document.getElementById('q'),cards=[].slice.call(document.querySelectorAll('.card[data-q]')),groups=[].slice.call(document.querySelectorAll('.group')),chips=[].slice.call(document.querySelectorAll('.chip')),empty=document.getElementById('empty'),cat='';
if(!cards.length){return}
function norm(t){return t.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'')}
function run(){var t=norm(q.value.trim()),n=0;
 cards.forEach(function(c){var ok=(!t||c.dataset.q.indexOf(t)>-1)&&(!cat||c.dataset.c===cat);c.hidden=!ok;if(ok)n++});
 if(empty)empty.style.display=n?'none':'block';}
q.addEventListener('input',run);
q.form.addEventListener('submit',function(ev){ev.preventDefault();run();document.getElementById('productos').scrollIntoView({behavior:'smooth'})});
chips.forEach(function(b){b.addEventListener('click',function(){cat=b.dataset.c;chips.forEach(function(x){x.setAttribute('aria-pressed',x===b)});run()})});
function hc(){var c=location.hash.slice(1),b=document.querySelector('.chip[data-c="'+c+'"]');if(c&&b){b.click();document.getElementById('productos').scrollIntoView()}}window.addEventListener('hashchange',hc);hc();
var m=location.search.match(/[?&]q=([^&]+)/);if(m){q.value=decodeURIComponent(m[1].replace(/\\+/g,' '));run()}
})();
</script>"""

def write(path, doc):
    os.makedirs(os.path.dirname(OUT + path) or OUT, exist_ok=True)
    open(OUT + path, "w").write(doc)

def photo(slug, prefix=""):
    # Foto oficial de Amazon (SiteStripe) si existe; si no, la foto libre descargada en la construcción
    return AMAZON_IMG.get(slug) or f"{prefix}img/{slug}.jpg"
def alt(p):
    return p["name"] if AMAZON_IMG.get(p["slug"]) else f"Foto de {p['name'].lower()}"
def ppath(p):
    return f"producto/{p['slug']}.html"
def norm(t):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")

def nphotos(slug):
    # Cuántas fotos libres se descargaron de cada producto (fetch_photos.py escribe img/fotos.json)
    try:
        return max(1, int(json.load(open(OUT + "img/fotos.json")).get(slug, 1)))
    except Exception:
        return 1

def gallery(p, prefix):
    if AMAZON_IMG.get(p["slug"]):
        srcs = [AMAZON_IMG[p["slug"]]]
    else:
        srcs = [f"{prefix}img/{p['slug']}.jpg"] + [f"{prefix}img/{p['slug']}-{k}.jpg" for k in range(2, nphotos(p["slug"]) + 1)]
    th = "".join(f'<button type="button" aria-pressed="{"true" if k == 0 else "false"}" aria-label="Ver foto {k + 1}" data-src="{s}"><img src="{s}" width="160" height="160" alt="" loading="lazy"></button>' for k, s in enumerate(srcs))
    return f'<div class="gal{" one" if len(srcs) == 1 else ""}"><div class="th">{th}</div><div class="main"><img id="gm" src="{srcs[0]}" width="900" height="1125" alt="{e(alt(p))}"></div></div>'

def card(p, prefix="", lazy=True):
    q = norm(" ".join([p["name"], p["short"], p["task"], CATS[p["cat"]]]))
    ld = ' loading="lazy"' if lazy else ""
    pr = e(p["price"]) if "€" in p["price"] else "Ver precio"
    return f"""<li class="card" data-c="{p['cat']}" data-q="{e(q)}"><a class="ph" href="{prefix}{ppath(p)}" tabindex="-1" aria-hidden="true"><img src="{photo(p['slug'], prefix)}" width="600" height="750" alt=""{ld}><span class="ct">{CATS[p['cat']]}</span></a>
<div class="bd"><h3><a href="{prefix}{ppath(p)}">{e(p['name'])}</a></h3><p class="sh">{e(p['short'])}</p>
<div class="row"><p class="pr num-t">{pr}<small>en Amazon</small></p><a class="btn" href="{amazon_url(p['query'])}" target="_blank" rel="sponsored noopener">Comprar</a></div></div></li>"""

HERO_JS = """<script>
(function(){
var d=document.querySelectorAll('.dots button'),im=document.querySelectorAll('.show img'),nm=document.getElementById('hn'),bt=document.getElementById('hb'),lk=document.getElementById('hl'),i=0,t;
if(!d.length)return;
function go(k){i=k;d.forEach(function(b,j){b.setAttribute('aria-pressed',j===k)});im.forEach(function(x,j){x.classList.toggle('on',j===k)});
 nm.textContent=d[k].dataset.n;bt.href=d[k].dataset.u;lk.href=d[k].dataset.p;}
d.forEach(function(b,j){b.addEventListener('click',function(){clearInterval(t);go(j)})});
if(!matchMedia('(prefers-reduced-motion: reduce)').matches){t=setInterval(function(){go((i+1)%d.length)},5000)}
})();
</script>"""

PDP_JS = """<script>
(function(){
var th=document.querySelectorAll('.gal .th button'),gm=document.getElementById('gm');
th.forEach(function(b){b.addEventListener('click',function(){gm.src=b.dataset.src;th.forEach(function(x){x.setAttribute('aria-pressed',x===b)})})});
var tb=document.querySelectorAll('.tabs button');
tb.forEach(function(b){b.addEventListener('click',function(){tb.forEach(function(x){var on=x===b;x.setAttribute('aria-selected',on);document.getElementById(x.getAttribute('aria-controls')).hidden=!on})})});
})();
</script>"""

def index():
    shows, dots = "", ""
    for i, s in enumerate(HERO):
        p = BYSLUG[s]
        shows += f'<img class="{"on" if i == 0 else ""}" src="{photo(s)}" width="900" height="1125" alt="{e(alt(p))}"{"" if i == 0 else " loading=\"lazy\""}>'
        dots += f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}" aria-label="Ver {e(p["name"])}" data-n="{e(p["name"])}" data-u="{amazon_url(p["query"])}" data-p="{ppath(p)}"><img src="{photo(s)}" width="108" height="108" alt=""></button>'
    first = BYSLUG[HERO[0]]
    ticks = "".join(f"<li>{I_CHECK}{t}</li>" for t in ["Pago seguro en Amazon", "Envío rápido", "Devolución fácil"])
    trust = "".join(f"<li>{i}<strong>{t}</strong><span>{d}</span></li>" for i, t, d in TRUST)
    cats = ""
    for k, v in CATS.items():
        n = sum(1 for p in PRODUCTS if p["cat"] == k)
        cats += f'<a class="cat" href="#{k}"><img src="{photo(CAT_IMG[k])}" width="800" height="700" alt="" loading="lazy"><span class="n">{n} productos</span><div><h3>{v}</h3><p>{CAT_TXT[k]}</p><span class="go">{I_ARROW}</span></div></a>'
    chips = '<button class="chip" type="button" data-c="" aria-pressed="true">Todo</button>' + "".join(f'<button class="chip" type="button" data-c="{k}" aria-pressed="false">{v}</button>' for k, v in CATS.items())
    order = [p for k in CATS for p in PRODUCTS if p["cat"] == k]
    anchors = "".join(f'<span class="anc" id="{k}"></span>' for k in CATS)
    groups = f'{anchors}<ul class="grid shop">{"".join(card(p) for p in order)}</ul>'
    blog = "".join(f'<li><a href="{g[0]}"><img src="{pic(g[4],900,675)}" width="900" height="675" alt="{e(GUIDE_ALT[g[4]])}" loading="lazy"><h3>{e(g[2])}</h3><p>{e(g[3])}</p></a></li>' for g in GUIDES)
    body = f"""{head("TODOHOME · Tienda online de productos para el hogar y la cocina","Facilita tu vida en casa: los mejores productos de cocina, limpieza y hogar. Compra segura en Amazon con envío rápido y devoluciones fáciles.","index.html","")}
{header("")}
<main>
<section class="hero wrap"><div class="stage"><div class="glass">
<div><span class="eyebrow">Tienda online · Hogar y cocina</span><h1>Facilita tu vida en casa</h1><p class="sub">Los mejores productos para la cocina, la limpieza y el hogar, elegidos uno a uno y a buen precio.</p>
<div class="ctas"><a class="btn white" href="#productos">Ver productos {I_ARROW}</a><a class="btn line" href="#categorias">Categorías</a></div>
<ul class="ticks">{ticks}</ul></div>
<a class="show" id="hl" href="{ppath(first)}" aria-label="Ver producto destacado">{shows}</a>
<div class="side"><span class="lbl">Destacado</span><p class="nm" id="hn">{e(first["name"])}</p><p class="pz">Ver precio<small>El precio lo marca Amazon</small></p>
<div class="dots" role="group" aria-label="Productos destacados">{dots}</div>
<a class="btn white" id="hb" href="{amazon_url(first["query"])}" target="_blank" rel="sponsored noopener">{I_CART} Comprar en Amazon</a></div>
</div></div></section>
<section class="trust" aria-label="Por qué comprar con nosotros"><div class="wrap"><ul>{trust}</ul></div></section>

<section class="sec wrap" id="categorias" aria-labelledby="cath" style="padding-top:clamp(24px,3vw,40px)"><div class="sec-h"><div><h2 id="cath">Compra por categoría</h2><p>Todo lo que necesitas para una casa más fácil.</p></div></div>
<div class="cats">{cats}</div></section>

<section class="sec wrap" id="productos" aria-labelledby="ph" style="padding-top:0"><div class="sec-h"><div><h2 id="ph">Nuestros productos</h2><p>{len(PRODUCTS)} productos elegidos para tu casa.</p></div></div>
<div class="shop-tools" role="group" aria-label="Filtrar por categoría">{chips}</div>
{groups}<p class="empty" id="empty">No hemos encontrado ese producto. Prueba con otra palabra, como «cocina» o «limpieza».</p></section>

<section class="how wrap" id="como-comprar" aria-labelledby="hh"><div class="box"><div class="sec-h"><div><h2 id="hh">Cómo comprar</h2><p>Tres pasos y lo tienes en casa.</p></div></div>
<ol class="steps"><li><h3>Elige tu producto</h3><p>Mira las fotos y las ventajas de cada producto.</p></li><li><h3>Pulsa «Comprar»</h3><p>Te llevamos a la página del producto en Amazon, donde ves el precio final.</p></li><li><h3>Paga y recíbelo en casa</h3><p>Amazon gestiona el pago, el envío y las devoluciones, con su garantía.</p></li></ol></div></section>

<section class="sec wrap" id="guias" aria-labelledby="gh"><div class="sec-h"><div><h2 id="gh">Ideas para tu casa</h2><p>Guías rápidas para ordenar y limpiar con menos esfuerzo.</p></div></div>
<ul class="blog">{blog}</ul></section>

<section class="social wrap" aria-labelledby="sh"><div class="box"><div><h2 id="sh">Un producto nuevo cada semana</h2><p>Te enseñamos en vídeo cómo funciona cada producto antes de añadirlo a la tienda.</p></div>
<div class="btns"><a class="btn white" href="{TIKTOK}" target="_blank" rel="noopener">Seguir en TikTok</a><a class="btn line" href="{INSTA}" target="_blank" rel="noopener">Instagram</a></div></div></section>
</main>
{footer("")}
{SEARCH_JS}
{HERO_JS}
</body></html>"""
    write("index.html", body)

def product_pages():
    for p in PRODUCTS:
        rel = [x for x in PRODUCTS if x["cat"] == p["cat"] and x["slug"] != p["slug"]]
        rel = (rel + [x for x in PRODUCTS if x["slug"] != p["slug"] and x not in rel])[:4]
        bl = "".join(f"<li>{I_CHECK}<span>{e(b)}</span></li>" for b in p["bullets"])
        tr = "".join(f"<li>{i}<span><strong>{t}.</strong> {d}</span></li>" for i, t, d in TRUST[:3])
        note = "" if AMAZON_IMG.get(p["slug"]) else '<p class="note">' + p.get("note", "Fotos orientativas del tipo de producto. El modelo de Amazon puede variar.") + '</p>'
        ld = json.dumps({"@context": "https://schema.org", "@type": "Product", "name": p["name"], "description": p["short"], "image": BASE + "/img/" + p["slug"] + ".jpg"}, ensure_ascii=False)
        pr = e(p["price"]) if "€" in p["price"] else "Ver precio en Amazon"
        body = f"""{head(p['name'] + ' | TODOHOME', p['short'] + ' Compra segura en Amazon.', ppath(p), '../')}
{header('../')}
<main class="wrap">
<p class="crumbs"><a href="../index.html">Inicio</a> / <a href="../index.html#{p['cat']}">{CATS[p['cat']]}</a> / {e(p['name'])}</p>
<div class="pdp"><div>{gallery(p, '../')}{note}</div>
<div><div class="tags"><span class="hot">{CATS[p['cat']]}</span><span>Envío por Amazon</span></div><h1>{e(p['name'])}</h1><p class="sh">{e(p['short'])}</p>
<p class="pr num-t">{pr}<small>El precio final lo marca Amazon.</small></p>
<div class="buy"><a class="btn hot" href="{amazon_url(p['query'])}" target="_blank" rel="sponsored noopener">{I_CART} Comprar en Amazon</a></div>
<ul class="tr">{tr}</ul>
<div class="tabs" role="tablist"><button type="button" role="tab" aria-selected="true" aria-controls="t1" id="b1">Ventajas</button><button type="button" role="tab" aria-selected="false" aria-controls="t2" id="b2">Descripción</button><button type="button" role="tab" aria-selected="false" aria-controls="t3" id="b3">Envío y devoluciones</button></div>
<div class="pane" id="t1" role="tabpanel" aria-labelledby="b1"><ul>{bl}</ul></div>
<div class="pane" id="t2" role="tabpanel" aria-labelledby="b2" hidden><p>{e(p['desc'])}</p></div>
<div class="pane" id="t3" role="tabpanel" aria-labelledby="b3" hidden><p>Lo compras en Amazon: el pago, el envío y las devoluciones los gestiona Amazon según sus condiciones. Muchos productos tienen envío con Prime.</p></div>
</div></div>
<section class="sec" style="padding-top:0" aria-labelledby="rh"><div class="sec-h"><div><h2 id="rh">También te puede gustar</h2></div><a href="../index.html#productos">Ver todo {I_ARROW}</a></div>
<ul class="grid">{''.join(card(x, '../') for x in rel)}</ul></section>
</main>
{footer('../')}
<script type="application/ld+json">{ld}</script>
{PDP_JS}
</body></html>"""
        write(ppath(p), body)

def inner(path, title, desc, content, prefix):
    write(path, f"""{head(title, desc, path, prefix)}
{header(prefix)}<main class="wrap"><article class="doc">{content}</article></main>
{footer(prefix)}</body></html>""")

def guides():
    for path, short, title, desc, img, picks, steps in GUIDES:
        parts = "".join(f"<h2>{e(h)}</h2><p>{e(t)}</p>" for h, t in steps)
        pk = "".join(card(BYSLUG[s], "../") for s in picks)
        c = f'<h1>{e(title)}</h1><p class="lead">{e(desc)}</p>{parts}<h2>Productos de esta guía</h2><ul class="grid">{pk}</ul><a class="back" href="../index.html#productos">Ver todos los productos</a>'
        inner(path, title + " | TODOHOME", desc, c, "../")

def legal():
    c = f"""<h1>Aviso legal</h1>
<p>En cumplimiento de la Ley 34/2002 de Servicios de la Sociedad de la Información (LSSI-CE), se informa de los datos del titular de este sitio web:</p>
<ul><li><strong>Titular:</strong> [NOMBRE Y APELLIDOS]</li><li><strong>NIF:</strong> [NIF]</li><li><strong>Domicilio:</strong> [DIRECCIÓN]</li><li><strong>Correo de contacto:</strong> {EMAIL}</li></ul>
<h2>Objeto</h2><p>TODOHOME es una tienda online de productos para el hogar que funciona como escaparate: la compra, el pago, el envío y las devoluciones se realizan en tiendas de terceros, principalmente Amazon, a través de los enlaces de cada producto.</p>
<h2>Enlaces de afiliado</h2><p>{DISCLOSURE} Esto no supone ningún coste adicional para quien compra. La selección de productos se basa en criterios propios.</p>
<h2>Responsabilidad</h2><p>Los precios, la disponibilidad y las condiciones de venta los fija cada tienda y pueden cambiar. TODOHOME no se hace responsable de los contenidos de webs de terceros.</p>
<h2>Propiedad intelectual</h2><p>Los textos, el logotipo y el diseño de esta web pertenecen a su titular. Las fotografías de producto proceden de Pexels y las de ambiente de Unsplash, con sus licencias. Las marcas de terceros pertenecen a sus respectivos dueños.</p>"""
    inner("aviso-legal.html", "Aviso legal | TODOHOME", "Aviso legal de TODOHOME.", c, "")
    c = f"""<h1>Privacidad y cookies</h1>
<h2>Datos personales</h2><p>Esta web no tiene formularios ni registra datos personales de quienes la visitan. Si nos escribes a {EMAIL}, usaremos tus datos solo para responderte y no los cederemos a terceros. Puedes pedir su acceso, rectificación o supresión en esa misma dirección, y reclamar ante la Agencia Española de Protección de Datos (aepd.es).</p>
<h2>Cookies</h2><p>Esta web no instala cookies propias de análisis ni de publicidad. Al pulsar un enlace a Amazon u otra tienda, esa tienda puede instalar sus propias cookies según su política, por ejemplo para atribuir la compra a un enlace de afiliado.</p>
<h2>Servicios de terceros</h2><p>Las fotos de producto proceden de Pexels y se sirven desde la propia web; las de ambiente se cargan desde Unsplash (a través de picsum.photos) y la web se aloja en Vercel. Estos servicios pueden registrar datos técnicos de conexión como la dirección IP. La tipografía se sirve desde la propia web.</p>"""
    inner("privacidad.html", "Privacidad y cookies | TODOHOME", "Política de privacidad y cookies de TODOHOME.", c, "")

os.makedirs(OUT, exist_ok=True)
index(); product_pages(); guides(); legal()
open(OUT + "styles.css", "w").write(CSS)
open(OUT + "todohome-icono.svg", "w").write(ICON)
open(OUT + "robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
urls = ["", "aviso-legal.html", "privacidad.html"] + [g[0] for g in GUIDES] + [ppath(p) for p in PRODUCTS]
open(OUT + "sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{BASE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
print("ok")
