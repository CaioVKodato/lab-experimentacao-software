"""Exportação CSV da coleta."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from src.collect.constants import DATA_DIR, FIELDNAMES


def default_output_path(n: int) -> Path:
    """Caminho padrão: S01 (100) mantém repositories.csv; S02 usa top1000."""
    if n == 100:
        return DATA_DIR / "repositories.csv"
    return DATA_DIR / f"repositories_top{n}.csv"


def save_csv(repos: list[dict[str, Any]], path: Path) -> None:
    """Persiste as linhas no CSV com schema estável das RQs."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(repos)
    print(f"[collect] {len(repos)} repositórios salvos em {path}")
