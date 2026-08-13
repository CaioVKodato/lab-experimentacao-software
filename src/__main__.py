"""CLI de teste: autenticação + rateLimit (`python -m src`)."""

from __future__ import annotations

import sys

from src.github import graphql_request


def main() -> None:
    query = """
    query {
      viewer {
        login
      }
      rateLimit {
        cost
        remaining
        resetAt
        limit
      }
    }
    """
    try:
        data = graphql_request(query)
    except RuntimeError as exc:
        print(f"Falha na requisição: {exc}", file=sys.stderr)
        sys.exit(1)

    login = data["data"]["viewer"]["login"]
    rate = data["data"]["rateLimit"]
    print(f"Autenticação OK. Usuário autenticado: {login}")
    print(
        f"rateLimit OK. remaining={rate['remaining']} "
        f"limit={rate['limit']} resetAt={rate['resetAt']}"
    )


if __name__ == "__main__":
    main()
