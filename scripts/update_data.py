import logging

from src.data_ingestion.update_pipeline import update_data_for_league


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)


if __name__ == "__main__":
    # TODO: substituir pelo ID real da Primeira Liga no Sofascore
    PRIMEIRA_LIGA_ID = 1234
    update_data_for_league(PRIMEIRA_LIGA_ID)
