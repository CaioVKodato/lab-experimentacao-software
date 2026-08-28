# Validação S02 — RQ03 e RQ06

**Issue:** #22  
**Dataset:** `data/repositories_top1000.csv`  
**Repositórios analisados:** 1000

## Metodologia

O script `src/analysis/validate_s02_rq03_rq06.py` lê `releases`, `total_issues`, `closed_issues`, `open_issues` e `closed_ratio`. A razão é analisada somente quando `total_issues > 0`; repositórios sem issues são contabilizados como dados ausentes, e não como 0% de issues fechadas. Outliers usam o critério de Tukey (1,5 × IQR).

## RQ03 — releases

| Métrica | N válido | Mínimo | Mediana | Máximo | Q1 | Q3 | Outliers |
|---|---:|---:|---:|---:|---:|---:|---:|
| `releases` | 1000 | 0 | 40 | 1000 | 0 | 149 | 93 |

Há 277 repositórios sem releases e 723 com pelo menos uma release. A distribuição é concentrada em valores baixos, mas possui uma cauda de projetos com muitas versões publicadas; esses casos aparecem como outliers acima de 372.5000 releases.

## RQ06 — razão de issues fechadas

| Grupo | Repositórios | Tratamento |
|---|---:|---|
| `total_issues = 0` | 43 | `closed_ratio = ausente` e excluído da mediana |
| `total_issues > 0` | 957 | incluído na estatística |

| Métrica | N válido | Mínimo | Mediana | Máximo | Q1 | Q3 | Outliers |
|---|---:|---:|---:|---:|---:|---:|---:|
| `closed_ratio` (total > 0) | 957 | 0.0769 | 0.8750 | 1 | 0.7042 | 0.9681 | 38 |

A implementação em `src/collect/transform.py` agora retorna `None` quando `total_issues` é zero. Assim, um repositório sem issues não é interpretado como tendo 0% de fechamento; a situação correta é ausência de observação para essa métrica.

Para reproduzir:

```bash
python3 src/analysis/validate_s02_rq03_rq06.py
```
