
from __future__ import annotations

import logging
import subprocess
import sys

from .config import (
    DATASET_ESCENARIOS, DATASET_CLIMA, TABLES, REPORTS, LOGS,
    KRUSKAL_DUNN_SCRIPT, DOCX_OUT, XLSX_OUT, LOG_OUT,
)
from .io_utils import read_csv, write_csv
from .analysis import (
    shapiro_table, descriptives, rain_sensitivity, classify_rain,
    rain_count, rain_performance, hourly_spearman, dunn_summary,
)
from .reporting import create_word, create_excel


def configure_logging() -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_OUT, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def run_inferential_if_needed() -> None:
    required = [
        TABLES / "tabla_4_2_kruskal_wallis.csv",
        TABLES / "tabla_4_3_dunn_completa.csv",
        TABLES / "tabla_4_6_estabilidad_por_escenario.csv",
    ]
    if all(path.exists() for path in required):
        logging.info("Las tablas inferenciales ya existen; no se regeneran.")
        return
    if not KRUSKAL_DUNN_SCRIPT.exists():
        raise FileNotFoundError(f"No se encontró {KRUSKAL_DUNN_SCRIPT}")
    logging.info("Ejecutando análisis inferencial...")
    subprocess.run(
        [sys.executable, str(KRUSKAL_DUNN_SCRIPT)],
        cwd=KRUSKAL_DUNN_SCRIPT.parent.parent,
        check=True,
    )


def main() -> None:
    configure_logging()
    logging.info("Inicio del Pipeline de Tesis V5")
    TABLES.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    run_inferential_if_needed()

    scenarios = read_csv(DATASET_ESCENARIOS)
    climate = read_csv(DATASET_CLIMA)

    shapiro = shapiro_table(scenarios)
    signal_desc, th_desc = descriptives(scenarios)
    sensitivity = rain_sensitivity(climate)
    climate_valid = classify_rain(climate)
    count = rain_count(climate_valid)
    performance = rain_performance(climate_valid)
    spearman = hourly_spearman(climate_valid)

    write_csv(shapiro, TABLES / "tabla_4_1_normalidad_shapiro.csv")
    write_csv(sensitivity, TABLES / "tabla_4_7_sensibilidad_umbral_lluvia.csv")
    write_csv(count, TABLES / "tabla_4_8_conteo_lluvia_validado.csv")
    write_csv(performance, TABLES / "tabla_4_9_desempeno_lluvia_validado.csv")
    write_csv(spearman, TABLES / "tabla_4_10_spearman_horario.csv")

    kruskal = read_csv(TABLES / "tabla_4_2_kruskal_wallis.csv")
    dunn_full = read_csv(TABLES / "tabla_4_3_dunn_completa.csv")
    stability = read_csv(TABLES / "tabla_4_6_estabilidad_por_escenario.csv")

    stability = stability.rename(columns={
        "escenario": "Escenario",
        "rssi_dl_mean": "RSSI media (dBm)",
        "rssi_dl_std": "RSSI DE",
        "rssi_dl_cv": "RSSI CV (%)",
        "snr_dl_mean": "SNR media (dB)",
        "snr_dl_std": "SNR DE",
        "snr_dl_cv": "SNR CV (%)",
        "mcs_dl_mean": "MCS media",
        "mcs_dl_std": "MCS DE",
        "mcs_dl_cv": "MCS CV (%)",
        "throughput_dl_mean": "Throughput media (Mbps)",
        "throughput_dl_std": "Throughput DE",
        "throughput_dl_cv": "Throughput CV (%)",
    }).round(3)

    stability_signal = stability[
        ["Escenario", "RSSI media (dBm)", "RSSI DE", "RSSI CV (%)",
         "SNR media (dB)", "SNR DE", "SNR CV (%)"]
    ]
    stability_capacity = stability[
        ["Escenario", "MCS media", "MCS DE", "MCS CV (%)",
         "Throughput media (Mbps)", "Throughput DE", "Throughput CV (%)"]
    ]

    rain_signal = performance[
        ["Condición", "RSSI media", "RSSI DE", "RSSI mediana",
         "SNR media", "SNR DE", "SNR mediana"]
    ]
    rain_capacity = performance[
        ["Condición", "MCS media", "MCS DE", "MCS mediana",
         "Throughput media", "Throughput DE", "Throughput mediana"]
    ]

    tables = {
        "shapiro": shapiro,
        "kruskal": kruskal,
        "dunn_summary": dunn_summary(dunn_full),
        "dunn_full": dunn_full,
        "descriptive_signal": signal_desc,
        "descriptive_throughput": th_desc,
        "rain_sensitivity": sensitivity,
        "rain_count": count,
        "rain_signal": rain_signal,
        "rain_capacity": rain_capacity,
        "spearman": spearman,
        "stability_signal": stability_signal,
        "stability_capacity": stability_capacity,
    }

    logging.info("Generando Excel...")
    create_excel(tables)
    logging.info("Generando Word...")
    create_word(tables)

    logging.info("Proceso completado.")
    print("\nProductos generados:")
    print(f" - {XLSX_OUT}")
    print(f" - {DOCX_OUT}")
    print(f" - {LOG_OUT}")


if __name__ == "__main__":
    main()
