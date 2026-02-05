import requests
from bs4 import BeautifulSoup

class FlashscoreScraper:
    BASE_URL = "https://www.flashscore.pt"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "pt-PT,pt;q=0.9"
    }

    def get_match_stats(self, match_url: str) -> dict:
        """
        Extrai estatísticas de um jogo do Flashscore.
        match_url é o caminho relativo, ex: '/jogo/xxxxxx/#/resumo-de-jogo/estatisticas-de-jogo/0'
        """
        url = self.BASE_URL + match_url
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        stats = {}

        for row in soup.select(".stat__row"):
            category = row.select_one(".stat__category")
            home = row.select_one(".stat__homeValue")
            away = row.select_one(".stat__awayValue")

            if category and home and away:
                key = category.text.strip().lower().replace(" ", "_")
                stats[key] = {
                    "home": self._safe_int(home.text),
                    "away": self._safe_int(away.text)
                }

        return stats

    def _safe_int(self, value):
        try:
            return int(value)
        except:
            return None
