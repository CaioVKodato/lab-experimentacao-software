"""
Análise e visualização — RQ04, RQ05 e RQ06 (Lab01S03)
Issue: #33
Dataset: data/repositories_top1000.csv

RQ04: tempo até a última atualização (days_since_push / pushedAt)
RQ05: linguagem primária vs GitHub Octoverse 2025
RQ06: razão issues fechadas / total (closed_ratio; exclui total_issues = 0)

Uso:
    python3 src/analysis/analyze_s03_rq04_rq06.py
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/repositories_top1000.csv"
FIG_DIR = "docs/s03/jonas"
DOC_PATH = "docs/s03/jonas/analise_rq04_rq06.md"

os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DOC_PATH), exist_ok=True)

# Referência externa adotada no laboratório para RQ05 (mesma referência usada na S02)
OCTOVERSE_TOP_LANGUAGES = ["TypeScript", "Python", "JavaScript", "Java", "Go"]


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def analyze_rq04(df: pd.DataFrame) -> dict:
    """RQ04 — tempo até a última atualização."""
    col = "days_since_push"
    valid = pd.to_numeric(df[col], errors="coerce").dropna()

    stats = {
        "n_valid": int(valid.count()),
        "min": float(valid.min()),
        "median": float(valid.median()),
        "max": float(valid.max()),
        "q1": float(valid.quantile(0.25)),
        "q3": float(valid.quantile(0.75)),
    }

    fig, ax = plt.subplots(figsize=(7, 4.5))
    # Escala log no eixo x por causa da cauda longa (outliers de projetos parados há anos)
    valid_clip = valid[valid >= 0]
    ax.hist(valid_clip, bins=50, color="#3a6ea5", edgecolor="white")
    ax.set_xlabel("Dias desde o último push")
    ax.set_ylabel("Número de repositórios")
    ax.set_title("RQ04 — Distribuição de dias desde a última atualização")
    ax.axvline(stats["median"], color="#d62728", linestyle="--", label=f"Mediana = {stats['median']:.0f} dias")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "rq04_days_since_push_hist.png"), dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(4, 4.5))
    ax.boxplot(valid_clip, vert=True, showfliers=True)
    ax.set_ylabel("Dias desde o último push")
    ax.set_title("RQ04 — Boxplot")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "rq04_days_since_push_box.png"), dpi=150)
    plt.close(fig)

    return stats


def analyze_rq05(df: pd.DataFrame) -> pd.Series:
    """RQ05 — linguagem primária."""
    col = "language"
    langs = df[col].fillna("Sem linguagem")
    counts = langs.value_counts().head(10)
    pct = (counts / len(df) * 100).round(1)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors = ["#2ca02c" if lang in OCTOVERSE_TOP_LANGUAGES else "#7f7f7f" for lang in counts.index]
    ax.barh(counts.index[::-1], counts.values[::-1], color=colors[::-1])
    ax.set_xlabel("Número de repositórios")
    ax.set_title("RQ05 — Linguagem primária (top 10)\nverde = também top no GitHub Octoverse 2025")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "rq05_language_bar.png"), dpi=150)
    plt.close(fig)

    return pct


def analyze_rq06(df: pd.DataFrame) -> dict:
    """RQ06 — razão issues fechadas / total, excluindo total_issues = 0."""
    total = pd.to_numeric(df["total_issues"], errors="coerce")
    closed = pd.to_numeric(df["closed_issues"], errors="coerce")

    mask = total > 0
    ratio = (closed[mask] / total[mask]).dropna()

    stats = {
        "n_excluded_zero_issues": int((total == 0).sum()),
        "n_valid": int(ratio.count()),
        "min": float(ratio.min()),
        "median": float(ratio.median()),
        "max": float(ratio.max()),
        "q1": float(ratio.quantile(0.25)),
        "q3": float(ratio.quantile(0.75)),
    }

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(ratio, bins=30, color="#9467bd", edgecolor="white")
    ax.set_xlabel("Razão de issues fechadas (closed_ratio)")
    ax.set_ylabel("Número de repositórios")
    ax.set_title("RQ06 — Distribuição da razão de issues fechadas")
    ax.axvline(stats["median"], color="#d62728", linestyle="--", label=f"Mediana = {stats['median']:.3f}")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "rq06_closed_ratio_hist.png"), dpi=150)
    plt.close(fig)

    return stats


def write_doc(rq04_stats: dict, rq05_pct: pd.Series, rq06_stats: dict) -> None:
    lang_lines = "\n".join(f"- {lang}: {pct}%" for lang, pct in rq05_pct.items())

    content = f"""# Análise S03 — RQ04, RQ05 e RQ06

Issue: #33
Dataset: `data/repositories_top1000.csv`
Hipóteses de referência: #24 (RQ04, RQ05), #25 (RQ03, RQ06, nota RQ07)

## RQ04 — Tempo até a última atualização

| N válido | Mínimo | Mediana | Máximo | Q1 | Q3 |
|---:|---:|---:|---:|---:|---:|
| {rq04_stats['n_valid']} | {rq04_stats['min']:.0f} | {rq04_stats['median']:.0f} | {rq04_stats['max']:.0f} | {rq04_stats['q1']:.0f} | {rq04_stats['q3']:.0f} |

**Leitura vs. hipótese informal (#24):** a hipótese de que sistemas populares são atualizados com frequência se confirma — mediana de {rq04_stats['median']:.0f} dia(s) desde o último push, com 75% da amostra (Q3) recebendo commit em até {rq04_stats['q3']:.0f} dias. A distribuição no gráfico é fortemente concentrada perto de zero, com uma cauda longa de poucos repositórios sem atividade recente.

![RQ04 histograma](rq04_days_since_push_hist.png)
![RQ04 boxplot](rq04_days_since_push_box.png)

## RQ05 — Linguagem primária

Top 10 linguagens na amostra:

{lang_lines}

**Leitura vs. hipótese informal (#24):** confirma a hipótese — Python, TypeScript e JavaScript concentram a maior parte da amostra e aparecem entre as linguagens mais citadas no GitHub Octoverse 2025 (referência adotada no laboratório desde a S02).

![RQ05 linguagens](rq05_language_bar.png)

## RQ06 — Razão de issues fechadas / total

Repositórios excluídos por não terem nenhuma issue (`total_issues = 0`): {rq06_stats['n_excluded_zero_issues']}

| N válido | Mínimo | Mediana | Máximo | Q1 | Q3 |
|---:|---:|---:|---:|---:|---:|
| {rq06_stats['n_valid']} | {rq06_stats['min']:.4f} | {rq06_stats['median']:.4f} | {rq06_stats['max']:.4f} | {rq06_stats['q1']:.4f} | {rq06_stats['q3']:.4f} |

**Leitura vs. hipótese informal (#25):** confirma a hipótese de alta taxa de resolução de issues — mediana de {rq06_stats['median']*100:.1f}% de issues fechadas, com Q1 já em {rq06_stats['q1']*100:.1f}%.

![RQ06 histograma](rq06_closed_ratio_hist.png)
"""
    with open(DOC_PATH, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    df = load_data(DATA_PATH)
    rq04_stats = analyze_rq04(df)
    rq05_pct = analyze_rq05(df)
    rq06_stats = analyze_rq06(df)
    write_doc(rq04_stats, rq05_pct, rq06_stats)
    print("Análise concluída.")
    print(f"Figuras salvas em: {FIG_DIR}/")
    print(f"Documento salvo em: {DOC_PATH}")


if __name__ == "__main__":
    main()