@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo GENERACION AUTOMATICA DEL CAPITULO IV
echo ============================================================

python -m pip install pandas xlsxwriter python-docx pillow
if errorlevel 1 (
    echo Error al verificar dependencias.
    pause
    exit /b 1
)

python scripts\11_generar_capitulo_iv.py
if errorlevel 1 (
    echo.
    echo No se pudo generar el Capitulo IV.
    pause
    exit /b 1
)

echo.
echo Productos disponibles en outputs\reportes\
pause
