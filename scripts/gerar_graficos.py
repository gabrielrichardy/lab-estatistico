import os
import math
import sys

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from nucleo import minhastats as ms
from nucleo import simulacao as sim
from nucleo import distribuicoes as dist
from nucleo import regressao as rg

ASSETS = os.path.join(RAIZ, "assets")
df = pd.read_csv(os.path.join(RAIZ, "data", "bodyPerformance.csv")).dropna()
NUM = ["age", "height_cm", "weight_kg", "body fat_%", "diastolic", "systolic",
       "gripForce", "sit and bend forward_cm", "sit-ups counts", "broad jump_cm"]
FIG = dict(width=1100, height=460)


def salvar(fig, nome):
    fig.update_layout(title_font_size=20, font=dict(size=14))
    pio.write_image(fig, os.path.join(ASSETS, nome), scale=2)
    print("ok", nome)


# M2 - histograma altura (Sturges) -------------------------------------------
x = df["height_cm"].astype(float)
k = math.ceil(math.log2(len(x))) + 1
fig = px.histogram(x, nbins=k, marginal="rug", labels={"value": "height_cm", "count": "Frequência"})
fig.update_layout(title=f"Histograma de height_cm ({k} classes, Sturges)", **FIG)
salvar(fig, "m2_histograma_altura.png")

# M2 - boxplot peso com outliers IQR -----------------------------------------
r = ms.resumo_completo(df["weight_kg"].astype(float))
fig = go.Figure()
fig.add_trace(go.Box(y=df["weight_kg"], name="weight_kg", boxpoints="outliers"))
fig.update_layout(title=f"Boxplot de weight_kg (outliers IQR = {r['n_outliers']}, Ls={r['limite_superior']:.1f})", **FIG)
salvar(fig, "m2_boxplot_peso.png")

# M2 - barras categoricas (class) ---------------------------------------------
tab = ms.tabela_frequencias_categorica(df["class"].astype(str).tolist())
fig = px.bar(x=[t["categoria"] for t in tab], y=[t["frequencia"] for t in tab],
             labels={"x": "class", "y": "Frequência"}, color=[t["categoria"] for t in tab])
fig.update_layout(title="Distribuição da variável categórica class (A–D)", showlegend=False, **FIG)
salvar(fig, "m2_categorica_barras.png")

# M3 - LGN ----------------------------------------------------------------------
out = sim.frequencias_relativas_acumuladas(100_000, 1 / 6, seed=42)
fig = go.Figure()
fig.add_trace(go.Scatter(x=out["tamanhos"], y=out["frequencias"], mode="lines", name="frequência relativa"))
fig.add_hline(y=1 / 6, line_dash="dash", line_color="red", annotation_text="P(sair 6) = 1/6")
fig.update_xaxes(type="log")
fig.update_layout(title="LGN: frequência relativa de 'sair 6' converge para 1/6 (10⁵ lançamentos)",
                  xaxis_title="Lançamentos", yaxis_title="Frequência relativa", **FIG)
salvar(fig, "m3_lgn.png")

# M3 - TCL (systolic, n=30, 5000 repetições) ------------------------------------
var = "systolic"
x = df[var].astype(float)
mus = sim.medias_amostrais_repetidas(x, 5000, 30, seed=7)
res = sim.resumo_tcl(x, 5000, 30, seed=7)
fig = px.histogram(mus, nbins=30, labels={"value": "média amostral", "count": "frequência"})
mu_t = float(ms.media(x)); sigma_t = res["sd_teorica"]
xs = np.linspace(mus.min(), mus.max(), 200)
pdf = (1 / (sigma_t * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((xs - mu_t) / sigma_t) ** 2)
fig.add_trace(go.Scatter(x=xs, y=pdf * 5000 * (mus.max() - mus.min()) / 30,
                         mode="lines", name="Normal: N(μ, σ²/n)"))
fig.update_layout(title=f"TCL: distribuição das médias de {var} (n=30, 5.000 repetições)",
                  xaxis_title="média amostral", showlegend=True, **FIG)
salvar(fig, "m3_tcl.png")

# M4 - distribuições teóricas sobre weight_kg ------------------------------------
var = "weight_kg"
x = df[var].astype(float)
grade = np.linspace(x.min(), x.max(), 400)
fig = go.Figure()
fig.add_trace(go.Histogram(x=list(x), histnorm="probability density", nbinsx=40, name="dados", opacity=0.55))
for nome, cor in [("Normal", "red"), ("Exponencial", "darkorange")]:
    fig.add_trace(go.Scatter(x=grade, y=dist.curva_para_variavel(x, nome, grade.tolist()),
                             mode="lines", name=f"{nome} (parâmetros estimados)", line=dict(color=cor, width=2.5)))
fig.update_layout(title=f"Histograma de {var} + curvas Normal e Exponencial", xaxis_title=var, yaxis_title="densidade", **FIG)
salvar(fig, "m4_distribuicoes.png")

# M5 - regressão height x weight -------------------------------------------------
x = df["height_cm"].astype(float)
y = df["weight_kg"].astype(float)
res = rg.regressao_linear(x.tolist(), y.tolist())
x_lin = np.linspace(float(x.min()), float(x.max()), 200)
y_lin = rg.prever_valores(x_lin, res["alpha"], res["beta"])
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name="observações", marker=dict(size=3, opacity=0.3)))
fig.add_trace(go.Scatter(x=x_lin, y=y_lin, mode="lines", name="reta OLS", line=dict(color="red", width=3)))
x_novo = float(x.median())
y_hat = rg.prever(x_novo, res["alpha"], res["beta"])
fig.add_trace(go.Scatter(x=[x_novo], y=[y_hat], mode="markers", name=f"predição X={x_novo:.0f} → Ŷ={y_hat:.1f}",
                         marker=dict(size=14, symbol="star", color="gold", line=dict(color="black", width=1))))
fig.update_layout(title=f"OLS: height_cm × weight_kg — {res['equacao']} (R² = {res['r2']:.4f})",
                  xaxis_title="height_cm", yaxis_title="weight_kg", **FIG)
salvar(fig, "m5_regressao.png")

print("FIM")