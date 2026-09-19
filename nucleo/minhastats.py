"""minhastats — biblioteca estatística implementada do zero.

Todas as medidas sao codificadas manualmente (sem numpy.mean, sem
statistics.*, sem scipy.*). Formulae equivalentes as de referencia sao
documentadas para permitir a validacao automatizada pelo arquivo de
testes testes/test_minhastats.py.

Convencoes adotadas (todas igualando a referencia NumPy/SciPy):

* variancia amostral   -> denom. (n - 1)   [ddof = 1]
* variancia populacional -> denom. (n)     [ddof = 0]
* percentil            -> metodo linear (type 7 do numpy)
* covariancia amostral -> denom. (n - 1)   [equivalente a np.cov]
"""

from __future__ import annotations

from math import sqrt
from collections import Counter
from typing import Sequence, Union, List

Number = Union[int, float]
Vector = Sequence[Number]


# --------------------------------------------------------------------------
# Validacao de entradas
# --------------------------------------------------------------------------

def _converter(x: Vector) -> list[float]:
    """Converte a sequencia de entrada para lista de floats validos."""
    dados = [float(v) for v in x]
    if not dados:
        raise ValueError("entrada vazia")
    return dados


def _pares(x: Vector, y: Vector) -> tuple[list[float], list[float]]:
    if len(x) != len(y):
        raise ValueError("x e y devem ter o mesmo tamanho")
    xs, ys = _converter(x), _converter(y)
    return xs, ys


# --------------------------------------------------------------------------
# Medidas de tendencia central
# --------------------------------------------------------------------------

def media(x: Vector) -> float:
    """Media aritmetica: x_bar = (1/n) * soma(x_i)."""
    dados = _converter(x)
    return sum(dados) / len(dados)


def mediana(x: Vector) -> float:
    """Mediana (2o quartil).

    Ordena os dados; se n impar retorna o elemento central, se n par a
    media dos dois centrais.
    """
    dados = sorted(_converter(x))
    n = len(dados)
    meio = n // 2
    if n % 2 == 1:
        return dados[meio]
    return (dados[meio - 1] + dados[meio]) / 2.0


def moda(x: Vector) -> List[float]:
    """Moda(s): valores de maior frequencia.

    Retorna lista ordenada. Lista vazia indica que nao ha moda
    (todos os valores possuem frequencia 1). Se ha empate entre dois ou
    mais valores, todos sao retornados (distribuicao multimodal).
    """
    dados = _converter(x)
    contagens = Counter(dados)
    max_freq = max(contagens.values())
    if max_freq == 1:
        return []
    return sorted(v for v, f in contagens.items() if f == max_freq)


# --------------------------------------------------------------------------
# Medidas de dispersao
# --------------------------------------------------------------------------

def amplitude(x: Vector) -> float:
    """Amplitude total: max(x) - min(x)."""
    dados = _converter(x)
    return max(dados) - min(dados)


def _variancia_gen(x: Vector, ddof: int) -> float:
    dados = _converter(x)
    n = len(dados)
    if n - ddof <= 0:
        raise ValueError(f"a variancia com ddof={ddof} exige n > {ddof}")
    x_bar = sum(dados) / n
    soma_q = 0.0
    for v in dados:
        soma_q += (v - x_bar) ** 2
    return soma_q / (n - ddof)


def variancia_amostral(x: Vector) -> float:
    """Variancia amostral: s^2 = soma((x_i - x_bar)^2) / (n - 1)."""
    return _variancia_gen(x, ddof=1)


def variancia_populacional(x: Vector) -> float:
    """Variancia populacional: sigma^2 = soma((x_i - mu)^2) / n."""
    return _variancia_gen(x, ddof=0)


def desvio_padrao_amostral(x: Vector) -> float:
    """Desvio padrao amostral: s = sqrt(s^2)."""
    return sqrt(variancia_amostral(x))


def desvio_padrao_populacional(x: Vector) -> float:
    """Desvio padrao populacional: sigma = sqrt(sigma^2)."""
    return sqrt(variancia_populacional(x))


def coeficiente_variacao(x: Vector) -> float:
    """Coeficiente de variacao (%) : CV = (s / x_bar) * 100.

    Medida relativa de dispersao, permite comparar variaveis de
    escalas diferentes. Requer media nao nula.
    """
    dados = _converter(x)
    x_bar = media(dados)
    if x_bar == 0.0:
        raise ValueError("CV indefinido quando a media e nula")
    return desvio_padrao_amostral(dados) / x_bar * 100.0


# --------------------------------------------------------------------------
# Medidas de posicao: percentis, quartis e outliers
# --------------------------------------------------------------------------

def percentil(x: Vector, p: float) -> float:
    """Percentil p (0 <= p <= 100) pelo metodo linear (type 7 / numpy).

    Passo a passo:
      1. ordena  x_0 <= x_1 <= ... <= x_{n-1}
      2. h = (n - 1) * q,     q = p / 100
      3. i = piso(h)
      4. percentil = x_i + (h - i) * (x_{i+1} - x_i)
    Equivale a np.percentile(x, p, method="linear").
    """
    if not 0.0 <= p <= 100.0:
        raise ValueError("p deve estar entre 0 e 100")
    dados = sorted(_converter(x))
    n = len(dados)
    q = p / 100.0
    h = (n - 1) * q
    i = int(h)  # piso (h >= 0)
    frac = h - i
    if i + 1 >= n:
        return dados[-1]
    return dados[i] + frac * (dados[i + 1] - dados[i])


