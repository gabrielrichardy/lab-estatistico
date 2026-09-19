from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from nucleo import distribuicoes as dist
from nucleo.minhastats import resumo_completo

NUMERICAS = [
    "age", "height_cm", "weight_kg", "body fat_%", "diastolic",
    "systolic", "gripForce", "sit and bend forward_cm",
    "sit-ups counts", "broad jump_cm",
]


def render(df: pd.DataFrame):
    st.header("Módulo 4 — Distribuições Teóricas")
    st.markdown(
        "Sobreposição ao histograma (densidade) de uma curva teórica com "
        "parâmetros **estimados dos próprios dados** pela biblioteca própria "
        "(`nucleo/distribuicoes.py`)."
    )

    var = st.selectbox("Variável numérica", NUMERICAS)
    x = df[var].astype(float)
    r = resumo_completo(x)

    r2 = st.columns(2)
    com_normal = r2[0].checkbox("Sobrepor curva Normal", value=True)
    segunda = r2[1].selectbox(
        "2ª distribuição candidata",
        ["Exponencial", "Uniforme"],
    )

    bin_min = float(np.min(x))
    bin_max = float(np.max(x))
    grade = np.linspace(bin_min, bin_max, 400)

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=list(x), histnorm="probability density", nbinsx=40,
        name="dados", opacity=0.55,
    ))

    candidatas = []
    if com_normal:
        candidatas.append("Normal")
    if x.min() >= 0 or segunda != "Exponencial":
        candidatas.append(segunda)
    elif segunda == "Exponencial":
        st.warning("Exponencial exige dados ≥ 0; usando Uniforme.")
        candidatas.append("Uniforme")

    for nome in candidatas:
        ys = dist.curva_para_variavel(x, nome, grade.tolist())
        cor = "red" if nome == "Normal" else "darkorange"
        fig.add_trace(go.Scatter(x=grade, y=ys, mode="lines",
                                 name=f"{nome} (parâmetros estimados)",
                                 line=dict(color=cor, width=2.5)))

    est = st.expander("Parâmetros estimados dos dados", expanded=False)
    with est:
        for nome in candidatas:
            p = (dist.estimar_normal(x) if nome == "Normal"
                 else dist.estimar_exponencial(x) if nome == "Exponencial"
                 else dist.estimar_uniforme(x))
            est.markdown(f"**{nome}**: " + ", ".join(f"{k} = {v:.4g}" for k, v in p.items()))

    fig.update_layout(title=f"Histograma de '{var}' e curvas teóricas",
                      xaxis_title=var, yaxis_title="densidade")
    st.plotly_chart(fig, width="stretch")

    _discutir_ajuste(var, r)


def _discutir_ajuste(var: str, r: dict):
    media, mediana, q1, q3 = r["media"], r["mediana"], r["Q1"], r["Q3"]
    if abs(media - mediana) < 0.05 * r["desvio_padrao"]:
        traco = "simétrica"
        conclusao = "a Normal tende a acompanhar bem o pico e as caudas."
    elif media > mediana:
        traco = "assimétrica à direita"
        conclusao = "o ajuste Normal costuma subestimar a cauda direita; distribuições assimétricas (Exponencial) acompanham melhor."
    else:
        traco = "assimétrica à esquerda"
        conclusao = "o ajuste Normal tende a perder a cauda esquerda; veja qual curva acompanha melhor o pico."

    st.markdown(
        f"**Leitura visual do ajuste:** com média {media:.3g} e mediana "
        f"{mediana:.3g} (Q1 = {q1:.3g}, Q3 = {q3:.3g}), a distribuição de "
        f"'{var}' é **{traco}** — portanto {conclusao}\n\n"
        "Esta é uma **inspeção visual** da qualidade do ajuste, como pede o "
        "módulo. Um teste formal (Kolmogorov–Smirnov) pode ser adicionado como "
        "bônus."
    )

    st.caption(
        "Quanto mais próxima a curva teórica estiver do contorno das barras, "
        "melhor o modelo descreve os dados. Deslocamentos no pico ou nas caudas "
        "indicam onde a distribuição teórica falha."
    )