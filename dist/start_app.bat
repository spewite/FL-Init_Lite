@echo off
cls
echo Activando el entorno virtual...
call venv\Scripts\activate
echo Iniciando la aplicación...
cls
python src\fl_init.py
pause
