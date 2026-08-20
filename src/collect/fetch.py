"""Paginação GraphQL dos repositórios mais estrelados."""

from __future__ import annotations

import time
from typing import Any

from src.collect.constants import (
    BATCH_DEEP,
    BATCH_INITIAL,
    DEEP_PAGINATION_AFTER,
    MAX_SEARCH_RESULTS,
    PAGE_DELAY_SECONDS,
    REQUEST_TIMEOUT_SECONDS,
)
from src.collect.query import TOP_REPOS_QUERY
from src.collect.transform import repository_to_row
from src.github import graphql_request


def _batch_size(already_fetched: int, remaining: int) -> int:
    """Escolhe o tamanho do lote (menor na paginação profunda)."""
    base = BATCH_DEEP if already_fetched >= DEEP_PAGINATION_AFTER else BATCH_INITIAL
    return min(base, remaining)


def _window_search_query(max_stars_exclusive: int | None) -> str:
    """
    Monta a query de busca.

    A Search API limita cada query a 1000 hits. Quando nós nulos fazem
    faltar válidos, abrimos uma nova janela com stars abaixo do mínimo
    já coletado (técnica de star-cursor).
    """
    if max_stars_exclusive is None:
        return "stars:>1 sort:stars-desc"
    return f"stars:<{max_stars_exclusive} sort:stars-desc"


def fetch_top_repos(n: int = 1000) -> list[dict[str, Any]]:
    """
    Busca os *n* repositórios mais populares via GraphQL (paginado).

    Garante *n* repositórios **válidos** (sem nós nulos). Se uma janela
    de search esgotar antes da meta, continua com `stars:<min` e deduplica.
    """
    target = min(max(n, 1), MAX_SEARCH_RESULTS)
    repos: list[dict[str, Any]] = []
    seen: set[str] = set()
    page = 0
    window = 0
    max_stars_exclusive: int | None = None

    print(
        f"[collect] meta={target} repositórios válidos "
        f"(Search API: até {MAX_SEARCH_RESULTS} hits por janela)"
    )

    while len(repos) < target:
        window += 1
        search_query = _window_search_query(max_stars_exclusive)
        after: str | None = None
        added_in_window = 0

        print(f"[collect] janela {window}: query={search_query!r}")

        while len(repos) < target:
            first = _batch_size(len(repos), target - len(repos))

            if page > 0:
                time.sleep(PAGE_DELAY_SECONDS)

            body = graphql_request(
                TOP_REPOS_QUERY,
                {
                    "searchQuery": search_query,
                    "first": first,
                    "after": after,
                },
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            page += 1
            search = body["data"]["search"]

            page_rows = 0
            for node in search.get("nodes") or []:
                if not node or "nameWithOwner" not in node:
                    continue
                name = node["nameWithOwner"]
                if name in seen:
                    continue
                row = repository_to_row(node)
                seen.add(name)
                repos.append(row)
                added_in_window += 1
                page_rows += 1
                if len(repos) >= target:
                    break

            print(
                f"[collect] página {page}: +{page_rows} válidos "
                f"(acumulado {len(repos)}/{target})"
            )

            page_info = search["pageInfo"]
            if len(repos) >= target:
                break
            if not page_info["hasNextPage"]:
                break
            after = page_info["endCursor"]

        if len(repos) >= target:
            break

        if added_in_window == 0 or not repos:
            print(
                "[collect] aviso: janela sem repositórios novos; "
                "interrompendo antes da meta.",
                flush=True,
            )
            break

        # Nova janela abaixo do menor star count já obtido.
        min_stars = min(int(r["stars"]) for r in repos)
        if max_stars_exclusive is not None and min_stars >= max_stars_exclusive:
            print(
                "[collect] aviso: não foi possível baixar o teto de stars; "
                "interrompendo.",
                flush=True,
            )
            break
        max_stars_exclusive = min_stars
        print(
            f"[collect] janela esgotada com {len(repos)} válidos; "
            f"próximo teto stars:<{max_stars_exclusive}"
        )

    # Garante ordem por popularidade (janelas extras entram no fim).
    repos.sort(key=lambda r: int(r["stars"]), reverse=True)
    return repos[:target]
