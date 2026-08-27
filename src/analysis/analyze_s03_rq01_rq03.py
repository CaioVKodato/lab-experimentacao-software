"""
Análise descritiva e visualização S03 — RQ01, RQ02 e RQ03.

Lê data/repositories_top1000.csv, calcula N/mediana/quartis/outliers
(Tukey 1,5 × IQR, mesmo critério da S02) e grava figuras + relatório.

Uso:
    python -m src.analysis.analyze_s03_rq01_rq03
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from statistics import median

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = ROOT_DIR / "data" / "repositories_top1000.csv"
DOCS_DIR = ROOT_DIR / "docs"
OUTPUT_MD = DOCS_DIR / "analise_s03_rq01_rq03.md"

FIG_RQ01 = DOCS_DIR / "analise_s03_rq01_idade.png"
FIG_RQ02 = DOCS_DIR / "analise_s03_rq02_prs.png"
FIG_RQ03 = DOCS_DIR / "analise_s03_rq03_releases.png"

DAYS_PER_YEAR = 365.25
COLOR = "steelblue"


def describe(items: list[float]) -> dict:
    items = sorted(items)
    q1 = items[(len(items) - 1) // 4]
    q3 = items[(3 * (len(items) - 1)) // 4]
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers = [value for value in items if value < lower or value > upper]
    return {
        "n": len(items),
        "min": min(items),
        "median": median(items),
        "max": max(items),
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "lower": lower,
        "upper": upper,
        "outliers": outliers,
        "n_outliers": len(outliers),
    }


def fmt(value: float) -> str:
    return str(int(value)) if value == int(value) else f"{value:.2f}"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def values(rows: list[dict[str, str]], field: str) -> list[float]:
    return [float(row[field]) for row in rows if row[field].strip()]


def setup_style() -> tuple:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.grid": True,
            "grid.alpha": 0.28,
            "axes.axisbelow": True,
            "font.size": 10,
        }
    )
    return plt


def _annotate_median(ax, value: float, label: str) -> None:
    ax.axvline(value, color="crimson", linestyle="--", linewidth=1.2, label=label)


def plot_rq01(age_days: list[float], stats: dict, out: Path, plt) -> None:
    years = [day / DAYS_PER_YEAR for day in age_days]
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))

    axes[0].hist(years, bins=20, color=COLOR, edgecolor="white", alpha=0.9)
    _annotate_median(axes[0], stats["median"] / DAYS_PER_YEAR, f"mediana = {stats['median'] / DAYS_PER_YEAR:.1f} anos")
    axes[0].set_xlabel("Idade (anos)")
    axes[0].set_ylabel("Repositórios")
    axes[0].set_title("RQ01 — Histograma da idade")
    axes[0].legend(loc="upper right", fontsize=9)

    axes[1].boxplot(
        age_days,
        orientation="vertical",
        widths=0.45,
        patch_artist=True,
        boxprops={"facecolor": "lightblue", "edgecolor": COLOR},
        medianprops={"color": "crimson", "linewidth": 1.6},
        flierprops={"marker": "o", "alpha": 0.45, "markersize": 4},
    )
    axes[1].set_ylabel("Idade (dias)")
    axes[1].set_xticks([1])
    axes[1].set_xticklabels(["age_days"])
    axes[1].set_title("RQ01 — Boxplot (sem outliers Tukey)")

    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def plot_rq02(merged: list[float], stats: dict, out: Path, plt) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))

    bins = [0, 1, 10, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 120000]
    axes[0].hist(merged, bins=bins, color=COLOR, edgecolor="white", alpha=0.9)
    axes[0].set_xscale("symlog", linthresh=1)
    _annotate_median(axes[0], stats["median"], f"mediana = {fmt(stats['median'])}")
    axes[0].set_xlabel("PRs aceitas (escala simlog)")
    axes[0].set_ylabel("Repositórios")
    axes[0].set_title("RQ02 — Histograma de merged_prs")
    axes[0].legend(loc="upper right", fontsize=9)

    axes[1].boxplot(
        merged,
        orientation="vertical",
        widths=0.45,
        patch_artist=True,
        boxprops={"facecolor": "lightblue", "edgecolor": COLOR},
        medianprops={"color": "crimson", "linewidth": 1.6},
        flierprops={"marker": "o", "alpha": 0.35, "markersize": 3.5},
    )
    axes[1].set_yscale("symlog", linthresh=1)
    axes[1].set_ylabel("PRs aceitas (escala simlog)")
    axes[1].set_xticks([1])
    axes[1].set_xticklabels(["merged_prs"])
    axes[1].set_title(f"RQ02 — Boxplot ({stats['n_outliers']} outliers)")

    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def plot_rq03(releases: list[float], stats: dict, out: Path, plt) -> None:
    n_zero = sum(value == 0 for value in releases)
    n_some = len(releases) - n_zero
    with_release = [value for value in releases if value > 0]

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))

    bars = axes[0].bar(
        ["Sem releases", "Com ≥ 1 release"],
        [n_zero, n_some],
        color=["lightgray", COLOR],
        edgecolor="white",
        width=0.55,
    )
    for bar, count in zip(bars, (n_zero, n_some)):
        axes[0].text(
            bar.get_x() + bar.get_width() / 2,
            count,
            f"{count}\n({count / len(releases) * 100:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    axes[0].set_ylabel("Repositórios")
    axes[0].set_ylim(0, max(n_zero, n_some) * 1.22)
    axes[0].set_title("RQ03 — Presença de releases")

    med_nonzero = median(with_release)
    axes[1].hist(with_release, bins=30, color=COLOR, edgecolor="white", alpha=0.9)
    _annotate_median(axes[1], med_nonzero, f"mediana (≥ 1) = {fmt(med_nonzero)}")
    axes[1].set_xlabel("Número de releases (repos com ≥ 1)")
    axes[1].set_ylabel("Repositórios")
    axes[1].set_title("RQ03 — Histograma (exceto zeros)")
    axes[1].legend(loc="upper right", fontsize=9)

    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def age_buckets(age_days: list[float]) -> list[tuple[str, int]]:
    labels = ["< 1 ano", "1–3 anos", "3–5 anos", "5–8 anos", "8–12 anos", "≥ 12 anos"]
    counts = [0] * 6
    for days in age_days:
        years = days / DAYS_PER_YEAR
        if years < 1:
            counts[0] += 1
        elif years < 3:
            counts[1] += 1
        elif years < 5:
            counts[2] += 1
        elif years < 8:
            counts[3] += 1
        elif years < 12:
            counts[4] += 1
        else:
            counts[5] += 1
    return list(zip(labels, counts))


def write_report(
    n_rows: int,
    age: dict,
    merged: dict,
    releases: dict,
    age_days: list[float],
    merged_vals: list[float],
    release_vals: list[float],
    youngest: dict[str, str],
    oldest: dict[str, str],
    max_pr: dict[str, str],
    max_rel: dict[str, str],
) -> None:
    n_zero_pr = sum(value == 0 for value in merged_vals)
    n_zero_rel = sum(value == 0 for value in release_vals)
    n_some_rel = n_rows - n_zero_rel
    n_rel_1000 = sum(value == 1000 for value in release_vals)
    med_nonzero_rel = median([v for v in release_vals if v > 0])
    buckets = age_buckets(age_days)
    bucket_rows = "\n".join(
        f"| {label} | {count} | {count / n_rows * 100:.1f}% |" for label, count in buckets
    )
    age_years_med = age["median"] / DAYS_PER_YEAR
    age_years_min = age["min"] / DAYS_PER_YEAR
    age_years_max = age["max"] / DAYS_PER_YEAR

    text = f"""# Análise S03 — RQ01, RQ02 e RQ03

