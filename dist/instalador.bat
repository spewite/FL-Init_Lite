@echo off
cls
echo Verificando instalacion de Python...
where python
if %errorlevel% neq 0 (
    echo Python no esta instalado. Por favor instale Python antes de continuar.
    pause
    exit
)

echo Verificando instalacion de FFmpeg...
where FFmpeg
if %errorlevel% neq 0 (
    echo FFmpeg no esta instalado. Por favor instale FFmpeg antes de continuar. Tienes documentacion de como instalarlo en el README.
    pause
    exit
)

echo Creando entorno virtual...
timeout /t 1 /nobreak >nul

if not exist "..\venv" (
    python -m venv ..\venv
    echo Entorno virtual creado.
) else (
    echo Entorno virtual ya existe.
)

echo Activando entorno virtual...
timeout /t 1 /nobreak >nul
call ..\venv\Scripts\activate

echo Entorno virtual activado.
timeout /t 1 /nobreak >nul

echo Instalando dependencias...
timeout /t 1 /nobreak >nul
pip install -r ..\requirements.txt

echo Creando accesos directo en la raiz del proyecto...
timeout /t 2 /nobreak >nul
cscript //nologo crear_acceso_directo_raiz.vbs

echo Creando accesos directo en el escritorio...
timeout /t 2 /nobreak >nul
cscript //nologo crear_acceso_directo_escritorio.vbs

cls
echo Iniciando la aplicacion...
timeout /t 3 /nobreak >nul
call python ..\src\fl_init.py

