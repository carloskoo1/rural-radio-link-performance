
from __future__ import annotations

import pandas as pd


def _p_phrase(value: object) -> str:
    text = str(value).strip()
    if text.startswith("<"):
        return f"p {text}"
    return f"p = {text}"


def shapiro_text(table: pd.DataFrame) -> str:
    total = len(table)
    rejected = int((table["Decisión"] == "No normal").sum())
    return (
        f"Los {rejected} de {total} contrastes presentaron valores de significancia "
        "inferiores a 0.05, por lo que se rechazó la hipótesis de normalidad en todas "
        "las combinaciones de métrica y escenario. En consecuencia, la comparación "
        "entre configuraciones se realizó mediante procedimientos no paramétricos."
    )


def kruskal_text(table: pd.DataFrame) -> str:
    parts = []
    for _, row in table.iterrows():
        parts.append(
            f"{row['Métrica']} (H = {float(row['Estadístico H']):.2f}; "
            f"{_p_phrase(row['Valor p'])}; ε² = {float(row['Épsilon cuadrado']):.3f})"
        )
    return (
        "Los resultados evidenciaron diferencias estadísticamente significativas entre "
        "los escenarios experimentales para "
        + ", ".join(parts)
        + ". Los valores de ε² se situaron entre 0.144 y 0.225 y fueron clasificados "
          "como grandes, lo que indica que la configuración técnica ejerció una "
          "influencia relevante sobre todas las métricas analizadas."
    )


def dunn_text(table: pd.DataFrame) -> str:
    segments = []
    for _, row in table.iterrows():
        segments.append(
            f"en {row['Métrica']}, las comparaciones no significativas fueron "
            f"{row['No significativas']}"
        )
    return (
        "Las comparaciones post hoc mostraron que la mayoría de pares de escenarios "
        "presentaron diferencias estadísticamente significativas. De manera puntual, "
        + "; ".join(segments)
        + ". Estos resultados evidencian que determinadas configuraciones produjeron "
          "comportamientos equivalentes, mientras que la mayoría generó respuestas "
          "técnicas diferenciadas."
    )


def descriptive_text(table: pd.DataFrame) -> str:
    rssi_best = table.loc[table["RSSI media (dBm)"].idxmax()]
    rssi_worst = table.loc[table["RSSI media (dBm)"].idxmin()]
    snr_best = table.loc[table["SNR media (dB)"].idxmax()]
    snr_worst = table.loc[table["SNR media (dB)"].idxmin()]
    mcs_best = table.loc[table["MCS media"].idxmax()]

    return (
        f"El escenario {rssi_best['Escenario']} presentó el mayor RSSI promedio "
        f"({rssi_best['RSSI media (dBm)']:.2f} dBm), mientras que "
        f"{rssi_worst['Escenario']} registró el menor "
        f"({rssi_worst['RSSI media (dBm)']:.2f} dBm). Asimismo, "
        f"{snr_best['Escenario']} alcanzó el mayor SNR "
        f"({snr_best['SNR media (dB)']:.2f} dB), en contraste con "
        f"{snr_worst['Escenario']} ({snr_worst['SNR media (dB)']:.2f} dB). "
        f"El valor medio más alto de MCS correspondió a "
        f"{mcs_best['Escenario']} ({mcs_best['MCS media']:.2f}). "
        "En términos descriptivos, estos resultados muestran que la configuración "
        "más favorable dependió del indicador técnico considerado."
    )


def throughput_text(table: pd.DataFrame) -> str:
    valid = table.dropna(
        subset=["Throughput media (Mbps)", "Throughput mediana (Mbps)"]
    )
    mean_best = valid.loc[valid["Throughput media (Mbps)"].idxmax()]
    median_best = valid.loc[valid["Throughput mediana (Mbps)"].idxmax()]
    return (
        f"El mayor throughput medio observado correspondió a "
        f"{mean_best['Escenario']} ({mean_best['Throughput media (Mbps)']:.3f} Mb/s), "
        f"mientras que la mayor mediana se registró en "
        f"{median_best['Escenario']} ({median_best['Throughput mediana (Mbps)']:.2f} Mb/s). "
        "La diferencia entre media y mediana evidencia la influencia de la dispersión "
        "y de valores extremos. Debe precisarse que esta métrica representa tráfico "
        "efectivamente cursado durante el monitoreo y no la capacidad máxima teórica "
        "del radioenlace."
    )


def rain_count_text(table: pd.DataFrame) -> str:
    wet = table.loc[table["Condición"] == "Con lluvia"].iloc[0]
    dry = table.loc[table["Condición"] == "Sin lluvia"].iloc[0]
    return (
        f"Con el umbral operativo adoptado, el {wet['Porcentaje (%)']:.2f} % de los "
        f"registros se clasificó como condición con lluvia y el "
        f"{dry['Porcentaje (%)']:.2f} % como condición sin lluvia. Aunque ambas "
        "categorías estuvieron representadas, predominó la condición con precipitación, "
        "aspecto considerado en la interpretación de los resultados."
    )


