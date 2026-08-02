
import logging

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from .m00_config import (
    UMBRAL_LLUVIA_MM_H,
    UMBRALES_SENSIBILIDAD,
    PRECIP_INPUT_COLUMN,
    PRECIP_INPUT_UNIT,
    PRECIP_CONVERSION_FACTOR,
    PRECIP_STRICT_NONNEGATIVE,
    PRECIP_HIGH_WET_FRACTION_WARNING,
)



def preparar_precipitacion(df: pd.DataFrame) -> pd.DataFrame:
    """Valida y normaliza la precipitación según la configuración declarada.

    No realiza conversiones implícitas. La transformación aplicada queda
    registrada mediante PRECIP_CONVERSION_FACTOR.
    """
    if PRECIP_INPUT_COLUMN not in df.columns:
        raise ValueError(
            f"No se encontró la columna de precipitación configurada: "
            f"{PRECIP_INPUT_COLUMN}"
        )

    out = df.copy()
    raw = pd.to_numeric(out[PRECIP_INPUT_COLUMN], errors="coerce")
    converted = raw * float(PRECIP_CONVERSION_FACTOR)

    if PRECIP_STRICT_NONNEGATIVE and (converted.dropna() < 0).any():
        count = int((converted.dropna() < 0).sum())
        raise ValueError(
            f"Se detectaron {count} valores negativos de precipitación. "
            "Revise la conversión y la fuente climática."
        )

    out["precip_mm"] = converted

    valid = converted.dropna()
    if valid.empty:
        raise ValueError("La precipitación no contiene valores numéricos válidos.")

    wet_fraction = float((valid >= UMBRAL_LLUVIA_MM_H).mean())
    if wet_fraction >= PRECIP_HIGH_WET_FRACTION_WARNING:
        logging.warning(
            "La fracción de registros con precipitación >= %.2f mm/h es %.2f%%. "
            "El valor no se modifica automáticamente; verifique que precip_mm esté "
            "expresada en mm/h y que el periodo analizado corresponda al esperado.",
            UMBRAL_LLUVIA_MM_H,
            100.0 * wet_fraction,
        )

    return out

def diagnostico_precipitacion(df: pd.DataFrame) -> pd.DataFrame:
    precip = pd.to_numeric(df["precip_mm"], errors="coerce").dropna()
    per_hour = df.groupby("hora_merge")["precip_mm"].nunique(dropna=True)
    wet_fraction = 100 * (precip >= UMBRAL_LLUVIA_MM_H).mean()

    values = {
        "Columna de entrada": PRECIP_INPUT_COLUMN,
        "Unidad declarada": PRECIP_INPUT_UNIT,
        "Factor de conversión aplicado": PRECIP_CONVERSION_FACTOR,
        "Umbral de clasificación (mm/h)": UMBRAL_LLUVIA_MM_H,
        "Registros válidos": int(len(precip)),
        "Mínimo (mm/h)": precip.min(),
        "Mediana (mm/h)": precip.median(),
        "Percentil 95 (mm/h)": precip.quantile(0.95),
        "Percentil 99 (mm/h)": precip.quantile(0.99),
        "Máximo (mm/h)": precip.max(),
        "Registros >= umbral (%)": wet_fraction,
        "Horas con más de un valor": int((per_hour > 1).sum()),
        "Máximo de valores distintos por hora": int(per_hour.max()),
    }
    return pd.DataFrame(
        {"Indicador": list(values.keys()), "Resultado": list(values.values())}
    ).round(4)

def sensibilidad_lluvia(df: pd.DataFrame) -> pd.DataFrame:
    precip = pd.to_numeric(df["precip_mm"], errors="coerce")
    valid = int(precip.notna().sum())
    rows = []
    for threshold in UMBRALES_SENSIBILIDAD:
        mask = precip > 0 if threshold == 0 else precip >= threshold
        wet = int(mask.sum())
        dry = valid - wet
        rows.append({
            "Umbral (mm/h)": threshold,
            "Con lluvia (N)": wet,
            "Con lluvia (%)": round(100 * wet / valid, 2),
            "Sin lluvia (N)": dry,
            "Sin lluvia (%)": round(100 * dry / valid, 2),
        })
    return pd.DataFrame(rows)


