# sh hacer.sh <dir> <salida.mp4>   (dir con v.html, spec.json, tl.json, voz.mp3)
set -e
d=$1; out=$2
D=$(python3 -c "import json;print(json.load(open('$d/spec.json'))['dur'])")
ST=$(grep -o 'ST = \[[^]]*\]' $d/v.html | tr -d 'ST=[] ')
python3 tecno2.py $D $ST $d/tecno.wav
node rend.js $d
ffmpeg -y -loglevel error -i $d/voz.mp3 -af "adelay=200|200,apad" -t $D -ar 48000 -ac 2 $d/voz.wav
ffmpeg -y -loglevel error -i $d/voz.wav -i $d/tecno.wav -filter_complex "[1:a]volume=0.55,aformat=channel_layouts=stereo[m];[0:a]asplit=2[v][vs];[m][vs]sidechaincompress=threshold=0.05:ratio=3:attack=5:release=250[md];[md][v]amix=inputs=2:normalize=0,loudnorm=I=-12:TP=-1:LRA=9[a]" -map "[a]" -t $D -ar 48000 $d/mezcla.wav
ffmpeg -y -loglevel error -framerate 30 -i $d/fr/%04d.jpg -i $d/mezcla.wav -c:v libx264 -preset slow -b:v 9M -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart $out
ffprobe -v error -show_entries format=duration -of csv=p=0 $out
