"""regressao — regressao linear simples por minimos quadrados (OLS).

Formula fechada (derivavel no relatorio):

    beta = cov(x, y) / var(x)
    alpha = y_bar - beta * x_bar
    y_hat = alpha + beta * x

    R^2 = r^2   (quadrado do coeficiente de Pearson, do minhastats)

Obs.: as medidas de posicao/dispersao sao reutilizadas de minhastats,
nada de np.polyfit aqui dentro.
"""

from __future__ import annotations

from typing import Sequence

from .minhastats import (media, covariancia, variancia_amostral,
                         correlacao_pearson)


def regressao_linear(x: Sequence[float], y: Sequence[float]) -> dict:
    """Ajusta y = alpha + beta*x e retorna uma analise completa.

    Retorna dict com: alpha, beta, equacao, r (Pearson), r2, e as
    interpretacoes textuais (direcao, forca, efeito de 1 unidade em x).
    """
    if len(x) != len(y):
        raise ValueError("x e y devem ter o mesmo tamanho")
    if len(x) < 3:
        raise ValueError("sao necessarios ao menos 3 pontos")

    x_bar = media(x)
    y_bar = media(y)
    var_x = variancia_amostral(x)

    if var_x == 0.0:
        raise ValueError("x constante: regressao indefinida")

    beta = covariancia(x, y) / var_x
    alpha = y_bar - beta * x_bar
    r = correlacao_pearson(x, y)
    r2 = r * r

    if beta > 0:
        direcao = "positiva"
        efeito = f"um aumento de 1 unidade em X eleva Y, em media, "
    elif beta < 0:
        direcao = "negativa"
        efeito = f"um aumento de 1 unidade em X reduz Y, em media, "
    else:
        direcao = "nula"
        efeito = ""

    if abs(r) >= 0.8:
        forca = "muito forte"
    elif abs(r) >= 0.6:
        forca = "forte"
    elif abs(r) >= 0.4:
        forca = "moderada"
    elif abs(r) >= 0.2:
        forca = "fraca"
    else:
        forca = "muito fraca"

    return {
        "alpha": alpha,
        "beta": beta,
        "equacao": f"y = {alpha:.4g} + ({beta:.4g})*x",
        "r": r,
        "r2": r2,
        "direcao": direcao,
        "forca": forca,
        "interpretacao_efeito": (
            f"{efeito}{beta:.4g} unidades (coeficiente angular)"
        ),
        "interpretacao_correlacao": (
            f"correlacao {forca} e {direcao} entre as variaveis "
            f"(Pearson r = {r:.4f})"
        ),
        "interpretacao_r2": (
            f"{r2*100:.2f}% da variacao de Y e explicada linearmente por X"
        ),
    }


def prever(x_novo: float, alpha: float, beta: float) -> float:
    """Predicao do modelo: y_hat = alpha + beta * x_novo."""
    return alpha + beta * x_novo


def prever_valores(xs: Sequence[float], alpha: float, beta: float) -> list[float]:
    """Aplica a reta a uma grade de valores (para o grafico da regressao)."""
    return [prever(v, alpha, beta) for v in xs]