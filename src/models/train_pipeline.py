from src.models.train_corners import train_corners_model
from src.models.train_shots import train_shots_model
from src.models.train_cards import train_cards_model


def train_all_models():
    print("=== Treinar modelos de Cantos ===")
    train_corners_model()

    print("\n=== Treinar modelos de Remates ===")
    train_shots_model()

    print("\n=== Treinar modelos de Cartões ===")
    train_cards_model()

    print("\n✔ Todos os modelos treinados com sucesso")
