import pandas as pd
from sklearn.linear_model import PoissonRegressor
from sklearn.metrics import mean_absolute_error
import joblib
from pathlib import Path

from src.config.settings import PROCESSED_DIR
from src.utils.io import ensure_dir


ARTIFACTS_DIR = Path("src/models/artifacts")


def train_cards_model():
    ensure_dir(ARTIFACTS_DIR)

    df = pd.read_csv(Path(PROCESSED_DIR) / "features_train.csv")

    y_home = df["home_avg_yellow_cards"]
    y_away = df["away_avg_yellow_cards"]

    X = df.drop(columns=["match_id", "home_team", "away_team",
                         "home_avg_yellow_cards", "away_avg_yellow_cards"])

    model_home = PoissonRegressor(alpha=0.1, max_iter=300)
    model_away = PoissonRegressor(alpha=0.1, max_iter=300)

    model_home.fit(X, y_home)
    model_away.fit(X, y_away)

    pred_home = model_home.predict(X)
    pred_away = model_away.predict(X)

    mae_home = mean_absolute_error(y_home, pred_home)
    mae_away = mean_absolute_error(y_away, pred_away)

    print(f"MAE Cartões Casa: {mae_home:.3f}")
    print(f"MAE Cartões Fora: {mae_away:.3f}")

    joblib.dump(model_home, ARTIFACTS_DIR / "cards_home.pkl")
    joblib.dump(model_away, ARTIFACTS_DIR / "cards_away.pkl")

    print("✔ Modelos de cartões guardados com sucesso")
