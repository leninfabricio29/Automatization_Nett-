import pandas as pd
from pathlib import Path

REQUIRED_COLUMNS = {
    "id","category_id","create_date","partner_email","stage_id","assigned_date","closed_date",
    "partner_name","number","priority","name","user_id","last_stage_update"
}

def read_visits_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    if not REQUIRED_COLUMNS.issubset(df.columns):
        raise ValueError("El CSV no tiene las columnas esperadas")

    return df

def get_latest_visits_csv(downloads_dir: str = "./downloads/visits") -> Path:
    """
    Returns the most recently downloaded CSV file from downloads directory.
    """
    downloads_path = Path(downloads_dir)

    if not downloads_path.exists():
        raise FileNotFoundError("La carpeta './downloads/visits' no existe")

    csv_files = list(downloads_path.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError("No se encontraron archivos CSV en ./downloads/visits/")

    latest_csv = max(csv_files, key=lambda f: f.stat().st_mtime)
    return latest_csv

