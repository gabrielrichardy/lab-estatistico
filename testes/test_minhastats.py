"""Validacao do nucleo estatistico proprio contra a referencia.

Regra documentada (tambem no RELATORIO.md): tolerancia numerica de
rtol=1e-10, atol=1e-12. Um desvio maior significa que a implementacao
"na unha" divergiu da referencia NumPy/SciPy.

Execucao:  pytest testes/ -v
"""

from __future__ import annotations

import os

import numpy as np
import pandas as pd
import pytest

from nucleo import minhastats as ms

RTL = 1e-10
ATL = 1e-12

CAMINHO_DADOS = os.path.join(os.path.dirname(__file__), "..", "data", "bodyPerformance.csv")

NUMERICAS = [
    "age", "height_cm", "weight_kg", "body fat_%", "diastolic",
    "systolic", "gripForce", "sit and bend forward_cm",
    "sit-ups counts", "broad jump_cm",
]


@pytest.fixture(scope="module")
def df() -> pd.DataFrame:
    return pd.read_csv(CAMINHO_DADOS)


@pytest.fixture(scope="module")
def subsets(df: pd.DataFrame) -> dict[str, np.ndarray]:
    """Subconjuntos variados: tamanhos pares/impares, com outliers."""
    rng = np.random.default_rng(7)
    return {
        "n_par": np.array(df["height_cm"].head(1000)),
        "n_impar": np.array(df["weight_kg"].head(999)),
        "pequeno": np.array([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]),
        "com_outliers": np.array(list(df["systolic"][:2000]) + [220.0, 240.0, 60.0]),
        "repetidos": np.array([float(v) for v in [1, 1, 1, 2, 2, 3, 3, 3, 3]]),
        "decimais": rng.normal(170, 8, 500),
    }


# --------------------------------------------------------------------------
# Tendencia central
# --------------------------------------------------------------------------

def test_media(df: pd.DataFrame):
    for col in NUMERICAS:
        x = df[col].astype(float)
        assert np.allclose(ms.media(x), np.mean(x), rtol=RTL, atol=ATL)


def test_mediana(df: pd.DataFrame):
    for col in NUMERICAS:
        x = df[col].astype(float)
        assert np.allclose(ms.mediana(x), np.median(x), rtol=RTL, atol=ATL)


@pytest.mark.parametrize("chave", ["n_par", "n_impar", "pequeno", "com_outliers", "repetidos", "decimais"])
def test_mediana_tamanhos(chave: str, subsets: dict):
    x = subsets[chave]
    assert np.allclose(ms.mediana(x), np.median(x), rtol=RTL, atol=ATL)


def test_moda_repetidos():
    assert ms.moda([1.0, 1.0, 1.0, 2.0, 2.0, 3.0]) == [1.0]
    assert ms.moda([1.0, 1.0, 2.0, 2.0]) == [1.0, 2.0]
    assert ms.moda([1.0, 2.0, 3.0]) == []


# --------------------------------------------------------------------------
# Dispersao
# --------------------------------------------------------------------------

def test_amplitude(df: pd.DataFrame):
    for col in NUMERICAS:
        x = df[col].astype(float)
        assert np.allclose(ms.amplitude(x), np.ptp(x), rtol=RTL, atol=ATL)


def test_variancia_amostral(df: pd.DataFrame):
    for col in NUMERICAS:
        x = df[col].astype(float)
        assert np.allclose(ms.variancia_amostral(x), np.var(x, ddof=1), rtol=RTL, atol=ATL)


def test_variancia_populacional(df: pd.DataFrame):
    for col in NUMERICAS:
        x = df[col].astype(float)
        assert np.allclose(ms.variancia_populacional(x), np.var(x, ddof=0), rtol=RTL, atol=ATL)


def test_desvio_amostral(df: pd.DataFrame):
    for col in NUMERICAS:
        x = df[col].astype(float)
        assert np.allclose(ms.desvio_padrao_amostral(x), np.std(x, ddof=1), rtol=RTL, atol=ATL)


def test_desvio_populacional(df: pd.DataFrame):
    for col in NUMERICAS:
        x = df[col].astype(float)
        assert np.allclose(ms.desvio_padrao_populacional(x), np.std(x, ddof=0), rtol=RTL, atol=ATL)


