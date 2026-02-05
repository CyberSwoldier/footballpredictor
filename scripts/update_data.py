from src.data_ingestion.match_collector import MatchCollector
import pandas as pd

def update_data():
    collector = MatchCollector()

    # Aqui tens de fornecer a lista de jogos:
    # flash_url e sofa_url para cada jogo
    # (posso automatizar isto também)

    matches = [
        {
            "match_id": "porto-benfica",
            "flash_url": "/jogo/xxxxxx/#/resumo-de-jogo/estatisticas-de-jogo/0",
            "sofa_url": "/porto-benfica/xxxxxx"
        }
    ]

    rows = []
    for m in matches:
        stats = collector.collect_match_stats(m["flash_url"], m["sofa_url"])
        rows.append({"match_id": m["match_id"], **stats})

    df = pd.DataFrame(rows)
    df.to_csv("data/raw/match_stats.csv", index=False)

if __name__ == "__main__":
    update_data()
