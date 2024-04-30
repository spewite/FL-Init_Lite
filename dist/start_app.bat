@echo off
cls
echo Activando el entorno virtual...
call ..\venv\Scripts\activate

echo Iniciando la aplicación...
python ..\src\fl_init.py

echo Aplicación finalizada. Presione cualquier tecla para salir...
pause
