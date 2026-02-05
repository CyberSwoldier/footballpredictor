import pandas as pd
from pathlib import Path

from src.config.settings import PROCESSED_DIR, PREDICTIONS_DIR
from src.models.predict import predict_match
from src.utils.io import ensure_dir


def generate_predictions():
    """
    Gera previsões para todos os jogos da próxima jornada.
    Lê features_next_round.csv e produz predictions_next_round.csv.
    """

    features_path = Path(PROCESSED_DIR) / "features_next_round.csv"
    predictions_path = Path(PREDICTIONS_DIR)
    ensure_dir(predictions_path)

    if not features_path.exists():
        raise FileNotFoundError(
            f"Ficheiro {features_path} não encontrado. "
            "Gera primeiro as features da próxima jornada."
        )

    df = pd.read_csv(features_path)
    prediction_rows = []

    for _, row in df.iterrows():
        pred = predict_match(row)
        prediction_rows.append(pred.__dict__)

    pred_df = pd.DataFrame(prediction_rows)
    pred_df.to_csv(predictions_path / "predictions_next_round.csv", index=False)

    print("✔ Previsões geradas com sucesso em data/predictions/predictions_next_round.csv")


if __name__ == "__main__":
    generate_predictions()
