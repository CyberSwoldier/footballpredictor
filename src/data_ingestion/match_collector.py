from src.data_ingestion.flashscore_scraper import FlashscoreScraper
from src.data_ingestion.sofascore_scraper import SofascoreScraper

class MatchCollector:
    def __init__(self):
        self.flash = FlashscoreScraper()
        self.sofa = SofascoreScraper()

    def collect_stats(self, flash_url: str, sofa_url: str | None = None):
        # Flashscore primeiro
        try:
            stats = self.flash.get_match_stats(flash_url)
        except:
            stats = {}

        # Sofascore fallback
        if sofa_url:
            try:
                sofa_stats = self.sofa.get_match_stats(sofa_url)
                stats.update(sofa_stats)
            except:
                pass

        return stats
