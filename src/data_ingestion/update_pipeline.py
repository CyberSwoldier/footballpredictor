import logging
from pathlib import Path
from typing import List

import pandas as pd

from src.config.settings import RAW_DIR, SEASONS
from src.data_ingestion.sofascore_client import SofascoreClient
from src.domain.schemas import MatchInfo, MatchStats


logger = logging.getLogger(__name__)


def update_data_for_league(league_id: int) -> None:
    """
    Orquestra o update de dados:
    - Vai buscar jogos por época
    - Vai buscar estatísticas de cada jogo
    - Guarda em CSVs em data/raw
    """
    client = SofascoreClient()
    raw_path = Path(RAW_DIR)
    raw_path.mkdir(parents=True, exist_ok=True)

    all_matches: List[MatchInfo] = []
    all_stats_rows = []

    for season in SEASONS:
        matches = client.get_matches_by_season(season=season, league_id=league_id)
        all_matches.extend(matches)

        for m in matches:
            try:
                stats = client.get_match_stats(m.match_id)
            except Exception as e:
                logger.error(f"Erro ao obter stats para match_id={m.match_id}: {e}")
                continue

            row = {
                "match_id": m.match_id,
                "season": m.season,
                "round_number": m.round_number,
                "date": m.date,
                "home_team": m.home_team,
                "away_team": m.away_team,
                "home_score": m.home_score,
                "away_score": m.away_score,
                # Flatten de MatchStats
                **stats.__dict__,
            }
            all_stats_rows.append(row)

    # Guardar jogos
    matches_df = pd.DataFrame([m.__dict__ for m in all_matches])
    matches_df.to_csv(raw_path / "matches.csv", index=False)

    # Guardar stats
    stats_df = pd.DataFrame(all_stats_rows)
    stats_df.to_csv(raw_path / "match_stats.csv", index=False)

    logger.info(f"Guardados {len(all_matches)} jogos e {len(all_stats_rows)} linhas de stats em {RAW_DIR}")
