from dataclasses import dataclass
from typing import Optional, Dict, Any


# ============================================================
# 1. Representação básica de um jogo (informação bruta)
# ============================================================

@dataclass
class MatchInfo:
    match_id: str
    season: str
    round_number: int
    date: str
    home_team: str
    away_team: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None


# ============================================================
# 2. Estatísticas completas do jogo (raw → processed)
# ============================================================

@dataclass
class MatchStats:
    # Principais
    xg_home: float
    xg_away: float
    possession_home: float
    possession_away: float
    shots_home: int
    shots_away: int
    shots_on_target_home: int
    shots_on_target_away: int
    big_chances_home: int
    big_chances_away: int
    corners_home: int
    corners_away: int
    passes_completed_home: int
    passes_total_home: int
    passes_completed_away: int
    passes_total_away: int
    yellow_cards_home: int
    yellow_cards_away: int

    # Remates detalhados
    xgot_home: float
    xgot_away: float
    shots_off_target_home: int
    shots_off_target_away: int
    shots_blocked_home: int
    shots_blocked_away: int
    shots_inside_box_home: int
    shots_inside_box_away: int
    shots_outside_box_home: int
    shots_outside_box_away: int
    hit_woodwork_home: int
    hit_woodwork_away: int
    headed_goals_home: int
    headed_goals_away: int

    # Ataque
    touches_in_box_home: int
    touches_in_box_away: int
    accurate_through_balls_home: int
    accurate_through_balls_away: int
    offsides_home: int
    offsides_away: int
    free_kicks_home: int
    free_kicks_away: int

    # Passes detalhados
    long_passes_completed_home: int
    long_passes_total_home: int
    long_passes_completed_away: int
    long_passes_total_away: int

    final_third_passes_completed_home: int
    final_third_passes_total_home: int
    final_third_passes_completed_away: int
    final_third_passes_total_away: int

    crosses_completed_home: int
    crosses_total_home: int
    crosses_completed_away: int
    crosses_total_away: int

    xa_home: float
    xa_away: float
    throw_ins_home: int
    throw_ins_away: int

    # Defesa
    fouls_home: int
    fouls_away: int
    tackles_won_home: int
    tackles_total_home: int
    tackles_won_away: int
    tackles_total_away: int
    duels_won_home: int
    duels_won_away: int
    clearances_home: int
    clearances_away: int
    interceptions_home: int
    interceptions_away: int
    errors_shot_home: int
    errors_shot_away: int
    errors_goal_home: int
    errors_goal_away: int

    # Guarda-redes
    saves_home: int
    saves_away: int
    xgot_faced_home: float
    xgot_faced_away: float
    goals_prevented_home: float
    goals_prevented_away: float


# ============================================================
# 3. Features para Machine Learning
# ============================================================

@dataclass
class MatchFeatures:
    match_id: str
    home_team: str
    away_team: str

    # Features agregadas (exemplos)
    home_avg_corners: float
    away_avg_corners: float
    home_avg_shots: float
    away_avg_shots: float
    home_avg_yellow_cards: float
    away_avg_yellow_cards: float
    home_avg_xg: float
    away_avg_xg: float

    # Forma recente
    home_form_last5: float
    away_form_last5: float

    # Casa/Fora
    home_home_performance: float
    away_away_performance: float

    # Diferenças entre equipas
    delta_corners: float
    delta_shots: float
    delta_xg: float
    delta_yellow_cards: float

    # Qualquer feature adicional
    extra: Optional[Dict[str, Any]] = None


# ============================================================
# 4. Previsões geradas pelos modelos
# ============================================================

@dataclass
class MatchPrediction:
    match_id: str
    home_team: str
    away_team: str

    predicted_corners_home: float
    predicted_corners_away: float

    predicted_shots_home: float
    predicted_shots_away: float

    predicted_yellow_cards_home: float
    predicted_yellow_cards_away: float

    predicted_xg_home: float
    predicted_xg_away: float

    # Intervalos de confiança (opcional)
    confidence_low: Optional[Dict[str, float]] = None
    confidence_high: Optional[Dict[str, float]] = None
