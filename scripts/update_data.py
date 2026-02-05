from src.data_ingestion.flashscore_match_list_scraper import FlashscoreMatchListScraper
from src.data_ingestion.match_collector import MatchCollector
import pandas as pd

def update_data():
    match_list_scraper = FlashscoreMatchListScraper()
    collector = MatchCollector()

    matches = match_list_scraper.get_next_round_matches()

    rows = []
    for m in matches:
        stats = collector.collect_stats(
            flash_url=m["flash_url"],
            sofa_url=None  # podemos mapear automaticamente mais tarde
        )

        rows.append({
            "home_team": m["home_team"],
            "away_team": m["away_team"],
            "flash_url": m["flash_url"],
            **stats
        })

    df = pd.DataFrame(rows)
    df.to_csv("data/raw/match_stats.csv", index=False)

if __name__ == "__main__":
    update_data()
