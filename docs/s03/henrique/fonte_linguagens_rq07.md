# Fonte de Linguagens Populares e Campos do RQ07

**Issue:** #9  
**Sprint:** S01  
**Data:** 2026-08-13  

## Fonte escolhida: GitHub Octoverse 2025

**Referência oficial:**  
GitHub Octoverse 2025 — https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/

**Justificativa:** Como o estudo analisa os repositórios mais populares do próprio GitHub, o Octoverse é a fonte mais internamente consistente — ele rankeia as linguagens pelo número de repositórios e contribuições diretamente na plataforma. As demais fontes (TIOBE, PYPL) medem popularidade por buscas na web, o que é menos representativo para um estudo centrado no GitHub.

## Ranking Octoverse 2025 (top 10)

| Posição | Linguagem |
|---------|-----------|
| 1 | TypeScript |
| 2 | Python |
| 3 | JavaScript |
| 4 | Java |
| 5 | C# |
| 6 | C++ |
| 7 | Shell |
| 8 | Go |
| 9 | PHP |
| 10 | Rust |

## Confirmação dos campos para RQ07

RQ07 exige o cruzamento dos resultados de RQ02, RQ03 e RQ04 por linguagem primária. Todos os campos necessários estão presentes em `data/repositories.csv`:

| Campo CSV | RQ relacionada | Presente? |
|-----------|---------------|-----------|
| `language` | RQ05 / RQ07 | Sim |
| `merged_prs` | RQ02 | Sim |
| `releases` | RQ03 | Sim |
| `days_since_push` | RQ04 | Sim |

## Distribuição de linguagens na coleta (100 repos)

| Linguagem | Repos | No Octoverse top-10? |
|-----------|-------|----------------------|
| Python | 24 | Sim (#2) |
| TypeScript | 17 | Sim (#1) |
| (sem linguagem) | 13 | — |
| JavaScript | 10 | Sim (#3) |
| Shell | 5 | Sim (#7) |
| C++ | 5 | Sim (#6) |
| Rust | 5 | Sim (#10) |
| Go | 4 | Sim (#8) |
| Markdown | 3 | Não |
| C | 3 | Não |
| HTML | 3 | Não |
| Jupyter Notebook | 2 | Não |
| Java | 1 | Sim (#4) |
| C# | 1 | Sim (#5) |
| Swift | 1 | Não |
| Dart | 1 | Não |
| MDX | 1 | Não |
| Batchfile | 1 | Não |

**Observação:** 87 dos 100 repositórios possuem linguagem detectável. Dos 87, 70 (80%) pertencem ao top-10 do Octoverse — o que indica forte correlação entre popularidade do repositório e uso de linguagens predominantes na plataforma.
