"""
Cliente HTTP genérico para a API GraphQL do GitHub.

Não usa bibliotecas específicas da API do GitHub (ex.: PyGithub).
A query GraphQL é escrita pelo grupo e enviada via HTTP POST.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

GRAPHQL_URL = "https://api.github.com/graphql"

# Carrega .env na raiz do repositório (um nível acima de src/)
_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_ROOT / ".env")


def get_token() -> str:
    """Lê o token do ambiente. Falha de forma clara se estiver ausente."""
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if not token or token.startswith("ghp_seu_token"):
        raise RuntimeError(
            "GITHUB_TOKEN não configurado. "
            "Copie .env.example para .env e preencha o token."
        )
    return token


def graphql_request(
    query: str,
    variables: dict[str, Any] | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    """
    Envia uma query GraphQL para o GitHub e devolve o JSON da resposta.

    Raises:
        RuntimeError: token ausente ou resposta HTTP/GraphQL com erro.
    """
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload: dict[str, Any] = {"query": query}
    if variables is not None:
        payload["variables"] = variables

    response = requests.post(
        GRAPHQL_URL,
        json=payload,
        headers=headers,
        timeout=timeout,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"HTTP {response.status_code} na API GraphQL: {response.text}"
        )

    body = response.json()
    if "errors" in body:
        raise RuntimeError(f"Erros GraphQL: {body['errors']}")

    return body


def main() -> None:
    """Teste mínimo de autenticação: viewer { login }."""
    query = """
    query {
      viewer {
        login
      }
    }
    """
    try:
        data = graphql_request(query)
    except RuntimeError as exc:
        print(f"Falha na autenticação: {exc}", file=sys.stderr)
        sys.exit(1)

    login = data["data"]["viewer"]["login"]
    print(f"Autenticação OK. Usuário autenticado: {login}")


if __name__ == "__main__":
    main()
