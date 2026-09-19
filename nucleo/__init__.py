"""Pacote nucleo — estatística e probabilidade implementadas "na unha".

Separação exigida pela Sistematização: o núcleo matemático não depende da
interface. A interface (app/) importa exclusivamente deste pacote.
"""

from . import minhastats
from . import distribuicoes
from . import simulacao
from . import regressao

__all__ = ["minhastats", "distribuicoes", "simulacao", "regressao"]