def clasificar_lluvia(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["precip_mm"] = pd.to_numeric(out["precip_mm"], errors="coerce")
    out["condicion_lluvia"] = np.where(
        out["precip_mm"].isna(),
        "Sin dato",
        np.where(
            out["precip_mm"] >= UMBRAL_LLUVIA_MM_H,
            "Precipitación >= 0.10 mm/h",
            "Precipitación < 0.10 mm/h",
        ),
    )
    return out

def conteo_lluvia(df: pd.DataFrame) -> pd.DataFrame:
    valid = df[df["condicion_lluvia"] != "Sin dato"]
    result = (
        valid["condicion_lluvia"]
        .value_counts()
        .rename_axis("Condición")
        .reset_index(name="N")
    )
    result["Porcentaje (%)"] = (100 * result["N"] / len(valid)).round(2)
    return result


def desempeno_lluvia(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for condition in ["Precipitación >= 0.10 mm/h", "Precipitación < 0.10 mm/h"]:
        group = df[df["condicion_lluvia"] == condition]
        row = {"Condición": condition}
        for col, label in {
            "rssi_dl": "RSSI",
            "snr_dl": "SNR",
            "mcs_dl": "MCS",
            "throughput_dl": "Throughput",
        }.items():
            values = pd.to_numeric(group[col], errors="coerce").dropna()
            row[f"{label} media"] = values.mean()
            row[f"{label} DE"] = values.std(ddof=1)
            row[f"{label} mediana"] = values.median()
        rows.append(row)

    table = pd.DataFrame(rows).round(3)
    signal = table[
        ["Condición", "RSSI media", "RSSI DE", "RSSI mediana",
         "SNR media", "SNR DE", "SNR mediana"]
    ]
    capacity = table[
        ["Condición", "MCS media", "MCS DE", "MCS mediana",
         "Throughput media", "Throughput DE", "Throughput mediana"]
    ]
    return signal, capacity


def spearman_horario(df: pd.DataFrame) -> pd.DataFrame:
    hourly = df.groupby("hora_merge", as_index=False)[
        ["precip_mm", "rssi_dl", "snr_dl", "mcs_dl", "throughput_dl"]
    ].mean(numeric_only=True)

    rows = []
    for col, label in {
        "rssi_dl": "RSSI DL",
        "snr_dl": "SNR DL",
        "mcs_dl": "MCS DL",
        "throughput_dl": "Throughput DL",
    }.items():
        pair = hourly[["precip_mm", col]].dropna()
        rho, p = spearmanr(pair["precip_mm"], pair[col])
        rows.append({
            "Métrica": label,
            "ρ de Spearman": round(float(rho), 3),
            "Valor p": "< 0.001" if p < 0.001 else f"{p:.4f}",
            "N horas": len(pair),
        })
    return pd.DataFrame(rows)


def texto_precipitacion(spearman: pd.DataFrame) -> tuple[str, str]:
    intro = (
        "La precipitación fue tratada como covariable y evaluada mediante "
        "estadísticos descriptivos y correlación de Spearman a escala horaria."
    )
    strongest = spearman.loc[spearman["ρ de Spearman"].abs().idxmax()]
    interpretation = (
        f"La asociación de mayor magnitud correspondió a {strongest['Métrica']} "
        f"(ρ = {float(strongest['ρ de Spearman']):.3f}); no obstante, su magnitud "
        "permaneció débil. Por tanto, la relación monotónica observada fue limitada "
        "dentro de los periodos y condiciones evaluados."
    )
    return intro, interpretation
