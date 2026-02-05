import streamlit as st
import pandas as pd
from pathlib import Path

from src.config.settings import RAW_DIR

st.title("📚 Estatísticas Históricas da Liga")

matches_path = Path(RAW_DIR) / "matches.csv"
stats_path = Path(RAW_DIR) / "match_stats.csv"

if not matches_path.exists() or not stats_path.exists():
    st.error("Faltam dados brutos. Corre update_data.py")
    st.stop()

matches = pd.read_csv(matches_path)
stats = pd.read_csv(stats_path)

st.subheader("Jogos")
st.dataframe(matches)

st.subheader("Estatísticas")
st.dataframe(stats)
