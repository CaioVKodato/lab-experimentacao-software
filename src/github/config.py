"""Configuração e autenticação (token via .env)."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Raiz do repositório: src/github/config.py -> sobe 3 níveis
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

GRAPHQL_URL = "https://api.github.com/graphql"
RATE_LIMIT_MIN_REMAINING = 50
DEFAULT_MAX_RETRIES = 5
DEFAULT_TIMEOUT = 30

# GitHub Projects v2 do grupo (snapshot do Kanban)
PROJECT_OWNER = os.getenv("GITHUB_PROJECT_OWNER", "CaioVKodato")
PROJECT_NUMBER = int(os.getenv("GITHUB_PROJECT_NUMBER", "6"))
PROJECT_STATUS_FIELD = os.getenv("GITHUB_PROJECT_STATUS_FIELD", "Status")


def get_token() -> str:
    """Lê o token do ambiente. Falha de forma clara se estiver ausente."""
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if not token or token.startswith("ghp_seu_token"):
        raise RuntimeError(
            "GITHUB_TOKEN não configurado. "
            "Copie .env.example para .env e preencha o token."
        )
    return token