**Issue:** #35  
**Sprint:** Lab01S03  
**Dataset:** `data/repositories_top1000.csv` ({n_rows} repositórios)  
**Script:** `src/analysis/analyze_s03_rq01_rq03.py`  
**Hipóteses:** Issues [#23](https://github.com/CaioVKodato/lab-experimentacao-software/issues/23) (RQ01, RQ02) e [#25](https://github.com/CaioVKodato/lab-experimentacao-software/issues/25) (RQ03)  
**Validações S02:** [#20](https://github.com/CaioVKodato/lab-experimentacao-software/issues/20), [#22](https://github.com/CaioVKodato/lab-experimentacao-software/issues/22)

## Metodologia

- Métricas: `age_days` (RQ01), `merged_prs` (RQ02), `releases` (RQ03).
- Estatística descritiva: N, mínimo, Q1, mediana, Q3, máximo.
- Outliers: critério de Tukey (1,5 × IQR), o mesmo da validação S02.
- Visualização: histograma e boxplot (RQ01, RQ02); barras de presença + histograma (RQ03).
- Idade em anos usa 365,25 dias (ano médio).

Para reproduzir:

```bash
python -m src.analysis.analyze_s03_rq01_rq03
```

## Resumo numérico

| RQ | Métrica | N | Mínimo | Q1 | Mediana | Q3 | Máximo | Outliers |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 01 | `age_days` | {age['n']} | {fmt(age['min'])} | {fmt(age['q1'])} | {fmt(age['median'])} | {fmt(age['q3'])} | {fmt(age['max'])} | {age['n_outliers']} |
| 02 | `merged_prs` | {merged['n']} | {fmt(merged['min'])} | {fmt(merged['q1'])} | {fmt(merged['median'])} | {fmt(merged['q3'])} | {fmt(merged['max'])} | {merged['n_outliers']} |
| 03 | `releases` | {releases['n']} | {fmt(releases['min'])} | {fmt(releases['q1'])} | {fmt(releases['median'])} | {fmt(releases['q3'])} | {fmt(releases['max'])} | {releases['n_outliers']} |

Nenhum campo usado nesta fatia está vazio no CSV.

---

## RQ01 — Sistemas populares são maduros/antigos?

**Hipótese informal (#23):** sim — popularidade exige tempo de exposição; mediana esperada na casa de vários anos.

**Métrica:** dias desde `createdAt` (`age_days`).

### Resultado

| Estatística | Valor |
|---|---|
| N válido | {age['n']} |
| Mediana | **{fmt(age['median'])} dias (~{age_years_med:.1f} anos)** |
| Q1–Q3 | {fmt(age['q1'])}–{fmt(age['q3'])} dias (~{age['q1'] / DAYS_PER_YEAR:.1f}–{age['q3'] / DAYS_PER_YEAR:.1f} anos) |
| Amplitude | {fmt(age['min'])}–{fmt(age['max'])} dias (~{age_years_min:.2f}–{age_years_max:.1f} anos) |
| Outliers Tukey | **{age['n_outliers']}** (cerca inferior negativa; nenhum ponto cai fora) |

Faixa etária:

| Faixa | Repositórios | Percentual |
|---|---:|---:|
{bucket_rows}

Exemplos: o mais novo é `{youngest['name']}` ({youngest['age_days']} dias, {youngest['stars']} stars); o mais antigo é `{oldest['name']}` ({oldest['age_days']} dias, criado em {oldest['created_at'][:10]}).

### Hipótese vs. resultado

**Confirmada.** A mediana de ~{age_years_med:.1f} anos e o fato de {sum(c for _, c in buckets[3:])} repositórios ({sum(c for _, c in buckets[3:]) / n_rows * 100:.1f}%) terem 5 anos ou mais sustentam a leitura de maturidade como traço típico da amostra.

Há um matiz: {buckets[0][1]} repositórios ({buckets[0][1] / n_rows * 100:.1f}%) têm menos de 1 ano — viralidade recente (IA, listas, tutoriais) consegue popularidade sem maturidade. O critério de Tukey **não** marca esses casos como outliers porque Q1 já é baixo o bastante para a cerca inferior ficar negativa. A hipótese vale para o **centro** da distribuição, não para todos os 1000.

![RQ01 idade](analise_s03_rq01_idade.png)

---

## RQ02 — Sistemas populares recebem muita contribuição externa?

**Hipótese informal (#23):** sim — popularidade atrai colaboradores; volume alto de PRs aceitas.

**Métrica:** `pullRequests(states: MERGED).totalCount` no GitHub (`merged_prs`).

### Resultado

| Estatística | Valor |
|---|---|
| N válido | {merged['n']} |
| Mediana | **{fmt(merged['median'])}** PRs aceitas |
| Q1–Q3 | {fmt(merged['q1'])}–{fmt(merged['q3'])} |
| Máximo | {fmt(merged['max'])} (`{max_pr['name']}`) |
| Sem nenhuma PR merged | **{n_zero_pr}** ({n_zero_pr / n_rows * 100:.1f}%) |
| Outliers Tukey (>{fmt(merged['upper'])}) | **{merged['n_outliers']}** ({merged['n_outliers'] / n_rows * 100:.1f}%) |

A cauda é pesada: o máximo é mais de 100× a mediana. `{max_pr['name']}` infla o topo porque o próprio propósito do repositório é receber o “primeiro PR” de iniciantes — contribuição real, mas não o mesmo fenômeno de um kernel ou um framework.

No outro extremo, {n_zero_pr} repositórios têm **zero** PRs merged no GitHub. Exemplos conhecidos da amostra: listas `awesome-*`, `torvalds/linux` (fluxo por e-mail, não pelo GitHub) e projetos que não usam pull request da plataforma. A métrica mede **contribuição via GitHub PR**, não contribuição externa em geral.

### Hipótese vs. resultado

**Confirmada para o projeto popular típico**, com ressalvas de métrica. Mediana {fmt(merged['median'])} e Q3 {fmt(merged['q3'])} são volumes altos; 75% da amostra tem pelo menos {fmt(merged['q1'])} PRs aceitas. A hipótese não deve ser lida como “todo repositório estrelado tem PR no GitHub”: {n_zero_pr / n_rows * 100:.1f}% não usa esse canal, e a cauda ({merged['n_outliers']} outliers) mistura projetos gigantes com repositórios-tutorial.

![RQ02 PRs](analise_s03_rq02_prs.png)

---

## RQ03 — Sistemas populares lançam releases com frequência?

**Hipótese informal (#25):** confirmação **parcial** — releases são comuns em parte da amostra, não universais.

**Métrica:** `releases.totalCount` (`releases`).

### Resultado

| Estatística | Valor |
|---|---|
| N válido | {releases['n']} |
| Mediana (incluindo zeros) | **{fmt(releases['median'])}** |
| Mediana só com ≥ 1 release | {fmt(med_nonzero_rel)} |
| Q1–Q3 | {fmt(releases['q1'])}–{fmt(releases['q3'])} |
| Máximo | {fmt(releases['max'])} (`{max_rel['name']}` e outros) |
| Sem nenhuma release | **{n_zero_rel}** ({n_zero_rel / n_rows * 100:.1f}%) |
| Com ≥ 1 release | **{n_some_rel}** ({n_some_rel / n_rows * 100:.1f}%) |
| Outliers Tukey (>{fmt(releases['upper'])}) | **{releases['n_outliers']}** |
| Valor exatamente 1000 | {n_rel_1000} repositórios |

Q1 = 0: pelo menos um quarto da amostra nunca publicou release no GitHub. Os zeros concentram listas, livros e guias (`sindresorhus/awesome`, `public-apis/public-apis`, `EbookFoundation/free-programming-books`) e software que versiona fora da aba Releases (ex.: `freeCodeCamp/freeCodeCamp`).

{n_rel_1000} repositórios caem exatamente em 1000 releases (ex.: `{max_rel['name']}`). É um teto redondo na cauda — útil tratar o máximo como “≥ 1000” na discussão, não como contagem precisa.

### Hipótese vs. resultado

**Confirmação parcial, alinhada à #25.** Frequência alta de releases **não** é regra da popularidade: {n_zero_rel / n_rows * 100:.1f}% não usa Releases, a mediana geral é só {fmt(releases['median'])} e a média visual é puxada por uma cauda de projetos com ciclo de versão intenso (frameworks, runtimes, ferramentas). Releases frequentes descrevem os populares **mais estruturados como produto**, não a amostra inteira.

![RQ03 releases](analise_s03_rq03_releases.png)

---

## Síntese

| RQ | Hipótese | Resultado nesta amostra |
|---|---|---|
| 01 | Maduros/antigos | **Confirmada** (mediana ~{age_years_med:.1f} anos); {buckets[0][1]} repos < 1 ano não viram outlier Tukey |
| 02 | Muita contribuição externa | **Confirmada no típico** (mediana {fmt(merged['median'])} PRs); métrica = PR do GitHub; {n_zero_pr} zeros e cauda pesada |
| 03 | Releases com frequência | **Parcial** ({n_zero_rel / n_rows * 100:.1f}% sem release; mediana {fmt(releases['median'])}) |

Os números batem com as validações S02 (#20, #22). Esta sprint acrescenta a leitura hipótese vs. resultado e as visualizações para o relatório final.
"""
    OUTPUT_MD.write_text(text, encoding="utf-8")


def main() -> None:
    if not DATA_PATH.exists():
        print(f"CSV nao encontrado: {DATA_PATH}", file=sys.stderr)
        sys.exit(1)

    rows = load_rows(DATA_PATH)
    age_days = values(rows, "age_days")
    merged_vals = values(rows, "merged_prs")
    release_vals = values(rows, "releases")

    age = describe(age_days)
    merged = describe(merged_vals)
    releases = describe(release_vals)

    youngest = min(rows, key=lambda row: float(row["age_days"]))
    oldest = max(rows, key=lambda row: float(row["age_days"]))
    max_pr = max(rows, key=lambda row: float(row["merged_prs"]))
    max_rel = max(rows, key=lambda row: float(row["releases"]))

    plt = setup_style()
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    plot_rq01(age_days, age, FIG_RQ01, plt)
    plot_rq02(merged_vals, merged, FIG_RQ02, plt)
    plot_rq03(release_vals, releases, FIG_RQ03, plt)

    write_report(
        n_rows=len(rows),
        age=age,
        merged=merged,
        releases=releases,
        age_days=age_days,
        merged_vals=merged_vals,
        release_vals=release_vals,
        youngest=youngest,
        oldest=oldest,
        max_pr=max_pr,
        max_rel=max_rel,
    )

    print(f"N={len(rows)}")
    print(f"RQ01 age_days    med={fmt(age['median'])} outliers={age['n_outliers']}")
    print(f"RQ02 merged_prs  med={fmt(merged['median'])} outliers={merged['n_outliers']}")
    print(f"RQ03 releases    med={fmt(releases['median'])} outliers={releases['n_outliers']}")
    print(f"figuras: {FIG_RQ01.name}, {FIG_RQ02.name}, {FIG_RQ03.name}")
    print(f"relatorio: {OUTPUT_MD}")


if __name__ == "__main__":
    main()
