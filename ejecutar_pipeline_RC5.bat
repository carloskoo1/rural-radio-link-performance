@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo PIPELINE DE TESIS RC5
echo ============================================================

if not exist "pipeline_rc1\main.py" (
    echo.
    echo ERROR: No se encontro pipeline_rc1\main.py.
    echo Descomprima todo el ZIP directamente en:
    echo C:\Users\koo_c\radioenlace-eber-burga-github\
    pause
    exit /b 1
)

python -m pip install pandas numpy scipy statsmodels matplotlib xlsxwriter python-docx pillow
if errorlevel 1 (
    echo.
    echo Error al verificar dependencias.
    pause
    exit /b 1
)

set "PYTHONPATH=%CD%;%PYTHONPATH%"
python -m pipeline_rc1.main

if errorlevel 1 (
    echo.
    echo El pipeline termino con error.
    echo Revise outputs\logs\pipeline_tesis_RC5.log
    pause
    exit /b 1
)

echo.
echo Proceso completado correctamente.
echo.
echo Archivos generados:
echo outputs\reportes\Capitulo_IV_Resultados_RC5.docx
echo outputs\reportes\resultados_tesis_RC5.xlsx
echo outputs\logs\pipeline_tesis_RC5.log
echo outputs\figures\publicacion_rc5\
echo.
pause
