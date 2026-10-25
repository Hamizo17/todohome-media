# Descarga en la construcción la primera foto libre que responda de cada producto a OUT/img/<slug>.jpg
import json, os, sys, urllib.request
from photos import FREE, pexels
OUT = os.environ.get("OUT", "public/")
os.makedirs(OUT + "img", exist_ok=True)
got, bad = {}, []
for slug, ids in FREE.items():
    for i in ids:
        try:
            req = urllib.request.Request(pexels(i), headers={"User-Agent": "Mozilla/5.0 TODOHOME build"})
            b = urllib.request.urlopen(req, timeout=20).read()
            if b[:3] != b"\xff\xd8\xff" or len(b) < 8000:
                raise ValueError("no es JPEG")
            open(f"{OUT}img/{slug}.jpg", "wb").write(b)
            got[slug] = i
            print(f"ok {slug} {i} {len(b)}")
            break
        except Exception as ex:
            print(f"fallo {slug} {i}: {ex}")
    else:
        bad.append(slug)
json.dump(got, open(OUT + "img/fotos.json", "w"))
if bad:
    sys.exit("Sin foto: " + ", ".join(bad))
