
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATA_PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"
TABLES = OUTPUTS / "tables"
FIGURES = OUTPUTS / "figures"
REPORTS = OUTPUTS / "reportes"
LOGS = OUTPUTS / "logs"

DATASET_ESCENARIOS = DATA_PROCESSED / "dataset_escenarios_full_day.csv"
DATASET_CLIMA = DATA_PROCESSED / "dataset_radio_clima.csv"

KRUSKAL_EXISTENTE = TABLES / "tabla_4_2_kruskal_wallis.csv"
DUNN_EXISTENTE = TABLES / "tabla_4_3_dunn_completa.csv"

DOCX_OUT = REPORTS / "Capitulo_IV_Resultados_RC5_3.docx"
XLSX_OUT = REPORTS / "resultados_tesis_RC5_3.xlsx"
LOG_OUT = LOGS / "pipeline_tesis_RC5_3.log"

ALPHA = 0.05
UMBRAL_LLUVIA_MM_H = 0.10
UMBRALES_SENSIBILIDAD = [0.00, 0.01, 0.05, 0.10, 0.20, 0.50, 1.00]

FIGURE_START = 7

TABLE_TITLES = {
    "normalidad": "Tabla IV. Resultados de Shapiro-Wilk por métrica y escenario",
    "kruskal": "Tabla V. Resultados de Kruskal-Wallis",
    "dunn": "Tabla VI. Síntesis de comparaciones post hoc de Dunn",
    "descriptivos": "Tabla VII. RSSI, SNR y MCS por escenario experimental",
    "throughput": "Tabla VIII. Throughput observado por escenario experimental",
    "franjas": "Tabla IX. Comparación entre franjas horarias por métrica",
    "precipitacion_diag": "Tabla X. Diagnóstico de consistencia de la precipitación",
    "precipitacion_sens": "Tabla XI. Sensibilidad de la clasificación de lluvia",
    "precipitacion_conteo": "Tabla XII. Registros según condición de precipitación",
    "precipitacion_senal": "Tabla XIII-A. RSSI y SNR según precipitación",
    "precipitacion_capacidad": "Tabla XIII-B. MCS y throughput según precipitación",
    "spearman": "Tabla XIV. Correlación horaria entre precipitación y métricas",
    "estabilidad_senal": "Tabla XV-A. Estabilidad de RSSI y SNR",
    "estabilidad_capacidad": "Tabla XV-B. Estabilidad de MCS y throughput",
    "objetivos": "Tabla XVI. Resumen integrado de objetivos e hipótesis",
    "anexo_dunn": "Tabla A1. Comparaciones post hoc de Dunn completas",
    "anexo_franjas": "Tabla A2. Comparaciones completas por franjas horarias",
}

FIGURE_TITLES = [
    "Desviación estándar del RSSI descendente por escenario experimental.",
    "Distribución del RSSI descendente por escenario experimental.",
    "Coeficiente de variación del MCS descendente por escenario experimental.",
    "Coeficiente de variación del throughput descendente observado.",
    "Índice compuesto de estabilidad operativa por escenario experimental.",
]


# Configuración explícita de la covariable de precipitación.
# El dataset procesado debe contener precip_mm expresada en mm/h.
PRECIP_INPUT_COLUMN = "precip_mm"
PRECIP_INPUT_UNIT = "mm/h"
PRECIP_CONVERSION_FACTOR = 1.0
PRECIP_STRICT_NONNEGATIVE = True
PRECIP_HIGH_WET_FRACTION_WARNING = 0.80
