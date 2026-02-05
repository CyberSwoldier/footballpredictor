import requests
from bs4 import BeautifulSoup

class FlashscoreMatchListScraper:
    BASE_URL = "https://www.flashscore.pt"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "pt-PT,pt;q=0.9"
    }

    def get_next_round_matches(self):
        url = f"{self.BASE_URL}/futebol/portugal/primeira-liga/calendario/"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        rounds = soup.select(".event__round")
        matches = soup.select(".event__match")

        # Encontrar a primeira jornada futura (sem resultado)
        next_round_id = None
        for r in rounds:
            if "event__round--scheduled" in r.get("class", []):
                next_round_id = r.text.strip()
                break

        if not next_round_id:
            return []

        round_matches = []
        for m in matches:
            if next_round_id in m.get("class", []):
                link = m.find("a", href=True)
                if not link:
                    continue

                flash_url = link["href"]
                home = m.select_one(".event__participant--home").text.strip()
                away = m.select_one(".event__participant--away").text.strip()

                round_matches.append({
                    "home_team": home,
                    "away_team": away,
                    "flash_url": flash_url
                })

        return round_matches
