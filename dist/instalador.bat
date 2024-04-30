@echo off
cls
echo Verificando instalacion de Python...
where python
if %errorlevel% neq 0 (
    echo Python no esta instalado. Por favor instale Python antes de continuar.
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

cls

echo Iniciando la aplicación...
timeout /t 1 /nobreak >nul
call python ..\src\fl_init.py

