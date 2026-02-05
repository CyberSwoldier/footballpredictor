import pandas as pd
from sklearn.linear_model import PoissonRegressor
from sklearn.metrics import mean_absolute_error
import joblib
from pathlib import Path

from src.config.settings import PROCESSED_DIR
from src.utils.io import ensure_dir


ARTIFACTS_DIR = Path("src/models/artifacts")


def train_corners_model():
    ensure_dir(ARTIFACTS_DIR)

    df = pd.read_csv(Path(PROCESSED_DIR) / "features_train.csv")

    # Targets
    y_home = df["home_avg_corners"]
    y_away = df["away_avg_corners"]

    # Features
    X = df.drop(columns=["match_id", "home_team", "away_team",
                         "home_avg_corners", "away_avg_corners"])

    # Modelos
    model_home = PoissonRegressor(alpha=0.1, max_iter=300)
    model_away = PoissonRegressor(alpha=0.1, max_iter=300)

    model_home.fit(X, y_home)
    model_away.fit(X, y_away)

    # Avaliação
    pred_home = model_home.predict(X)
    pred_away = model_away.predict(X)

    mae_home = mean_absolute_error(y_home, pred_home)
    mae_away = mean_absolute_error(y_away, pred_away)

    print(f"MAE Cantos Casa: {mae_home:.3f}")
    print(f"MAE Cantos Fora: {mae_away:.3f}")

    # Guardar modelos
    joblib.dump(model_home, ARTIFACTS_DIR / "corners_home.pkl")
    joblib.dump(model_away, ARTIFACTS_DIR / "corners_away.pkl")

    print("✔ Modelos de cantos guardados com sucesso")
