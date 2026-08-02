
import pandas as pd


def construir_resumen_objetivos(
    kruskal: pd.DataFrame,
    franjas: pd.DataFrame,
    spearman: pd.DataFrame,
    stability_index: pd.DataFrame,
) -> pd.DataFrame:
    strongest_effect = kruskal.loc[
        kruskal["Épsilon cuadrado"].astype(float).idxmax()
    ]
    time_sig = int(franjas["Escenarios significativos"].sum())
    time_valid = int(franjas["Escenarios válidos"].sum())
    strongest_rho = spearman.loc[
        spearman["ρ de Spearman"].astype(float).abs().idxmax()
    ]
    best_stability = stability_index.iloc[0]

    return pd.DataFrame([
        {
            "Componente": "Objetivo específico 1",
            "Evidencia principal": (
                f"Kruskal-Wallis y Dunn; mayor ε² en "
                f"{strongest_effect['Métrica']} "
                f"({float(strongest_effect['Épsilon cuadrado']):.3f})."
            ),
            "Resultado": "Diferencias entre configuraciones",
            "Decisión": "Objetivo atendido",
        },
        {
            "Componente": "Objetivo específico 2",
            "Evidencia principal": (
                f"Mann-Whitney, Holm y delta de Cliff: "
                f"{time_sig} de {time_valid} contrastes significativos."
            ),
            "Resultado": "Diferencias temporales estratificadas",
            "Decisión": "Objetivo atendido",
        },
        {
            "Componente": "Objetivo específico 3",
            "Evidencia principal": (
                f"Spearman; mayor |ρ| en {strongest_rho['Métrica']} "
                f"({float(strongest_rho['ρ de Spearman']):.3f})."
            ),
            "Resultado": "Asociación débil con precipitación",
            "Decisión": "Objetivo atendido",
        },
        {
            "Componente": "Objetivo específico 4",
            "Evidencia principal": (
                f"Índice compuesto: {best_stability['Escenario']} = "
                f"{float(best_stability['Índice de estabilidad']):.3f}."
            ),
            "Resultado": "Escenario de mayor estabilidad relativa identificado",
            "Decisión": "Objetivo atendido",
        },
        {
            "Componente": "Hipótesis general",
            "Evidencia principal": (
                "Resultados descriptivos, inferenciales, temporales y de estabilidad."
            ),
            "Resultado": (
                "Las configuraciones se asociaron con diferencias significativas "
                "y de magnitud relevante."
            ),
            "Decisión": "Respaldada en las condiciones evaluadas",
        },
    ])
