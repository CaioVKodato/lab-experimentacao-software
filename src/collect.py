"""
Coleta os 100 repositórios mais populares (por estrelas) com todos os campos
necessários para RQ01–RQ07 e salva em data/repositories.csv.

Campos coletados:
  RQ01 - age_days       : dias desde createdAt
  RQ02 - merged_prs     : total de pull requests aceitas (merged)
  RQ03 - releases       : total de releases
  RQ04 - days_since_push: dias desde pushedAt (último push de código)
  RQ05 - language       : linguagem primária
  RQ06 - closed_ratio   : closedIssues / (closedIssues + openIssues)
  RQ07 - cruzamento RQ02/03/04 por linguagem (feito na análise, dados aqui)

Uso:
    python -m src.collect
"""

from __future__ import annotations

import csv
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from src.github import graphql_request

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

QUERY = """
query TopRepos($first: Int!, $after: String) {
  search(
    query: "stars:>1 sort:stars-desc"
    type: REPOSITORY
    first: $first
    after: $after
  ) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        nameWithOwner
        stargazerCount
        createdAt
        pushedAt
        primaryLanguage { name }
        pullRequests(states: MERGED) { totalCount }
        releases { totalCount }
        closedIssues: issues(states: CLOSED) { totalCount }
        openIssues:   issues(states: OPEN)   { totalCount }
      }
    }
  }
  rateLimit {
    cost
    remaining
    resetAt
    limit
  }
}
"""

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


def _days_since(iso_date: str) -> int:
    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - dt).days


def _closed_ratio(closed: int, total: int) -> float:
    return round(closed / total, 4) if total > 0 else 0.0


_BATCH_INITIAL = 25   # GitHub retorna 502 com queries complexas acima desse valor
_BATCH_DEEP    = 10   # Batches menores para paginação mais profunda (>75 repos)
_PAGE_DELAY    = 3.0  # Segundos entre requisições para evitar 502/504


def fetch_top_repos(n: int = 100) -> list[dict]:
    """Busca os *n* repositórios mais populares via GraphQL (paginado)."""
    repos: list[dict] = []
    after: str | None = None
    page = 0

    while len(repos) < n:
        batch = _BATCH_DEEP if len(repos) >= 75 else _BATCH_INITIAL
        first = min(batch, n - len(repos))

        if page > 0:
            time.sleep(_PAGE_DELAY)

        body = graphql_request(QUERY, {"first": first, "after": after}, timeout=60)
        page += 1
        search = body["data"]["search"]

        for node in search["nodes"]:
            closed = node["closedIssues"]["totalCount"]
            open_ = node["openIssues"]["totalCount"]
            total = closed + open_
            repos.append({
                "name": node["nameWithOwner"],
                "stars": node["stargazerCount"],
                "created_at": node["createdAt"],
                "pushed_at": node["pushedAt"],
                "age_days": _days_since(node["createdAt"]),
                "days_since_push": _days_since(node["pushedAt"]),
                "merged_prs": node["pullRequests"]["totalCount"],
                "releases": node["releases"]["totalCount"],
                "closed_issues": closed,
                "open_issues": open_,
                "total_issues": total,
                "closed_ratio": _closed_ratio(closed, total),
                "language": (node["primaryLanguage"] or {}).get("name", ""),
            })

        page_info = search["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        after = page_info["endCursor"]

    return repos[:n]


def save_csv(repos: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(repos)
    print(f"[collect] {len(repos)} repositórios salvos em {path}")


def main() -> None:
    print("[collect] buscando os 100 repositórios mais populares no GitHub...")
    try:
        repos = fetch_top_repos(100)
    except RuntimeError as exc:
        print(f"Erro na coleta: {exc}", file=sys.stderr)
        sys.exit(1)

    save_csv(repos, DATA_DIR / "repositories.csv")
    print("[collect] concluído.")


if __name__ == "__main__":
    main()
