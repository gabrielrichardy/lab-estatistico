"""Laboratorio Estatistico Interativo — aplicacao Streamlit.

Execucao (na raiz do projeto):
    pip install -r requirements.txt
    streamlit run app/app.py

O nucleo matematico vive em nucleo/ (biblioteca propria); esta interface
apenas consome as funcoes de lá.
"""

from __future__ import annotations

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_CSV = os.path.join(RAIZ, "data", "bodyPerformance.csv")

if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

import pandas as pd
import streamlit as st

from views import descritiva, probabilidade, distribuicoes, regressao


@st.cache_data(show_spinner=False)
def carregar_dados(caminho: str) -> pd.DataFrame:
    return pd.read_csv(caminho).dropna()


def main():
    st.set_page_config(page_title="Laboratório Estatístico", layout="wide")

    df = carregar_dados(CAMINHO_CSV)

    st.sidebar.title("🧮 Laboratório Estatístico")
    n_registros = f"{df.shape[0]:,}".replace(",", ".")
    st.sidebar.caption(
        f"Body Performance Data — {n_registros} registros, "
        f"{df.shape[1]} variáveis (dataset real: Kaggle)."
    )

    modulo = st.sidebar.radio(
        "Módulos",
        [
            "Home",
            "2 — Estatística Descritiva",
            "3 — Probabilidade e Simulação",
            "4 — Distribuições Teóricas",
            "5 — Correlação e Regressão",
        ],
    )

    if modulo == "Home":
        st.title("🧮 Laboratório Estatístico Interativo")
        st.markdown(
            f"""
            Este projeto implementa **do zero** o núcleo matemático de um
            laboratório estatístico e o valida contra NumPy/SciPy
            (tolerância 1e-10), tudo dentro de uma interface Streamlit.

            **Dataset:** Body Performance Data — {n_registros} registros
            sobre desempenho físico, com {df.shape[1]} variáveis.

            **Módulos:**
            - **2 — Descritiva:** medidas próprias, tabelas de frequência,
              histograma/boxplot, outliers (IQR) e interpretação automática.
            - **3 — Simulação:** Lei dos Grandes Números e Teorema Central
              do Limite via Monte Carlo com parâmetros controláveis.
            - **4 — Distribuições:** curvas teóricas sobre o histograma com
              parâmetros estimados dos dados.
            - **5 — Regressão:** mínimos quadrados implementados à mão, R² e
              predição interativa.
            """
        )
        st.sidebar.success("Escolha um módulo no menu.")
        return

    df_numericas = df[descritiva.NUMERICAS].astype(float)

    if modulo == "2 — Estatística Descritiva":
        descritiva.render(df)
    elif modulo == "3 — Probabilidade e Simulação":
        probabilidade.render(df_numericas)
    elif modulo == "4 — Distribuições Teóricas":
        distribuicoes.render(df_numericas)
    else:
        regressao.render(df_numericas)


if __name__ == "__main__":
    main()