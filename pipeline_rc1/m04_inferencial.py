
import pandas as pd


def resumen_dunn(full: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for metric, group in full.groupby("Métrica", sort=False):
        significant = group["Diferencia significativa"].astype(str).str.strip().eq("Sí")
        not_sig = group.loc[~significant]
        pairs = (
            "Ninguna"
            if not_sig.empty
            else "; ".join(
                f"{r['Comparación']} (p={r['Valor p ajustado']})"
                for _, r in not_sig.iterrows()
            )
        )
        rows.append(
            {
                "Métrica": metric,
                "Significativas": f"{int(significant.sum())} de {len(group)}",
                "No significativas": pairs,
            }
        )
    return pd.DataFrame(rows)


def texto_kruskal(table: pd.DataFrame) -> tuple[str, str]:
    intro = (
        "Confirmado el incumplimiento de la normalidad, se aplicó Kruskal-Wallis "
        "para evaluar diferencias globales entre escenarios."
    )
    parts = []
    for _, row in table.iterrows():
        parts.append(
            f"{row['Métrica']} (H = {float(row['Estadístico H']):.2f}; "
            f"p {row['Valor p']}; ε² = {float(row['Épsilon cuadrado']):.3f})"
        )
    interpretation = (
        "Las configuraciones técnicas se asociaron con diferencias estadísticamente "
        "significativas en " + ", ".join(parts) + ". Los tamaños del efecto fueron "
        "grandes dentro de los periodos evaluados."
    )
    return intro, interpretation


def texto_dunn(table: pd.DataFrame) -> tuple[str, str]:
    intro = (
        "Debido a la significancia del contraste global, se aplicó Dunn con ajuste "
        "de Holm para identificar las diferencias específicas entre pares."
    )
    parts = [
        f"{r['Métrica']}: {r['No significativas']}"
        for _, r in table.iterrows()
    ]
    interpretation = (
        "La mayoría de comparaciones pareadas fue significativa. Los pares que no "
        "presentaron diferencias fueron " + "; ".join(parts) + "."
    )
    return intro, interpretation
