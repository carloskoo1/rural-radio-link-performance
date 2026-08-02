
from __future__ import annotations

import warnings
import numpy as np
import pandas as pd
from scipy.stats import shapiro, spearmanr

from .config import ALPHA, UMBRAL_LLUVIA_MM_H, UMBRALES_SENSIBILIDAD


def p_text(p: float) -> str:
    if pd.isna(p):
        return ""
    return "< 0.001" if p < 0.001 else f"{p:.4f}"


def shapiro_table(df: pd.DataFrame) -> pd.DataFrame:
    config = {
        "rssi_dl": ("RSSI DL", ["E0", "E1", "E2", "E3", "E4", "E5"]),
        "snr_dl": ("SNR DL", ["E0", "E1", "E2", "E3", "E4", "E5"]),
        "mcs_dl": ("MCS DL", ["E0", "E1", "E2", "E3", "E4", "E5"]),
        "throughput_dl": ("Throughput DL", ["E1", "E2", "E3", "E4", "E5"]),
    }
    rows = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for col, (label, scenarios) in config.items():
            for scenario in scenarios:
                values = pd.to_numeric(
                    df.loc[df["escenario"] == scenario, col],
                    errors="coerce",
                ).dropna()
                if len(values) < 3:
                    continue
                w, p = shapiro(values.to_numpy())
                rows.append({
                    "Métrica": label,
                    "Escenario": scenario,
                    "N": len(values),
                    "W": round(float(w), 3),
                    "Valor p": p_text(float(p)),
                    "Decisión": "No normal" if p < ALPHA else "Normal",
                })
    return pd.DataFrame(rows)


def descriptives(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    base = (
        df.groupby(["escenario", "frecuencia_mhz", "ancho_canal_mhz"], as_index=False)
        .agg(
            N=("escenario", "size"),
            Días=("fecha", "nunique"),
            RSSI_media=("rssi_dl", "mean"),
            RSSI_DE=("rssi_dl", "std"),
            SNR_media=("snr_dl", "mean"),
            SNR_DE=("snr_dl", "std"),
            MCS_media=("mcs_dl", "mean"),
            MCS_DE=("mcs_dl", "std"),
            Throughput_media=("throughput_dl", "mean"),
            Throughput_DE=("throughput_dl", "std"),
            Throughput_mediana=("throughput_dl", "median"),
        )
    )
    signal = base[
        ["escenario", "frecuencia_mhz", "ancho_canal_mhz", "N", "Días",
         "RSSI_media", "RSSI_DE", "SNR_media", "SNR_DE", "MCS_media", "MCS_DE"]
    ].rename(columns={
        "escenario": "Escenario",
        "frecuencia_mhz": "Frecuencia (MHz)",
        "ancho_canal_mhz": "Canal (MHz)",
        "RSSI_media": "RSSI media (dBm)",
        "RSSI_DE": "RSSI DE",
        "SNR_media": "SNR media (dB)",
        "SNR_DE": "SNR DE",
        "MCS_media": "MCS media",
        "MCS_DE": "MCS DE",
    })
    throughput = base[
        ["escenario", "frecuencia_mhz", "ancho_canal_mhz",
         "Throughput_media", "Throughput_DE", "Throughput_mediana"]
    ].rename(columns={
        "escenario": "Escenario",
        "frecuencia_mhz": "Frecuencia (MHz)",
        "ancho_canal_mhz": "Canal (MHz)",
        "Throughput_media": "Throughput media (Mbps)",
        "Throughput_DE": "Throughput DE",
        "Throughput_mediana": "Throughput mediana (Mbps)",
    })
    return signal.round(3), throughput.round(3)


def rain_sensitivity(df: pd.DataFrame) -> pd.DataFrame:
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
            "Con lluvia (%)": round(100 * wet / valid, 2) if valid else np.nan,
            "Sin lluvia (N)": dry,
            "Sin lluvia (%)": round(100 * dry / valid, 2) if valid else np.nan,
        })
    return pd.DataFrame(rows)


def classify_rain(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["precip_mm"] = pd.to_numeric(out["precip_mm"], errors="coerce")
    out["condicion_lluvia_validada"] = np.where(
        out["precip_mm"].isna(),
        "Sin dato",
        np.where(out["precip_mm"] >= UMBRAL_LLUVIA_MM_H, "Con lluvia", "Sin lluvia"),
    )
    return out


def rain_count(df: pd.DataFrame) -> pd.DataFrame:
    valid = df[df["condicion_lluvia_validada"] != "Sin dato"]
    result = (
        valid["condicion_lluvia_validada"]
        .value_counts()
        .rename_axis("Condición")
        .reset_index(name="N")
    )
    result["Porcentaje (%)"] = (100 * result["N"] / len(valid)).round(2)
    order = pd.Categorical(
        result["Condición"],
        categories=["Con lluvia", "Sin lluvia"],
        ordered=True,
    )
    return result.assign(_order=order).sort_values("_order").drop(columns="_order")


def rain_performance(df: pd.DataFrame) -> pd.DataFrame:
    metrics = {
        "rssi_dl": "RSSI",
        "snr_dl": "SNR",
        "mcs_dl": "MCS",
        "throughput_dl": "Throughput",
    }
    rows = []
    for condition in ["Con lluvia", "Sin lluvia"]:
        group = df[df["condicion_lluvia_validada"] == condition]
        row = {"Condición": condition}
        for col, label in metrics.items():
            vals = pd.to_numeric(group[col], errors="coerce").dropna()
            row[f"{label} media"] = vals.mean()
            row[f"{label} DE"] = vals.std(ddof=1)
            row[f"{label} mediana"] = vals.median()
        rows.append(row)
    return pd.DataFrame(rows).round(3)


def hourly_spearman(df: pd.DataFrame) -> pd.DataFrame:
    if "hora_merge" not in df.columns:
        raise ValueError("dataset_radio_clima.csv no contiene 'hora_merge'.")
    cols = ["precip_mm", "rssi_dl", "snr_dl", "mcs_dl", "throughput_dl"]
    hourly = df.groupby("hora_merge", as_index=False)[cols].mean(numeric_only=True)
    labels = {
        "rssi_dl": "RSSI DL",
        "snr_dl": "SNR DL",
        "mcs_dl": "MCS DL",
        "throughput_dl": "Throughput DL",
    }
    rows = []
    for col, label in labels.items():
        pair = hourly[["precip_mm", col]].dropna()
        rho, p = spearmanr(pair["precip_mm"], pair[col]) if len(pair) >= 3 else (np.nan, np.nan)
        rows.append({
            "Métrica": label,
            "ρ de Spearman": round(float(rho), 3) if pd.notna(rho) else np.nan,
            "Valor p": p_text(float(p)) if pd.notna(p) else "",
            "N horas": len(pair),
        })
    return pd.DataFrame(rows)


def dunn_summary(full: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for metric, group in full.groupby("Métrica", sort=False):
        significant = group["Diferencia significativa"].astype(str).str.strip().eq("Sí")
        not_sig = group.loc[~significant]
        pairs = "Ninguna" if not_sig.empty else "; ".join(
            f"{r['Comparación']} (p={r['Valor p ajustado']})" for _, r in not_sig.iterrows()
        )
        rows.append({
            "Métrica": metric,
            "Significativas": f"{int(significant.sum())} de {len(group)}",
            "No significativas": pairs,
        })
    return pd.DataFrame(rows)
