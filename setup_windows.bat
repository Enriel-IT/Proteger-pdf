@echo off
SETLOCAL

:: Elevar a administrador si es necesario
net session >nul 2>&1
if %errorlevel% neq 0 (
  echo Se requieren permisos de administrador. Se va a solicitar elevación...
  powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
  exit /b
)

echo.
echo ==== Verificando Python 3 (se usará el lanzador 'py') ====
py -3 --version >nul 2>&1
if %errorlevel% neq 0 (
  echo ERROR: Python 3 no detectado en el sistema o no en PATH.
  echo Instala Python 3 desde: https://www.python.org/downloads/  y activa "Add Python to PATH" durante la instalacion.
  pause
  exit /b 1
)

echo Actualizando pip...
py -3 -m pip install --upgrade pip

echo.
echo ==== Instalando paquetes Python necesarios ====
echo Instalando: tkinterdnd2, pillow, pyinstaller
py -3 -m pip install --upgrade tkinterdnd2 pillow pyinstaller

echo.
echo ==== Comprobando Chocolatey (necesario para instalar qpdf) ====
choco -v >nul 2>&1
if %errorlevel% neq 0 (
  echo Chocolatey no detectado. Se procederá a su instalacion (requiere Internet).
  powershell -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
  if %errorlevel% neq 0 (
    echo ERROR: Fallo la instalacion automatica de Chocolatey. Instala Chocolatey manualmente https://chocolatey.org/install
    pause
  ) else (
    echo Chocolatey instalado correctamente.
  )
) else (
  echo Chocolatey ya instalado.
)

echo.
echo ==== Instalando qpdf via Chocolatey ====
choco install -y qpdf

echo.
echo Verificando qpdf en PATH...
where qpdf >nul 2>&1
if %errorlevel% neq 0 (
  echo ADVERTENCIA: qpdf no se detecta en PATH. Reinicia la consola o agrega la carpeta de qpdf al PATH manualmente.
) else (
  echo qpdf detectado correctamente.
)

echo.
echo ==== Instalacion finalizada ====
echo - Python packages: tkinterdnd2, pillow, pyinstaller
echo - qpdf: instalado (si no, revisa mensajes previos)
echo.
echo Para generar un ejecutable (opcional):
echo py -3 -m pyinstaller --onefile --windowed --icon=icono.ico pdf_protector.py
echo.
echo Reinicia el equipo si se han añadido nuevas variables de entorno.
pause
exit /b 0
