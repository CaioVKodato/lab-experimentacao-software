# Validação RQ01–RQ03 — Amostra de 5 repositórios

**Issue:** #7  
**Sprint:** S01  
**Data:** 2026-08-13  

## Campos GraphQL utilizados

| RQ | Campo GraphQL | Descrição |
|----|--------------|-----------|
| RQ01 | `createdAt` | Data de criação do repositório |
| RQ02 | `pullRequests(states: MERGED) { totalCount }` | Total de PRs aceitas (merged) |
| RQ03 | `releases { totalCount }` | Total de releases publicadas |

## Metodologia

Consulta GraphQL direta via `repository(owner, name)` para cada repositório da amostra, comparando os valores retornados com os registrados em `data/repositories.csv` (gerado pela coleta principal em `src/collect.py`).

Script de validação: `validate_rq01_rq03.py`

## Resultados

| Repositório | created_at (CSV) | created_at (API) | merged_prs (CSV) | merged_prs (API) | releases (CSV) | releases (API) | Status |
|---|---|---|---|---|---|---|---|
| codecrafters-io/build-your-own-x | 2018-05-09 | 2018-05-09 | 157 | 157 | 0 | 0 | OK |
| sindresorhus/awesome | 2014-07-11 | 2014-07-11 | 700 | 700 | 0 | 0 | OK |
| freeCodeCamp/freeCodeCamp | 2014-12-24 | 2014-12-24 | 29089 | 29089 | 0 | 0 | OK |
| donnemartin/system-design-primer | 2017-02-26 | 2017-02-26 | 210 | 210 | 0 | 0 | OK |
| jwasham/coding-interview-university | 2016-06-06 | 2016-06-06 | 415 | 415 | 0 | 0 | OK |

**Resultado: 15/15 campos validados sem divergências.**

## Observações

- O campo `createdAt` é estável e imutável — sem risco de inconsistência.
- O campo `pullRequests(states: MERGED)` reflete o total histórico de PRs merged; como a validação ocorreu logo após a coleta, os valores coincidem exatamente.
- O campo `releases` retorna 0 para a maioria dos repositórios mais populares do GitHub, pois muitos projetos de lista/tutorial não usam o sistema de releases do GitHub.
- O custo GraphQL da query de validação (5 repos em paralelo via aliases) foi de **1 ponto**, demonstrando que a abordagem é eficiente.
