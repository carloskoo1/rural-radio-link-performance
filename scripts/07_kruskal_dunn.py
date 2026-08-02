"""
07_kruskal_dunn.py
===================

Análisis inferencial del desempeño técnico del radioenlace.

Procedimientos:
1. Prueba de Kruskal-Wallis para comparar los escenarios.
2. Cálculo del tamaño del efecto épsilon cuadrado.
3. Prueba post hoc de Dunn.
4. Corrección de Holm para comparaciones múltiples.
5. Generación de tablas CSV listas para la tesis.

Archivo de entrada:
    dataset_escenarios_full_day.csv

Archivos de salida:
    resultados_inferenciales/
        tabla_4_2_kruskal_wallis.csv
        tabla_4_3_dunn_completa.csv
        tabla_4_3_dunn_significativas.csv

Requisitos:
    pip install pandas numpy scipy statsmodels
"""

from __future__ import annotations

from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kruskal, norm, rankdata
from statsmodels.stats.multitest import multipletests


# ============================================================
# CONFIGURACIÓN
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ARCHIVO_ENTRADA = (
    BASE_DIR
    / "data"
    / "processed"
    / "dataset_escenarios_full_day.csv"
)

CARPETA_SALIDA = (
    BASE_DIR
    / "outputs"
    / "tables"
)

ALPHA = 0.05

# Holm controla el error familiar y es menos conservador
# que Bonferroni.
METODO_AJUSTE = "holm"

