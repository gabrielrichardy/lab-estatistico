"""Validacao de distribuicoes, simulacao e regressao contra SciPy/NumPy."""

from __future__ import annotations

import os

import numpy as np
import pandas as pd
from scipy import stats
import pytest

from nucleo import distribuicoes as dist
from nucleo import simulacao as sim
from nucleo import regressao as reg

RTL = 1e-10
ATL = 1e-12

CAMINHO_DADOS = os.path.join(os.path.dirname(__file__), "..", "data", "bodyPerformance.csv")


@pytest.fixture(scope="module")
def df() -> pd.DataFrame:
    return pd.read_csv(CAMINHO_DADOS)


@pytest.fixture(scope="module")
def x(df: pd.DataFrame) -> np.ndarray:
    return df["weight_kg"].astype(float).values


# --------------------------------------------------------------------------
# Funcoes densidade
# --------------------------------------------------------------------------

def test_pdf_normal(x):
    mu, sigma = np.mean(x), np.std(x, ddof=1)
    grade = np.linspace(x.min(), x.max(), 50)
    ref = stats.norm.pdf(grade, loc=mu, scale=sigma)
    mine = [dist.pdf_normal(v, mu, sigma) for v in grade]
    assert np.allclose(mine, ref, rtol=RTL, atol=ATL)


def test_pdf_exponencial():
    lamb = 0.5
    grade = np.linspace(0, 10, 100)
    ref = stats.expon.pdf(grade, scale=1 / lamb)
    mine = [dist.pdf_exponencial(v, lamb) for v in grade]
    assert np.allclose(mine, ref, rtol=RTL, atol=ATL)
    assert dist.pdf_exponencial(-1.0, lamb) == 0.0


def test_pdf_uniforme():
    grade = np.linspace(-1, 4, 100)
    ref = stats.uniform.pdf(grade, loc=0, scale=3)
    mine = [dist.pdf_uniforme(v, 0.0, 3.0) for v in grade]
    assert np.allclose(mine, ref, rtol=RTL, atol=ATL)
    assert dist.pdf_uniforme(5.0, 0.0, 3.0) == 0.0


def test_pmf_poisson():
    lamb = 3.5
    ks = np.arange(0, 15)
    ref = stats.poisson.pmf(ks, lamb)
    mine = [dist.pmf_poisson(int(k), lamb) for k in ks]
    assert np.allclose(mine, ref, rtol=RTL, atol=ATL)


def test_pmf_binomial():
    n, p = 10, 0.3
    ks = np.arange(0, 11)
    ref = stats.binom.pmf(ks, n, p)
    mine = [dist.pmf_binomial(int(k), n, p) for k in ks]
    assert np.allclose(mine, ref, rtol=RTL, atol=ATL)


# --------------------------------------------------------------------------
# Estimacao de parametros (e a curva gerada normaliza a area?)
# --------------------------------------------------------------------------

def test_estimacao_e_integracao_normal(x):
    p = dist.estimar_normal(x)
    assert np.isclose(p["mu"], np.mean(x), rtol=RTL, atol=ATL)
    assert np.isclose(p["sigma"], np.std(x, ddof=1), rtol=RTL, atol=ATL)
    grade = np.linspace(x.min(), x.max(), 2000)
    dens = [dist.pdf_normal(v, p["mu"], p["sigma"]) for v in grade]
    area = np.trapezoid(dens, grade) if hasattr(np, "trapezoid") else np.trapz(dens, grade)
    assert np.isclose(area, 1.0, rtol=1e-2, atol=1e-2)


def test_estimacao_exponencial(x):
    p = dist.estimar_exponencial(x)
    assert np.isclose(p["lamb"], 1.0 / np.mean(x), rtol=RTL, atol=ATL)


def test_curva_para_variavel_descohecida(x):
    with pytest.raises(ValueError):
        dist.curva_para_variavel(x, "Cauchy", [1.0, 2.0])


# --------------------------------------------------------------------------
# Simulacao — LGN e TCL
# --------------------------------------------------------------------------

def test_lgn_frequencia_converge_para_p():
    res = sim.convergencia_lgn(100_000, p=0.5, seed=42)
    assert abs(res["frequencia_relativa_final"] - 0.5) < 0.01
    # a relacao final deve estar tabulada junto do teorico


def test_lgn_acumulados_tamanho():
    out = sim.frequencias_relativas_acumuladas(5000, p=1 / 6, seed=1)
    assert len(out["tamanhos"]) == len(out["frequencias"]) == 5000
    assert np.isclose(out["valor_teorico"], 1 / 6)


def test_tcl_media_medias():
    x = np.linspace(0, 1, 1000) ** 2  # distribuicao bem assimetrica
    res = sim.resumo_tcl(x, n_repeticoes=5000, tamanho_amostra=30, seed=3)
    assert abs(res["media_medias"] - res["mu_populacao"]) < 0.02
    assert abs(res["dp_medias"] - res["sd_teorica"]) < 0.02 * res["sd_teorica"]


def test_tcl_dimensoes():
    mus = sim.medias_amostrais_repetidas(np.arange(50, dtype=float),
                                         n_repeticoes=200, tamanho_amostra=5, seed=2)
    assert mus.shape == (200,)


# --------------------------------------------------------------------------
# Regressao linear — OLS vs np.polyfit e scipy.linregress
# --------------------------------------------------------------------------

def test_coeficientes_ols(df):
    x = df["height_cm"].astype(float).values
    y = df["weight_kg"].astype(float).values
    res = reg.regressao_linear(x.tolist(), y.tolist())
    ref = np.polyfit(x, y, 1)
    assert np.isclose(res["beta"], ref[0], rtol=1e-6, atol=1e-9)
    assert np.isclose(res["alpha"], ref[1], rtol=1e-6, atol=1e-9)
    lin = stats.linregress(x, y)
    assert np.isclose(res["r"], lin.rvalue, rtol=1e-6, atol=1e-9)
    assert np.isclose(res["r2"], lin.rvalue ** 2, rtol=1e-6, atol=1e-9)


def test_predicao_na_reta():
    x = np.arange(10, dtype=float)
    y = 2.0 * x + 1.0
    res = reg.regressao_linear(x.tolist(), y.tolist())
    assert np.isclose(res["beta"], 2.0, rtol=1e-10)
    assert np.isclose(res["alpha"], 1.0, rtol=1e-10)
    assert np.isclose(reg.prever(5.0, res["alpha"], res["beta"]), 11.0, rtol=1e-10)


def test_regressao_tamanhos_diferentes():
    with pytest.raises(ValueError):
        reg.regressao_linear([1.0, 2.0], [1.0, 2.0, 3.0])