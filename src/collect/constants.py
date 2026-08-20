"""Constantes da coleta GraphQL (S01 = 100, S02 = 1000)."""

from __future__ import annotations

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"

# Meta da S02: 1000 repos válidos. Cada query Search limita a 1000 hits;
# nós nulos são compensados com novas janelas (stars:<min).
DEFAULT_LIMIT = 1000
MAX_SEARCH_RESULTS = 1000

# Batches menores evitam HTTP 502 em queries com vários totalCount.
BATCH_INITIAL = 25
BATCH_DEEP = 10
DEEP_PAGINATION_AFTER = 75
PAGE_DELAY_SECONDS = 3.0
REQUEST_TIMEOUT_SECONDS = 60

FIELDNAMES = [
    "name",
    "stars",
    "created_at",
    "pushed_at",
    "age_days",
    "days_since_push",
    "merged_prs",
    "releases",
    "closed_issues",
    "open_issues",
    "total_issues",
    "closed_ratio",
    "language",
]
