import time
import logging
from typing import List, Dict, Any, Optional

import requests

from src.domain.schemas import MatchInfo, MatchStats


logger = logging.getLogger(__name__)


class SofascoreClient:
    """
    Cliente para obter dados do Sofascore.

    NOTA IMPORTANTE:
    - Os endpoints e paths aqui são placeholders.
    - Deves ajustá-los aos endpoints reais do Sofascore (JSON),
      respeitando sempre os termos de uso.
    """

    def __init__(self, base_url: str = "https://api.sofascore.com/api/v1", pause_seconds: float = 0.8):
        self.base_url = base_url.rstrip("/")
        self.pause_seconds = pause_seconds
        self.session = requests.Session()

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        logger.debug(f"GET {url} params={params}")
        resp = self.session.get(url, params=params, timeout=10)
        resp.raise_for_status()
        time.sleep(self.pause_seconds)
        return resp.json()

    # ---------------------------------------------------------
    # 1) Listar jogos de uma época / competição
    # ---------------------------------------------------------
    def get_matches_by_season(self, season: str, league_id: int) -> List[MatchInfo]:
        """
        Obtém a lista de jogos de uma época para uma liga específica.

        :param season: ex: "2024-2025"
        :param league_id: ID interno da liga no Sofascore (a definir por ti)
        """
        # Placeholder de endpoint – ajustar ao real
        path = f"unique-tournament/{league_id}/season/{season}/events"
        data = self._get(path)

        matches: List[MatchInfo] = []

        # A estrutura abaixo depende do JSON real do Sofascore
        for ev in data.get("events", []):
            match_id = str(ev.get("id"))
            round_number = ev.get("round", {}).get("round", 0)
            home_team = ev.get("homeTeam", {}).get("name", "")
            away_team = ev.get("awayTeam", {}).get("name", "")
            home_score = ev.get("homeScore", {}).get("current")
            away_score = ev.get("awayScore", {}).get("current")
            date_ts = ev.get("startTimestamp")

            match_info = MatchInfo(
                match_id=match_id,
                season=season,
                round_number=round_number,
                date=str(date_ts),
                home_team=home_team,
                away_team=away_team,
                home_score=home_score,
                away_score=away_score,
            )
            matches.append(match_info)

        logger.info(f"Obtidos {len(matches)} jogos para season={season}, league_id={league_id}")
        return matches

    # ---------------------------------------------------------
    # 2) Estatísticas detalhadas de um jogo
    # ---------------------------------------------------------
    def get_match_stats(self, match_id: str) -> MatchStats:
        """
        Obtém estatísticas detalhadas de um jogo específico.

        :param match_id: ID do jogo no Sofascore
        """
        # Placeholder de endpoint – ajustar ao real
        path = f"event/{match_id}/statistics"
        data = self._get(path)

        # Aqui assumes que o JSON tem algo como:
        # { "statistics": [ { "period": "ALL", "groups": [ ... ] } ] }
        # Vais ter de mapear cada métrica para os campos do MatchStats.

        # Para já, vou deixar um parser simplificado com helpers
        stats_all = self._extract_all_period_stats(data)

        return MatchStats(
            # Principais
            xg_home=stats_all.get("xg_home", 0.0),
            xg_away=stats_all.get("xg_away", 0.0),
            possession_home=stats_all.get("possession_home", 0.0),
            possession_away=stats_all.get("possession_away", 0.0),
            shots_home=stats_all.get("shots_home", 0),
            shots_away=stats_all.get("shots_away", 0),
            shots_on_target_home=stats_all.get("shots_on_target_home", 0),
            shots_on_target_away=stats_all.get("shots_on_target_away", 0),
            big_chances_home=stats_all.get("big_chances_home", 0),
            big_chances_away=stats_all.get("big_chances_away", 0),
            corners_home=stats_all.get("corners_home", 0),
            corners_away=stats_all.get("corners_away", 0),
            passes_completed_home=stats_all.get("passes_completed_home", 0),
            passes_total_home=stats_all.get("passes_total_home", 0),
            passes_completed_away=stats_all.get("passes_completed_away", 0),
            passes_total_away=stats_all.get("passes_total_away", 0),
            yellow_cards_home=stats_all.get("yellow_cards_home", 0),
            yellow_cards_away=stats_all.get("yellow_cards_away", 0),

            # Remates detalhados
            xgot_home=stats_all.get("xgot_home", 0.0),
            xgot_away=stats_all.get("xgot_away", 0.0),
            shots_off_target_home=stats_all.get("shots_off_target_home", 0),
            shots_off_target_away=stats_all.get("shots_off_target_away", 0),
            shots_blocked_home=stats_all.get("shots_blocked_home", 0),
            shots_blocked_away=stats_all.get("shots_blocked_away", 0),
            shots_inside_box_home=stats_all.get("shots_inside_box_home", 0),
            shots_inside_box_away=stats_all.get("shots_inside_box_away", 0),
            shots_outside_box_home=stats_all.get("shots_outside_box_home", 0),
            shots_outside_box_away=stats_all.get("shots_outside_box_away", 0),
            hit_woodwork_home=stats_all.get("hit_woodwork_home", 0),
            hit_woodwork_away=stats_all.get("hit_woodwork_away", 0),
            headed_goals_home=stats_all.get("headed_goals_home", 0),
            headed_goals_away=stats_all.get("headed_goals_away", 0),

            # Ataque
            touches_in_box_home=stats_all.get("touches_in_box_home", 0),
            touches_in_box_away=stats_all.get("touches_in_box_away", 0),
            accurate_through_balls_home=stats_all.get("accurate_through_balls_home", 0),
            accurate_through_balls_away=stats_all.get("accurate_through_balls_away", 0),
            offsides_home=stats_all.get("offsides_home", 0),
            offsides_away=stats_all.get("offsides_away", 0),
            free_kicks_home=stats_all.get("free_kicks_home", 0),
            free_kicks_away=stats_all.get("free_kicks_away", 0),

            # Passes detalhados
            long_passes_completed_home=stats_all.get("long_passes_completed_home", 0),
            long_passes_total_home=stats_all.get("long_passes_total_home", 0),
            long_passes_completed_away=stats_all.get("long_passes_completed_away", 0),
            long_passes_total_away=stats_all.get("long_passes_total_away", 0),

            final_third_passes_completed_home=stats_all.get("final_third_passes_completed_home", 0),
            final_third_passes_total_home=stats_all.get("final_third_passes_total_home", 0),
            final_third_passes_completed_away=stats_all.get("final_third_passes_completed_away", 0),
            final_third_passes_total_away=stats_all.get("final_third_passes_total_away", 0),

            crosses_completed_home=stats_all.get("crosses_completed_home", 0),
            crosses_total_home=stats_all.get("crosses_total_home", 0),
            crosses_completed_away=stats_all.get("crosses_completed_away", 0),
            crosses_total_away=stats_all.get("crosses_total_away", 0),

            xa_home=stats_all.get("xa_home", 0.0),
            xa_away=stats_all.get("xa_away", 0.0),
            throw_ins_home=stats_all.get("throw_ins_home", 0),
            throw_ins_away=stats_all.get("throw_ins_away", 0),

            # Defesa
            fouls_home=stats_all.get("fouls_home", 0),
            fouls_away=stats_all.get("fouls_away", 0),
            tackles_won_home=stats_all.get("tackles_won_home", 0),
            tackles_total_home=stats_all.get("tackles_total_home", 0),
            tackles_won_away=stats_all.get("tackles_won_away", 0),
            tackles_total_away=stats_all.get("tackles_total_away", 0),
            duels_won_home=stats_all.get("duels_won_home", 0),
            duels_won_away=stats_all.get("duels_won_away", 0),
            clearances_home=stats_all.get("clearances_home", 0),
            clearances_away=stats_all.get("clearances_away", 0),
            interceptions_home=stats_all.get("interceptions_home", 0),
            interceptions_away=stats_all.get("interceptions_away", 0),
            errors_shot_home=stats_all.get("errors_shot_home", 0),
            errors_shot_away=stats_all.get("errors_shot_away", 0),
            errors_goal_home=stats_all.get("errors_goal_home", 0),
            errors_goal_away=stats_all.get("errors_goal_away", 0),

            # Guarda-redes
            saves_home=stats_all.get("saves_home", 0),
            saves_away=stats_all.get("saves_away", 0),
            xgot_faced_home=stats_all.get("xgot_faced_home", 0.0),
            xgot_faced_away=stats_all.get("xgot_faced_away", 0.0),
            goals_prevented_home=stats_all.get("goals_prevented_home", 0.0),
            goals_prevented_away=stats_all.get("goals_prevented_away", 0.0),
        )

    # ---------------------------------------------------------
    # 3) Helper para extrair estatísticas do JSON
    # ---------------------------------------------------------
    def _extract_all_period_stats(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converte o JSON de estatísticas do Sofascore num dicionário plano
        com as métricas que o MatchStats espera.

        Aqui vais mapear nomes como "Shots on target" → shots_on_target_home/away, etc.
        """
        stats_all: Dict[str, Any] = {}

        statistics = data.get("statistics", [])
        if not statistics:
            return stats_all

        # Normalmente há um bloco com period="ALL"
        all_period = next((s for s in statistics if s.get("period") == "ALL"), statistics[0])

        for group in all_period.get("groups", []):
            group_name = group.get("groupName", "").lower()

            for item in group.get("statisticsItems", []):
                name = item.get("name", "").lower()
                home_val = item.get("home", 0)
                away_val = item.get("away", 0)

                # Aqui fazes o mapping manual das métricas
                key_base = self._map_stat_name_to_key(name, group_name)
                if not key_base:
                    continue

                home_key = f"{key_base}_home"
                away_key = f"{key_base}_away"

                stats_all[home_key] = self._parse_value(home_val)
                stats_all[away_key] = self._parse_value(away_val)

        return stats_all

    def _map_stat_name_to_key(self, name: str, group_name: str) -> Optional[str]:
        """
        Mapeia o nome da estatística (em texto) para a chave interna usada em MatchStats.
        Aqui é onde ligas, por exemplo:
        - "shots on target" → "shots_on_target"
        - "total shots" → "shots"
        - "possession" → "possession"
        - etc.
        """
        n = name.lower()

        # Exemplos – vais afinando isto com base no JSON real
        if "expected goals (xg)" in n or n == "xg":
            return "xg"
        if "possession" in n:
            return "possession"
        if "total shots" in n or n == "shots":
            return "shots"
        if "shots on target" in n:
            return "shots_on_target"
        if "big chances" in n:
            return "big_chances"
        if "corners" in n:
            return "corners"
        if "passes" in n and "accurate" in n:
            return "passes_completed"
        if "passes" in n and "accurate" not in n:
            return "passes_total"
        if "yellow cards" in n:
            return "yellow_cards"
        if "xg on target" in n or "xgot" in n:
            return "xgot"
        if "shots off target" in n:
            return "shots_off_target"
        if "blocked shots" in n:
            return "shots_blocked"
        if "shots inside box" in n:
            return "shots_inside_box"
        if "shots outside box" in n:
            return "shots_outside_box"
        if "hit woodwork" in n or "hit post" in n:
            return "hit_woodwork"
        if "headed goals" in n:
            return "headed_goals"
        if "touches in opposition box" in n:
            return "touches_in_box"
        if "accurate through balls" in n:
            return "accurate_through_balls"
        if "offsides" in n:
            return "offsides"
        if "free kicks" in n:
            return "free_kicks"
        if "long balls accurate" in n:
            return "long_passes_completed"
        if "long balls" in n:
            return "long_passes_total"
        if "passes to final third accurate" in n:
            return "final_third_passes_completed"
        if "passes to final third" in n:
            return "final_third_passes_total"
        if "crosses accurate" in n:
            return "crosses_completed"
        if "crosses" in n:
            return "crosses_total"
        if "expected assists (xa)" in n or n == "xa":
            return "xa"
        if "throw-ins" in n:
            return "throw_ins"
        if "fouls" in n:
            return "fouls"
        if "tackles won" in n:
            return "tackles_won"
        if "tackles" in n:
            return "tackles_total"
        if "duels won" in n:
            return "duels_won"
        if "clearances" in n:
            return "clearances"
        if "interceptions" in n:
            return "interceptions"
        if "errors leading to shot" in n:
            return "errors_shot"
        if "errors leading to goal" in n:
            return "errors_goal"
        if "saves" in n:
            return "saves"
        if "xgot faced" in n:
            return "xgot_faced"
        if "goals prevented" in n:
            return "goals_prevented"

        return None

    def _parse_value(self, v: Any) -> float | int:
        """
        Converte valores que podem vir como '73%' ou '195/267' em números.
        """
        if isinstance(v, (int, float)):
            return v

        if isinstance(v, str):
            s = v.strip()
            if s.endswith("%"):
                try:
                    return float(s.replace("%", "").strip())
                except ValueError:
                    return 0
            if "/" in s:
                # Ex: "195/267" → poderás querer só o numerador ou ambos
                num, denom = s.split("/", 1)
                try:
                    return float(num.strip())
                except ValueError:
                    return 0
            try:
                return float(s)
            except ValueError:
                return 0

        return 0