def rain_signal_text(table: pd.DataFrame) -> str:
    wet = table.loc[table["Condición"] == "Con lluvia"].iloc[0]
    dry = table.loc[table["Condición"] == "Sin lluvia"].iloc[0]
    return (
        f"Bajo condiciones de lluvia, el RSSI medio fue "
        f"{wet['RSSI media']:.3f} dBm y el SNR medio "
        f"{wet['SNR media']:.3f} dB; en ausencia de lluvia, los valores fueron "
        f"{dry['RSSI media']:.3f} dBm y {dry['SNR media']:.3f} dB, respectivamente. "
        "Las diferencias descriptivas fueron reducidas, aunque se observó una ligera "
        "disminución de ambos indicadores en presencia de precipitación."
    )


def rain_capacity_text(table: pd.DataFrame) -> str:
    wet = table.loc[table["Condición"] == "Con lluvia"].iloc[0]
    dry = table.loc[table["Condición"] == "Sin lluvia"].iloc[0]
    return (
        f"El MCS medio fue {wet['MCS media']:.3f} bajo lluvia y "
        f"{dry['MCS media']:.3f} sin lluvia. Por su parte, el throughput medio alcanzó "
        f"{wet['Throughput media']:.3f} Mb/s y {dry['Throughput media']:.3f} Mb/s, "
        "respectivamente. La proximidad de estos valores indica que la condición "
        "atmosférica no produjo una separación descriptiva amplia en la modulación "
        "ni en el tráfico observado."
    )


def spearman_text(table: pd.DataFrame) -> str:
    parts = []
    for _, row in table.iterrows():
        rho = float(row["ρ de Spearman"])
        direction = "positiva" if rho > 0 else "negativa" if rho < 0 else "nula"
        magnitude = (
            "muy débil" if abs(rho) < 0.10
            else "débil" if abs(rho) < 0.30
            else "moderada"
        )
        parts.append(
            f"{row['Métrica']} presentó una asociación {direction} {magnitude} "
            f"(ρ = {rho:.3f}; {_p_phrase(row['Valor p'])})"
        )
    return (
        "; ".join(parts)
        + ". En conjunto, la magnitud de las asociaciones fue reducida, por lo que "
          "la precipitación explicó únicamente una fracción menor de la variabilidad "
          "observada en el desempeño técnico."
    )


def stability_text(signal: pd.DataFrame, capacity: pd.DataFrame) -> str:
    rssi = signal.loc[signal["RSSI CV (%)"].idxmin()]
    snr = signal.loc[signal["SNR CV (%)"].idxmin()]
    mcs = capacity.loc[capacity["MCS CV (%)"].idxmin()]
    th = capacity.dropna(subset=["Throughput CV (%)"])
    throughput = th.loc[th["Throughput CV (%)"].idxmin()]

    return (
        f"La menor variabilidad relativa del RSSI correspondió a "
        f"{rssi['Escenario']} (CV = {rssi['RSSI CV (%)']:.3f} %); la del SNR, a "
        f"{snr['Escenario']} (CV = {snr['SNR CV (%)']:.3f} %); la del MCS, a "
        f"{mcs['Escenario']} (CV = {mcs['MCS CV (%)']:.3f} %); y la del throughput, "
        f"a {throughput['Escenario']} (CV = {throughput['Throughput CV (%)']:.3f} %). "
        "Por tanto, ningún escenario fue simultáneamente el más estable para todas "
        "las métricas, lo que justifica complementar los indicadores individuales "
        "con un índice integrado de variabilidad operativa."
    )


def final_synthesis(
    kruskal: pd.DataFrame,
    spearman: pd.DataFrame,
    signal: pd.DataFrame,
    capacity: pd.DataFrame,
) -> str:
    stability = stability_text(signal, capacity)
    return (
        "En conjunto, los resultados obtenidos evidencian que la configuración técnica "
        "del radioenlace constituyó el principal factor asociado al desempeño operativo "
        "del sistema. Las pruebas de Kruskal-Wallis confirmaron diferencias "
        "estadísticamente significativas en RSSI, SNR, MCS y throughput, todas con "
        "tamaños del efecto grandes. Las comparaciones post hoc permitieron precisar "
        "qué configuraciones diferían entre sí, mientras que el análisis descriptivo "
        "mostró que los escenarios E2, E3 y E4 concentraron los mejores resultados "
        "según el indicador examinado. Por otra parte, la precipitación presentó "
        "asociaciones de magnitud débil con las métricas técnicas, por lo que su "
        "influencia fue secundaria respecto de la configuración espectral. "
        f"{stability} "
        "En consecuencia, los hallazgos respaldan la hipótesis general de investigación "
        "y demuestran que la selección conjunta de la frecuencia de operación y el "
        "ancho de canal influyó significativamente sobre el desempeño técnico del "
        "radioenlace bajo condiciones reales de operación."
    )
