# Evaluación experimental del desempeño técnico de un radioenlace rural

Repositorio científico asociado a una investigación sobre la relación entre la configuración técnica de un radioenlace punto a punto y su desempeño bajo condiciones reales de operación en un entorno rural altoandino de Cajamarca, Perú.

## Objetivo general

Evaluar la asociación entre la configuración técnica del radioenlace y su desempeño técnico bajo condiciones reales de operación.

## Objetivos específicos

1. Comparar el desempeño técnico entre los escenarios E0–E5.
2. Comparar el desempeño entre las franjas 20:00–22:00 y 01:00–03:00.
3. Analizar la asociación entre precipitación horaria y métricas técnicas.
4. Identificar la configuración con mayor estabilidad operativa.

## Escenarios

| Escenario | Frecuencia | Ancho de canal |
|---|---:|---:|
| E0 | 5800 MHz | 20 MHz |
| E1 | 5660 MHz | 40 MHz |
| E2 | 5660 MHz | 80 MHz |
| E3 | 5730 MHz | 40 MHz |
| E4 | 5730 MHz | 80 MHz |
| E5 | 5805 MHz | 40 MHz |

## Métricas

RSSI DL, SNR DL, MCS DL, Throughput DL observado, DE, RIC, CV, índice compuesto de estabilidad y precipitación horaria.

## Flujo

```text
Telemetría + cnMaestro + ERA5-Land
                ↓
Depuración y homologación
                ↓
Sincronización temporal
                ↓
Dataset consolidado
                ↓
Shapiro–Wilk
                ↓
Kruskal–Wallis + ε²
                ↓
Dunn + Holm
                ↓
Mann–Whitney + Holm + delta de Cliff
                ↓
Spearman
                ↓
Índice compuesto de estabilidad
                ↓
CSV + figuras + Word + Excel
```

## Instalación

```bash
python -m pip install -r requirements.txt
```

## Ejecución en Windows

```bat
ejecutar_pipeline_RC5.bat
```

Verifique que el nombre coincida con el lanzador definitivo del repositorio.

## Documentación

- `docs/metodologia.md`
- `docs/pipeline_estadistico.md`
- `docs/estructura_datos.md`
- `docs/reproducibilidad.md`

## Seguridad

No publique credenciales, tokens, claves, direcciones IP de administración ni archivos con información personal.

## Licencia

Código bajo licencia MIT.
