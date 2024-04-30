@echo off
cls
echo Activando el entorno virtual...
call ..\venv\Scripts\activate

echo Iniciando la aplicacion...
cls
python ..\src\fl_init.py

