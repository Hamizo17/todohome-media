# Genera el HTML animado de un vídeo TODOHOME a partir de spec.json + tl.json
# Uso: python3 gen.py <dir>   (dir contiene spec.json, tl.json; escribe v.html)
import json, sys, os
d = sys.argv[1]
S = json.load(open(os.path.join(d, "spec.json")))
TL = json.load(open(os.path.join(d, "tl.json")))
D = S["dur"]
st = [0.0] + [round(l["t0"] - .1, 2) for l in TL[1:]]
st = st[:7]
img = S["img"]
pill = lambda i, b, t: f'<div class="pill" id="{i}" style="left:80px;top:{t}px"><b>{b}</b>{{}}</div>'
steps = "".join(pill(f"p3{k+1}", k + 1, 300 + 150 * k).format(x) for k, x in enumerate(S["steps"]))
bens = "".join(pill(f"p5{k+1}", "✓", 320 + 150 * k).format(x) for k, x in enumerate(S["benefits"]))
html = open(os.path.join(os.path.dirname(__file__), "tpl.html")).read()
rep = dict(IMG=img, HOOK=S["hook"], HOOKSIZE=str(S.get("hooksize", 140)), NAME=S["name"], STEPS=steps,
           STAT_TOP=S["stat_top"], STAT_BIG=S["stat_big"], STAT_SUB=S["stat_sub"], BENS=bens,
           PRICE=S["price"], PRICE_PRE=S.get("price_pre", "Desde"), POS3=S.get("pos3", "50% 30%"), POS5=S.get("pos5", "50% 75%"),
           ST=json.dumps(st), TLJ=json.dumps(TL), DUR=str(D), KEY=json.dumps(S["keys"]),
           THUMBS="".join(f'<div class="card" style="position:relative;width:260px;height:260px;border-radius:28px"><img src="{t}"></div>' for t in S["thumbs"]))
for k, v in rep.items():
    html = html.replace("__" + k + "__", v)
open(os.path.join(d, "v.html"), "w").write(html)
print("escenas", st)
