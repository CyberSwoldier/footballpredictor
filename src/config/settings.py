from pathlib import Path

# Diretórios base
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
PREDICTIONS_DIR = DATA_DIR / "predictions"

# Liga / contexto
LEAGUE = "Primeira Liga"
SEASONS = ["2022-2023", "2023-2024"]

# (Opcional) ID da liga no Sofascore
PRIMEIRA_LIGA_ID = 1234  # substituir pelo real
