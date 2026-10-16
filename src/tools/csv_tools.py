from pathlib import Path
import pandas as pd
from .registry import tool
from ..config import get_data_path


@tool("csv_reader")
def csv_reader(path: str | Path, **kwargs) -> pd.DataFrame:
    """Read a CSV file, resolving path relative to project or data directory."""
    resolved_path = get_data_path(path)
    if not resolved_path.exists():
        raise FileNotFoundError(f"CSV file not found: {resolved_path}")
    return pd.read_csv(resolved_path)


@tool("excel_parser")
def excel_parser(path: str | Path, sheet_name=0, **kwargs) -> pd.DataFrame:
    """Parse an Excel or CSV file, resolving path safely."""
    resolved_path = get_data_path(path)
    # Fallback to CSV if xlsx doesn't exist but csv does
    if not resolved_path.exists():
        csv_fallback = resolved_path.with_suffix(".csv")
        if csv_fallback.exists():
            return pd.read_csv(csv_fallback)
        raise FileNotFoundError(f"Spreadsheet file not found: {resolved_path}")

    if str(resolved_path).endswith(".csv"):
        return pd.read_csv(resolved_path)
    return pd.read_excel(resolved_path, sheet_name=sheet_name)