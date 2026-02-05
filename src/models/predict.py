import joblib
import pandas as pd
from pathlib import Path

from src.config.settings import PROCESSED_DIR
from src.domain.schemas import MatchPrediction


ARTIFACTS_DIR = Path("src/models/artifacts")


def predict_match(features_row: pd.Series) -> MatchPrediction:
    # Carregar modelos
    corners_home = joblib.load(ARTIFACTS_DIR / "corners_home.pkl")
    corners_away = joblib.load(ARTIFACTS_DIR / "corners_away.pkl")

    shots_home = joblib.load(ARTIFACTS_DIR / "shots_home.pkl")
    shots_away = joblib.load(ARTIFACTS_DIR / "shots_away.pkl")

    cards_home = joblib.load(ARTIFACTS_DIR / "cards_home.pkl")
    cards_away = joblib.load(ARTIFACTS_DIR / "cards_away.pkl")

    # Features (remover colunas não numéricas)
    X = features_row.drop(labels=["match_id", "home_team", "away_team"]).to_frame().T

    return MatchPrediction(
        match_id=features_row["match_id"],
        home_team=features_row["home_team"],
        away_team=features_row["away_team"],
        predicted_corners_home=float(corners_home.predict(X)[0]),
        predicted_corners_away=float(corners_away.predict(X)[0]),
        predicted_shots_home=float(shots_home.predict(X)[0]),
        predicted_shots_away=float(shots_away.predict(X)[0]),
        predicted_yellow_cards_home=float(cards_home.predict(X)[0]),
        predicted_yellow_cards_away=float(cards_away.predict(X)[0]),
        predicted_xg_home=0.0,  # reservado para modelo futuro
        predicted_xg_away=0.0,
    )
