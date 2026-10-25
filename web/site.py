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
        '<path d="M15 31 32 16l17 15h-4v17H19V31z" fill="#FFFFFF"/><rect x="28" y="37" width="8" height="11" rx="2" fill="#1F7A47"/></svg>')
MARK = ('<svg class="mark" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14"/>'
        '<path d="M15 31 32 16l17 15h-4v17H19V31z" fill="#FFFFFF"/><rect x="28" y="37" width="8" height="11" rx="2" fill="#1F7A47"/></svg>')

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
  --bg:#FFFFFF; --soft:#F3F4F2; --tile:#ECEEEB; --ink:#1A1C1E; --ink-2:#3A3F43; --steel:#5D6368; --line:#E1E4E1;
  --signal:#1F7A47; --signal-2:#17603A; --signal-soft:#E5F1E9;
  --font:"Archivo",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --fs-small:.875rem; --fs-body:1rem; --fs-lead:clamp(1.0625rem,1rem + .35vw,1.25rem);
  --fs-h3:clamp(1.0625rem,1rem + .25vw,1.1875rem); --fs-h2:clamp(1.625rem,1.25rem + 1.5vw,2.375rem);
  --fs-display:clamp(2.375rem,1.4rem + 3.6vw,4.25rem);
  --m:clamp(16px,4vw,48px); --max:1280px; --r:14px;
  --ease-out:cubic-bezier(.22,1,.36,1); --t-fast:160ms; --t-med:320ms;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:90px;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:400 var(--fs-body)/1.55 var(--font);-webkit-font-smoothing:antialiased}
