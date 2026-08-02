
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests

from .m00_config import ALPHA
from .m02_validacion import resolve_datetime


def _cliffs_delta(u_value: float, n_a: int, n_b: int) -> float:
    return (2.0 * u_value / (n_a * n_b)) - 1.0


def _magnitude(delta: float) -> str:
    value = abs(delta)
    if value < 0.147:
        return "Despreciable"
    if value < 0.330:
        return "Pequeño"
    if value < 0.474:
        return "Mediano"
    return "Grande"



def _format_p_value(value: float) -> str:
    """Formatea valores p sin representarlos como cero."""
    if pd.isna(value):
        return ""
    if value < 0.001:
        return "< 0.001"
    return f"{value:.4f}"

def analizar_franjas(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = df.copy()
    data["_dt"] = resolve_datetime(data)
    data["_hour"] = data["_dt"].dt.hour

    band_evening = data["_hour"].isin([20, 21])
    band_night = data["_hour"].isin([1, 2])

    metrics = {
        "rssi_dl": "RSSI DL",
        "snr_dl": "SNR DL",
        "mcs_dl": "MCS DL",
        "throughput_dl": "Throughput DL",
    }

    rows = []
    for metric_col, metric_name in metrics.items():
        metric_rows = []
        for scenario in sorted(data["escenario"].dropna().astype(str).unique()):
            subset = data[data["escenario"].astype(str) == scenario]
            a = pd.to_numeric(
                subset.loc[band_evening.loc[subset.index], metric_col],
                errors="coerce",
            ).dropna()
            b = pd.to_numeric(
                subset.loc[band_night.loc[subset.index], metric_col],
                errors="coerce",
            ).dropna()

            if len(a) < 20 or len(b) < 20:
                continue

            u_value, p_value = mannwhitneyu(
                a,
                b,
                alternative="two-sided",
                method="asymptotic",
            )
            delta = _cliffs_delta(float(u_value), len(a), len(b))
            metric_rows.append({
                "Métrica": metric_name,
                "Escenario": scenario,
                "N 20:00–22:00": len(a),
                "N 01:00–03:00": len(b),
                "Mediana 20:00–22:00": a.median(),
                "Mediana 01:00–03:00": b.median(),
                "U": float(u_value),
                "Valor p": float(p_value),
                "Delta de Cliff": delta,
                "Magnitud": _magnitude(delta),
            })

        if metric_rows:
            adjusted = multipletests(
                [row["Valor p"] for row in metric_rows],
                alpha=ALPHA,
                method="holm",
            )[1]
            for row, p_adj in zip(metric_rows, adjusted):
                row["Valor p ajustado"] = float(p_adj)
                row["Diferencia significativa"] = "Sí" if p_adj < ALPHA else "No"
                rows.append(row)

    full = pd.DataFrame(rows)
    if full.empty:
        raise ValueError(
            "No existen observaciones suficientes para comparar las franjas horarias."
        )

    summary_rows = []
    for metric, group in full.groupby("Métrica", sort=False):
        sig = group["Diferencia significativa"].eq("Sí")
        scenarios = group.loc[sig, "Escenario"].astype(str).tolist()
        summary_rows.append({
            "Métrica": metric,
            "Escenarios válidos": len(group),
            "Escenarios significativos": int(sig.sum()),
            "Escenarios con diferencia": ", ".join(scenarios) if scenarios else "Ninguno",
        })

    full["Valor p numérico"] = full["Valor p"].astype(float)
    full["Valor p ajustado numérico"] = full["Valor p ajustado"].astype(float)
    full["Valor p"] = full["Valor p numérico"].map(_format_p_value)
    full["Valor p ajustado"] = full["Valor p ajustado numérico"].map(_format_p_value)

    display_columns = [
        "Métrica",
        "Escenario",
        "N 20:00–22:00",
        "N 01:00–03:00",
        "Mediana 20:00–22:00",
        "Mediana 01:00–03:00",
        "U",
        "Valor p",
        "Delta de Cliff",
        "Magnitud",
        "Valor p ajustado",
        "Diferencia significativa",
    ]
    full_display = full[display_columns].copy()
    numeric_columns = [
        "Mediana 20:00–22:00",
        "Mediana 01:00–03:00",
        "U",
        "Delta de Cliff",
    ]
    full_display[numeric_columns] = full_display[numeric_columns].round(4)

    return full_display, pd.DataFrame(summary_rows)


def texto_franjas(summary: pd.DataFrame) -> tuple[str, str]:
    intro = (
        "Para responder al objetivo temporal, se compararon las franjas "
        "20:00–22:00 y 01:00–03:00 dentro de cada escenario mediante U de "
        "Mann–Whitney, ajuste de Holm y delta de Cliff."
    )
    parts = [
        f"{r['Métrica']}: {int(r['Escenarios significativos'])} de "
        f"{int(r['Escenarios válidos'])} escenarios"
        for _, r in summary.iterrows()
    ]
    interpretation = (
        "La evidencia por franjas indicó diferencias en " + "; ".join(parts) + ". "
        "El análisis se efectuó dentro de cada escenario para evitar confundir el "
        "efecto temporal con la composición de las configuraciones."
    )
    return intro, interpretation
