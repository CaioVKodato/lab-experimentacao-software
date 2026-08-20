"""CLI: python -m src.collect [--n 1000] [--out caminho.csv]"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.collect.constants import DEFAULT_LIMIT, MAX_SEARCH_RESULTS
from src.collect.export import default_output_path, save_csv
from src.collect.fetch import fetch_top_repos


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Coleta os N repositórios mais estrelados do GitHub (GraphQL) "
            "e gera CSV com métricas das RQ01–RQ07."
        )
    )
    parser.add_argument(
        "--n",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Quantidade de repositórios (default: {DEFAULT_LIMIT}, máx.: {MAX_SEARCH_RESULTS})",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Caminho do CSV de saída (default depende de --n)",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    n = min(max(args.n, 1), MAX_SEARCH_RESULTS)
    out_path = args.out or default_output_path(n)

    print(f"[collect] buscando os {n} repositórios mais populares no GitHub...")
    print(f"[collect] saída: {out_path}")
    try:
        repos = fetch_top_repos(n)
    except RuntimeError as exc:
        print(f"Erro na coleta: {exc}", file=sys.stderr)
        sys.exit(1)

    if len(repos) < n:
        print(
            f"[collect] aviso: obtidos {len(repos)} de {n} pedidos "
            "(Search API ou paginação sem hasNextPage).",
            file=sys.stderr,
        )

    save_csv(repos, out_path)
    print("[collect] concluído.")


if __name__ == "__main__":
    main()
