@echo off
setlocal

cd /d "%~dp0"

echo ============================================================
echo GENERACION DE REPORTES DE TESIS
echo ============================================================

python -m pip install pandas xlsxwriter python-docx pillow
if errorlevel 1 (
    echo.
    echo No fue posible instalar o verificar las dependencias.
    pause
    exit /b 1
)

python scripts\10_generar_reporte_tesis.py
if errorlevel 1 (
    echo.
    echo El reporte no pudo generarse. Revise el mensaje anterior.
    pause
    exit /b 1
)

echo.
echo Productos disponibles en:
echo outputs\reportes\
echo.
pause
