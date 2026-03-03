import pandas as pd
from pathlib import Path

REQUIRED_COLUMNS = {
    "id","create_date","partner_id","name","state","tag_ids","recurring_next_date",
    "payment_type_id","contract_invoice_amount","contract_line_id","state_service",
    "contract_line_id/price_unit"

}

def read_contracts_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    if not REQUIRED_COLUMNS.issubset(df.columns):
        raise ValueError("El CSV no tiene las columnas esperadas")

    return df

def get_latest_contracts_csv(downloads_dir: str = "./downloads/contracts") -> Path:
    """
    Returns the most recently downloaded CSV file from downloads directory.
    """
    downloads_path = Path(downloads_dir)

    if not downloads_path.exists():
        raise FileNotFoundError("La carpeta './downloads/contracts' no existe")

    csv_files = list(downloads_path.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError("No se encontraron archivos CSV en ./downloads/contracts/")

    latest_csv = max(csv_files, key=lambda f: f.stat().st_mtime)
    return latest_csv

