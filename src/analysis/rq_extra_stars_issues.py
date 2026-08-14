"""
RQ Extra: popularidade (stars) se correlaciona com % de issues fechadas?

Correlaciona `stars` com `closed_ratio` nos 100 repositórios coletados,
excluindo repos com `total_issues = 0` (sem histórico de issues).

Uso:
    python -m src.analysis.rq_extra_stars_issues
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
DOCS_DIR = ROOT_DIR / "docs"


def load_filtered(csv_path: Path) -> tuple[list[float], list[float], list[str]]:
    """Carrega stars e closed_ratio, excluindo repos sem issues."""
    stars, ratios, excluded = [], [], []
    with csv_path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if int(row["total_issues"]) == 0:
                excluded.append(row["name"])
                continue
            stars.append(float(row["stars"]))
            ratios.append(float(row["closed_ratio"]))
    return stars, ratios, excluded


def pearson(x: list[float], y: list[float]) -> float:
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    den = (sum((xi - mx) ** 2 for xi in x) * sum((yi - my) ** 2 for yi in y)) ** 0.5
    return num / den if den else 0.0


def spearman(x: list[float], y: list[float]) -> float:
    from scipy.stats import spearmanr
    r, _ = spearmanr(x, y)
    return float(r)


def plot_scatter(stars: list[float], ratios: list[float], out: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(stars, ratios, alpha=0.6, edgecolors="steelblue", facecolors="lightblue", s=60)
    ax.set_xlabel("Estrelas (stars)", fontsize=12)
    ax.set_ylabel("Razão issues fechadas (closed_ratio)", fontsize=12)
    ax.set_title("RQ Extra: Stars vs. Closed-Issue Ratio\n(100 repos mais populares — excluídos os sem issues)", fontsize=13)
    ax.set_ylim(-0.05, 1.05)

    r_p = pearson(stars, ratios)
    r_s = spearman(stars, ratios)
    ax.text(
        0.97, 0.04,
        f"Pearson r = {r_p:.3f}\nSpearman ρ = {r_s:.3f}\nn = {len(stars)}",
        transform=ax.transAxes,
        ha="right", va="bottom",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="gray", alpha=0.8),
    )

    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"[rq_extra] grafico salvo em {out}")


def main() -> None:
    csv_path = DATA_DIR / "repositories.csv"
    if not csv_path.exists():
        print("CSV nao encontrado. Execute `python -m src.collect` primeiro.", file=sys.stderr)
        sys.exit(1)

    stars, ratios, excluded = load_filtered(csv_path)
    n_total = len(stars) + len(excluded)

    r_p = pearson(stars, ratios)
    r_s = spearman(stars, ratios)

    print(f"Total de repos          : {n_total}")
    print(f"Excluidos (total_issues=0): {len(excluded)}")
    print(f"Amostra usada           : {len(stars)}")
    print(f"Pearson  r              : {r_p:+.4f}")
    print(f"Spearman rho            : {r_s:+.4f}")
    print()

    if abs(r_s) < 0.10:
        interpretacao = "correlacao praticamente nula"
    elif abs(r_s) < 0.30:
        direcao = "positiva" if r_s > 0 else "negativa"
        interpretacao = f"correlacao fraca {direcao}"
    else:
        direcao = "positiva" if r_s > 0 else "negativa"
        interpretacao = f"correlacao moderada/forte {direcao}"

    print(f"Interpretacao: {interpretacao}")
    print()
    print("Repos excluidos (total_issues = 0):")
    for name in excluded:
        print(f"  {name}")

    plot_scatter(stars, ratios, DOCS_DIR / "rq_extra_stars_vs_closed_ratio.png")


if __name__ == "__main__":
    main()