::selection{background:var(--signal);color:#fff}
img{display:block;max-width:100%;height:auto}
a{color:inherit;text-underline-offset:.22em}
h1,h2,h3{margin:0;font-weight:700;font-stretch:106%;letter-spacing:-.02em;line-height:1.08;text-wrap:balance}
p{margin:0;text-wrap:pretty}
:focus-visible{outline:3px solid var(--signal);outline-offset:3px;border-radius:6px}
.wrap{width:min(100% - 2*var(--m),var(--max));margin-inline:auto}
.num-t{font-variant-numeric:tabular-nums}
.ico{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;flex:none}

.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:50px;padding:0 24px;border-radius:999px;border:0;background:var(--signal);color:#fff;font:inherit;font-weight:600;text-decoration:none;cursor:pointer;transition:background var(--t-fast),transform var(--t-fast) var(--ease-out)}
.btn:hover{background:var(--signal-2)}
.btn:active{transform:scale(.97)}
.btn .ico{width:18px;height:18px}
.btn.ghost{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1.5px var(--ink)}
.btn.ghost:hover{background:var(--ink);color:#fff}
.btn.light{background:#fff;color:var(--ink)}.btn.light:hover{background:var(--tile)}

/* barra superior y cabecera */
.topbar{background:var(--ink);color:#fff;font-size:var(--fs-small);text-align:center;padding:9px 16px}
.hdr{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.97);box-shadow:0 1px 0 var(--line)}
.hdr .in{display:flex;align-items:center;gap:28px;padding-block:14px}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;font-stretch:115%;text-decoration:none;font-size:1.125rem}
.mark{width:36px;height:36px;fill:var(--ink)}
.search{flex:1;max-width:520px;display:flex;align-items:center;gap:10px;background:var(--soft);border-radius:999px;padding:0 18px;min-height:46px;box-shadow:inset 0 0 0 1px var(--line)}
.search:focus-within{box-shadow:inset 0 0 0 2px var(--signal)}
.search .ico{color:var(--steel);width:20px;height:20px}
.search input{all:unset;flex:1;font-size:var(--fs-body);min-width:0}
.search input::placeholder{color:var(--steel)}
.hdr nav{display:flex;gap:24px;font-weight:500;margin-left:auto}
.hdr nav a{text-decoration:none;white-space:nowrap}.hdr nav a:hover{color:var(--signal)}
.cart{display:inline-flex;align-items:center;gap:8px;font-weight:600;text-decoration:none;min-height:44px;white-space:nowrap}
.cart:hover{color:var(--signal)}

/* portada */
.hero{padding-block:clamp(28px,4vw,56px)}
.hero .in{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:clamp(28px,4vw,64px);align-items:center}
.hero h1{font-size:var(--fs-display);max-width:12ch}
.hero .sub{font-size:var(--fs-lead);color:var(--ink-2);max-width:44ch;margin-top:18px}
.hero .ctas{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}
.hero .ticks{list-style:none;padding:0;margin:26px 0 0;display:flex;flex-wrap:wrap;gap:10px 22px;color:var(--ink-2);font-size:var(--fs-small);font-weight:500}
.hero .ticks li{display:flex;align-items:center;gap:6px}
.hero .ticks .ico{color:var(--signal);width:18px;height:18px}
.mosaic{display:grid;grid-template-columns:1.25fr 1fr;grid-template-rows:1fr 1fr;gap:14px;aspect-ratio:6/5}
.mosaic a{position:relative;border-radius:var(--r);overflow:hidden;background:var(--tile);text-decoration:none}
.mosaic a:first-child{grid-row:1/3}
.mosaic img{width:100%;height:100%;object-fit:cover;transition:transform .6s var(--ease-out)}
.mosaic a:hover img{transform:scale(1.04)}
.tag{position:absolute;left:12px;bottom:12px;right:12px;display:flex;justify-content:space-between;align-items:center;gap:10px;background:#fff;border-radius:10px;padding:10px 12px;font-size:var(--fs-small);font-weight:600;line-height:1.25}
.tag b{color:var(--signal);white-space:nowrap}

/* confianza */
.trust{background:var(--soft)}
.trust ul{list-style:none;margin:0;padding:22px 0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px}
.trust li{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;align-items:start}
.trust .ico{width:26px;height:26px;color:var(--signal);grid-row:1/3}
.trust strong{font-weight:600}
.trust span{font-size:var(--fs-small);color:var(--steel);line-height:1.4}

/* secciones */
.sec{padding-block:clamp(48px,6vw,88px)}
.sec-h{display:flex;justify-content:space-between;align-items:end;gap:20px;margin-bottom:26px;flex-wrap:wrap}
.sec-h h2{font-size:var(--fs-h2)}
.sec-h p{color:var(--steel);margin-top:6px}
.sec-h a{font-weight:600;white-space:nowrap}

/* categorías */
.cats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.cat{position:relative;display:block;border-radius:var(--r);overflow:hidden;background:var(--tile);aspect-ratio:4/3;text-decoration:none;color:#fff}
.cat img{width:100%;height:100%;object-fit:cover;transition:transform .6s var(--ease-out)}
.cat:hover img{transform:scale(1.04)}
.cat::after{content:"";position:absolute;inset:0;background:linear-gradient(transparent 40%,rgba(10,12,13,.72))}
.cat div{position:absolute;left:20px;right:20px;bottom:18px;z-index:1}
.cat h3{font-size:clamp(1.375rem,1.1rem + 1vw,1.75rem)}
.cat p{font-size:var(--fs-small);opacity:.92;margin-top:4px}
.cat .n{display:inline-flex;align-items:center;gap:6px;margin-top:10px;font-weight:600;font-size:var(--fs-small)}
.cat .n .ico{width:16px;height:16px}

/* productos */
.shop-tools{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}
.chip{all:unset;cursor:pointer;padding:9px 16px;border-radius:999px;background:var(--soft);font-weight:500;font-size:var(--fs-small);box-shadow:inset 0 0 0 1px var(--line);transition:background var(--t-fast)}
.chip:hover{background:var(--tile)}
.chip[aria-pressed="true"]{background:var(--ink);color:#fff;box-shadow:none}
.chip:focus-visible{outline:3px solid var(--signal);outline-offset:2px}
.group{margin-top:34px}
.group > h3{font-size:clamp(1.25rem,1.1rem + .6vw,1.5rem);margin-bottom:16px;display:flex;align-items:baseline;gap:10px}
.group > h3 span{font-size:var(--fs-small);font-weight:500;color:var(--steel);letter-spacing:0}
.grid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:22px 18px}
.card{display:flex;flex-direction:column;background:#fff;border-radius:var(--r);box-shadow:0 0 0 1px var(--line);overflow:hidden;transition:box-shadow var(--t-fast)}
.card:hover{box-shadow:0 0 0 1px var(--ink-2)}
.card .ph{display:block;aspect-ratio:1/1;background:var(--tile);overflow:hidden}
.card .ph img{width:100%;height:100%;object-fit:cover;transition:transform .6s var(--ease-out)}
.card:hover .ph img{transform:scale(1.04)}
.card .bd{padding:14px 16px 16px;display:flex;flex-direction:column;gap:6px;flex:1}
.card .ct{font-size:.8125rem;color:var(--steel);font-weight:500}
.card h3{font-size:var(--fs-h3);font-weight:600;letter-spacing:-.01em;line-height:1.25}
.card h3 a{text-decoration:none}.card h3 a:hover{text-decoration:underline}
.card .sh{font-size:var(--fs-small);color:var(--ink-2);line-height:1.45}
.card .pr{margin-top:auto;padding-top:8px;font-size:1.25rem;font-weight:700}
.card .pr small{display:block;font-size:.75rem;font-weight:500;color:var(--steel)}
.card .btn{min-height:44px;font-size:var(--fs-small);margin-top:6px;width:100%}
.empty{display:none;padding:40px;text-align:center;color:var(--steel);background:var(--soft);border-radius:var(--r);margin-top:24px}

/* cómo comprar */
.how{background:var(--soft)}
.steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;counter-reset:s}
.steps li{background:#fff;border-radius:var(--r);padding:26px;counter-increment:s}
.steps li::before{content:counter(s);display:grid;place-items:center;width:38px;height:38px;border-radius:50%;background:var(--signal);color:#fff;font-weight:700;margin-bottom:16px}
.steps h3{font-size:var(--fs-h3)}
.steps p{color:var(--ink-2);margin-top:6px;font-size:var(--fs-small)}

/* guías */
.blog{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;list-style:none;margin:0;padding:0}
.blog a{display:block;text-decoration:none}
.blog img{width:100%;aspect-ratio:3/2;object-fit:cover;border-radius:var(--r);background:var(--tile)}
.blog h3{font-size:var(--fs-h3);margin-top:14px}
.blog p{font-size:var(--fs-small);color:var(--steel);margin-top:6px}
.blog a:hover h3{text-decoration:underline}

/* redes */
.social .box{display:grid;grid-template-columns:minmax(0,1.3fr) auto;gap:24px;align-items:center;background:var(--ink);color:#fff;border-radius:var(--r);padding:clamp(28px,4vw,48px)}
.social h2{font-size:var(--fs-h2)}
.social p{color:#C9CFCB;margin-top:8px}
.social .btns{display:flex;gap:12px;flex-wrap:wrap}

/* ficha de producto */
.crumbs{font-size:var(--fs-small);color:var(--steel);padding-top:20px}
.crumbs a{text-decoration:none}.crumbs a:hover{text-decoration:underline}
.pdp{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:clamp(24px,4vw,56px);padding-block:20px clamp(40px,5vw,72px);align-items:start}
.pdp .ph{border-radius:var(--r);overflow:hidden;background:var(--tile);aspect-ratio:1/1}
.pdp .ph img{width:100%;height:100%;object-fit:cover}
.pdp .note{font-size:.8125rem;color:var(--steel);margin-top:10px}
.pdp .ct{color:var(--steel);font-weight:500;font-size:var(--fs-small)}
.pdp h1{font-size:clamp(1.875rem,1.4rem + 1.8vw,2.75rem);margin-top:6px}
.pdp .sh{font-size:var(--fs-lead);color:var(--ink-2);margin-top:12px}
.pdp .pr{font-size:2rem;font-weight:700;margin-top:20px}
.pdp .pr small{display:block;font-size:var(--fs-small);font-weight:500;color:var(--steel)}
.pdp .btn{width:100%;margin-top:20px;min-height:56px;font-size:1.0625rem}
.pdp ul.bl{list-style:none;padding:0;margin:24px 0 0;display:grid;gap:10px}
.pdp ul.bl li{display:flex;gap:10px;align-items:flex-start}
.pdp ul.bl .ico{color:var(--signal);width:20px;height:20px;margin-top:2px}
.pdp .tr{list-style:none;padding:18px 0 0;margin:24px 0 0;display:grid;gap:10px;box-shadow:inset 0 1px 0 var(--line);font-size:var(--fs-small);color:var(--ink-2)}
.pdp .tr li{display:flex;gap:10px;align-items:center}
.pdp .tr .ico{width:20px;height:20px;color:var(--steel)}
.pdp .desc{margin-top:28px}
.pdp .desc h2{font-size:var(--fs-h3);margin-bottom:8px}
.pdp .desc p{color:var(--ink-2);max-width:65ch}

/* pie */
footer{background:var(--soft);padding-block:56px 32px;font-size:var(--fs-small);margin-top:clamp(48px,6vw,88px)}
.cols{display:grid;grid-template-columns:1.4fr repeat(3,minmax(0,1fr));gap:32px}
.cols ul{list-style:none;margin:0;padding:0;display:grid;gap:8px;align-content:start;color:var(--steel)}
.cols li:first-child{color:var(--ink);font-weight:600}
.cols a{text-decoration:none}.cols a:hover{text-decoration:underline;color:var(--ink)}
.cols .about{color:var(--steel);display:grid;gap:14px;align-content:start;max-width:36ch}
.legal{margin-top:40px;padding-top:20px;box-shadow:inset 0 1px 0 var(--line);display:grid;gap:6px;color:var(--steel)}
.legal p{max-width:90ch}

/* páginas interiores */
.doc{padding-block:clamp(24px,4vw,48px);max-width:820px}
.doc h1{font-size:var(--fs-h2);margin-bottom:16px}
.doc h2{font-size:var(--fs-h3);margin:36px 0 10px}
.doc p,.doc li{max-width:68ch;color:var(--ink-2)}
.doc .lead{font-size:var(--fs-lead);color:var(--steel)}
.doc ul{padding-left:20px;display:grid;gap:8px}
.doc .grid{grid-template-columns:repeat(3,minmax(0,1fr));margin-top:16px}
.doc .grid li{color:inherit}
.back{display:inline-block;margin-top:32px;font-weight:600}

@media (prefers-reduced-motion:reduce){*,*::before,*::after{transition-duration:1ms!important;animation-duration:1ms!important}}
@media (max-width:1080px){
  .hdr nav{display:none}
  .grid{grid-template-columns:repeat(3,minmax(0,1fr))}
  .trust ul{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:760px){
  .hdr .in{flex-wrap:wrap;gap:12px}
  .search{order:3;flex-basis:100%;max-width:none}
  .cart{margin-left:auto}
  .cart span{display:none}
  .hero .in{grid-template-columns:1fr}
  .mosaic{aspect-ratio:auto;grid-template-rows:180px 180px}
  .cats{grid-template-columns:1fr;gap:12px}
  .cat{aspect-ratio:16/9}
  .grid,.doc .grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:14px 12px}
  .card .bd{padding:12px}
  .card .sh{display:none}
  .card .pr{font-size:1.125rem}
  .card .btn{padding:0 10px}
  .trust ul{grid-template-columns:1fr;gap:14px}
  .steps,.blog{grid-template-columns:1fr}
  .social .box{grid-template-columns:1fr}
  .social .btns .btn{flex:1}
  .pdp{grid-template-columns:1fr}
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
    return f"""<p class="topbar">Compra segura en Amazon · Envío y devoluciones gestionados por Amazon</p>
<header class="hdr"><div class="wrap in"><a class="brand" href="{prefix}index.html" aria-label="TODOHOME, inicio">{MARK}<span>TODOHOME</span></a>
<form class="search" role="search" action="{prefix}index.html#productos">{I_SEARCH}<input type="search" name="q" id="q" placeholder="Buscar productos para tu casa" aria-label="Buscar productos"></form>
<nav aria-label="Categorías">{links}<a href="{prefix}index.html#guias">Ideas</a></nav>
<a class="cart" href="{prefix}index.html#productos">{I_CART}<span>Comprar</span></a></div></header>"""

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
 groups.forEach(function(g){g.hidden=!g.querySelector('.card:not([hidden])')});
 if(empty)empty.style.display=n?'none':'block';}
q.addEventListener('input',run);
q.form.addEventListener('submit',function(ev){ev.preventDefault();run();document.getElementById('productos').scrollIntoView({behavior:'smooth'})});
chips.forEach(function(b){b.addEventListener('click',function(){cat=b.dataset.c;chips.forEach(function(x){x.setAttribute('aria-pressed',x===b)});run()})});
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

def card(p, prefix="", lazy=True):
    q = norm(" ".join([p["name"], p["short"], p["task"], CATS[p["cat"]]]))
    ld = ' loading="lazy"' if lazy else ""
    return f"""<li class="card" data-c="{p['cat']}" data-q="{e(q)}"><a class="ph" href="{prefix}{ppath(p)}" tabindex="-1" aria-hidden="true"><img src="{photo(p['slug'], prefix)}" width="600" height="600" alt=""{ld}></a>
<div class="bd"><span class="ct">{CATS[p['cat']]}</span><h3><a href="{prefix}{ppath(p)}">{e(p['name'])}</a></h3><p class="sh">{e(p['short'])}</p>
<p class="pr num-t">{e(p['price'])}{'<small>Precio orientativo</small>' if '€' in p['price'] else ''}</p><a class="btn" href="{amazon_url(p['query'])}" target="_blank" rel="sponsored noopener">Comprar en Amazon</a></div></li>"""

def index():
    tiles = ""
    for i, s in enumerate(HERO):
        p = BYSLUG[s]
        tiles += f'<a href="{ppath(p)}"><img src="{photo(s)}" width="900" height="900" alt="{e(alt(p))}"{"" if i == 0 else " loading=\"lazy\""}><span class="tag">{e(p["name"])}<b class="num-t">{("desde " + e(p["price"].split(" –")[0]) + " €") if "€" in p["price"] else "Ver precio"}</b></span></a>'
    ticks = "".join(f"<li>{I_CHECK}{t}</li>" for t in ["Pago seguro en Amazon", "Envío rápido", "Devolución fácil"])
    trust = "".join(f"<li>{i}<strong>{t}</strong><span>{d}</span></li>" for i, t, d in TRUST)
    cats = ""
    for k, v in CATS.items():
        n = sum(1 for p in PRODUCTS if p["cat"] == k)
        cats += f'<a class="cat" href="#{k}"><img src="{photo(CAT_IMG[k])}" width="800" height="600" alt="" loading="lazy"><div><h3>{v}</h3><p>{CAT_TXT[k]}</p><span class="n">{n} productos {I_ARROW}</span></div></a>'
    chips = '<button class="chip" type="button" data-c="" aria-pressed="true">Todo</button>' + "".join(f'<button class="chip" type="button" data-c="{k}" aria-pressed="false">{v}</button>' for k, v in CATS.items())
    groups = ""
    for k, v in CATS.items():
        items = [p for p in PRODUCTS if p["cat"] == k]
        groups += f'<div class="group" id="{k}"><h3>{v} <span>{len(items)} productos</span></h3><ul class="grid">{"".join(card(p) for p in items)}</ul></div>'
    blog = "".join(f'<li><a href="{g[0]}"><img src="{pic(g[4],900,600)}" width="900" height="600" alt="{e(GUIDE_ALT[g[4]])}" loading="lazy"><h3>{e(g[2])}</h3><p>{e(g[3])}</p></a></li>' for g in GUIDES)
    body = f"""{head("TODOHOME · Tienda online de productos para el hogar y la cocina","Facilita tu vida en casa: los mejores productos de cocina, limpieza y hogar. Compra segura en Amazon con envío rápido y devoluciones fáciles.","index.html","")}
{header("")}
<main>
<section class="hero"><div class="wrap in">
<div><h1>Facilita tu vida en casa</h1><p class="sub">Tenemos los mejores productos para el hogar y la cocina: cocina, limpieza y hogar, elegidos uno a uno y a buen precio.</p>
<div class="ctas"><a class="btn" href="#productos">Ver productos {I_ARROW}</a><a class="btn ghost" href="#categorias">Comprar por categoría</a></div>
<ul class="ticks">{ticks}</ul></div>
<div class="mosaic">{tiles}</div>
</div></section>
<section class="trust" aria-label="Por qué comprar con nosotros"><div class="wrap"><ul>{trust}</ul></div></section>

<section class="sec wrap" id="categorias" aria-labelledby="cath"><div class="sec-h"><div><h2 id="cath">Compra por categoría</h2><p>Todo lo que necesitas para una casa más fácil.</p></div></div>
<div class="cats">{cats}</div></section>

<section class="sec wrap" id="productos" aria-labelledby="ph" style="padding-top:0"><div class="sec-h"><div><h2 id="ph">Nuestros productos</h2><p>{len(PRODUCTS)} productos elegidos para tu casa.</p></div></div>
<div class="shop-tools" role="group" aria-label="Filtrar por categoría">{chips}</div>
{groups}<p class="empty" id="empty">No hemos encontrado ese producto. Prueba con otra palabra, como «cocina» o «limpieza».</p></section>

<section class="sec how" id="como-comprar" aria-labelledby="hh"><div class="wrap"><div class="sec-h"><div><h2 id="hh">Cómo comprar</h2><p>Tres pasos y lo tienes en casa.</p></div></div>
<ol class="steps"><li><h3>Elige tu producto</h3><p>Mira las fotos, las ventajas y el precio orientativo de cada producto.</p></li><li><h3>Pulsa «Comprar en Amazon»</h3><p>Te llevamos a la página del producto en Amazon, donde ves el precio final.</p></li><li><h3>Paga y recíbelo en casa</h3><p>Amazon gestiona el pago, el envío y las devoluciones, con su garantía.</p></li></ol></div></section>

<section class="sec wrap" id="guias" aria-labelledby="gh"><div class="sec-h"><div><h2 id="gh">Ideas para tu casa</h2><p>Guías rápidas para ordenar y limpiar con menos esfuerzo.</p></div></div>
<ul class="blog">{blog}</ul></section>

<section class="social wrap" aria-labelledby="sh"><div class="box"><div><h2 id="sh">Un producto nuevo cada semana</h2><p>Te enseñamos en vídeo cómo funciona cada producto antes de añadirlo a la tienda.</p></div>
<div class="btns"><a class="btn light" href="{TIKTOK}" target="_blank" rel="noopener">Seguir en TikTok</a><a class="btn light" href="{INSTA}" target="_blank" rel="noopener">Instagram</a></div></div></section>
</main>
{footer("")}
{SEARCH_JS}
</body></html>"""
    write("index.html", body)

def product_pages():
    for p in PRODUCTS:
        rel = [x for x in PRODUCTS if x["cat"] == p["cat"] and x["slug"] != p["slug"]][:3]
        rel = (rel + [x for x in PRODUCTS if x["slug"] != p["slug"] and x not in rel])[:3]
        bl = "".join(f"<li>{I_CHECK}<span>{e(b)}</span></li>" for b in p["bullets"])
        tr = "".join(f"<li>{i}<span><strong>{t}.</strong> {d}</span></li>" for i, t, d in TRUST[:3])
        note = "" if AMAZON_IMG.get(p["slug"]) else '<p class="note">' + p.get("note", "Foto orientativa del tipo de producto. El modelo de Amazon puede variar.") + '</p>'
        ld = json.dumps({"@context": "https://schema.org", "@type": "Product", "name": p["name"], "description": p["short"], "image": BASE + "/img/" + p["slug"] + ".jpg"}, ensure_ascii=False)
        body = f"""{head(p['name'] + ' | TODOHOME', p['short'] + ' Compra segura en Amazon.', ppath(p), '../')}
{header('../')}
<main class="wrap">
<p class="crumbs"><a href="../index.html">Inicio</a> / <a href="../index.html#{p['cat']}">{CATS[p['cat']]}</a> / {e(p['name'])}</p>
<div class="pdp"><div><div class="ph"><img src="{photo(p['slug'], '../')}" width="900" height="900" alt="{e(alt(p))}"></div>{note}</div>
<div><span class="ct">{CATS[p['cat']]}</span><h1>{e(p['name'])}</h1><p class="sh">{e(p['short'])}</p>
<p class="pr num-t">{e(p['price'])}<small>{'Precio orientativo. ' if '€' in p['price'] else ''}El precio final lo marca Amazon.</small></p>
<a class="btn" href="{amazon_url(p['query'])}" target="_blank" rel="sponsored noopener">{I_CART} Comprar en Amazon</a>
<ul class="bl">{bl}</ul><ul class="tr">{tr}</ul>
<div class="desc"><h2>Descripción</h2><p>{e(p['desc'])}</p></div></div></div>
<section class="sec" style="padding-top:0" aria-labelledby="rh"><div class="sec-h"><div><h2 id="rh">También te puede interesar</h2></div><a href="../index.html#{p['cat']}">Ver todo en {CATS[p['cat']]}</a></div>
<ul class="grid">{''.join(card(x, '../') for x in rel)}</ul></section>
</main>
{footer('../')}
<script type="application/ld+json">{ld}</script>
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
