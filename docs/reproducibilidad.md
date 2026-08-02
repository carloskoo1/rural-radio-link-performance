# Reproducibilidad

## Preparación

```bat
cd C:\ruta\al\repositorio
python -m pip install -r requirements.txt
```

## Ejecución

```bat
ejecutar_pipeline_RC5.bat
```

## Control de versión

```bash
git status
git add .
git commit -m "Release v1.0.0 - Final reproducible thesis pipeline"
git tag -a v1.0.0 -m "Final reproducible thesis release"
git push origin main
git push origin v1.0.0
```

## Verificación

- ejecución sin excepciones;
- tablas, figuras, Word y Excel generados;
- README alineado con el código;
- ausencia de credenciales;
- nombres de archivos coincidentes con el pipeline real.