METRICAS = {
    "rssi_dl": {
        "nombre": "RSSI DL",
        "escenarios": ["E0", "E1", "E2", "E3", "E4", "E5"],
    },
    "snr_dl": {
        "nombre": "SNR DL",
        "escenarios": ["E0", "E1", "E2", "E3", "E4", "E5"],
    },
    "mcs_dl": {
        "nombre": "MCS DL",
        "escenarios": ["E0", "E1", "E2", "E3", "E4", "E5"],
    },
    "throughput_dl": {
        "nombre": "Throughput DL",
        # E0 se excluye porque no tiene throughput comparable.
        "escenarios": ["E1", "E2", "E3", "E4", "E5"],
    },
}


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def cargar_datos(ruta: Path) -> pd.DataFrame:
    """Carga y valida el archivo consolidado."""

    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de entrada:\n{ruta.resolve()}"
        )

    df = pd.read_csv(ruta)

    columnas_requeridas = {"escenario", *METRICAS.keys()}
    faltantes = columnas_requeridas.difference(df.columns)

    if faltantes:
        raise ValueError(
            "El archivo no contiene las columnas requeridas: "
            + ", ".join(sorted(faltantes))
        )

    df["escenario"] = (
        df["escenario"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    for metrica in METRICAS:
        df[metrica] = pd.to_numeric(df[metrica], errors="coerce")

    return df


def interpretar_efecto(epsilon2: float) -> str:
    """
    Clasifica de forma orientativa la magnitud del efecto.

    Criterios:
        < 0.01  : despreciable
        < 0.06  : pequeño
        < 0.14  : moderado
        >= 0.14 : grande
    """

    if epsilon2 < 0.01:
        return "Despreciable"
    if epsilon2 < 0.06:
        return "Pequeño"
    if epsilon2 < 0.14:
        return "Moderado"
    return "Grande"


def formatear_p(p: float) -> str:
    """Devuelve el valor p en formato apropiado para tablas."""

    if pd.isna(p):
        return ""

    if p < 0.001:
        return "< 0.001"

    return f"{p:.4f}"


def epsilon_cuadrado(
    estadistico_h: float,
    n_total: int,
    numero_grupos: int,
) -> float:
    """
    Calcula el tamaño del efecto épsilon cuadrado para Kruskal-Wallis.

    Fórmula:
        epsilon² = (H - k + 1) / (n - k)

    donde:
        H = estadístico de Kruskal-Wallis
        k = número de grupos
        n = número total de observaciones
    """

    denominador = n_total - numero_grupos

    if denominador <= 0:
        return np.nan

    valor = (
        estadistico_h - numero_grupos + 1
    ) / denominador

    # Se evita un valor negativo por aproximaciones numéricas.
    return max(0.0, float(valor))


def prueba_kruskal(
    df: pd.DataFrame,
    columna: str,
    escenarios: list[str],
    nombre_metrica: str,
) -> dict:
    """Ejecuta Kruskal-Wallis para una métrica."""

    grupos = []
    escenarios_validos = []

    for escenario in escenarios:
        valores = (
            df.loc[df["escenario"] == escenario, columna]
            .dropna()
            .to_numpy(dtype=float)
        )

        if len(valores) > 0:
            grupos.append(valores)
            escenarios_validos.append(escenario)

    if len(grupos) < 2:
        raise ValueError(
            f"No existen al menos dos grupos válidos para {columna}."
        )

    h, p = kruskal(*grupos)

    n_total = sum(len(grupo) for grupo in grupos)
    k = len(grupos)
    eps2 = epsilon_cuadrado(h, n_total, k)

    return {
        "Métrica": nombre_metrica,
        "Escenarios comparados": "–".join(
            [escenarios_validos[0], escenarios_validos[-1]]
        ),
        "N": n_total,
        "Estadístico H": float(h),
        "gl": k - 1,
        "Valor p numérico": float(p),
        "Valor p": formatear_p(float(p)),
        "Épsilon cuadrado": eps2,
        "Magnitud del efecto": interpretar_efecto(eps2),
        "Decisión": (
            "Se rechaza H0"
            if p < ALPHA
            else "No se rechaza H0"
        ),
    }


def prueba_dunn_manual(
    df: pd.DataFrame,
    columna: str,
    escenarios: list[str],
    nombre_metrica: str,
) -> pd.DataFrame:
    """
    Ejecuta la prueba post hoc de Dunn con corrección por empates.

    Posteriormente ajusta los valores p mediante Holm.
    """

    datos = (
        df.loc[
            df["escenario"].isin(escenarios),
            ["escenario", columna],
        ]
        .dropna()
        .copy()
    )

    if datos.empty:
        raise ValueError(
            f"No existen datos válidos para la métrica {columna}."
        )

    datos[columna] = pd.to_numeric(
        datos[columna],
        errors="coerce",
    )
    datos = datos.dropna(subset=[columna])

    # Rangos globales de todas las observaciones.
    datos["rango"] = rankdata(
        datos[columna].to_numpy(dtype=float),
        method="average",
    )

    resumen = (
        datos.groupby("escenario", observed=True)
        .agg(
            n=(columna, "size"),
            rango_promedio=("rango", "mean"),
            mediana=(columna, "median"),
        )
        .reindex(escenarios)
        .dropna()
    )

    n_total = len(datos)

    if n_total < 2:
        raise ValueError(
            f"Número insuficiente de observaciones para {columna}."
        )

    # Corrección por empates.
    _, conteos_empates = np.unique(
        datos[columna].to_numpy(dtype=float),
        return_counts=True,
    )

    suma_empates = np.sum(
        conteos_empates**3 - conteos_empates
    )

    correccion_empates = (
        1.0
        - suma_empates
        / (n_total**3 - n_total)
        if n_total > 1
        else 1.0
    )

    varianza_base = (
        n_total * (n_total + 1) / 12.0
    ) * correccion_empates

    resultados = []

    for escenario_1, escenario_2 in combinations(
        resumen.index.tolist(),
        2,
    ):
        n1 = int(resumen.loc[escenario_1, "n"])
        n2 = int(resumen.loc[escenario_2, "n"])

        r1 = float(
            resumen.loc[escenario_1, "rango_promedio"]
        )
        r2 = float(
            resumen.loc[escenario_2, "rango_promedio"]
        )

        mediana_1 = float(
            resumen.loc[escenario_1, "mediana"]
        )
        mediana_2 = float(
            resumen.loc[escenario_2, "mediana"]
        )

        error_estandar = np.sqrt(
            varianza_base * (1.0 / n1 + 1.0 / n2)
        )

        if error_estandar == 0:
            z = 0.0
            p_sin_ajustar = 1.0
        else:
            z = (r1 - r2) / error_estandar
            p_sin_ajustar = 2.0 * norm.sf(abs(z))

        resultados.append(
            {
                "Métrica": nombre_metrica,
                "Comparación": (
                    f"{escenario_1}–{escenario_2}"
                ),
                "Escenario 1": escenario_1,
                "Escenario 2": escenario_2,
                "N 1": n1,
                "N 2": n2,
                "Mediana 1": mediana_1,
                "Mediana 2": mediana_2,
                "Rango promedio 1": r1,
                "Rango promedio 2": r2,
                "Diferencia de rangos": r1 - r2,
                "Estadístico z": float(z),
                "p sin ajustar": float(p_sin_ajustar),
            }
        )

    tabla = pd.DataFrame(resultados)

    if tabla.empty:
        return tabla

    rechazo, p_ajustados, _, _ = multipletests(
        tabla["p sin ajustar"].to_numpy(),
        alpha=ALPHA,
        method=METODO_AJUSTE,
    )

    tabla["p ajustado numérico"] = p_ajustados
    tabla["Valor p ajustado"] = [
        formatear_p(float(p))
        for p in p_ajustados
    ]
    tabla["Diferencia significativa"] = np.where(
        rechazo,
        "Sí",
        "No",
    )

    return tabla


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main() -> None:
    """Ejecuta el análisis completo."""

    CARPETA_SALIDA.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = cargar_datos(ARCHIVO_ENTRADA)

    resultados_kruskal = []
    resultados_dunn = []

    for columna, configuracion in METRICAS.items():
        nombre = configuracion["nombre"]
        escenarios = configuracion["escenarios"]

        print(f"\nProcesando {nombre}...")

        resultado_kw = prueba_kruskal(
            df=df,
            columna=columna,
            escenarios=escenarios,
            nombre_metrica=nombre,
        )
        resultados_kruskal.append(resultado_kw)

        if (
            resultado_kw["Valor p numérico"]
            < ALPHA
        ):
            resultado_dunn = prueba_dunn_manual(
                df=df,
                columna=columna,
                escenarios=escenarios,
                nombre_metrica=nombre,
            )
            resultados_dunn.append(resultado_dunn)

    # --------------------------------------------------------
    # TABLA III: KRUSKAL-WALLIS
    # --------------------------------------------------------

    tabla_kruskal = pd.DataFrame(
        resultados_kruskal
    )

    columnas_tabla_iii = [
        "Métrica",
        "Escenarios comparados",
        "N",
        "Estadístico H",
        "gl",
        "Valor p",
        "Épsilon cuadrado",
        "Magnitud del efecto",
        "Decisión",
    ]

    tabla_iii = tabla_kruskal[
        columnas_tabla_iii
    ].copy()

    tabla_iii["Estadístico H"] = (
        tabla_iii["Estadístico H"].round(3)
    )
    tabla_iii["Épsilon cuadrado"] = (
        tabla_iii["Épsilon cuadrado"].round(3)
    )

    ruta_tabla_iii = (
        CARPETA_SALIDA
        / "tabla_4_2_kruskal_wallis.csv"
    )

    tabla_iii.to_csv(
        ruta_tabla_iii,
        index=False,
        encoding="utf-8-sig",
    )

    # --------------------------------------------------------
    # TABLA IV: DUNN
    # --------------------------------------------------------

    if resultados_dunn:
        tabla_dunn = pd.concat(
            resultados_dunn,
            ignore_index=True,
        )

        columnas_tabla_iv = [
            "Métrica",
            "Comparación",
            "N 1",
            "N 2",
            "Mediana 1",
            "Mediana 2",
            "Estadístico z",
            "Valor p ajustado",
            "Diferencia significativa",
        ]

        tabla_iv = tabla_dunn[
            columnas_tabla_iv
        ].copy()

        columnas_redondear = [
            "Mediana 1",
            "Mediana 2",
            "Estadístico z",
        ]

        for columna in columnas_redondear:
            tabla_iv[columna] = (
                tabla_iv[columna].round(3)
            )

        ruta_tabla_iv = (
            CARPETA_SALIDA
            / "tabla_4_3_dunn_completa.csv"
        )

        tabla_iv.to_csv(
            ruta_tabla_iv,
            index=False,
            encoding="utf-8-sig",
        )

        tabla_iv_significativa = tabla_iv.loc[
            tabla_iv[
                "Diferencia significativa"
            ] == "Sí"
        ].copy()

        ruta_tabla_iv_sig = (
            CARPETA_SALIDA
            / "tabla_4_3_dunn_significativas.csv"
        )

        tabla_iv_significativa.to_csv(
            ruta_tabla_iv_sig,
            index=False,
            encoding="utf-8-sig",
        )

    # --------------------------------------------------------
    # SALIDA EN CONSOLA
    # --------------------------------------------------------

    print("\n" + "=" * 90)
    print("TABLA III. KRUSKAL-WALLIS")
    print("=" * 90)
    print(tabla_iii.to_string(index=False))

    if resultados_dunn:
        print("\n" + "=" * 90)
        print("TABLA IV. DUNN — TODAS LAS COMPARACIONES")
        print("=" * 90)
        print(tabla_iv.to_string(index=False))

        print("\n" + "=" * 90)
        print("COMPARACIONES SIGNIFICATIVAS")
        print("=" * 90)

        if tabla_iv_significativa.empty:
            print(
                "No se identificaron comparaciones "
                "significativas."
            )
        else:
            print(
                tabla_iv_significativa.to_string(
                    index=False
                )
            )

    print("\nArchivos generados:")

    for archivo in sorted(
        CARPETA_SALIDA.glob("*.csv")
    ):
        print(f" - {archivo}")


if __name__ == "__main__":
    main()