def test_coeficiente_variacao(df: pd.DataFrame):
    for col in NUMERICAS:
        x = df[col].astype(float)
        ref = np.std(x, ddof=1) / np.mean(x) * 100.0
        assert np.allclose(ms.coeficiente_variacao(x), ref, rtol=RTL, atol=ATL)


# --------------------------------------------------------------------------
# Posicao: percentis, quartis, IQR e outliers
# --------------------------------------------------------------------------

def test_percentis_openai(df: pd.DataFrame):
    """Compara varios percentis simultaneamente (metodo linear type 7)."""
    for col in NUMERICAS:
        x = df[col].astype(float)
        for p in [1, 5, 25, 50, 75, 90, 99]:
            assert np.allclose(ms.percentil(x, p), np.percentile(x, p),
                               rtol=RTL, atol=ATL), f"coluna={col} p={p}"


def test_quartis(df: pd.DataFrame):
    x = df["weight_kg"].astype(float)
    q = ms.quartis(x)
    assert np.allclose(q["Q1"], np.percentile(x, 25), rtol=RTL, atol=ATL)
    assert np.allclose(q["Q2"], np.percentile(x, 50), rtol=RTL, atol=ATL)
    assert np.allclose(q["Q3"], np.percentile(x, 75), rtol=RTL, atol=ATL)


def test_iqr(df: pd.DataFrame):
    x = df["systolic"].astype(float)
    assert np.allclose(ms.iqr(x),
                       np.percentile(x, 75) - np.percentile(x, 25),
                       rtol=RTL, atol=ATL)


def test_detectar_outliers():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 100.0, -50.0])
    li, ls, outs = ms.detectar_outliers(x)
    q1, q3 = np.percentile(x, [25, 75])
    ref_li, ref_ls = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
    assert np.allclose(li, ref_li, rtol=RTL, atol=ATL)
    assert np.allclose(ls, ref_ls, rtol=RTL, atol=ATL)
    assert sorted(outs) == sorted([100.0, -50.0])


# --------------------------------------------------------------------------
# Relacao: covariancia e Pearson
# --------------------------------------------------------------------------

@pytest.mark.parametrize("x_col,y_col", [
    ("height_cm", "weight_kg"),
    ("weight_kg", "body fat_%"),
    ("systolic", "diastolic"),
    ("age", "broad jump_cm"),
])
def test_covariancia(df: pd.DataFrame, x_col: str, y_col: str):
    x = df[x_col].astype(float)
    y = df[y_col].astype(float)
    ref = np.cov(x, y, ddof=1)[0, 1]
    assert np.allclose(ms.covariancia(x, y), ref, rtol=RTL, atol=ATL)


@pytest.mark.parametrize("x_col,y_col", [
    ("height_cm", "weight_kg"),
    ("weight_kg", "body fat_%"),
    ("systolic", "diastolic"),
    ("age", "broad jump_cm"),
])
def test_correlacao_pearson(df: pd.DataFrame, x_col: str, y_col: str):
    x = df[x_col].astype(float)
    y = df[y_col].astype(float)
    ref = np.corrcoef(x, y)[0, 1]
    assert np.allclose(ms.correlacao_pearson(x, y), ref, rtol=RTL, atol=ATL)


# --------------------------------------------------------------------------
# Valores de referencia manual (caso deterministico conhecido)
# --------------------------------------------------------------------------

def test_valores_manuais():
    x = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    assert np.isclose(ms.media(x), 5.0, rtol=RTL, atol=ATL)
    assert np.isclose(ms.mediana(x), 4.5, rtol=RTL, atol=ATL)
    assert ms.moda(x) == [4.0]
    assert np.isclose(ms.amplitude(x), 7.0, rtol=RTL, atol=ATL)
    assert np.isclose(ms.variancia_amostral(x), 32.0 / 7.0, rtol=RTL, atol=ATL)


# --------------------------------------------------------------------------
# Erros esperados em entradas invalidas
# --------------------------------------------------------------------------

def test_entradas_invalidas():
    with pytest.raises(ValueError):
        ms.media([])
    with pytest.raises(ValueError):
        ms.variancia_amostral([1.0])
    with pytest.raises(ValueError):
        ms.percentil([1.0, 2.0], 150)
    with pytest.raises(ValueError):
        ms.covariancia([1.0, 2.0], [1.0, 2.0, 3.0])