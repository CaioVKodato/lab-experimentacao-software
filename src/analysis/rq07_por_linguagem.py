"""
RQ07: Sistemas escritos em linguagens mais populares recebem mais contribuição
externa, lançam mais releases e são atualizados com mais frequência?

Cruza RQ02 (merged_prs), RQ03 (releases) e RQ04 (days_since_push)
por linguagem primária, comparando top-10 Octoverse 2025 vs demais.

Fonte: GitHub Octoverse 2025 (Issue #9)
Dados: data/repositories_top1000.csv

Uso:
    python -m src.analysis.rq07_por_linguagem
"""

from __future__ import annotations

import csv
import statistics
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR  = ROOT_DIR / "data"
DOCS_DIR  = ROOT_DIR / "docs"

CSV_FILE = DATA_DIR / "repositories_top1000.csv"

OCTOVERSE_TOP10 = [
    "TypeScript", "Python", "JavaScript", "Java",
    "C#", "C++", "Shell", "Go", "PHP", "Rust",
]

METRICS = {
    "merged_prs":      "PRs aceitas (RQ02)",
    "releases":        "Releases (RQ03)",
    "days_since_push": "Dias desde último push (RQ04)",
}


def load(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def group_by_language(rows: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for r in rows:
        lang = r["language"].strip() if r["language"].strip() else "(sem linguagem)"
        groups.setdefault(lang, []).append(r)
    return groups


def med(rows: list[dict], col: str) -> float:
    vals = [float(r[col]) for r in rows]
    return statistics.median(vals) if vals else float("nan")


def build_table(groups: dict[str, list[dict]]) -> list[dict]:
    table = []
    for lang, repos in groups.items():
        table.append({
            "language":      lang,
            "n":             len(repos),
            "popular":       lang in OCTOVERSE_TOP10,
            "med_prs":       med(repos, "merged_prs"),
            "med_releases":  med(repos, "releases"),
            "med_days_push": med(repos, "days_since_push"),
        })
    return sorted(table, key=lambda r: (not r["popular"], -r["n"]))


def print_table(table: list[dict]) -> None:
    header = f"{'Linguagem':<22} {'n':>4}  {'Pop':>3}  {'med_prs':>9}  {'med_rel':>7}  {'med_dias':>8}"
    print(header)
    print("-" * len(header))
    for row in table:
        pop = "Sim" if row["popular"] else "Nao"
        print(
            f"{row['language']:<22} {row['n']:>4}  {pop:>3}  "
            f"{row['med_prs']:>9.1f}  {row['med_releases']:>7.1f}  {row['med_days_push']:>8.1f}"
        )


def summary(groups: dict[str, list[dict]]) -> dict:
    pop   = [r for lang, repos in groups.items() if lang in OCTOVERSE_TOP10 for r in repos]
    other = [r for lang, repos in groups.items() if lang not in OCTOVERSE_TOP10 for r in repos]
    result = {}
    for label, repos in [("Populares (top-10 Octoverse)", pop), ("Nao populares / sem linguagem", other)]:
        result[label] = {
            "n":             len(repos),
            "med_prs":       med(repos, "merged_prs"),
            "med_releases":  med(repos, "releases"),
            "med_days_push": med(repos, "days_since_push"),
        }
    return result


def plot(table: list[dict], out_dir: Path) -> None:
    # filtra linguagens com pelo menos 5 repos e exclui "(sem linguagem)"
    filtered = [r for r in table if r["n"] >= 5 and r["language"] != "(sem linguagem)"]
    langs = [r["language"] for r in filtered]
    colors = ["steelblue" if r["popular"] else "lightcoral" for r in filtered]

    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    fig.suptitle("RQ07 — Medianas por linguagem primária (≥5 repos)\n"
                 "Azul = top-10 Octoverse 2025 | Vermelho = demais", fontsize=13)

    for ax, (col, label) in zip(axes, [
        ("med_prs",       "Mediana PRs aceitas (RQ02)"),
        ("med_releases",  "Mediana releases (RQ03)"),
        ("med_days_push", "Mediana dias desde push (RQ04)"),
    ]):
        values = [r[col] for r in filtered]
        bars = ax.barh(langs, values, color=colors)
        ax.set_xlabel(label, fontsize=10)
        ax.invert_yaxis()
        for bar, val in zip(bars, values):
            ax.text(bar.get_width() + max(values) * 0.01, bar.get_y() + bar.get_height() / 2,
                    f"{val:.0f}", va="center", fontsize=8)

    fig.tight_layout()
    out = out_dir / "rq07_por_linguagem.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[rq07] grafico salvo em {out}")


def main() -> None:
    rows   = load(CSV_FILE)
    groups = group_by_language(rows)
    table  = build_table(groups)

    print("=== RQ07: medianas por linguagem primaria (1000 repos) ===\n")
    print_table(table)

    print("\n=== Resumo: populares vs. demais ===")
    s = summary(groups)
    hdr = f"{'Grupo':<32} {'n':>4}  {'med_prs':>9}  {'med_rel':>7}  {'med_dias':>8}"
    print(hdr)
    print("-" * len(hdr))
    for label, vals in s.items():
        print(
            f"{label:<32} {vals['n']:>4}  {vals['med_prs']:>9.1f}  "
            f"{vals['med_releases']:>7.1f}  {vals['med_days_push']:>8.1f}"
        )

    plot(table, DOCS_DIR)


if __name__ == "__main__":
    main()
