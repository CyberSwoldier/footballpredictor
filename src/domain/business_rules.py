from dataclasses import dataclass
from typing import Literal

from src.domain.schemas import MatchPrediction


@dataclass
class BettingSignal:
    match_id: str
    home_team: str
    away_team: str
    market: str
    suggestion: Literal["over", "under", "none"]
    rationale: str


def derive_corners_signal(pred: MatchPrediction, line: float = 9.5) -> BettingSignal:
    """
    Exemplo de regra de negócio:
    - se cantos esperados totais > line + margem → over
    - se < line - margem → under
    - caso contrário → none
    """
    total_corners = pred.predicted_corners_home + pred.predicted_corners_away
    margin = 1.0

    if total_corners > line + margin:
        suggestion = "over"
        rationale = f"Total esperado de cantos ({total_corners:.2f}) acima da linha {line}"
    elif total_corners < line - margin:
        suggestion = "under"
        rationale = f"Total esperado de cantos ({total_corners:.2f}) abaixo da linha {line}"
    else:
        suggestion = "none"
        rationale = f"Total esperado de cantos ({total_corners:.2f}) próximo da linha {line}"

    return BettingSignal(
        match_id=pred.match_id,
        home_team=pred.home_team,
        away_team=pred.away_team,
        market=f"Total Cantos {line}",
        suggestion=suggestion,
        rationale=rationale,
    )
