@echo off
cls
@REM Este script tiene que ser ejecutado desde el acceso directo que crea los archivos .vbs
echo Activando el entorno virtual...
call venv\Scripts\activate
echo Iniciando la aplicación...
cls
python src\fl_init.py
pause
