"""Abas da aplicacao Streamlit. Cada aba expoe render(df: pd.DataFrame)."""

from . import descritiva
from . import probabilidade
from . import distribuicoes
from . import regressao

__all__ = ["descritiva", "probabilidade", "distribuicoes", "regressao"]