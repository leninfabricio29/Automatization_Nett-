import pandas as pd
from pathlib import Path

REQUIRED_COLUMNS = {
    "id", "display_name", "area_id", "assigned_id",
    "user_id", "module_id", "state",
    "time_create_turn", "turn_solution"
}

def read_turnos_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    if not REQUIRED_COLUMNS.issubset(df.columns):
        raise ValueError("El CSV no tiene las columnas esperadas")

    return df

def get_latest_turnos_csv(downloads_dir: str = "./downloads") -> Path:
    """
    Returns the most recently downloaded CSV file from downloads directory.
    """
    downloads_path = Path(downloads_dir)

    if not downloads_path.exists():
        raise FileNotFoundError("La carpeta './downloads/' no existe")

    csv_files = list(downloads_path.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError("No se encontraron archivos CSV en ./downloads/")

    latest_csv = max(csv_files, key=lambda f: f.stat().st_mtime)
    return latest_csv

