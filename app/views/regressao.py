from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from nucleo import regressao as rg

NUMERICAS = [
    "age", "height_cm", "weight_kg", "body fat_%", "diastolic",
    "systolic", "gripForce", "sit and bend forward_cm",
    "sit-ups counts", "broad jump_cm",
]


def render(df: pd.DataFrame):
    st.header("Módulo 5 — Correlação e Regressão Linear (mínimos quadrados)")

    c1, c2 = st.columns(2)
    x_var = c1.selectbox("Variável X (independente)", NUMERICAS, index=1)
    restantes = [v for v in NUMERICAS if v != x_var]
    y_var = c2.selectbox("Variável Y (dependente)", restantes, index=2)

    x = df[x_var].astype(float)
    y = df[y_var].astype(float)

    res = rg.regressao_linear(x.tolist(), y.tolist())

    # ----- diagrama de dispersao + reta -----------------------------------
    x_lin = np.linspace(float(x.min()), float(x.max()), 200)
    y_lin = rg.prever_valores(x_lin, res["alpha"], res["beta"])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name="observações",
                             marker=dict(size=3, opacity=0.35)))
    fig.add_trace(go.Scatter(x=x_lin, y=y_lin, mode="lines", name="reta OLS",
                             line=dict(color="red", width=3)))
    fig.update_layout(title=f"y = {res['equacao']}",
                      xaxis_title=x_var, yaxis_title=y_var)
    st.plotly_chart(fig, width="stretch")

    # ----- cartao de coeficientes ------------------------------------------
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("α (intercepto)", f"{res['alpha']:.4g}")
    c2.metric("β (coeficiente angular)", f"{res['beta']:.4g}")
    c3.metric("r de Pearson", f"{res['r']:.4f}")
    c4.metric("R²", f"{res['r2']:.4f}")

    st.markdown(
        f"**Equação da reta:** `{res['equacao']}`  \n"
        f"**Interpretação:** {res['interpretacao_efeito']}. "
        f"{res['interpretacao_correlacao']}. {res['interpretacao_r2']}."
    )

    st.subheader("Predição interativa")
    x_novo = st.number_input(f"Digite um valor de X ({x_var}):",
                             value=float(x.median()), step=0.5, format="%.2f")
    y_hat = rg.prever(x_novo, res["alpha"], res["beta"])
    st.success(f"Para {x_var} = {x_novo:g}, o modelo prevê **{y_var} = {y_hat:.4g}**.")

    st.warning(
        "**⚠️ Correlação não implica causalidade.** O fato de duas variáveis "
        "andarem juntas (r alto) não significa que uma causa a outra. Pode haver "
        "uma terceira variável influenciando ambas (ex.: idade)."
    )