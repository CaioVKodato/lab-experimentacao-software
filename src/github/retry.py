"""Política de retry / backoff para chamadas HTTP."""

from __future__ import annotations

import time


def is_retryable_http(status_code: int) -> bool:
    """Indica se o status HTTP merece nova tentativa."""
    return status_code in {429, 502, 503, 504} or status_code >= 500


def backoff_seconds(attempt: int, retry_after: str | None = None) -> float:
    """
    Calcula o tempo de espera antes da próxima tentativa.

    Prefere o header Retry-After quando numérico; senão usa backoff exponencial.
    """
    if retry_after and retry_after.isdigit():
        return float(retry_after)
    return float(min(2 ** (attempt - 1), 60))


def sleep_before_retry(attempt: int, reason: str, retry_after: str | None = None) -> None:
    """Dorme e registra o motivo do retry."""
    sleep_seconds = backoff_seconds(attempt, retry_after)
    print(f"[retry] {reason}. Nova tentativa em {sleep_seconds:.0f}s...")
    time.sleep(sleep_seconds)
