import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
from pathlib import Path

from src.config.settings import PROCESSED_DIR
from src.utils.io import ensure_dir


ARTIFACTS_DIR = Path("src/models/artifacts")


def train_shots_model():
    ensure_dir(ARTIFACTS_DIR)

    df = pd.read_csv(Path(PROCESSED_DIR) / "features_train.csv")

    y_home = df["home_avg_shots"]
    y_away = df["away_avg_shots"]

    X = df.drop(columns=["match_id", "home_team", "away_team",
                         "home_avg_shots", "away_avg_shots"])

    model_home = RandomForestRegressor(n_estimators=300, random_state=42)
    model_away = RandomForestRegressor(n_estimators=300, random_state=42)

    model_home.fit(X, y_home)
    model_away.fit(X, y_away)

    pred_home = model_home.predict(X)
    pred_away = model_away.predict(X)

    mae_home = mean_absolute_error(y_home, pred_home)
    mae_away = mean_absolute_error(y_away, pred_away)

    print(f"MAE Remates Casa: {mae_home:.3f}")
    print(f"MAE Remates Fora: {mae_away:.3f}")

    joblib.dump(model_home, ARTIFACTS_DIR / "shots_home.pkl")
    joblib.dump(model_away, ARTIFACTS_DIR / "shots_away.pkl")

    print("✔ Modelos de remates guardados com sucesso")
