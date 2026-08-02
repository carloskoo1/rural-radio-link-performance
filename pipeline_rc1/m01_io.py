
from pathlib import Path
import logging
import pandas as pd


def require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo requerido: {path}")


def read_csv(path: Path) -> pd.DataFrame:
    require_file(path)
    logging.info("Leyendo CSV: %s", path)
    return pd.read_csv(path, encoding="utf-8-sig")


def write_csv(df: pd.DataFrame, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    logging.info("CSV generado: %s", path)
    return path
