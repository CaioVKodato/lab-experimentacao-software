"""Gera estatísticas S02 para RQ04 (push) e RQ05 (linguagem primária)."""
import csv
from collections import Counter
from pathlib import Path
from statistics import median

INPUT = Path("data/repositories_top1000.csv")
OUTPUT = Path("docs/validacao_s02_rq04_rq05.md")


def describe(items):
    items = sorted(items)
    q1 = items[(len(items) - 1) // 4]
    q3 = items[(3 * (len(items) - 1)) // 4]
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return len(items), min(items), median(items), max(items), q1, q3, len([x for x in items if x < lower or x > upper]), upper


def fmt(value):
    return str(int(value)) if value == int(value) else f"{value:.2f}"


rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
push = describe([float(r["days_since_push"]) for r in rows if r["days_since_push"].strip()])
languages = Counter(r["language"].strip() or "Sem linguagem" for r in rows)
missing = languages["Sem linguagem"]
top = languages.most_common(10)

text = f"""# Validação S02 — RQ04 e RQ05

**Issue:** #21  
**Dataset:** `data/repositories_top1000.csv`  
**Repositórios analisados:** {len(rows)}

## Metodologia

O script `src/analysis/validate_s02_rq04_rq05.py` calcula a distribuição de `days_since_push` e a frequência de `language` diretamente sobre o CSV S02. Outliers de atividade são identificados por 1,5 × IQR; linguagens vazias são mantidas em uma categoria explícita, `Sem linguagem`.

## RQ04 — atividade de código

| Métrica | N válido | Mínimo (dias) | Mediana | Máximo (dias) | Q1 | Q3 | Outliers |
|---|---:|---:|---:|---:|---:|---:|---:|
| `days_since_push` | {push[0]} | {fmt(push[1])} | {fmt(push[2])} | {fmt(push[3])} | {fmt(push[4])} | {fmt(push[5])} | {push[6]} |

A métrica foi calculada a partir de `pushedAt`, persistido na coluna `pushed_at`; `updatedAt` não é usado. Isso evita confundir atividade de código com alterações de metadados, estrelas ou eventos da interface. O limite superior estatístico é {fmt(push[7])} dias. Os outliers devem ser investigados como projetos menos recentemente atualizados, não descartados automaticamente.

## RQ05 — linguagem primária

| Linguagem/categoria | Repositórios | Percentual |
|---|---:|---:|
""" + "\n".join(f"| {name} | {count} | {count / len(rows) * 100:.1f}% |" for name, count in top) + f"""
| **Total sem linguagem** | **{missing}** | **{missing / len(rows) * 100:.1f}%** |

`language` representa `primaryLanguage {{name}}` retornada pela API. Os resultados têm maior frequência em Python, TypeScript e JavaScript. A comparação de popularidade deve usar a mesma fonte adotada pelo laboratório, o [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/); a tabela acima descreve a amostra, não substitui o ranking externo.

Para reproduzir:

```bash
python3 src/analysis/validate_s02_rq04_rq05.py
```
"""
OUTPUT.write_text(text, encoding="utf-8")
print(OUTPUT)
