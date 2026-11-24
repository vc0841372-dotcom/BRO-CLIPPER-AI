# BRO CLIPPER AI — Beta Android

Primera versión local para Termux. No requiere suscripción ni API de pago.

## Qué hace
- Recibe un enlace de YouTube.
- Descarga el video con yt-dlp (úsalo solo con contenido propio o autorizado).
- Transcribe el audio localmente con whisper.cpp.
- Puntúa ventanas de 45 segundos mediante señales del texto y elige fragmentos no solapados.
- Exporta clips MP4 verticales 9:16 a `Movies/BRO_CLIPPER`.

## Limitaciones honestas
Esta beta **no usa un LLM para entender semánticamente el video**. Whisper reconoce el habla; el selector usa reglas y palabras/frases de interés para proponer momentos. No garantiza que cada clip tenga sentido completo. Revisa los resultados antes de publicarlos. Una selección semántica más avanzada requeriría integrar y ejecutar un modelo de lenguaje local compatible con tu teléfono, lo cual puede ser lento y consumir bastante almacenamiento/RAM.

## Instalación en Android
1. Instala Termux desde F-Droid: https://f-droid.org/packages/com.termux/
2. Abre Termux y concede permisos cuando Android los solicite.
3. Copia `install.sh` y `bro_clipper.py` a la carpeta de Termux (por ejemplo, Descargas y luego moverlos a `~/bro_clipper/`).
4. En Termux ejecuta:
   ```bash
   termux-setup-storage
   mkdir -p ~/bro_clipper
   ```
5. Ejecuta el instalador:
   ```bash
   bash ~/bro_clipper/install.sh
   ```
   Si el archivo quedó en Descargas, usa la ruta real donde lo guardaste.
6. Inicia la aplicación:
   ```bash
   python ~/bro_clipper/bro_clipper.py
   ```

## Requisitos
- Internet para instalar dependencias y obtener el video/modelo.
- Espacio libre: el modelo tiny ocupa aproximadamente 75 MB; el video y el audio temporal necesitan espacio adicional.
- El primer análisis puede tardar bastante porque se ejecuta en CPU.

## Nota de YouTube
No elude restricciones de acceso ni DRM. No uses cookies ni intentes descargar videos privados, de pago o restringidos. Respeta derechos de autor, permisos del creador y las condiciones aplicables de YouTube.
