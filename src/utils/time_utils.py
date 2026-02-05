from datetime import datetime
from typing import Union


def parse_timestamp(ts: Union[int, float, str]) -> str:
    """
    Converte timestamps (epoch ou string) para ISO8601 (YYYY-MM-DD).
    """
    if isinstance(ts, (int, float)):
        return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")
    if isinstance(ts, str):
        try:
            # tenta epoch em string
            if ts.isdigit():
                return datetime.utcfromtimestamp(int(ts)).strftime("%Y-%m-%d")
            # tenta ISO direto
            return datetime.fromisoformat(ts).strftime("%Y-%m-%d")
        except Exception:
            return ts
    return str(ts)
