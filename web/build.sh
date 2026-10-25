# Construcción de la web en Vercel (proyecto todohome): fuente, fotos libres y HTML en public/
set -e
npm pack @fontsource-variable/archivo@5.3.0 >/dev/null
tar xzf fontsource-variable-archivo-5.3.0.tgz
mkdir -p public/fonts
cp package/files/archivo-latin-standard-normal.woff2 public/fonts/archivo.woff2
OUT=public/ python3 fetch_photos.py
OUT=public/ python3 site.py
