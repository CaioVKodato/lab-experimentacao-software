"""Transforma nós GraphQL nas linhas do CSV (métricas RQ01–RQ07)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def days_since(iso_date: str | None) -> int | None:
    """Dias decorridos desde uma data ISO-8601 (UTC)."""
    if not iso_date:
        return None
    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - dt).days


def closed_ratio(closed: int, total: int) -> float:
    """Razão issues fechadas / total; 0.0 se não houver issues."""
    return round(closed / total, 4) if total > 0 else 0.0


def repository_to_row(node: dict[str, Any]) -> dict[str, Any]:
    """
    Converte um nó Repository da API nas colunas do CSV.

    RQ01 age_days ← createdAt
    RQ02 merged_prs ← pullRequests(MERGED)
    RQ03 releases
    RQ04 days_since_push ← pushedAt (não updatedAt)
    RQ05/RQ07 language ← primaryLanguage
    RQ06 closed_ratio ← closed / (closed + open); issues GraphQL sem PRs
    """
    closed = node["closedIssues"]["totalCount"]
    open_ = node["openIssues"]["totalCount"]
    total = closed + open_
    return {
        "name": node["nameWithOwner"],
        "stars": node["stargazerCount"],
        "created_at": node["createdAt"],
        "pushed_at": node["pushedAt"],
        "age_days": days_since(node["createdAt"]),
        "days_since_push": days_since(node["pushedAt"]),
        "merged_prs": node["pullRequests"]["totalCount"],
        "releases": node["releases"]["totalCount"],
        "closed_issues": closed,
        "open_issues": open_,
        "total_issues": total,
        "closed_ratio": closed_ratio(closed, total),
        "language": (node["primaryLanguage"] or {}).get("name", ""),
    }
