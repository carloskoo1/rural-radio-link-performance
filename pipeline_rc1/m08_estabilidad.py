
import numpy as np
import pandas as pd


def calcular_estabilidad(
    signal_desc: pd.DataFrame,
    throughput_desc: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    signal = signal_desc.copy()

    signal["SNR CV (%)"] = (
        signal["SNR DE"] / signal["SNR media (dB)"].abs() * 100
    )

    capacity = signal_desc[
        ["Escenario", "MCS media", "MCS DE"]
    ].copy()
    capacity["MCS CV (%)"] = (
        capacity["MCS DE"] / capacity["MCS media"].abs() * 100
    )
    capacity = capacity.merge(
        throughput_desc[
            ["Escenario", "Throughput media (Mb/s)", "Throughput DE"]
        ],
        on="Escenario",
        how="left",
    )
    capacity["Throughput CV (%)"] = (
        capacity["Throughput DE"]
        / capacity["Throughput media (Mb/s)"].abs()
        * 100
    )

    stability_signal = signal[
        [
            "Escenario", "RSSI media (dBm)", "RSSI DE (dB)", "RSSI RIC (dB)",
            "SNR media (dB)", "SNR DE", "SNR CV (%)",
        ]
    ].round(3)

    stability_capacity = capacity[
        [
            "Escenario", "MCS media", "MCS DE", "MCS CV (%)",
            "Throughput media (Mb/s)", "Throughput DE", "Throughput CV (%)",
        ]
    ].round(3)

    index = stability_signal[
        ["Escenario", "RSSI DE (dB)", "SNR CV (%)"]
    ].merge(
        stability_capacity[
            ["Escenario", "MCS CV (%)", "Throughput CV (%)"]
        ],
        on="Escenario",
        how="left",
    )

    components = ["RSSI DE (dB)", "SNR CV (%)", "MCS CV (%)", "Throughput CV (%)"]
    norm_cols = []
    for component in components:
        minimum = index[component].min(skipna=True)
        maximum = index[component].max(skipna=True)
        norm = f"{component} normalizado"
        norm_cols.append(norm)
        if maximum == minimum:
            index[norm] = 0.0
        else:
            index[norm] = (index[component] - minimum) / (maximum - minimum)

    index["Índice de variabilidad"] = index[norm_cols].mean(axis=1, skipna=True)
    index["Índice de estabilidad"] = 1.0 - index["Índice de variabilidad"]
    stability_index = index[
        ["Escenario", "Índice de variabilidad", "Índice de estabilidad"]
    ].sort_values("Índice de estabilidad", ascending=False).round(4)

    return stability_signal, stability_capacity, stability_index


def texto_estabilidad(
    signal: pd.DataFrame,
    capacity: pd.DataFrame,
    index: pd.DataFrame,
) -> tuple[str, str]:
    intro = (
        "La estabilidad se evaluó mediante DE y RIC para RSSI, y mediante CV para "
        "SNR, MCS y throughput. El CV del RSSI fue excluido por tratarse de una "
        "variable expresada en dBm."
    )
    best = index.iloc[0]
    interpretation = (
        f"{best['Escenario']} presentó el mayor índice compuesto de estabilidad "
        f"({best['Índice de estabilidad']:.3f}). El índice se obtuvo como el "
        "complemento del promedio de los indicadores de variabilidad normalizados "
        "mediante Min-Max; por ello, valores más altos indican mayor estabilidad "
        "relativa dentro del conjunto evaluado."
    )
    return intro, interpretation
