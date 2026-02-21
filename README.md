# Proteger_pdf

Programa en Python que cifra archivos PDF y genera una copia segura con una contraseña fuerte generada automáticamente.

Características

- Interfaz gráfica con `Tkinter` (incluido en Python).
- Ventana para seleccionar el PDF.
- Genera y muestra una contraseña segura (para copiar/guardar).
- Crea el PDF encriptado usando `qpdf` con cifrado AES-256.
- Opción para elegir dónde guardar el archivo resultante.

Requisitos previos

- Python 3 instalado.
- `qpdf` instalado y accesible desde la línea de comandos (en el PATH).
- (Opcional, pero recomendado para mejor experiencia) Instalar paquetes Python extra:

  ```bash
  pip install tkinterdnd2 pillow
  ```

## Dependencias opcionales

- `Pillow` — mejora la carga de iconos y formatos de imagen en la GUI (opcional).

  Instalar con:

  ```bash
  pip install pillow
  ```

  Nota: el script intenta cargar `tren.ico` usando Pillow si está disponible; si no, usa un intento de fallback con `tk.PhotoImage`. Si quieres ver el icono en la esquina inferior derecha asegúrate de instalar `Pillow`.

Instalación de qpdf

- En Windows (recomendado con Chocolatey):

  1. Abrir CMD o PowerShell como administrador.
  2. Ejecutar:
     ```powershell
     choco install qpdf
     ```
  Si no usas Chocolatey, descarga qpdf desde https://github.com/qpdf/qpdf/releases y agrega la carpeta de qpdf al PATH del sistema.

- En macOS (Homebrew):

  ```bash
  brew install qpdf
  ```

- En Linux (ejemplo Debian/Ubuntu):

  ```bash
  sudo apt update && sudo apt install qpdf
  ```

Nota: el programa necesita que `qpdf` esté instalado y accesible desde la línea de comandos. Si `qpdf` no está en el PATH, el cifrado fallará.

Uso rápido (sin GUI)

Desde una terminal (ejemplo):

```bash
qpdf --encrypt MiClaveSegura123! MiClaveSegura123! 256 --modify=none -- input.pdf output_protegido.pdf
```

- `256` indica cifrado AES-256.
- `--modify=none` restringe la mayoría de modificaciones en el PDF cifrado.

Ejecutable independiente (.exe / binario)

Para empaquetar el script `pdf_protector.py` en un ejecutable independiente usar `PyInstaller`:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icono.ico pdf_protector.py
```

- El `.exe` (o binario en `dist/`) aparecerá en la carpeta `dist/`.
- Si no tienes un icono `.ico`, elimina `--icon=icono.ico` de la línea de comandos.
- Nota: empaquetar no elimina la dependencia de `qpdf` a menos que empaquetes `qpdf` también con métodos avanzados; normalmente la máquina de destino debe tener `qpdf` instalado o accesible.

## Iconos y formatos (macOS / Windows)

Si quieres usar un icono personalizado para el ejecutable o para la GUI (`tren.ico` incluido), aquí tienes comandos y pasos útiles.

- Convertir un PNG a `.icns` (macOS, usa `sips` + `iconutil`):

  ```zsh
  # parte 1: crear una carpeta icon.iconset con las resoluciones necesarias
  mkdir icon.iconset
  sips -z 16 16   icon.png --out icon.iconset/icon_16x16.png
  sips -z 32 32   icon.png --out icon.iconset/icon_16x16@2x.png
  sips -z 32 32   icon.png --out icon.iconset/icon_32x32.png
  sips -z 64 64   icon.png --out icon.iconset/icon_32x32@2x.png
  sips -z 128 128 icon.png --out icon.iconset/icon_128x128.png
  sips -z 256 256 icon.png --out icon.iconset/icon_128x128@2x.png
  sips -z 256 256 icon.png --out icon.iconset/icon_256x256.png
  sips -z 512 512 icon.png --out icon.iconset/icon_256x256@2x.png
  sips -z 512 512 icon.png --out icon.iconset/icon_512x512.png
  sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png

  # parte 2: generar .icns
  iconutil -c icns icon.iconset
  ```

  iconutil está incluido en macOS; `sips` también.

- Convertir un `.ico` a `.png` o a `.icns` (si tienes ImageMagick):

  ```zsh
  # instalar ImageMagick en macOS
  brew install imagemagick

  # convertir .ico a png (extrae la mejor resolución disponible)
  magick convert tren.ico tren.png

  # luego genera .icns usando el método anterior (crear icon.iconset con tren.png)
  ```

- Crear un `.ico` (Windows) desde PNG (ImageMagick):

  ```powershell
  magick convert -background transparent icon_512x512.png -define icon:auto-resize=64,48,32,16 tren.ico
  ```

- Notas:
  - Para usar `.icns` como icono de la app en macOS con PyInstaller, pasa `--icon=icono.icns` al generar el binario.
  - Para Windows, usa `--icon=tren.ico` al crear el `.exe`.
  - Si solo necesitas ver el icono dentro de la GUI Tkinter, el script intenta cargar `tren.ico` usando Pillow; instala Pillow con `pip install pillow` para mejor compatibilidad.

Cómo funciona (resumen técnico)

- El script genera una contraseña segura aleatoria y la muestra al usuario para que la copie y la guarde de forma segura.
- Usa `qpdf` para crear una copia cifrada del PDF con AES-256 y parámetros que limitan modificaciones (`--modify=none`).

Consejos de seguridad

- Guarda la contraseña en un gestor de contraseñas seguro. Si pierdes la contraseña, no podrás abrir el PDF cifrado.
- Revisa los permisos y la localización del archivo resultante antes de compartirlo.

Archivos importantes

- `pdf_protector.py` — script principal con la interfaz gráfica y la lógica de cifrado.
- `notas.txt` — notas sobre instalación y uso (origen de este README).

Más información

- Documentación y lanzamientos de `qpdf`: https://github.com/qpdf/qpdf/releases

Si necesitas adaptar las instrucciones a otra plataforma o quieres que incluya ejemplos adicionales, indicar la plataforma objetivo.