def quartis(x: Vector) -> dict[str, float]:
    """Quartis Q1, Q2 (mediana) e Q3."""
    return {"Q1": percentil(x, 25), "Q2": mediana(x), "Q3": percentil(x, 75)}


def iqr(x: Vector) -> float:
    """Amplitude interquartil: IQR = Q3 - Q1."""
    return percentil(x, 75) - percentil(x, 25)


def detectar_outliers(x: Vector) -> tuple[float, float, List[float]]:
    """Outliers pela regra do IQR.

    Limites:  LI = Q1 - 1.5*IQR   e   LS = Q3 + 1.5*IQR.
    Retorna (LI, LS, lista dos valores fora desses limites).
    """
    dados = _converter(x)
    q1 = percentil(dados, 25)
    q3 = percentil(dados, 75)
    distancia = 1.5 * (q3 - q1)
    li, ls = q1 - distancia, q3 + distancia
    outliers = [v for v in dados if v < li or v > ls]
    return li, ls, outliers


# --------------------------------------------------------------------------
# Medidas de relacao entre duas variaveis
# --------------------------------------------------------------------------

def covariancia(x: Vector, y: Vector) -> float:
    """Covariancia amostral:
    cov = soma((x_i - x_bar)(y_i - y_bar)) / (n - 1).

    Equivale a np.cov(x, y, ddof=1)[0, 1].
    """
    xs, ys = _pares(x, y)
    n = len(xs)
    if n < 2:
        raise ValueError("covariancia exige n > 1")
    x_bar = sum(xs) / n
    y_bar = sum(ys) / n
    soma = 0.0
    for xi, yi in zip(xs, ys):
        soma += (xi - x_bar) * (yi - y_bar)
    return soma / (n - 1)


def correlacao_pearson(x: Vector, y: Vector) -> float:
    """Coeficiente de correlacao de Pearson:
    r = cov(x, y) / (s_x * s_y).

    Equivale a np.corrcoef(x, y)[0, 1].
    Retorna 0.0 (nao NaN) quando qualquer desvio padrao e nulo.
    """
    xs, ys = _pares(x, y)
    sd_x = desvio_padrao_amostral(xs)
    sd_y = desvio_padrao_amostral(ys)
    if sd_x == 0.0 or sd_y == 0.0:
        return 0.0
    return covariancia(xs, ys) / (sd_x * sd_y)


# --------------------------------------------------------------------------
# Medidas auxiliares usadas pelas abas (construidas sobre as anteriores)
# --------------------------------------------------------------------------

def resumo_completo(x: Vector) -> dict[str, Union[float, int, List[float]]]:
    """Todos os valores exibidos no painel de medidas (Modulo 2)."""
    dados = _converter(x)
    quart = quartis(dados)
    li, ls, outs = detectar_outliers(dados)
    dp = desvio_padrao_amostral(dados)
    return {
        "n": len(dados),
        "media": media(dados),
        "mediana": quart["Q2"],
        "moda": moda(dados),
        "amplitude": amplitude(dados),
        "variancia_amostral": variancia_amostral(dados),
        "variancia_populacional": variancia_populacional(dados),
        "desvio_padrao": dp,
        "coeficiente_variacao": coeficiente_variacao(dados) if media(dados) != 0 else float("nan"),
        "Q1": quart["Q1"],
        "Q3": quart["Q3"],
        "IQR": iqr(dados),
        "limite_inferior": li,
        "limite_superior": ls,
        "n_outliers": len(outs),
        "outliers": outs,
    }


def tabela_frequencias_classes(x: Vector, k: int | None = None) -> list[dict]:
    """Tabela de frequencias para variavel continua usando classes.

    Numero de classes pela regra de Sturges quando k nao e informado:
        k = ceil(log2(n)) + 1
    Cada classe possui mesmos comprimento e limites [inf, sup).
    """
    from math import ceil, log2

    dados = _converter(x)
    n = len(dados)
    if k is None:
        k = ceil(log2(n)) + 1
    if k < 1:
        raise ValueError("k deve ser >= 1")
    minimo, maximo = min(dados), max(dados)
    passo = (maximo - minimo) / k
    if passo == 0.0:
        passo = 1.0
    linhas = []
    inf = minimo
    for i in range(k):
        sup = minimo + (i + 1) * passo
        if i == k - 1:
            sup = maximo + 1e-12
        contagem = sum(1 for v in dados if inf <= v < sup)
        linhas.append({
            "classe": f"[{inf:.2f}, {sup:.2f})",
            "frequencia": contagem,
            "frequencia_relativa_%": contagem / n * 100.0,
        })
        inf = sup
    return linhas


def tabela_frequencias_categorica(rotulos: Sequence[str]) -> list[dict]:
    """Tabela de frequencias para variavel categorica."""
    n = len(rotulos)
    contador = Counter(rotulos)
    linhas = []
    for chave in sorted(contador, key=lambda c: -contador[c]):
        c = contador[chave]
        linhas.append({
            "categoria": str(chave),
            "frequencia": c,
            "frequencia_relativa_%": c / n * 100.0,
        })
    return linhas