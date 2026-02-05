import pandas as pd
from pathlib import Path
from typing import List

from src.config.settings import RAW_DIR, PROCESSED_DIR
from src.domain.schemas import MatchFeatures


class FeatureBuilder:
    """
    Constrói features para treino e previsão.
    """

    def __init__(self):
        self.raw_matches_path = Path(RAW_DIR) / "matches.csv"
        self.raw_stats_path = Path(RAW_DIR) / "match_stats.csv"
        self.processed_path = Path(PROCESSED_DIR)
        self.processed_path.mkdir(parents=True, exist_ok=True)

        self.matches_df = pd.read_csv(self.raw_matches_path)
        self.stats_df = pd.read_csv(self.raw_stats_path)

        # Merge inicial
        self.df = self.matches_df.merge(self.stats_df, on="match_id", how="left")

    # ---------------------------------------------------------
    # 1) Funções auxiliares
    # ---------------------------------------------------------

    def _team_history(self, team: str) -> pd.DataFrame:
        """Filtra todos os jogos de uma equipa."""
        return self.df[(self.df["home_team"] == team) | (self.df["away_team"] == team)]

    def _team_last_n(self, team: str, n: int = 5) -> pd.DataFrame:
        """Últimos n jogos da equipa."""
        hist = self._team_history(team)
        return hist.sort_values("date", ascending=False).head(n)

    def _team_avg(self, team: str, column_home: str, column_away: str) -> float:
        """Média de uma métrica para uma equipa (casa + fora)."""
        hist = self._team_history(team)
        values = []

        for _, row in hist.iterrows():
            if row["home_team"] == team:
                values.append(row[column_home])
            else:
                values.append(row[column_away])

        return float(pd.Series(values).mean()) if values else 0.0

    def _team_form_last5(self, team: str) -> float:
        """Forma recente baseada em pontos (vitória=3, empate=1, derrota=0)."""
        last5 = self._team_last_n(team, 5)
        points = []

        for _, row in last5.iterrows():
            if row["home_team"] == team:
                if row["home_score"] > row["away_score"]:
                    points.append(3)
                elif row["home_score"] == row["away_score"]:
                    points.append(1)
                else:
                    points.append(0)
            else:
                if row["away_score"] > row["home_score"]:
                    points.append(3)
                elif row["away_score"] == row["home_score"]:
                    points.append(1)
                else:
                    points.append(0)

        return float(pd.Series(points).mean()) if points else 0.0

    # ---------------------------------------------------------
    # 2) Construção de features para um jogo
    # ---------------------------------------------------------

    def build_features_for_match(self, match_row: pd.Series) -> MatchFeatures:
        home = match_row["home_team"]
        away = match_row["away_team"]

        # Médias históricas
        home_avg_corners = self._team_avg(home, "corners_home", "corners_away")
        away_avg_corners = self._team_avg(away, "corners_home", "corners_away")

        home_avg_shots = self._team_avg(home, "shots_home", "shots_away")
        away_avg_shots = self._team_avg(away, "shots_home", "shots_away")

        home_avg_yellow = self._team_avg(home, "yellow_cards_home", "yellow_cards_away")
        away_avg_yellow = self._team_avg(away, "yellow_cards_home", "yellow_cards_away")

        home_avg_xg = self._team_avg(home, "xg_home", "xg_away")
        away_avg_xg = self._team_avg(away, "xg_home", "xg_away")

        # Forma recente
        home_form = self._team_form_last5(home)
        away_form = self._team_form_last5(away)

        # Casa/Fora
        home_home_perf = self._team_avg(home, "shots_home", "shots_away")
        away_away_perf = self._team_avg(away, "shots_away", "shots_home")

        # Diferenças
        delta_corners = home_avg_corners - away_avg_corners
        delta_shots = home_avg_shots - away_avg_shots
        delta_xg = home_avg_xg - away_avg_xg
        delta_yellow = home_avg_yellow - away_avg_yellow

        return MatchFeatures(
            match_id=match_row["match_id"],
            home_team=home,
            away_team=away,
            home_avg_corners=home_avg_corners,
            away_avg_corners=away_avg_corners,
            home_avg_shots=home_avg_shots,
            away_avg_shots=away_avg_shots,
            home_avg_yellow_cards=home_avg_yellow,
            away_avg_yellow_cards=away_avg_yellow,
            home_avg_xg=home_avg_xg,
            away_avg_xg=away_avg_xg,
            home_form_last5=home_form,
            away_form_last5=away_form,
            home_home_performance=home_home_perf,
            away_away_performance=away_away_perf,
            delta_corners=delta_corners,
            delta_shots=delta_shots,
            delta_xg=delta_xg,
            delta_yellow_cards=delta_yellow,
        )

    # ---------------------------------------------------------
    # 3) Construção de features para todos os jogos
    # ---------------------------------------------------------

    def build_all_features(self):
        rows = []

        for _, row in self.df.iterrows():
            features = self.build_features_for_match(row)
            rows.append(features.__dict__)

        df_features = pd.DataFrame(rows)
        df_features.to_csv(self.processed_path / "features_train.csv", index=False)
        print("✔ features_train.csv gerado com sucesso")

    # ---------------------------------------------------------
    # 4) Features para a próxima jornada
    # ---------------------------------------------------------

    def build_next_round_features(self, next_round_matches: pd.DataFrame):
        rows = []

        for _, row in next_round_matches.iterrows():
            features = self.build_features_for_match(row)
            rows.append(features.__dict__)

        df_features = pd.DataFrame(rows)
        df_features.to_csv(self.processed_path / "features_next_round.csv", index=False)
        print("✔ features_next_round.csv gerado com sucesso")
