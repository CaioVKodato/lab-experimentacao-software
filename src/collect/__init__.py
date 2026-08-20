"""
Pacote de coleta dos repositórios mais populares (Lab01).

S01: 100 repos → data/repositories.csv
S02: 1000 repos → data/repositories_top1000.csv

Uso:
    python -m src.collect
    python -m src.collect --n 1000
    python -m src.collect --n 100 --out data/repositories.csv
"""

from __future__ import annotations

from src.collect.export import default_output_path, save_csv
from src.collect.fetch import fetch_top_repos

__all__ = ["default_output_path", "fetch_top_repos", "save_csv"]
