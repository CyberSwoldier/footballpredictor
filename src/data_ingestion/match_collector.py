from src.data_ingestion.flashscore_scraper import FlashscoreScraper
from src.data_ingestion.sofascore_scraper import SofascoreScraper

class MatchCollector:
    def __init__(self):
        self.flash = FlashscoreScraper()
        self.sofa = SofascoreScraper()

    def collect_match_stats(self, flash_url: str, sofa_url: str) -> dict:
        """
        flash_url: caminho relativo do Flashscore
        sofa_url: caminho relativo do Sofascore
        """

        # 1) Flashscore primeiro
        try:
            stats = self.flash.get_match_stats(flash_url)
        except Exception:
            stats = {}

        # 2) Sofascore como fallback
        try:
            sofa_stats = self.sofa.get_match_stats(sofa_url)
        except Exception:
            sofa_stats = {}

        # 3) Combinar (Sofascore sobrescreve Flashscore)
        combined = {**stats, **sofa_stats}

        return combined
