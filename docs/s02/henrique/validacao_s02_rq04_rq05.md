# Validação S02 — RQ04 e RQ05

**Issue:** #21  
**Dataset:** `data/repositories_top1000.csv`  
**Repositórios analisados:** 1000

## Metodologia

O script `src/analysis/validate_s02_rq04_rq05.py` calcula a distribuição de `days_since_push` e a frequência de `language` diretamente sobre o CSV S02. Outliers de atividade são identificados por 1,5 × IQR; linguagens vazias são mantidas em uma categoria explícita, `Sem linguagem`.

## RQ04 — atividade de código

| Métrica | N válido | Mínimo (dias) | Mediana | Máximo (dias) | Q1 | Q3 | Outliers |
|---|---:|---:|---:|---:|---:|---:|---:|
| `days_since_push` | 1000 | 0 | 1 | 2452 | 0 | 48 | 196 |

A métrica foi calculada a partir de `pushedAt`, persistido na coluna `pushed_at`; `updatedAt` não é usado. Isso evita confundir atividade de código com alterações de metadados, estrelas ou eventos da interface. O limite superior estatístico é 120 dias. Os outliers devem ser investigados como projetos menos recentemente atualizados, não descartados automaticamente.

## RQ05 — linguagem primária

| Linguagem/categoria | Repositórios | Percentual |
|---|---:|---:|
| Python | 227 | 22.7% |
| TypeScript | 173 | 17.3% |
| JavaScript | 111 | 11.1% |
| Sem linguagem | 87 | 8.7% |
| Go | 77 | 7.7% |
| Rust | 58 | 5.8% |
| C++ | 41 | 4.1% |
| Java | 41 | 4.1% |
| Jupyter Notebook | 24 | 2.4% |
| C | 21 | 2.1% |
| **Total sem linguagem** | **87** | **8.7%** |

`language` representa `primaryLanguage {name}` retornada pela API. Os resultados têm maior frequência em Python, TypeScript e JavaScript. A comparação de popularidade deve usar a mesma fonte adotada pelo laboratório, o [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/); a tabela acima descreve a amostra, não substitui o ranking externo.

Para reproduzir:

```bash
python3 src/analysis/validate_s02_rq04_rq05.py
```
