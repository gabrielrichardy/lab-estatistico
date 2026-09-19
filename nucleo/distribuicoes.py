"""distribuicoes — funcoes densidade de probabilidade implementadas do zero.

Usado no Modulo 4 para sobrepor curvas teoricas ao histograma da variavel
escolhida, com parametros estimados dos dados. Notacao IGUAL a da teoria:

    Normal       f(x) = (1/(sigma*sqrt(2pi))) * exp(-(x-mu)^2 / (2sigma^2))
    Exponencial  f(x) = lambda * exp(-lambda * x),          x >= 0
    Uniforme     f(x) = 1/(b - a),                          a <= x <= b
    Poisson      P(X=k) = (lambda^k * e^-lambda) / k!,      k = 0, 1, 2, ...
    Binomial     P(X=k) = C(n,k) * p^k * (1-p)^(n-k)
"""

from __future__ import annotations

from math import exp, pi, sqrt, factorial, comb
from typing import Sequence

from .minhastats import media, variancia_amostral


# --------------------------------------------------------------------------
# Funcoes densidade (pdf) teoricas
# --------------------------------------------------------------------------

def pdf_normal(x: float, mu: float, sigma: float) -> float:
    """Densidade da distribuicao Normal(mu, sigma^2)."""
    if sigma <= 0:
        raise ValueError("sigma deve ser > 0")
    z = (x - mu) / sigma
    return (1.0 / (sigma * sqrt(2.0 * pi))) * exp(-0.5 * z * z)


def pdf_exponencial(x: float, lamb: float) -> float:
    """Densidade da distribuicao Exponencial(lamb) para x >= 0."""
    if lamb <= 0:
        raise ValueError("lambda deve ser > 0")
    if x < 0:
        return 0.0
    return lamb * exp(-lamb * x)


def pdf_uniforme(x: float, a: float, b: float) -> float:
    """Densidade da distribuicao Uniforme(a, b)."""
    if b <= a:
        raise ValueError("exige a < b")
    if a <= x <= b:
        return 1.0 / (b - a)
    return 0.0


def pmf_poisson(k: int, lamb: float) -> float:
    """Probabilidade P(X=k) da distribuicao Poisson(lamb)."""
    if lamb <= 0:
        raise ValueError("lambda deve ser > 0")
    if k < 0:
        return 0.0
    return (lamb ** k) * exp(-lamb) / factorial(k)


def pmf_binomial(k: int, n: int, p: float) -> float:
    """Probabilidade P(X=k) da distribuicao Binomial(n, p)."""
    if not 0 <= p <= 1:
        raise ValueError("p deve estar entre 0 e 1")
    if n < 0 or k < 0 or k > n:
        return 0.0
    return comb(n, k) * (p ** k) * ((1 - p) ** (n - k))


# --------------------------------------------------------------------------
# Estimacao de parametros a partir dos dados (maxima verossimilhanca)
# --------------------------------------------------------------------------

def _estimar_media_dp(x: Sequence[float]) -> tuple[float, float]:
    """Estimadores de MV: mu = media amostral, sigma = dp amostral."""
    mu = media(x)
    sigma = sqrt(variancia_amostral(x))
    return mu, sigma


def estimar_normal(x: Sequence[float]) -> dict[str, float]:
    """Parametros da Normal candidata: mu e sigma estimados dos dados."""
    mu, sigma = _estimar_media_dp(x)
    return {"mu": mu, "sigma": sigma}


def estimar_exponencial(x: Sequence[float]) -> dict[str, float]:
    """Parametros da Exponencial candidata: lambda = 1 / media."""
    mu = media(x)
    if mu <= 0:
        raise ValueError("exponencial requer dados estritamente positivos")
    return {"lamb": 1.0 / mu}


def estimar_uniforme(x: Sequence[float]) -> dict[str, float]:
    """Parametros da Uniforme candidata: a=min e b=max."""
    return {"a": min(x), "b": max(x)}


def curva_para_variavel(x: Sequence[float], nome_dist: str, xs: Sequence[float]) -> list[float]:
    """Avalia a pdf candidata sobre uma grade de pontos xs."""
    if nome_dist == "Normal":
        p = estimar_normal(x)
        return [pdf_normal(v, p["mu"], p["sigma"]) for v in xs]
    if nome_dist == "Exponencial":
        p = estimar_exponencial(x)
        return [pdf_exponencial(v, p["lamb"]) for v in xs]
    if nome_dist == "Uniforme":
        p = estimar_uniforme(x)
        return [pdf_uniforme(v, p["a"], p["b"]) for v in xs]
    raise ValueError(f"distribuicao desconhecida: {nome_dist}")