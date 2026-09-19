from __future__ import annotations

import math

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from nucleo import minhastats as ms

NUMERICAS = [
    "age", "height_cm", "weight_kg", "body fat_%", "diastolic",
    "systolic", "gripForce", "sit and bend forward_cm",
    "sit-ups counts", "broad jump_cm",
]
CATEGORICAS = ["gender", "class"]


def _interpretar_automatico(r: dict, var: str) -> str:
    """Gera o paragrafo de interpretacao a partir das medidas calculadas."""
    media, mediana = r["media"], r["mediana"]
    if abs(media - mediana) < 0.05 * r["desvio_padrao"]:
        assimetria = (
            f"a media ({media:.3g}) praticamente coincide com a mediana "
            f"({mediana:.3g}), indicando distribuicao aproximadamente simetrica."
        )
    elif media > mediana:
        assimetria = (
            f"a media ({media:.3g}) e MAIOR que a mediana ({mediana:.3g}), "
            f"caracteristico de assimetria a DIREITA (cauda longa para valores altos)."
        )
    else:
        assimetria = (
            f"a media ({media:.3g}) e MENOR que a mediana ({mediana:.3g}), "
            f"caracteristico de assimetria a ESQUERDA (cauda longa para valores baixos)."
        )

    if r["coeficiente_variacao"] != r["coeficiente_variacao"]:
        cv_txt = "CV nao calculavel (media nula)."
    elif r["coeficiente_variacao"] < 15:
        cv_txt = f"CV de {r['coeficiente_variacao']:.2f}% indica dispersao relativa baixa."
    elif r["coeficiente_variacao"] < 40:
        cv_txt = f"CV de {r['coeficiente_variacao']:.2f}% indica dispersao relativa moderada."
    else:
        cv_txt = f"CV de {r['coeficiente_variacao']:.2f}% indica dispersao relativa ALTA."

    moda_txt = (
        f"modal{'' if len(r['moda']) == 1 else 'es':} {', '.join(f'{m:g}' for m in r['moda'])}"
        if r["moda"]
        else "sem moda (todos os valores com frequencia 1)"
    )

    return (
        f"**Sobre '{var}':** {assimetria} "
        f"{cv_txt} A moda e {moda_txt}. "
        f"Pela regra do IQR (1.5x), foram detectados **{r['n_outliers']} outliers** "
        f"(abaixo de {r['limite_inferior']:.3g} ou acima de {r['limite_superior']:.3g})."
    )


def _painel_medidas(r: dict):
    st.subheader("Medidas calculadas pela biblioteca própria (`minhastats`)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Média", f"{r['media']:.4g}")
    c1.metric("Mediana", f"{r['mediana']:.4g}")
    c1.metric("Moda", ", ".join(f"{m:g}" for m in r["moda"]) if r["moda"] else "—")
    c2.metric("Amplitude", f"{r['amplitude']:.4g}")
    c2.metric("Variância (amostral)", f"{r['variancia_amostral']:.4g}")
    c2.metric("Variância (populacional)", f"{r['variancia_populacional']:.4g}")
    c3.metric("Desvio padrão", f"{r['desvio_padrao']:.4g}")
    c3.metric("CV (%)", f"{r['coeficiente_variacao']:.4g}")
    c3.metric("Q1 / Q3", f"{r['Q1']:.4g} / {r['Q3']:.4g}")
    c4.metric("IQR", f"{r['IQR']:.4g}")
    c4.metric("n", f"{r['n']:,}")
    c4.metric("Outliers (IQR)", f"{r['n_outliers']}")


def render(df: pd.DataFrame):
    st.header("Módulo 2 — Estatística Descritiva Interativa")

    tipo = st.radio("Tipo de variável", ["Numérica", "Categórica"], horizontal=True)

    if tipo == "Categórica":
        var = st.selectbox("Variável categórica", CATEGORICAS)
        rotulos = df[var].astype(str).tolist()
        tab = ms.tabela_frequencias_categorica(rotulos)
        st.subheader("Tabela de frequências")
        st.dataframe(pd.DataFrame(tab), width="stretch")
        col1, col2 = st.columns(2)
        fig_b = px.bar(x=[t["categoria"] for t in tab],
                       y=[t["frequencia"] for t in tab],
                       labels={"x": var, "y": "Frequência"})
        fig_b.update_layout(showlegend=False)
        col1.plotly_chart(fig_b, width="stretch")
        fig_p = px.pie(names=[t["categoria"] for t in tab],
                       values=[t["frequencia"] for t in tab], hole=0.4)
        col2.plotly_chart(fig_p, width="stretch")
        max_txt = f"A categoria com maior frequência é **{tab[0]['categoria']}**, com {tab[0]['frequencia']:,} registros ({tab[0]['frequencia_relativa_%']:.1f}%)."
        st.info(max_txt)
        return

    var = st.selectbox("Variável numérica", NUMERICAS)
    x = df[var].astype(float)

    r = ms.resumo_completo(x)
    _painel_medidas(r)

    k = math.ceil(math.log2(r["n"])) + 1
    linhas = ms.tabela_frequencias_classes(x, k=k)
    st.subheader(f"Tabela de frequências com {k} classes (regra de Sturges)")
    st.dataframe(pd.DataFrame(linhas), width="stretch")

    c1, c2 = st.columns(2)
    fig_h = px.histogram(x, nbins=k, marginal="rug",
                         labels={"value": var, "count": "Frequência"})
    fig_h.update_layout(title="Histograma", showlegend=False)
    c1.plotly_chart(fig_h, width="stretch")

    fig_b = go.Figure()
    fig_b.add_trace(go.Box(
        y=x.tolist(), name=var,
        boxpoints="outliers", marker_color="tomato",
    ))
    fig_b.update_layout(title="Boxplot (whiskers = 1.5×IQR)", showlegend=False)
    c2.plotly_chart(fig_b, width="stretch")

    if r["outliers"]:
        st.warning(f"Valores fora do limite 1.5×IQR: {', '.join(f'{v:g}' for v in sorted(r['outliers'])[:12])}{'...' if len(r['outliers']) > 12 else ''}")
    st.success(_interpretar_automatico(r, var))