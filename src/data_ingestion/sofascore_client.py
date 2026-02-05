import requests
from bs4 import BeautifulSoup
import json

class SofascoreScraper:
    BASE_URL = "https://www.sofascore.com"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.sofascore.com/"
    }

    def get_match_stats(self, match_url: str) -> dict:
        """
        Extrai estatísticas do JSON interno __NEXT_DATA__ do Sofascore.
        match_url é o caminho relativo, ex: '/porto-benfica/xxxxxx'
        """
        url = self.BASE_URL + match_url
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        script = soup.find("script", id="__NEXT_DATA__")

        if not script:
            return {}

        try:
            data = json.loads(script.text)
        except:
            return {}

        try:
            stats = data["props"]["pageProps"]["event"]["statistics"]
        except KeyError:
            return {}

        parsed = {}
        for group in stats:
            for item in group["statisticsItems"]:
                key = item["name"].lower().replace(" ", "_")
                parsed[key] = {
                    "home": item.get("home"),
                    "away": item.get("away")
                }

        return parsed
