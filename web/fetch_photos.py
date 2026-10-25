# Descarga en la construcción las fotos libres de cada producto: la primera que responda va a
# OUT/img/<slug>.jpg y las demás a <slug>-2.jpg, <slug>-3.jpg... (galería de la ficha)
import json, os, sys, urllib.request
from photos import FREE, pexels
OUT = os.environ.get("OUT", "public/")
os.makedirs(OUT + "img", exist_ok=True)
got, bad = {}, []
for slug, ids in FREE.items():
    n = 0
    for i in ids:
        try:
            req = urllib.request.Request(pexels(i), headers={"User-Agent": "Mozilla/5.0 TODOHOME build"})
            b = urllib.request.urlopen(req, timeout=20).read()
            if b[:3] != b"\xff\xd8\xff" or len(b) < 8000:
                raise ValueError("no es JPEG")
            n += 1
            open(f"{OUT}img/{slug}{'' if n == 1 else '-' + str(n)}.jpg", "wb").write(b)
            print(f"ok {slug} {i} {len(b)}")
        except Exception as ex:
            print(f"fallo {slug} {i}: {ex}")
    if n:
        got[slug] = n
    else:
        bad.append(slug)
json.dump(got, open(OUT + "img/fotos.json", "w"))
if bad:
    sys.exit("Sin foto: " + ", ".join(bad))
