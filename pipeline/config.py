
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

KRUSKAL_DUNN_SCRIPT = ROOT / "scripts" / "07_kruskal_dunn.py"

DOCX_OUT = REPORTS / "Capitulo_IV_Resultados_V5.docx"
XLSX_OUT = REPORTS / "resultados_tesis_V5.xlsx"
LOG_OUT = LOGS / "pipeline_tesis_V5.log"

ALPHA = 0.05
UMBRAL_LLUVIA_MM_H = 0.10
UMBRALES_SENSIBILIDAD = [0.00, 0.01, 0.05, 0.10, 0.20, 0.50, 1.00]

TABLE_START_ROMAN = "IV"
FIGURE_START = 7

FIGURE_ORDER = [
    ("fig_4_9_cv_rssi", "Coeficiente de variación del RSSI descendente por escenario experimental."),
    ("fig_4_10_boxplot_rssi", "Distribución del RSSI descendente por escenario experimental."),
    ("fig_4_11_cv_mcs", "Coeficiente de variación del MCS descendente por escenario experimental."),
    ("fig_4_11_cv_throughput", "Coeficiente de variación del throughput descendente observado."),
    ("fig_4_12_indice_variabilidad", "Índice relativo de variabilidad operativa por escenario experimental."),
]
