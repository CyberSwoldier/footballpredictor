import sys
import os

# Adiciona a raiz do projeto ao PYTHONPATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

import streamlit as st
import pandas as pd
from pathlib import Path

from src.config.settings import PREDICTIONS_DIR

st.set_page_config(
    page_title="Football Predictor – Primeira Liga",
    layout="wide"
)

# CSS
with open("app/assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("⚽ Football Predictor – Primeira Liga Portuguesa")
st.subheader("Previsões estatísticas baseadas em Machine Learning")

pred_path = Path(PREDICTIONS_DIR) / "predictions_next_round.csv"

if pred_path.exists():
    df = pd.read_csv(pred_path)
    st.success("Previsões da próxima jornada carregadas com sucesso")
    st.dataframe(df)
else:
    st.warning("Ainda não existem previsões. Gera-as com o script generate_predictions.py")

st.markdown("---")
st.markdown("Navega pelas páginas à esquerda para explorar análises detalhadas.")
