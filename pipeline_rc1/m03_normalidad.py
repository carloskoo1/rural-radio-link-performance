
import warnings
import pandas as pd
from scipy.stats import shapiro

from .m00_config import ALPHA


def _p_text(p: float) -> str:
    return "< 0.001" if p < 0.001 else f"{p:.4f}"


def calcular_normalidad(df: pd.DataFrame) -> pd.DataFrame:
    config = {
        "rssi_dl": ("RSSI DL", ["E0", "E1", "E2", "E3", "E4", "E5"]),
        "snr_dl": ("SNR DL", ["E0", "E1", "E2", "E3", "E4", "E5"]),
        "mcs_dl": ("MCS DL", ["E0", "E1", "E2", "E3", "E4", "E5"]),
        "throughput_dl": ("Throughput DL", ["E1", "E2", "E3", "E4", "E5"]),
    }

    rows = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for column, (label, scenarios) in config.items():
            for scenario in scenarios:
                values = pd.to_numeric(
                    df.loc[df["escenario"] == scenario, column],
                    errors="coerce",
                ).dropna()
                if len(values) < 3:
                    continue
                w, p = shapiro(values.to_numpy())
                rows.append(
                    {
                        "Métrica": label,
                        "Escenario": scenario,
                        "N": len(values),
                        "W": round(float(w), 3),
                        "Valor p": _p_text(float(p)),
                        "Decisión": "No normal" if p < ALPHA else "Normal",
                    }
                )
    return pd.DataFrame(rows)


def texto_normalidad(table: pd.DataFrame) -> tuple[str, str]:
    intro = (
        "Antes de seleccionar los procedimientos inferenciales, se verificó el "
        "supuesto de normalidad en cada combinación de métrica y escenario."
    )
    rejected = int((table["Decisión"] == "No normal").sum())
    interpretation = (
        f"Los {rejected} de {len(table)} contrastes rechazaron la hipótesis de "
        "normalidad. Debido al elevado tamaño muestral, esta decisión se complementó "
        "con la naturaleza discreta del MCS y la inspección de las distribuciones. "
        "Por tanto, se emplearon procedimientos no paramétricos."
    )
    return intro, interpretation
