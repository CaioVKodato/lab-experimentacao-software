# Validação S02 — RQ01 e RQ02

**Issue:** #20  
**Dataset:** `data/repositories_top1000.csv`  
**Repositórios analisados:** 1000

## Metodologia

O script `src/analysis/validate_s02_rq01_rq02.py` lê o CSV produzido pela coleta S02, converte `age_days` e `merged_prs` para valores numéricos e calcula mínimo, mediana, máximo e outliers pelo critério de Tukey (1,5 × IQR). Valores ausentes são excluídos da estatística e contabilizados separadamente.

## Resultados

| Métrica | N válido | Mínimo | Mediana | Máximo | Q1 | Q3 | Outliers |
|---|---:|---:|---:|---:|---:|---:|---:|
| `age_days` (RQ01) | 1000 | 7 | 2826 | 6705 | 1267 | 4147 | 0 |
| `merged_prs` (RQ02) | 1000 | 0 | 768 | 103403 | 175 | 3415 | 124 |

## Nulos e observações

| Campo | Nulos |
|---|---:|
| `created_at` | 0 |
| `age_days` | 0 |
| `merged_prs` | 0 |

`age_days` varia de 7 a 6705 dias, sem outliers pelo critério adotado. `merged_prs` tem mediana de 768 e 124 valores acima do limite superior de 8275; esses valores representam projetos com volume excepcional de contribuições, não necessariamente erro de coleta. A inspeção dos nulos não encontrou ausência nos campos usados.

Para reproduzir:

```bash
python -m src.analysis.validate_s02_rq01_rq02
```
