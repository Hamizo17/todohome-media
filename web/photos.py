# Fotos reales de cada producto.
# FREE: fotos libres de Pexels (licencia Pexels, uso comercial gratis), por orden de preferencia.
# AMAZON_IMG: cuando haya acceso a la API de Amazon (PA-API), poner aquí la URL de imagen de cada producto
# y sustituirá a la foto libre sin tocar el diseño. Nunca descargar ni copiar fotos de Amazon.
FREE = {
 "robot-friegasuelos-cecotec": [8566426, 7641488, 8566427],
 "aspiradora-sin-cable-vactechpro": [12167653, 12167650],
 "alfombrilla-bano-diatomita": [34667257, 12273900],
 "pulverizador-aceite-2-en-1": [38490979, 38476686, 38476688],
 "vaporera-ufesa": [8093852, 8093871],
 "tostadora-philips": [4493668, 3997309, 5825406],
 "perchero-vasagle": [10838789, 6032031],
 "calefactor-ceramico-dreo": [6530548, 11564927],
}
AMAZON_IMG = {}

def pexels(i, w=900):
    return f"https://images.pexels.com/photos/{i}/pexels-photo-{i}.jpeg?auto=compress&cs=tinysrgb&w={w}"
