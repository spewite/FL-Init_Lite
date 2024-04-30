@echo off
cls
echo Verificando instalación de Python...
where python
if %errorlevel% neq 0 (
    echo Python no está instalado. Por favor instale Python antes de continuar.
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

echo Iniciando
