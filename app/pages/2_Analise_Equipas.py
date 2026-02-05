import streamlit as st
import pandas as pd
from pathlib import Path

from src.config.settings import RAW_DIR

st.title("📊 Análise de Equipas")

matches_path = Path(RAW_DIR) / "matches.csv"
stats_path = Path(RAW_DIR) / "match_stats.csv"

if not matches_path.exists() or not stats_path.exists():
    st.error("Faltam dados brutos. Corre update_data.py")
    st.stop()

matches = pd.read_csv(matches_path)
stats = pd.read_csv(stats_path)

teams = sorted(matches["home_team"].unique())
team = st.selectbox("Escolhe uma equipa", teams)

team_matches = matches[(matches["home_team"] == team) | (matches["away_team"] == team)]
team_stats = stats[stats["match_id"].isin(team_matches["match_id"])]

st.subheader(f"Jogos do {team}")
st.dataframe(team_matches)

st.subheader("Estatísticas agregadas")
agg = team_stats.mean(numeric_only=True)
st.dataframe(agg.to_frame("Média"))
