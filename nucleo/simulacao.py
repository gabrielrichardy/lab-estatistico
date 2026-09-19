"""simulacao — Monte Carlo para o Modulo 3 (LGN e TCL).

Aquic a geracao de numeros aleatorios usa numpy.random (apenas para
simular experimentos); as medidas estatisticas (medias, desvios,
frequencias relativas) sao calculadas pelo nucleo proprio (minhastats).
"""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .minhastats import media, desvio_padrao_amostral


# --------------------------------------------------------------------------
# Experimento A — Lei dos Grandes Numeros
# --------------------------------------------------------------------------

def frequencias_relativas_acumuladas(n_lancamentos: int, p: float, seed: int = 42) -> dict:
    """Frequencia relativa acumulada de um dado/uma moeda honesta.

    Executa n lançamentos de um experimento Bernoulli(p) e retorna, para
    cada t = 1..n, a frequencia relativa observada ate o lancamento t.
    A Lei dos Grandes Numeros garante convergencia para p.

    Retorna {"tamanhos": [...], "frequencias": [...], "valor_teorico": p}.
    """
    rng = np.random.default_rng(seed)
    mascara = rng.random(n_lancamentos) < p
    acumulado = np.cumsum(mascara, dtype=np.float64)
    tamanhos = np.arange(1, n_lancamentos + 1)
    frequencias = acumulado / tamanhos
    return {
        "tamanhos": tamanhos,
        "frequencias": frequencias,
        "valor_teorico": float(p),
    }


def convergencia_lgn(n_lancamentos: int, p: float, seed: int = 42) -> dict:
    """Resumo comparativo para a conclusao automatica do experimento A."""
    rng = np.random.default_rng(seed)
    mascara = rng.random(n_lancamentos) < p
    freq_relativa_final = float(mascara.mean())
    return {
        "frequencia_relativa_final": freq_relativa_final,
        "esperado": float(p),
        "diferenca": abs(freq_relativa_final - p),
    }


# --------------------------------------------------------------------------
# Experimento B — Teorema Central do Limite
# --------------------------------------------------------------------------

def medias_amostrais_repetidas(x: Sequence[float], n_repeticoes: int,
                               tamanho_amostra: int, seed: int = 42) -> np.ndarray:
    """Distribuicao das medias amostrais (TCL).

    Sorteia n_repeticoes amostras de tamanho_amostra (com reposicao) da
    variavel x e retorna a media de cada amostra.

    Pelo TCL:   media(medias) ~ mu    e    dp(medias) ~ sigma/sqrt(n).
    """
    dados = np.asarray(x, dtype=np.float64)
    rng = np.random.default_rng(seed)
    amostras = rng.choice(dados, size=(n_repeticoes, tamanho_amostra), replace=True)
    return amostras.mean(axis=1)


def resumo_tcl(x: Sequence[float], n_repeticoes: int,
               tamanho_amostra: int, seed: int = 42) -> dict:
    """Medidas da distribuicao das medias + comparacao teorica SDOM."""
    dados = np.asarray(x, dtype=np.float64)
    mus = medias_amostrais_repetidas(dados, n_repeticoes,
                                     tamanho_amostra, seed)
    mu_pop = media(dados)
    sigma_pop = desvio_padrao_amostral(dados)
    sd_teorica = sigma_pop / np.sqrt(tamanho_amostra)
    return {
        "media_medias": media(mus.tolist()),
        "mu_populacao": mu_pop,
        "dp_medias": desvio_padrao_amostral(mus.tolist()),
        "sd_teorica": float(sd_teorica),
        "sigma_populacao": sigma_pop,
    }