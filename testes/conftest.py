"""Configuracao do pytest: garante que a raiz do projeto esteja no sys.path
para que `import nucleo` funcione, independentemente de onde o pytest roda.
"""

from __future__ import annotations

import os
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)