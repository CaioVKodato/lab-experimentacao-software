"""
Validação dos campos RQ04–RQ06 em amostra de 8 repositórios (Issue #8).

Consulta GraphQL via cliente do grupo e compara com data/repositories.csv.
Também imprime updatedAt vs pushedAt para justificar a métrica da RQ04.

Uso:
    python validate_rq04_rq06.py
"""

from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

from src.github import graphql_request

ROOT_DIR = Path(__file__).resolve().parent
CSV_PATH = ROOT_DIR / "data" / "repositories.csv"

# Amostra 8/10: mistura de linguagens, issues desabilitadas, linguagem nula e push antigo.
SAMPLE = [
    ("freeCodeCamp", "freeCodeCamp"),
    ("public-apis", "public-apis"),
    ("torvalds", "linux"),
    ("vuejs", "vue"),
    ("sindresorhus", "awesome"),
    ("donnemartin", "system-design-primer"),
    ("golang", "go"),
    ("kubernetes", "kubernetes"),
]


def _days_since(iso_date: str) -> int:
    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - dt).days


def _closed_ratio(closed: int, total: int) -> float | None:
    return round(closed / total, 4) if total > 0 else None


def _build_query() -> str:
    aliases = []
    for i, (owner, name) in enumerate(SAMPLE):
        aliases.append(
            f"""
  r{i}: repository(owner: "{owner}", name: "{name}") {{
    nameWithOwner
    updatedAt
    pushedAt
    hasIssuesEnabled
    primaryLanguage {{ name }}
    closedIssues: issues(states: CLOSED) {{ totalCount }}
    openIssues: issues(states: OPEN) {{ totalCount }}
  }}"""
        )
    joined = "\n".join(aliases)
    return f"""
query ValidateRQ0406 {{
{joined}
  rateLimit {{
    cost
    remaining
    resetAt
    limit
  }}
}}
"""


def _load_csv() -> dict[str, dict[str, str]]:
    names = {f"{owner}/{repo}" for owner, repo in SAMPLE}
    data: dict[str, dict[str, str]] = {}
    with CSV_PATH.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["name"] in names:
                data[row["name"]] = row
    return data


def main() -> None:
    csv_data = _load_csv()
    try:
        body = graphql_request(_build_query())
    except RuntimeError as exc:
        print(f"Falha na requisição: {exc}", file=sys.stderr)
        sys.exit(1)

    payload = body["data"]
    print(
        f"{'Repositório':<42} {'Campo':<18} {'CSV':>22}  {'API':>22}  {'OK?'}"
    )
    print("-" * 112)

    all_ok = True
    print("\n--- RQ04: updatedAt vs pushedAt (decisão da métrica) ---\n")

    for i, (owner, repo) in enumerate(SAMPLE):
        name = f"{owner}/{repo}"
        api = payload[f"r{i}"]
        csv_row = csv_data.get(name, {})

        language = (api["primaryLanguage"] or {}).get("name", "")
        closed = api["closedIssues"]["totalCount"]
        open_ = api["openIssues"]["totalCount"]
        total = closed + open_
        ratio = _closed_ratio(closed, total)

        pushed_days = _days_since(api["pushedAt"])
        updated_days = _days_since(api["updatedAt"])

        print(
            f"{name}: pushedAt={api['pushedAt']} ({pushed_days}d) | "
            f"updatedAt={api['updatedAt']} ({updated_days}d) | "
            f"hasIssues={api['hasIssuesEnabled']}"
        )

        checks = [
            ("pushed_at", csv_row.get("pushed_at", ""), api["pushedAt"]),
            ("language", csv_row.get("language", ""), language),
            ("closed_issues", csv_row.get("closed_issues", ""), str(closed)),
            ("open_issues", csv_row.get("open_issues", ""), str(open_)),
            ("closed_ratio", csv_row.get("closed_ratio", ""), str(ratio)),
        ]

        for field, csv_val, api_val in checks:
            ok = "OK" if str(csv_val) == str(api_val) else "DIVERGE"
            if ok != "OK":
                all_ok = False
            print(
                f"{name:<42} {field:<18} {csv_val:>22}  {api_val:>22}  {ok}"
            )
        print()

    rate = payload["rateLimit"]
    print(f"rateLimit cost={rate['cost']} remaining={rate['remaining']}")
    print("Resultado:", "TODOS OK" if all_ok else "HA DIVERGENCIAS")
    print(
        "Nota: DIVERGE em issues/ratio é esperado se o CSV foi gerado horas "
        "antes (repositórios muito ativos). pushed_at e language devem bater "
        "salvo novo push."
    )


if __name__ == "__main__":
    main()
