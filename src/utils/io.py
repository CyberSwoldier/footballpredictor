from pathlib import Path


def ensure_dir(path: Path):
    """Garante que um diretório existe."""
    path.mkdir(parents=True, exist_ok=True)
