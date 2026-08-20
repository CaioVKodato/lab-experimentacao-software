"""Gera estatísticas S02 para RQ03 (releases) e RQ06 (closed_ratio)."""
import csv
from pathlib import Path
from statistics import median

INPUT = Path("data/repositories_top1000.csv")
OUTPUT = Path("docs/validacao_s02_rq03_rq06.md")


def describe(items):
    items = sorted(items)
    q1 = items[(len(items) - 1) // 4]
    q3 = items[(3 * (len(items) - 1)) // 4]
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers = [x for x in items if x < lower or x > upper]
    return len(items), min(items), median(items), max(items), q1, q3, len(outliers), upper


def fmt(value):
    return str(int(value)) if value == int(value) else f"{value:.4f}"


rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
releases = [float(r["releases"]) for r in rows if r["releases"].strip()]
zero_total = [r for r in rows if int(float(r["total_issues"] or 0)) == 0]
with_issues = [r for r in rows if int(float(r["total_issues"] or 0)) > 0]
ratios = [float(r["closed_ratio"]) for r in with_issues if r["closed_ratio"].strip()]
rel = describe(releases)
ratio = describe(ratios)

text = f"""# Validação S02 — RQ03 e RQ06

**Issue:** #22  
**Dataset:** `data/repositories_top1000.csv`  
**Repositórios analisados:** {len(rows)}

## Metodologia

O script `src/analysis/validate_s02_rq03_rq06.py` lê `releases`, `total_issues`, `closed_issues`, `open_issues` e `closed_ratio`. A razão é analisada somente quando `total_issues > 0`; repositórios sem issues são contabilizados como dados ausentes, e não como 0% de issues fechadas. Outliers usam o critério de Tukey (1,5 × IQR).

## RQ03 — releases

| Métrica | N válido | Mínimo | Mediana | Máximo | Q1 | Q3 | Outliers |
|---|---:|---:|---:|---:|---:|---:|---:|
| `releases` | {rel[0]} | {fmt(rel[1])} | {fmt(rel[2])} | {fmt(rel[3])} | {fmt(rel[4])} | {fmt(rel[5])} | {rel[6]} |

Há {sum(value == 0 for value in releases)} repositórios sem releases e {sum(value > 0 for value in releases)} com pelo menos uma release. A distribuição é concentrada em valores baixos, mas possui uma cauda de projetos com muitas versões publicadas; esses casos aparecem como outliers acima de {fmt(rel[7])} releases.

## RQ06 — razão de issues fechadas

| Grupo | Repositórios | Tratamento |
|---|---:|---|
| `total_issues = 0` | {len(zero_total)} | `closed_ratio = ausente` e excluído da mediana |
| `total_issues > 0` | {len(with_issues)} | incluído na estatística |

| Métrica | N válido | Mínimo | Mediana | Máximo | Q1 | Q3 | Outliers |
|---|---:|---:|---:|---:|---:|---:|---:|
| `closed_ratio` (total > 0) | {ratio[0]} | {fmt(ratio[1])} | {fmt(ratio[2])} | {fmt(ratio[3])} | {fmt(ratio[4])} | {fmt(ratio[5])} | {ratio[6]} |

A implementação em `src/collect/transform.py` agora retorna `None` quando `total_issues` é zero. Assim, um repositório sem issues não é interpretado como tendo 0% de fechamento; a situação correta é ausência de observação para essa métrica.

Para reproduzir:

```bash
python3 src/analysis/validate_s02_rq03_rq06.py
```
"""
OUTPUT.write_text(text, encoding="utf-8")
print(OUTPUT)
