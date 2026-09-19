from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from nucleo import simulacao as sim
from nucleo.minhastats import media

NUMERICAS = [
    "age", "height_cm", "weight_kg", "body fat_%", "diastolic",
    "systolic", "gripForce", "sit and bend forward_cm",
    "sit-ups counts", "broad jump_cm",
]


def _view_lgn():
    st.subheader("Experimento A — Lei dos Grandes Números")
    st.markdown(
        "A frequência relativa de um evento converge para sua probabilidade "
        "teórica conforme o número de experimentos cresce."
    )
    experimento = st.radio("Experimento", ["Dado (p = 1/6 ≈ 0,1667)", "Moeda (p = 0,5)"],
                           horizontal=True)
    p = 1 / 6 if "Dado" in experimento else 0.5
    n = st.slider("Número de lançamentos", 100, 100_000, 10_000, step=100)
    seed = st.number_input("Semente (reprodutibilidade)", value=42, step=1)

    out = sim.frequencias_relativas_acumuladas(int(n), p, seed=int(seed))
    resumo = sim.convergencia_lgn(int(n), p, seed=int(seed))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=out["tamanhos"], y=out["frequencias"],
                             mode="lines", name="frequência relativa acumulada"))
    fig.add_hline(y=p, line_dash="dash", line_color="red",
                  annotation_text=f"P(valor) = {p:.4f}")
    fig.update_xaxes(type="log")
    fig.update_layout(title="Frequência relativa × nº de lançamentos (eixo log)",
                      xaxis_title="Lançamentos", yaxis_title="Frequência relativa")
    st.plotly_chart(fig, width="stretch")

    st.success(
        f"Após **{n:,} lançamentos**, a frequência relativa foi "
        f"**{resumo['frequencia_relativa_final']:.4f}**, contra o valor teórico "
        f"{resumo['esperado']:.4f} (diferença de {resumo['diferenca']:.4f}). "
        "Nenhuma sequência curta garante o valor teórico — o LGN só vale "
        "\"no limite\", com muitos experimentos."
    )


def _view_tcl(df: pd.DataFrame):
    st.subheader("Experimento B — Teorema Central do Limite")
    st.markdown(
        "Sorteamos repetidamente amostras de uma variável do dataset e olhamos "
        "a **distribuição das médias amostrais**. Pelo TCL, ela se aproxima de "
        "uma Normal com média = μ e desvio = σ/√n à medida que o tamanho da "
        "amostra cresce."
    )
    var = st.selectbox("Variável do dataset", NUMERICAS)
    x = df[var].astype(float)
    r = st.slider("Nº de repetições (amostras)", 100, 5_000, 1_000, step=100)
    n = st.slider("Tamanho da amostra (n)", 1, 50, 30)
    seed = st.number_input("Semente", value=7, step=1)

    mus = sim.medias_amostrais_repetidas(x, int(r), int(n), seed=int(seed))
    resumo = sim.resumo_tcl(x, int(r), int(n), seed=int(seed))

    fig = px.histogram(mus, nbins=30,
                       labels={"value": "média amostral", "count": "frequência"})
    fig.update_layout(title=f"Distribuição das médias de {r:,} amostras (n = {n})",
                      showlegend=False)

    # Normal teórica do TCL sobreposta: N(mu_pop, sigma_pop^2 / n)
    mu_t = float(media(x))
    sigma_t = resumo["sd_teorica"]
    xs = np.linspace(mus.min(), mus.max(), 200)
    pdf = (1 / (sigma_t * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((xs - mu_t) / sigma_t) ** 2)
    fig.add_trace(go.Scatter(x=xs, y=pdf * r * (mus.max() - mus.min()) / 30,
                             mode="lines", name="Normal: N(μ, σ²/n)"))
    st.plotly_chart(fig, width="stretch")

    st.info(
        f"Média das medias amostrais = **{resumo['media_medias']:.4f}** "
        f"(população: {resumo['mu_populacao']:.4f}) — convergência de μ ✓\n\n"
        f"DP das médias = **{resumo['dp_medias']:.4f}** contra o teórico σ/√n = "
        f"**{resumo['sd_teorica']:.4f}** — convergência do desvio. "
        "Com **n = 1** a distribuição tem a forma original da variável; "
        "conforme **n** cresce, a forma se aproxima da Normal (TCL)."
    )


def render(df: pd.DataFrame):
    st.header("Módulo 3 — Probabilidade e Simulação (Monte Carlo)")
    aba = st.radio("Experimento", ["Lei dos Grandes Números",
                                   "Teorema Central do Limite"], horizontal=True)
    if "Lei" in aba:
        _view_lgn()
    else:
        _view_tcl(df)