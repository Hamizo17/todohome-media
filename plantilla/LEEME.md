# Plantilla de vídeos TODOHOME

Formato: TikTok vertical 1080x1920, unos 18 s, 7 escenas (gancho, producto, 3 pasos, dato, 2 ventajas, precio, cierre «enlace en la bio»).
Estilo fijado por hamza: sin salir él, voz comercial de ElevenLabs «Bobby Your Commercial Voice» (voice_id RXPQcKYH6wnQn5NLiWCD, modelo eleven_v4, prompt que empieza con [energetic] y frases separadas por « ... »), música techno alta, subtítulos grandes con palabras clave en verde.

## Hacer un vídeo nuevo
1. Escribe 7 frases (una por escena) y genera la voz con ElevenLabs. Descarga la toma como `productos/<p>/voz.mp3`.
2. Saca los cortes entre frases: `ffmpeg -i voz.mp3 -af silencedetect=n=-32dB:d=0.15 -f null -`. Si sobran cortes (pausas dentro de una frase), quédate con los que separan frases.
3. Escribe `productos/<p>/tl.json` con t0/t1 de cada frase **+0.2 s** (la voz entra con 0,2 s de retraso) y `spec.json` (mira los ejemplos en productos/).
   `dur` = duración de la voz + 0,5 s.
4. `cd plantilla && ln -sfn ../../img productos/<p>/img && ln -sf ../../archivo.woff2 productos/<p>/archivo.woff2`
5. `python3 gen.py productos/<p>` y revisa fotogramas con `node rend.js productos/<p> 1.5,4,7,10,13,16`.
6. `sh hacer.sh productos/<p> ../videos/<p>.mp4`
7. Portada: copia portada.html a productos/<p>/, cambia imagen, titular y precio, y saca la captura con Playwright (ver port.js).

Requisitos: python3 con numpy y soundfile, ffmpeg, node con playwright.
