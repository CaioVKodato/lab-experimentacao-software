"""
Cliente HTTP genérico para a API GraphQL do GitHub.

Não usa bibliotecas específicas da API do GitHub (ex.: PyGithub).
A query GraphQL é escrita pelo grupo e enviada via HTTP POST.
"""

from __future__ import annotations

from typing import Any

import requests

from src.github.config import (
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    GRAPHQL_URL,
    get_token,
)
from src.github.rate_limit import extract_rate_limit, log_rate_limit, wait_if_needed
from src.github.retry import is_retryable_http, sleep_before_retry


def graphql_request(
    query: str,
    variables: dict[str, Any] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    max_retries: int = DEFAULT_MAX_RETRIES,
) -> dict[str, Any]:
    """
    Envia uma query GraphQL com retry/backoff e tratamento de rateLimit.

    Inclua o campo `rateLimit { remaining resetAt cost limit }` na query
    para que o cliente possa pausar automaticamente quando o limite estiver baixo.

    Raises:
        RuntimeError: token ausente ou falha após esgotar as tentativas.
    """
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload: dict[str, Any] = {"query": query}
    if variables is not None:
        payload["variables"] = variables

    last_error: Exception | None = None

    for attempt in range(1, max_retries + 1):
        try:
            print(f"[graphql] tentativa {attempt}/{max_retries}...")
            response = requests.post(
                GRAPHQL_URL,
                json=payload,
                headers=headers,
                timeout=timeout,
            )

            if is_retryable_http(response.status_code):
                sleep_before_retry(
                    attempt,
                    reason=f"HTTP {response.status_code}",
                    retry_after=response.headers.get("Retry-After"),
                )
                continue

            if response.status_code != 200:
                raise RuntimeError(
                    f"HTTP {response.status_code} na API GraphQL: {response.text}"
                )

            body = response.json()

            if "errors" in body:
                messages = " ".join(
                    str(err.get("message", err)) for err in body["errors"]
                )
                if "rate limit" in messages.lower():
                    sleep_before_retry(attempt, reason="rate limit GraphQL")
                    continue
                raise RuntimeError(f"Erros GraphQL: {body['errors']}")

            rate_limit = extract_rate_limit(body)
            if rate_limit:
                log_rate_limit(rate_limit)
                wait_if_needed(rate_limit)

            print("[graphql] sucesso")
            return body

        except (requests.Timeout, requests.ConnectionError) as exc:
            last_error = exc
            sleep_before_retry(attempt, reason=f"erro de rede ({exc})")

    raise RuntimeError(
        f"Falha na API GraphQL após {max_retries} tentativas. "
        f"Último erro: {last_error}"
    )
