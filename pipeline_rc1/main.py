
import logging
import sys

from .m00_config import (
    DATASET_ESCENARIOS,
    DATASET_CLIMA,
    KRUSKAL_EXISTENTE,
    DUNN_EXISTENTE,
    TABLES,
    FIGURES,
    REPORTS,
    LOGS,
    DOCX_OUT,
    XLSX_OUT,
    LOG_OUT,
)
from .m01_io import read_csv, write_csv
from .m02_validacion import (
    validate_inputs,
    validate_no_rssi_cv,
    validate_text_blocks,
)
from .m03_normalidad import calcular_normalidad, texto_normalidad
from .m04_inferencial import resumen_dunn, texto_kruskal, texto_dunn
from .m05_descriptivos import calcular_descriptivos, texto_descriptivos
from .m06_franjas import analizar_franjas, texto_franjas
from .m07_precipitacion import (
    preparar_precipitacion,
    diagnostico_precipitacion,
    sensibilidad_lluvia,
    clasificar_lluvia,
    conteo_lluvia,
    desempeno_lluvia,
    spearman_horario,
    texto_precipitacion,
)
from .m08_estabilidad import calcular_estabilidad, texto_estabilidad
from .m09_objetivos import construir_resumen_objetivos
from .m10_figuras import generar_figuras
from .m11_word import create_word
from .m12_excel import create_excel
from .m13_verificacion import verify_outputs


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


def main() -> None:
    configure_logging()
    logging.info("Inicio del Pipeline de Tesis RC5.3")

    scenarios = read_csv(DATASET_ESCENARIOS)
    climate = read_csv(DATASET_CLIMA)
    validate_inputs(scenarios, climate)
    climate = preparar_precipitacion(climate)

    kruskal = read_csv(KRUSKAL_EXISTENTE)
    dunn_full = read_csv(DUNN_EXISTENTE)

    normalidad = calcular_normalidad(scenarios)
    dunn = resumen_dunn(dunn_full)
    descriptivos, throughput = calcular_descriptivos(scenarios)
    franjas_full, franjas_summary = analizar_franjas(scenarios)

    precip_diag = diagnostico_precipitacion(climate)
    precip_sens = sensibilidad_lluvia(climate)
    climate_classified = clasificar_lluvia(climate)
    precip_count = conteo_lluvia(climate_classified)
    precip_signal, precip_capacity = desempeno_lluvia(climate_classified)
    spearman = spearman_horario(climate_classified)

    stability_signal, stability_capacity, stability_index = calcular_estabilidad(
        descriptivos,
        throughput,
    )

    objetivos = construir_resumen_objetivos(
        kruskal,
        franjas_summary,
        spearman,
        stability_index,
    )

    tables = {
        "normalidad": normalidad,
        "kruskal": kruskal,
        "dunn": dunn,
        "descriptivos": descriptivos,
        "throughput": throughput,
        "franjas": franjas_summary,
        "precipitacion_diag": precip_diag,
        "precipitacion_sens": precip_sens,
        "precipitacion_conteo": precip_count,
        "precipitacion_senal": precip_signal,
        "precipitacion_capacidad": precip_capacity,
        "spearman": spearman,
        "estabilidad_senal": stability_signal,
        "estabilidad_capacidad": stability_capacity,
        "indice_estabilidad": stability_index,
        "objetivos": objetivos,
        "anexo_dunn": dunn_full,
        "anexo_franjas": franjas_full,
    }

    validate_no_rssi_cv(tables)

    intro_desc, interp_desc, intro_th, interp_th = texto_descriptivos(
        descriptivos,
        throughput,
    )
    texts = {
        "normalidad": texto_normalidad(normalidad),
        "kruskal": texto_kruskal(kruskal),
        "dunn": texto_dunn(dunn),
        "descriptivos": (intro_desc, interp_desc),
        "throughput": (intro_th, interp_th),
        "franjas": texto_franjas(franjas_summary),
        "precipitacion": texto_precipitacion(spearman),
        "estabilidad": texto_estabilidad(
            stability_signal,
            stability_capacity,
            stability_index,
        ),
    }

    narrative_blocks = [
        {"tipo": "tabla", "introduccion": intro, "interpretacion": interpretation}
        for intro, interpretation in texts.values()
    ]
    validate_text_blocks(narrative_blocks)

    TABLES.mkdir(parents=True, exist_ok=True)
    for name, table in tables.items():
        write_csv(table, TABLES / f"rc1_{name}.csv")

    figures = generar_figuras(
        FIGURES,
        scenarios,
        tables,
    )

    create_excel(XLSX_OUT, tables)
    create_word(DOCX_OUT, tables, texts, figures)
    verify_outputs(DOCX_OUT, XLSX_OUT, figures)

    logging.info("Proceso completado correctamente.")
    print("\nProductos generados:")
    print(f" - {DOCX_OUT}")
    print(f" - {XLSX_OUT}")
    print(f" - {LOG_OUT}")


if __name__ == "__main__":
    main()
