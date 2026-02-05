import streamlit as st
import pandas as pd
from pathlib import Path

from src.config.settings import PREDICTIONS_DIR

st.title("📅 Próxima Jornada – Previsões")

pred_path = Path(PREDICTIONS_DIR) / "predictions_next_round.csv"

if not pred_path.exists():
    st.error("Ainda não existem previsões. Corre generate_predictions.py")
    st.stop()

df = pd.read_csv(pred_path)

for _, row in df.iterrows():
    st.markdown(f"### {row['home_team']} vs {row['away_team']}")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Cantos (Casa)", f"{row['predicted_corners_home']:.2f}")
        st.metric("Remates (Casa)", f"{row['predicted_shots_home']:.2f}")
        st.metric("Cartões (Casa)", f"{row['predicted_yellow_cards_home']:.2f}")

    with col2:
        st.metric("Cantos (Fora)", f"{row['predicted_corners_away']:.2f}")
        st.metric("Remates (Fora)", f"{row['predicted_shots_away']:.2f}")
        st.metric("Cartões (Fora)", f"{row['predicted_yellow_cards_away']:.2f}")

    st.markdown("---")
