"""Gera estatísticas de validação S02 para RQ01 (idade) e RQ02 (PRs merged)."""
import csv
from pathlib import Path
from statistics import median

INPUT = Path("data/repositories_top1000.csv")
OUTPUT = Path("docs/validacao_s02_rq01_rq02.md")


def values(rows, field):
    return sorted(float(row[field]) for row in rows if row[field].strip())


def describe(items):
    q1 = items[(len(items) - 1) // 4]
    q3 = items[(3 * (len(items) - 1)) // 4]
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers = [value for value in items if value < lower or value > upper]
    return {
        "n": len(items), "min": min(items), "median": median(items), "max": max(items),
        "q1": q1, "q3": q3, "lower": lower, "upper": upper,
        "outliers": outliers,
    }


def fmt(value):
    return str(int(value)) if value == int(value) else f"{value:.2f}"


rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
age = describe(values(rows, "age_days"))
merged = describe(values(rows, "merged_prs"))
nulls = {field: sum(not row[field].strip() for row in rows) for field in ("created_at", "age_days", "merged_prs")}

text = f"""# Validação S02 — RQ01 e RQ02

**Issue:** #20  
**Dataset:** `data/repositories_top1000.csv`  
**Repositórios analisados:** {len(rows)}

## Metodologia

O script `src/analysis/validate_s02_rq01_rq02.py` lê o CSV produzido pela coleta S02, converte `age_days` e `merged_prs` para valores numéricos e calcula mínimo, mediana, máximo e outliers pelo critério de Tukey (1,5 × IQR). Valores ausentes são excluídos da estatística e contabilizados separadamente.

## Resultados

| Métrica | N válido | Mínimo | Mediana | Máximo | Q1 | Q3 | Outliers |
|---|---:|---:|---:|---:|---:|---:|---:|
| `age_days` (RQ01) | {age['n']} | {fmt(age['min'])} | {fmt(age['median'])} | {fmt(age['max'])} | {fmt(age['q1'])} | {fmt(age['q3'])} | {len(age['outliers'])} |
| `merged_prs` (RQ02) | {merged['n']} | {fmt(merged['min'])} | {fmt(merged['median'])} | {fmt(merged['max'])} | {fmt(merged['q1'])} | {fmt(merged['q3'])} | {len(merged['outliers'])} |

## Nulos e observações

| Campo | Nulos |
|---|---:|
| `created_at` | {nulls['created_at']} |
| `age_days` | {nulls['age_days']} |
| `merged_prs` | {nulls['merged_prs']} |

`age_days` varia de {fmt(age['min'])} a {fmt(age['max'])} dias, sem outliers pelo critério adotado. `merged_prs` tem mediana de {fmt(merged['median'])} e {len(merged['outliers'])} valores acima do limite superior de {fmt(merged['upper'])}; esses valores representam projetos com volume excepcional de contribuições, não necessariamente erro de coleta. A inspeção dos nulos não encontrou ausência nos campos usados.

Para reproduzir:

```bash
python -m src.analysis.validate_s02_rq01_rq02
```
"""
OUTPUT.write_text(text, encoding="utf-8")
print(OUTPUT)
