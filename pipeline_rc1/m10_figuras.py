
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd


PRIMARY = "#1F4E79"
PRIMARY_DARK = "#163A5C"
SECONDARY = "#5B9BD5"
HIGHLIGHT = "#548235"
NEUTRAL = "#B4C7E7"
GRID = "#D9D9D9"
TEXT = "#202020"
NEGATIVE = "#A61C1C"


def _available_font() -> str:
    installed = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in ("Arial", "Calibri", "Aptos", "DejaVu Sans"):
        if candidate in installed:
            return candidate
    return "sans-serif"


def _configure_matplotlib() -> None:
    plt.rcParams.update({
        "font.family": _available_font(),
        "font.size": 10,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "text.color": TEXT,
        "axes.labelcolor": TEXT,
        "xtick.color": TEXT,
        "ytick.color": TEXT,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.linewidth": 0.8,
        "savefig.dpi": 600,
        "savefig.facecolor": "white",
        "savefig.bbox": "tight",
    })


def _polish(ax, grid_axis: str | None = "y") -> None:
    if grid_axis:
        ax.grid(
            axis=grid_axis,
            linestyle=(0, (3, 3)),
            linewidth=0.65,
            color=GRID,
            alpha=0.85,
        )
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#777777")
    ax.spines["bottom"].set_color("#777777")
    ax.tick_params(width=0.8, length=4)


def _bar_labels(ax, decimals: int = 3) -> None:
    """Añade etiquetas únicamente a contenedores de barras.

    Los gráficos con barras de error agregan también un ErrorbarContainer,
    el cual no dispone del atributo ``datavalues``. Por ello se filtran
    explícitamente los contenedores antes de etiquetar.
    """
    fmt = f"%.{decimals}f"

    for container in ax.containers:
        values = getattr(container, "datavalues", None)
        if values is None:
            continue

        labels = []
        for value in values:
            try:
                labels.append(fmt % float(value))
            except (TypeError, ValueError):
                labels.append("")

        ax.bar_label(
            container,
            labels=labels,
            padding=3,
            fontsize=8.8,
            fontweight="bold",
            color=TEXT,
        )


def _save(fig, base: Path) -> Path:
    base.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(base.with_suffix(".png"), dpi=600, bbox_inches="tight")
    fig.savefig(base.with_suffix(".tiff"), dpi=600, bbox_inches="tight")
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    return base.with_suffix(".png")


def _scenario_order(df: pd.DataFrame) -> list[str]:
    return sorted(df["Escenario"].dropna().astype(str).unique())


