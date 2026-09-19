"""Baixa o dataset publico Body Performance Data (Kaggle) para data/.

Uso:
    python -m scripts.baixar_dados    # de dentro da raiz do projeto

Requer kagglehub (ja listado em requirements.txt). Se o CSV existir,
apenas avisa e nao sobrescreve.
"""

from __future__ import annotations

import os
import shutil

import kagglehub

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "data", "bodyPerformance.csv")

SLUG_DATASET = "kukuroo3/body-performance-data"


def main() -> None:
    if os.path.exists(DESTINO):
        print(f"ja existe: {DESTINO} (nada a fazer)")
        return
    caminho = kagglehub.dataset_download(SLUG_DATASET)
    origem = os.path.join(caminho, "bodyPerformance.csv")
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    shutil.copy(origem, DESTINO)
    print(f"baixado para {DESTINO}")


if __name__ == "__main__":
    main()