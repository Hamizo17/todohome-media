# Vídeo TODOHOME con clips reales de uso (Pexels) de fondo + rótulos encima.
# Uso: python3 clips.py <dir> <carpeta_clips> <salida.mp4>
# <dir> contiene spec.json (dur, hook, hooksize, name, keys, clips=[[id, segundo_inicio] x7]), tl.json y voz.mp3.
# Cada clip cubre una frase de la voz. Los verticales van a pantalla completa; los horizontales,
# ampliados en el centro sobre el mismo clip desenfocado.
import json, os, subprocess, sys
d, cdir, out = sys.argv[1], sys.argv[2], sys.argv[3]
here = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(d, "spec.json")))
TL = json.load(open(os.path.join(d, "tl.json")))
D = S["dur"]
st = [0.0] + [round(l["t0"] - .1, 2) for l in TL[1:]][:6]
run = lambda c: subprocess.run(c, shell=True, check=True)

# 1) fondo
segs = []
for k, (cid, ss) in enumerate(S["clips"]):
    f = os.path.join(cdir, f"{cid}.mp4")
    dur = (st[k + 1] if k < 6 else D) - st[k]
    h = int(subprocess.check_output(f"ffprobe -v error -select_streams v -show_entries stream=height -of csv=p=0 {f}", shell=True))
    full = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
    if h >= 1500:
        vf = f"[0:v]{full},setsar=1,fps=30[v]"
    else:
        vf = (f"[0:v]split[a][b];[a]{full},boxblur=40:2,eq=brightness=-0.12[bg];"
              f"[b]scale=-2:1000,crop=1080:1000[fg];[bg][fg]overlay=0:430,setsar=1,fps=30[v]")
    o = os.path.join(d, f"seg{k}.mp4")
    run(f"ffmpeg -y -loglevel error -ss {ss} -t {dur:.3f} -i {f} -filter_complex \"{vf}\" -map \"[v]\" -an -c:v libx264 -crf 16 -preset fast {o}")
    segs.append(o)
open(os.path.join(d, "segs.txt"), "w").write("".join(f"file '{os.path.abspath(s)}'\n" for s in segs))
run(f"ffmpeg -y -loglevel error -f concat -safe 0 -i {d}/segs.txt -c copy {d}/bg.mp4")

# 2) rótulos (PNG transparentes)
html = open(os.path.join(here, "ov.html")).read()
for k, v in dict(HOOK=S["hook"], HOOKSIZE=str(S.get("hooksize", 130)), NAME=S["name"], TLJ=json.dumps(TL),
                 DUR=str(D), ST=json.dumps(st), KEY=json.dumps(S["keys"])).items():
    html = html.replace("__" + k + "__", v)
open(os.path.join(here, "_ov.html"), "w").write(html)
js = """const {chromium}=require('playwright');(async()=>{const [,,page,dir,D]=process.argv;const fs=require('fs');fs.mkdirSync(dir+'/ov',{recursive:true});
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+page);await p.evaluate(()=>document.fonts.ready);
for(let i=0;i<Math.round(D*30);i++){await p.evaluate(t=>seek(t),i/30);await p.screenshot({path:`${dir}/ov/${String(i).padStart(4,'0')}.png`,omitBackground:true});}
await b.close()})();"""
open(os.path.join(d, "_ov.js"), "w").write(js)
run(f"cd {here} && node {os.path.abspath(d)}/_ov.js {here}/_ov.html {os.path.abspath(d)} {D}")

# 3) audio: voz (+0,2 s) y tecno con sidechain, como en hacer.sh
run(f"cd {here} && python3 tecno2.py {D} {','.join(map(str, st))} {os.path.abspath(d)}/tecno.wav")
run(f"ffmpeg -y -loglevel error -i {d}/voz.mp3 -af 'adelay=200|200,apad' -t {D} -ar 48000 -ac 2 {d}/voz.wav")
run(f"ffmpeg -y -loglevel error -i {d}/voz.wav -i {d}/tecno.wav -filter_complex \"[1:a]volume=0.55,aformat=channel_layouts=stereo[m];[0:a]asplit=2[v][vs];[m][vs]sidechaincompress=threshold=0.05:ratio=3:attack=5:release=250[md];[md][v]amix=inputs=2:normalize=0,loudnorm=I=-12:TP=-1:LRA=9[a]\" -map \"[a]\" -t {D} -ar 48000 {d}/mezcla.wav")

# 4) composición final
run(f"ffmpeg -y -loglevel error -i {d}/bg.mp4 -framerate 30 -i {d}/ov/%04d.png -i {d}/mezcla.wav -filter_complex \"[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[v]\" -map \"[v]\" -map 2:a -c:v libx264 -preset slow -b:v 9M -c:a aac -b:a 192k -t {D} -movflags +faststart {out}")
print(subprocess.check_output(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {out}", shell=True).decode().strip())
