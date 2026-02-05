from pathlib import Path
import pandas as pd


def ensure_dir(path: Path):
    """Garante que um diretório existe."""
    path.mkdir(parents=True, exist_ok=True)


def read_csv_safe(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Ficheiro não encontrado: {path}")
    return pd.read_csv(path)
