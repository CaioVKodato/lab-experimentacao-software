# Validação RQ04–RQ06 — Amostra de 8 repositórios

**Issue:** #8  
**Sprint:** S01  
**Data:** 2026-08-13

## Campos GraphQL utilizados

| RQ | Campo GraphQL | Métrica derivada | Descrição |
|----|---------------|------------------|-----------|
| RQ04 | `pushedAt` | `days_since_push` | Tempo até a última atualização de código |
| RQ04 (comparação) | `updatedAt` | — | Coletado só na validação; **não** é a métrica |
| RQ05 | `primaryLanguage { name }` | `language` | Linguagem primária do repositório |
| RQ06 | `closedIssues: issues(states: CLOSED) { totalCount }` | `closed_issues` | Issues fechadas (sem PRs) |
| RQ06 | `openIssues: issues(states: OPEN) { totalCount }` | `open_issues` | Issues abertas (sem PRs) |
| RQ06 | — | `closed_ratio = closed / (closed + open)` | Razão de issues fechadas; `0.0` se total = 0 |

Script: `validate_rq04_rq06.py`  
Coleta principal: `src/collect.py` (já persiste `pushedAt`, `primaryLanguage` e issues no CSV)

## Decisão RQ04: `pushedAt` (não `updatedAt`)

A RQ04 pergunta se sistemas populares **são atualizados com frequência**. Os dois timestamps do GitHub medem coisas diferentes:

- `pushedAt`: último **push git** (atividade de código).
- `updatedAt`: última alteração no **objeto do repositório** (metadados). Estrelas, descrição e eventos da UI atualizam esse campo **sem** haver commit novo.

Conferência na amostra (REST, 13/08/2026):

| Repositório | `pushedAt` | `updatedAt` | Interpretação |
|---|---|---|---|
| vuejs/vue | 2024-10-10 | 2026-08-13 | Código parado ~672 dias; `updatedAt` “hoje” por estrelas |
| donnemartin/system-design-primer | 2026-03-20 | 2026-08-13 | Mesmo efeito: metadados recentes, push antigo |
| sindresorhus/awesome | 2026-06-30 | 2026-08-13 | `updatedAt` mais recente que o último push |
| torvalds/linux | 2026-08-13 16:41 | 2026-08-13 23:44 | Push recente, mas `updatedAt` ainda mais tarde |
| public-apis/public-apis | 2026-08-13 21:07 | 2026-08-13 23:57 | Idem |
| freeCodeCamp/freeCodeCamp | 2026-08-13 21:20 | 2026-08-13 23:57 | Idem |

Se a métrica usasse `updatedAt`, vuejs/vue e system-design-primer pareceriam atualizados “hoje”, o que falseia a RQ04. **A coleta usa `pushedAt`.**

## Fonte RQ05 (alinhamento com a Issue #9)

A **métrica** da RQ05 é a linguagem primária (`primaryLanguage { name }`), já presente no CSV.

Para classificar o que conta como “linguagens mais populares”, a fonte proposta (a confirmar na #9, mesma referência o laboratório inteiro) é o **GitHub Octoverse 2025**:

https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/

Ranking por contribuidores mensais (ago/2025): TypeScript, Python, JavaScript, Java, C#. O relatório também indica que ~80% dos repositórios novos usam seis linguagens: Python, JavaScript, TypeScript, Java, C++ e C#.

Octoverse foi escolhida (em vez de TIOBE/GitHut) porque a mineração é no GitHub — mesma população da amostra. A #9 deve gravar essa fonte no README do grupo.

## Conferência manual (REST + Search `is:issue`)

`issues` no GraphQL **não inclui pull requests**. O campo REST `open_issues_count` inclui PRs e **não** deve ser usado na RQ06.

| Repositório | language CSV | language REST | pushed_at CSV = REST | open CSV | open Search | closed CSV | closed Search | Observação |
|---|---|---|---|---|---|---|---|---|
| freeCodeCamp/freeCodeCamp | TypeScript | TypeScript | sim | 171 | 172 | 21888 | 21882 | Drift de horas (repo ativo) |
| public-apis/public-apis | Python | Python | sim | 10 | 10 | 911 | 909 | REST `open_issues_count` = 1634 (mistura PRs) |
| torvalds/linux | C | C | sim | 0 | 0 | 0 | 0 | `has_issues = false` |
| vuejs/vue | TypeScript | TypeScript | sim | 365 | 365 | 9670 | 9667 | Push de 2024; `updatedAt` de 2026 |
| sindresorhus/awesome | *(vazio)* | `null` | sim | 16 | 16 | 352 | 352 | Linguagem nula (lista Markdown) |
| donnemartin/system-design-primer | Python | Python | sim | 272 | 272 | 127 | 127 | Match exato; `closed_ratio` = 0.3183 |
| golang/go | Go | Go | sim | 9714 | — | 63108 | — | REST `open_issues_count` = 10221 (inclui PRs) |
| kubernetes/kubernetes | Go | Go | sim | 1820 | — | 47699 | — | REST `open_issues_count` = 2883 (inclui PRs) |

**Campos estáveis (language, pushed_at, casos sem drift): conferidos.**  
Issues de repositórios muito ativos podem variar entre a geração do CSV e a conferência — esperado.

## Observações para a análise (S03)

- RQ06 com total = 0 (linux, alguns awesome-lists) não significa “0% de issues fechadas”: issues desabilitadas ou nunca usadas. Tratar como valor ausente na estatística, não como zero real.
- RQ05: `primaryLanguage` nulo (sindresorhus/awesome) deve entrar como “sem linguagem / não classificado”, não como linguagem popular.
- O custo GraphQL da query de validação (8 repositórios em aliases) é o mesmo padrão da #7 (1 ponto).
