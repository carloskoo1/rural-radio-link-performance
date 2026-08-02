@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo GENERACION VALIDADA DEL CAPITULO IV
echo ============================================================

python -m pip install pandas numpy scipy xlsxwriter python-docx pillow
if errorlevel 1 (
    echo Error al verificar dependencias.
    pause
    exit /b 1
)

python scripts\12_generar_capitulo_iv_validado.py
if errorlevel 1 (
    echo.
    echo No se pudo generar el Capitulo IV validado.
    pause
    exit /b 1
)

echo.
echo Productos disponibles en outputs\reportes\
pause
