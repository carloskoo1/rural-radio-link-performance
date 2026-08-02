
from __future__ import annotations

from pathlib import Path
import pandas as pd


SCENARIO_COLUMNS = {
    "escenario",
    "frecuencia_mhz",
    "ancho_canal_mhz",
    "fecha",
    "rssi_dl",
    "snr_dl",
    "mcs_dl",
    "throughput_dl",
}

CLIMATE_COLUMNS = {
    "hora_merge",
    "precip_mm",
    "rssi_dl",
    "snr_dl",
    "mcs_dl",
    "throughput_dl",
}


def resolve_datetime(df: pd.DataFrame) -> pd.Series:
    direct = [
        "timestamp",
        "datetime",
        "fecha_hora",
        "timestamp_local",
        "fecha_hora_local",
        "hora_merge",
    ]
    for column in direct:
        if column in df.columns:
            parsed = pd.to_datetime(df[column], errors="coerce")
            if parsed.notna().mean() >= 0.80:
                return parsed

    for date_col in ["fecha", "date"]:
        if date_col not in df.columns:
            continue
        for hour_col in ["hora", "hour", "time", "time_local"]:
            if hour_col not in df.columns:
                continue
            parsed = pd.to_datetime(
                df[date_col].astype(str).str.strip()
                + " "
                + df[hour_col].astype(str).str.strip(),
                errors="coerce",
            )
            if parsed.notna().mean() >= 0.80:
                return parsed

    raise ValueError(
        "No se pudo identificar una fecha y hora válida en el dataset de escenarios."
    )


def validate_inputs(scenarios: pd.DataFrame, climate: pd.DataFrame) -> None:
    missing_scenarios = sorted(SCENARIO_COLUMNS - set(scenarios.columns))
    missing_climate = sorted(CLIMATE_COLUMNS - set(climate.columns))

    errors = []
    if missing_scenarios:
        errors.append(
            "dataset_escenarios_full_day.csv: " + ", ".join(missing_scenarios)
        )
    if missing_climate:
        errors.append(
            "dataset_radio_clima.csv: " + ", ".join(missing_climate)
        )

    if errors:
        raise ValueError("Faltan columnas requeridas:\n- " + "\n- ".join(errors))

    resolve_datetime(scenarios)


def validate_no_rssi_cv(tables: dict[str, pd.DataFrame]) -> None:
    forbidden = []
    for name, df in tables.items():
        for column in df.columns:
            if "rssi" in str(column).lower() and "cv" in str(column).lower():
                forbidden.append(f"{name}: {column}")

    if forbidden:
        raise ValueError(
            "El pipeline detectó CV aplicado al RSSI, lo cual está prohibido:\n- "
            + "\n- ".join(forbidden)
        )


def validate_text_blocks(blocks: list[dict]) -> None:
    errors = []
    for i, block in enumerate(blocks, start=1):
        if not block.get("introduccion", "").strip():
            errors.append(f"Bloque {i}: falta introducción.")
        if not block.get("interpretacion", "").strip():
            errors.append(f"Bloque {i}: falta interpretación.")
        if block.get("tipo") == "figura" and not block.get("titulo", "").strip():
            errors.append(f"Bloque {i}: figura sin título.")

    if errors:
        raise ValueError(
            "La validación narrativa detectó problemas:\n- " + "\n- ".join(errors)
        )
