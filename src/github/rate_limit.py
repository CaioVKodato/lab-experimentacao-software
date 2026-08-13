"""Utilitários de rateLimit da API GraphQL do GitHub."""

from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any

from src.github.config import RATE_LIMIT_MIN_REMAINING


def parse_reset_at(reset_at: str) -> float:
    """Converte resetAt (ISO-8601) em timestamp epoch (segundos)."""
    normalized = reset_at.replace("Z", "+00:00")
    dt = datetime.fromisoformat(normalized)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


def extract_rate_limit(body: dict[str, Any]) -> dict[str, Any] | None:
    """Extrai o objeto rateLimit do JSON GraphQL, se existir."""
    data = body.get("data") or {}
    rate_limit = data.get("rateLimit")
    return rate_limit if isinstance(rate_limit, dict) else None


def log_rate_limit(rate_limit: dict[str, Any]) -> None:
    print(
        "[rateLimit] "
        f"remaining={rate_limit.get('remaining')} "
        f"cost={rate_limit.get('cost')} "
        f"limit={rate_limit.get('limit')} "
        f"resetAt={rate_limit.get('resetAt')}"
    )


def wait_if_needed(rate_limit: dict[str, Any]) -> None:
    """
    Se o remaining estiver baixo, dorme até o horário de reset (+ margem).
    """
    remaining = rate_limit.get("remaining")
    reset_at = rate_limit.get("resetAt")
    if remaining is None or reset_at is None:
        return

    if remaining >= RATE_LIMIT_MIN_REMAINING:
        return

    reset_ts = parse_reset_at(reset_at)
    sleep_seconds = max(0.0, reset_ts - time.time()) + 1.0
    print(
        f"[rateLimit] remaining={remaining} "
        f"(limite interno={RATE_LIMIT_MIN_REMAINING}). "
        f"Aguardando {sleep_seconds:.0f}s até resetAt={reset_at}..."
    )
    time.sleep(sleep_seconds)
