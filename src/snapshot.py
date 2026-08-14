"""
Exporta o estado atual do GitHub Projects (v2) para CSV.

O Projects não guarda histórico de mudança de coluna via API. Cada execução
gera um arquivo novo em snapshots/, acumulado sprint a sprint (Labs 04 e 05).

Uso (na raiz do repositório):
    python -m src.snapshot
    python -m src.snapshot --sprint Lab01S01

O token precisa de leitura de Projects (classic: read:project).
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

from src.github import graphql_request
from src.github.config import (
    PROJECT_NUMBER,
    PROJECT_OWNER,
    PROJECT_STATUS_FIELD,
)

ROOT_DIR = Path(__file__).resolve().parent.parent
SNAPSHOTS_DIR = ROOT_DIR / "snapshots"

QUERY = """
query BoardSnapshot($login: String!, $number: Int!, $first: Int!, $after: String, $statusField: String!) {
  user(login: $login) {
    projectV2(number: $number) {
      title
      url
      items(first: $first, after: $after) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          id
          updatedAt
          content {
            __typename
            ... on Issue {
              number
              title
              state
              url
              assignees(first: 10) { nodes { login } }
              labels(first: 10) { nodes { name } }
            }
            ... on DraftIssue {
              title
            }
            ... on PullRequest {
              number
              title
              state
              url
            }
          }
          status: fieldValueByName(name: $statusField) {
            ... on ProjectV2ItemFieldSingleSelectValue {
              name
            }
          }
        }
      }
    }
  }
  rateLimit {
    cost
    remaining
    resetAt
    limit
  }
}
"""

FIELDNAMES = [
    "snapshot_at",
    "sprint",
    "project_title",
    "item_id",
    "item_type",
    "issue_number",
    "title",
    "status",
    "assignees",
    "state",
    "labels",
    "url",
    "item_updated_at",
]


def _join_logins(nodes: list[dict] | None) -> str:
    if not nodes:
        return ""
    return ";".join(node.get("login", "") for node in nodes if node.get("login"))


def _join_labels(nodes: list[dict] | None) -> str:
    if not nodes:
        return ""
    return ";".join(node.get("name", "") for node in nodes if node.get("name"))


def _row_from_node(
    node: dict,
    *,
    snapshot_at: str,
    sprint: str,
    project_title: str,
) -> dict[str, str]:
    content = node.get("content") or {}
    typename = content.get("__typename") or ""
    status = (node.get("status") or {}).get("name") or ""

    issue_number = content.get("number")
    return {
        "snapshot_at": snapshot_at,
        "sprint": sprint,
        "project_title": project_title,
        "item_id": node.get("id") or "",
        "item_type": typename,
        "issue_number": "" if issue_number is None else str(issue_number),
        "title": content.get("title") or "",
        "status": status,
        "assignees": _join_logins((content.get("assignees") or {}).get("nodes")),
        "state": content.get("state") or "",
        "labels": _join_labels((content.get("labels") or {}).get("nodes")),
        "url": content.get("url") or "",
        "item_updated_at": node.get("updatedAt") or "",
    }


def fetch_board_items() -> tuple[str, list[dict]]:
    """Lê todos os itens do Project v2 (paginado)."""
    items: list[dict] = []
    after: str | None = None
    project_title = ""

    while True:
        try:
            body = graphql_request(
                QUERY,
                {
                    "login": PROJECT_OWNER,
                    "number": PROJECT_NUMBER,
                    "first": 50,
                    "after": after,
                    "statusField": PROJECT_STATUS_FIELD,
                },
            )
        except RuntimeError as exc:
            message = str(exc).lower()
            if "resource not accessible" in message or "forbidden" in message:
                raise RuntimeError(
                    "Sem permissão para ler o GitHub Projects. "
                    "O token precisa do escopo classic `read:project` "
                    "(ou fine-grained: Projects Read)."
                ) from exc
            raise

        user = (body.get("data") or {}).get("user") or {}
        project = user.get("projectV2")
        if not project:
            raise RuntimeError(
                f"Project v2 não encontrado: {PROJECT_OWNER}/{PROJECT_NUMBER}. "
                "Confira GITHUB_PROJECT_OWNER e GITHUB_PROJECT_NUMBER."
            )

        project_title = project.get("title") or project_title
        connection = project["items"]
        for node in connection.get("nodes") or []:
            if node:
                items.append(node)

        page_info = connection["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        after = page_info["endCursor"]

    return project_title, items


def save_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[snapshot] {len(rows)} itens salvos em {path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exporta o GitHub Projects v2 para CSV (snapshot do Kanban)."
    )
    parser.add_argument(
        "--sprint",
        default="Lab01S01",
        help="Identificador da sprint (default: Lab01S01)",
    )
    args = parser.parse_args()

    now = datetime.now().astimezone()
    snapshot_at = now.isoformat(timespec="seconds")
    date_stamp = now.date().isoformat()
    out_path = SNAPSHOTS_DIR / f"{args.sprint.lower()}-{date_stamp}.csv"

    print(
        f"[snapshot] lendo Project {PROJECT_OWNER}/{PROJECT_NUMBER} "
        f"(campo {PROJECT_STATUS_FIELD})..."
    )
    try:
        project_title, nodes = fetch_board_items()
    except RuntimeError as exc:
        print(f"Erro no snapshot: {exc}", file=sys.stderr)
        sys.exit(1)

    rows = [
        _row_from_node(
            node,
            snapshot_at=snapshot_at,
            sprint=args.sprint,
            project_title=project_title,
        )
        for node in nodes
    ]
    save_csv(rows, out_path)
    print(f"[snapshot] projeto={project_title!r} sprint={args.sprint}")


if __name__ == "__main__":
    main()