def generar_figuras(
    figures_dir: Path,
    scenarios: pd.DataFrame,
    tables: dict[str, pd.DataFrame],
) -> dict[str, Path]:
    _configure_matplotlib()
    out = figures_dir / "publicacion_rc5"
    out.mkdir(parents=True, exist_ok=True)
    figures: dict[str, Path] = {}

    # Fig. 7. Estadísticos W de Shapiro-Wilk.
    normal = tables["normalidad"].copy()
    pivot = normal.pivot(index="Métrica", columns="Escenario", values="W")
    fig, ax = plt.subplots(figsize=(7.2, 3.8), constrained_layout=True)
    image = ax.imshow(pivot.values, cmap="Blues", aspect="auto", vmin=0, vmax=1)
    ax.set_title("Estadísticos W de Shapiro-Wilk")
    ax.set_xticks(range(len(pivot.columns)), pivot.columns)
    ax.set_yticks(range(len(pivot.index)), pivot.index)
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            value = pivot.iloc[i, j]
            if pd.notna(value):
                ax.text(j, i, f"{value:.3f}", ha="center", va="center",
                        color="white" if value > 0.65 else TEXT, fontsize=8.5)
    cbar = fig.colorbar(image, ax=ax, shrink=0.85)
    cbar.set_label("Estadístico W")
    figures["normalidad"] = _save(fig, out / "fig_4_7_shapiro_w")
    plt.close(fig)

    # Fig. 8. Tamaños del efecto Kruskal-Wallis.
    kw = tables["kruskal"].copy()
    fig, ax = plt.subplots(figsize=(7.2, 4.0), constrained_layout=True)
    ax.barh(kw["Métrica"], kw["Épsilon cuadrado"], color=PRIMARY,
            edgecolor=PRIMARY_DARK, linewidth=0.8)
    ax.set_title("Tamaño del efecto entre escenarios")
    ax.set_xlabel("Épsilon cuadrado (ε²)")
    ax.invert_yaxis()
    _polish(ax, "x")
    for i, value in enumerate(kw["Épsilon cuadrado"]):
        ax.text(value + 0.004, i, f"{value:.3f}", va="center",
                fontsize=9, fontweight="bold")
    ax.set_xlim(0, max(kw["Épsilon cuadrado"]) * 1.22)
    figures["kruskal"] = _save(fig, out / "fig_4_8_kruskal_efecto")
    plt.close(fig)

    # Fig. 9. Proporción de comparaciones Dunn significativas.
    dunn = tables["dunn"].copy()
    fractions = []
    for value in dunn["Significativas"].astype(str):
        num, den = value.split(" de ")
        fractions.append(100 * float(num) / float(den))
    fig, ax = plt.subplots(figsize=(7.2, 4.0), constrained_layout=True)
    ax.bar(dunn["Métrica"], fractions, color=PRIMARY,
           edgecolor=PRIMARY_DARK, linewidth=0.8, width=0.7)
    ax.set_title("Comparaciones post hoc significativas")
    ax.set_ylabel("Comparaciones significativas (%)")
    ax.set_ylim(0, 110)
    _polish(ax)
    for i, value in enumerate(fractions):
        ax.text(i, value + 2, f"{value:.1f} %", ha="center",
                fontsize=9, fontweight="bold")
    figures["dunn"] = _save(fig, out / "fig_4_9_dunn_significativas")
    plt.close(fig)

    desc = tables["descriptivos"].copy()
    order = _scenario_order(desc)
    desc = desc.set_index("Escenario").loc[order].reset_index()

    # Fig. 10. RSSI promedio ± DE.
    fig, ax = plt.subplots(figsize=(7.2, 4.0), constrained_layout=True)
    ax.errorbar(desc["Escenario"], desc["RSSI media (dBm)"],
                yerr=desc["RSSI DE (dB)"], fmt="o", markersize=7,
                color=PRIMARY, ecolor=PRIMARY_DARK, capsize=4, linewidth=1.2)
    ax.set_title("RSSI promedio y dispersión por escenario")
    ax.set_xlabel("Escenario experimental")
    ax.set_ylabel("RSSI DL (dBm)")
    _polish(ax)
    figures["rssi_media"] = _save(fig, out / "fig_4_10_rssi_media_de")
    plt.close(fig)

    # Fig. 11. SNR promedio ± DE.
    fig, ax = plt.subplots(figsize=(7.2, 4.0), constrained_layout=True)
    ax.errorbar(desc["Escenario"], desc["SNR media (dB)"],
                yerr=desc["SNR DE"], fmt="o", markersize=7,
                color=PRIMARY, ecolor=PRIMARY_DARK, capsize=4, linewidth=1.2)
    ax.set_title("SNR promedio y dispersión por escenario")
    ax.set_xlabel("Escenario experimental")
    ax.set_ylabel("SNR DL (dB)")
    _polish(ax)
    figures["snr_media"] = _save(fig, out / "fig_4_11_snr_media_de")
    plt.close(fig)

    # Fig. 12. MCS promedio ± DE.
    fig, ax = plt.subplots(figsize=(7.2, 4.0), constrained_layout=True)
    ax.errorbar(desc["Escenario"], desc["MCS media"],
                yerr=desc["MCS DE"], fmt="o", markersize=7,
                color=PRIMARY, ecolor=PRIMARY_DARK, capsize=4, linewidth=1.2)
    ax.set_title("MCS promedio y dispersión por escenario")
    ax.set_xlabel("Escenario experimental")
    ax.set_ylabel("MCS DL")
    _polish(ax)
    figures["mcs_media"] = _save(fig, out / "fig_4_12_mcs_media_de")
    plt.close(fig)

    # Fig. 13. Throughput medio ± DE.
    th = tables["throughput"].dropna(subset=["Throughput media (Mb/s)"]).copy()
    fig, ax = plt.subplots(figsize=(7.2, 4.0), constrained_layout=True)
    ax.bar(th["Escenario"], th["Throughput media (Mb/s)"],
           yerr=th["Throughput DE"], capsize=4, color=PRIMARY,
           edgecolor=PRIMARY_DARK, linewidth=0.8, width=0.7)
    ax.set_title("Throughput descendente observado")
    ax.set_xlabel("Escenario experimental")
    ax.set_ylabel("Throughput medio (Mb/s)")
    _polish(ax)
    _bar_labels(ax, 3)
    ax.set_ylim(0, (th["Throughput media (Mb/s)"] + th["Throughput DE"]).max() * 1.16)
    figures["throughput"] = _save(fig, out / "fig_4_13_throughput_media_de")
    plt.close(fig)

    # Fig. 14. Escenarios con diferencias por franja.
    fr = tables["franjas"].copy()
    fig, ax = plt.subplots(figsize=(7.2, 4.0), constrained_layout=True)
    x = np.arange(len(fr))
    ax.bar(x, fr["Escenarios significativos"], color=PRIMARY,
           edgecolor=PRIMARY_DARK, width=0.65, label="Significativos")
    ax.bar(x, fr["Escenarios válidos"] - fr["Escenarios significativos"],
           bottom=fr["Escenarios significativos"], color=NEUTRAL,
           edgecolor=PRIMARY_DARK, width=0.65, label="No significativos")
    ax.set_xticks(x, fr["Métrica"])
    ax.set_title("Diferencias entre franjas horarias")
    ax.set_ylabel("Número de escenarios")
    ax.legend(frameon=False, ncol=2, loc="upper left")
    _polish(ax)
    figures["franjas"] = _save(fig, out / "fig_4_14_franjas_resumen")
    plt.close(fig)

    # Fig. 15. Delta de Cliff por escenario y métrica.
    full = tables["anexo_franjas"].copy()
    cliff = full.pivot(index="Métrica", columns="Escenario", values="Delta de Cliff")
    fig, ax = plt.subplots(figsize=(7.2, 3.8), constrained_layout=True)
    image = ax.imshow(cliff.values, cmap="RdBu_r", aspect="auto", vmin=-1, vmax=1)
    ax.set_title("Magnitud y dirección del efecto temporal")
    ax.set_xticks(range(len(cliff.columns)), cliff.columns)
    ax.set_yticks(range(len(cliff.index)), cliff.index)
    for i in range(len(cliff.index)):
        for j in range(len(cliff.columns)):
            value = cliff.iloc[i, j]
            if pd.notna(value):
                ax.text(j, i, f"{value:.3f}", ha="center", va="center",
                        color="white" if abs(value) > 0.45 else TEXT, fontsize=8.5)
    cbar = fig.colorbar(image, ax=ax, shrink=0.85)
    cbar.set_label("Delta de Cliff")
    figures["cliff"] = _save(fig, out / "fig_4_15_cliff_heatmap")
    plt.close(fig)

    # Fig. 16. Sensibilidad al umbral de precipitación.
    sens = tables["precipitacion_sens"].copy()
    fig, ax = plt.subplots(figsize=(7.2, 4.0), constrained_layout=True)
    ax.plot(sens["Umbral (mm/h)"], sens["Con lluvia (%)"],
            marker="o", linewidth=1.8, color=PRIMARY)
    ax.axvline(0.10, color=HIGHLIGHT, linestyle="--", linewidth=1.2,
               label="Umbral adoptado: 0.10 mm/h")
    ax.set_title("Sensibilidad de la clasificación de precipitación")
    ax.set_xlabel("Umbral (mm/h)")
    ax.set_ylabel("Registros clasificados con lluvia (%)")
    ax.set_ylim(0, 105)
    ax.legend(frameon=False)
    _polish(ax)
    figures["lluvia_sens"] = _save(fig, out / "fig_4_16_sensibilidad_lluvia")
    plt.close(fig)

    # Fig. 17. Distribución de registros por condición.
    count = tables["precipitacion_conteo"].copy()
    fig, ax = plt.subplots(figsize=(6.2, 3.8), constrained_layout=True)
    colors = [PRIMARY, NEUTRAL]
    count_labels = [">= 0.10 mm/h", "< 0.10 mm/h"]
    ax.bar(count_labels, count["Porcentaje (%)"], color=colors,
           edgecolor=PRIMARY_DARK, width=0.58)
    ax.set_title("Distribución de registros según precipitación")
    ax.set_ylabel("Porcentaje de registros (%)")
    ax.set_ylim(0, 100)
    _polish(ax)
    _bar_labels(ax, 2)
    figures["lluvia_conteo"] = _save(fig, out / "fig_4_17_conteo_lluvia")
    plt.close(fig)

    # Fig. 18. Throughput según condición de precipitación.
    cap = tables["precipitacion_capacidad"].copy()
    fig, ax = plt.subplots(figsize=(6.2, 3.8), constrained_layout=True)
    cap_labels = [">= 0.10 mm/h", "< 0.10 mm/h"]
    ax.bar(cap_labels, cap["Throughput media"],
           yerr=cap["Throughput DE"], capsize=4,
           color=[PRIMARY, NEUTRAL], edgecolor=PRIMARY_DARK, width=0.58)
    ax.set_title("Throughput según condición de precipitación")
    ax.set_ylabel("Throughput medio (Mb/s)")
    _polish(ax)
    _bar_labels(ax, 3)
    ax.set_ylim(0, (cap["Throughput media"] + cap["Throughput DE"]).max() * 1.15)
    figures["lluvia_throughput"] = _save(fig, out / "fig_4_18_throughput_lluvia")
    plt.close(fig)

    # Fig. 19. Correlaciones de Spearman.
    sp = tables["spearman"].copy()
    colors = [NEGATIVE if value < 0 else PRIMARY for value in sp["ρ de Spearman"]]
    fig, ax = plt.subplots(figsize=(7.2, 4.0), constrained_layout=True)
    ax.barh(sp["Métrica"], sp["ρ de Spearman"], color=colors,
            edgecolor=PRIMARY_DARK, linewidth=0.7)
    ax.axvline(0, color="#555555", linewidth=0.8)
    ax.set_title("Asociación entre precipitación y métricas")
    ax.set_xlabel("ρ de Spearman")
    ax.invert_yaxis()
    _polish(ax, "x")
    for i, value in enumerate(sp["ρ de Spearman"]):
        offset = 0.008 if value >= 0 else -0.008
        ax.text(value + offset, i, f"{value:.3f}",
                ha="left" if value >= 0 else "right", va="center",
                fontsize=9, fontweight="bold")
    limit = max(abs(sp["ρ de Spearman"]).max() * 1.35, 0.20)
    ax.set_xlim(-limit, limit)
    figures["spearman"] = _save(fig, out / "fig_4_19_spearman")
    plt.close(fig)

    sig = tables["estabilidad_senal"].copy()
    cap_st = tables["estabilidad_capacidad"].copy()

    # Fig. 20. DE RSSI.
    fig, ax = plt.subplots(figsize=(7.2, 4.0), constrained_layout=True)
    ax.bar(sig["Escenario"], sig["RSSI DE (dB)"], color=PRIMARY,
           edgecolor=PRIMARY_DARK, width=0.7)
    ax.set_title("Dispersión del RSSI por escenario")
    ax.set_xlabel("Escenario experimental")
    ax.set_ylabel("DE del RSSI DL (dB)")
    _polish(ax)
    _bar_labels(ax, 3)
    ax.set_ylim(0, sig["RSSI DE (dB)"].max() * 1.15)
    figures["est_rssi"] = _save(fig, out / "fig_4_20_estabilidad_rssi")
    plt.close(fig)

    # Fig. 21. CV MCS.
    fig, ax = plt.subplots(figsize=(7.2, 4.0), constrained_layout=True)
    ax.bar(cap_st["Escenario"], cap_st["MCS CV (%)"], color=PRIMARY,
           edgecolor=PRIMARY_DARK, width=0.7)
    ax.set_title("Variabilidad relativa del MCS")
    ax.set_xlabel("Escenario experimental")
    ax.set_ylabel("CV del MCS DL (%)")
    _polish(ax)
    _bar_labels(ax, 3)
    ax.set_ylim(0, cap_st["MCS CV (%)"].max() * 1.15)
    figures["est_mcs"] = _save(fig, out / "fig_4_21_estabilidad_mcs")
    plt.close(fig)

    # Fig. 22. CV throughput.
    cap_th = cap_st.dropna(subset=["Throughput CV (%)"])
    fig, ax = plt.subplots(figsize=(7.2, 4.0), constrained_layout=True)
    ax.bar(cap_th["Escenario"], cap_th["Throughput CV (%)"], color=PRIMARY,
           edgecolor=PRIMARY_DARK, width=0.7)
    ax.set_title("Variabilidad relativa del throughput")
    ax.set_xlabel("Escenario experimental")
    ax.set_ylabel("CV del throughput DL (%)")
    _polish(ax)
    _bar_labels(ax, 2)
    ax.set_ylim(0, cap_th["Throughput CV (%)"].max() * 1.15)
    figures["est_throughput"] = _save(fig, out / "fig_4_22_estabilidad_throughput")
    plt.close(fig)

    # Fig. 23. Índice compuesto.
    idx = tables["indice_estabilidad"].sort_values(
        "Índice de estabilidad", ascending=False
    ).copy()
    best = str(idx.iloc[0]["Escenario"])
    colors = [HIGHLIGHT if str(s) == best else PRIMARY for s in idx["Escenario"]]
    fig, ax = plt.subplots(figsize=(7.2, 4.0), constrained_layout=True)
    ax.bar(idx["Escenario"], idx["Índice de estabilidad"], color=colors,
           edgecolor=PRIMARY_DARK, width=0.7)
    ax.set_title("Índice compuesto de estabilidad operativa")
    ax.set_xlabel("Escenario experimental")
    ax.set_ylabel("Índice de estabilidad")
    ax.set_ylim(0, 1.02)
    _polish(ax)
    _bar_labels(ax, 3)
    figures["indice"] = _save(fig, out / "fig_4_23_indice_estabilidad")
    plt.close(fig)

    return figures
