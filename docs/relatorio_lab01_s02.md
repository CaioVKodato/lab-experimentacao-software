# Laboratório 01 — Relatório (1ª versão, Sprint S02)

**Disciplina:** Laboratório de Experimentação de Software  
**Curso:** Engenharia de Software — PUC Minas  
**Docente:** Prof. Danilo Maia  
**Sprint:** Lab01S02  

## Integrantes

| Integrante | GitHub |
|---|---|
| Caio Victor Kodato Teixeira | [CaioVKodato](https://github.com/CaioVKodato) |
| Henrique Volponi | [Henrique-volponi](https://github.com/Henrique-volponi) |
| Jonas Martins | Membro 3 (Issues #23–#25) |

## Links do processo

| Recurso | URL |
|---|---|
| Repositório | https://github.com/CaioVKodato/lab-experimentacao-software |
| GitHub Projects (v2) | https://github.com/users/CaioVKodato/projects/6 |

> Esta é a **primeira versão** do relatório (entrega da S02): introdução, metodologia de coleta dos **1000** repositórios, hipóteses informais e resultados descritivos preliminares. A análise/visualização completa das 7 RQs fica para a **S03**; o relatório final do Lab01 consolida discussão e anexos do board.

---

## 1. Introdução

Este laboratório investiga características de sistemas open-source populares no GitHub: maturidade, contribuição externa, releases, atualização de código, linguagens, resolução de issues e o cruzamento dessas métricas por linguagem (RQ07).

Na **S01** o grupo montou o cliente GraphQL próprio (sem SDK da API), coletou 100 repositórios, configurou o Kanban (Projects v2) e propôs uma questão extra (correlação stars × `closed_ratio`). Na **S02** a coleta foi escalada para **1000** repositórios válidos, com validação de consistência por fatia de RQ e registro formal das hipóteses informais.

O enunciado cobre cerca de 60% do trabalho; os ~40% restantes são experimentação do grupo (ex.: RQ extra da S01 e decisões metodológicas como usar `pushedAt` em vez de `updatedAt`).

### 1.1. Questões de pesquisa

| RQ | Pergunta |
|---|---|
| RQ01 | Sistemas populares são maduros/antigos? |
| RQ02 | Sistemas populares recebem muita contribuição externa? |
| RQ03 | Sistemas populares lançam releases com frequência? |
| RQ04 | Sistemas populares são atualizados com frequência? |
| RQ05 | Sistemas populares são escritos nas linguagens mais populares? |
| RQ06 | Sistemas populares possuem um alto percentual de issues fechadas? |
| RQ07 | Sistemas em linguagens mais populares recebem mais PRs, lançam mais releases e são atualizados com mais frequência? |

### 1.2. Hipóteses informais (S02)

Textos consolidados a partir das Issues **#23**, **#24** e **#25** (Jonas Martins), alinhados às validações **#20–#22** (Henrique Volponi) sobre `data/repositories_top1000.csv`.

#### RQ01 — Maduros/antigos?

**Hipótese:** sim, sistemas populares tendem a ser maduros.

**Justificativa:** construir uma base grande de estrelas costuma exigir tempo de exposição e adoção. A validação (#20) mostra mediana de **2826 dias** de idade (~7,7 anos), sem outliers pelo critério de Tukey, sugerindo maturidade consistente na amostra.

#### RQ02 — Muita contribuição externa?

**Hipótese:** sim, alto volume de contribuição externa (PRs aceitas).

**Justificativa:** popularidade atrai colaboradores. Mediana de **768** PRs merged; Q3 = **3415**; **124** outliers acima de 8275 PRs — cauda pesada de projetos com contribuição excepcional.

#### RQ03 — Releases com frequência?

**Hipótese:** confirmação **parcial** — releases são comuns em parte da amostra, não universais.

**Justificativa:** **27,7%** dos repos não têm nenhuma release; mediana geral = **40**. Há cauda com muitas releases (Q3 = 149, máximo = 1000). Frequência alta aparece mais em projetos estruturados, não como regra da popularidade.

#### RQ04 — Atualizados com frequência?

**Hipótese:** sim, atualização frequente de código.

**Justificativa:** mediana de apenas **1 dia** desde o último push (`pushedAt`); Q3 = **48** dias (75% com commit no último ~mês e meio). Os **196** outliers pouco atualizados são minoria. A métrica usa **`pushedAt`**, não `updatedAt` (estrelas/metadados não contam como atualização de software).

#### RQ05 — Linguagens mais populares?

**Hipótese:** sim, concentração nas linguagens mais adotadas no GitHub.

**Justificativa:** Python (**22,7%**), TypeScript (**17,3%**) e JavaScript (**11,1%**) somam mais da metade da amostra — todas no [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/), fonte única do laboratório. **8,7%** sem linguagem primária na API (listas Markdown etc.), mantidos como categoria separada.

#### RQ06 — Alto % de issues fechadas?

**Hipótese:** sim, alta taxa de resolução entre quem usa o tracker.

**Justificativa:** nos **957** repos com pelo menos uma issue, mediana de `closed_ratio` = **87,5%** (Q1 = 70,4%). Os **43** com `total_issues = 0` são **ausência** de observação, não “0% fechadas”.

#### RQ07 — Nota informal (análise completa na S03)

Cruzar RQ02, RQ03 e RQ04 **por linguagem**. Os campos já estão no CSV (`language`, `merged_prs`, `releases`, `days_since_push`). Como Python/TypeScript/JavaScript dominam a amostra, o comportamento agregado deve ser fortemente influenciado por esses ecossistemas; linguagens de nicho podem divergir. **Análise e gráficos: S03.**

#### RQ extra (S01, experimentação do grupo)

**Pergunta:** stars correlacionam com `%` de issues fechadas?  
**Hipótese:** não.  
**Achado (n = 89 nos top 100):** Spearman ρ ≈ **−0,05** (correlação nula). Ver `docs/rq_extra_stars_vs_closed_ratio.md`.

Fontes originais das hipóteses:  
`docs/Hipóteses Informais — RQ01 e RQ02`,  
`docs/Hipóteses Informais — RQ04 e RQ05`,  
`docs/Hipóteses Informais — RQ03, RQ06 e nota da RQ07`.

---

## 2. Metodologia de coleta

### 2.1. População e amostra (S02)

- **População de interesse:** repositórios públicos do GitHub ordenados por popularidade (estrelas).
- **Amostra S02:** **1000** repositórios válidos mais estrelados.
- **Arquivo:** `data/repositories_top1000.csv`
- **Script:** `python -m src.collect --n 1000` (pacote `src/collect/`)

### 2.2. Instrumento

- API **GraphQL** do GitHub (`https://api.github.com/graphql`).
- Cliente **próprio** do grupo (`src/github/`): HTTP POST com `requests`, token em `.env`.
- **Sem** bibliotecas do tipo PyGithub/Octokit (exigência do enunciado).
- Retry/backoff e leitura de `rateLimit` no cliente.

### 2.3. Paginação e 1000 válidos

A Search API limita cada query a **1000 hits**; alguns nós vêm nulos. A coleta:

1. pagina `stars:>1 sort:stars-desc`;
2. descarta nós inválidos;
3. se faltar válidos, abre nova janela `stars:<mínimo_já_coletado` e deduplica;
4. ordena por stars e corta em 1000.

### 2.4. Métricas (colunas do CSV)

| Coluna | RQ | Origem |
|---|---|---|
| `created_at` / `age_days` | RQ01 | `createdAt` |
| `merged_prs` | RQ02 | `pullRequests(states: MERGED)` |
| `releases` | RQ03 | `releases` |
| `pushed_at` / `days_since_push` | RQ04 | `pushedAt` |
| `language` | RQ05 / RQ07 | `primaryLanguage` |
| `closed_issues`, `open_issues`, `closed_ratio` | RQ06 | `issues(CLOSED\|OPEN)` (sem PRs) |

**Decisões metodológicas importantes**

1. **RQ04 = `pushedAt`**, não `updatedAt` (Issue #8 / #21).  
2. **RQ06** não usa `open_issues_count` do REST (mistura PRs).  
3. **RQ05/RQ07:** fonte de “linguagens populares” = **Octoverse 2025** (Issue #9).  
4. **`closed_ratio`:** com `total_issues = 0`, trata-se como ausente na análise (Issue #22).

### 2.5. Validação de consistência (S02)

| Fatia | Issue | Artefatos |
|---|---|---|
| RQ01–RQ02 | #20 | `src/analysis/validate_s02_rq01_rq02.py`, `docs/validacao_s02_rq01_rq02.md` |
| RQ04–RQ05 | #21 | `src/analysis/validate_s02_rq04_rq05.py`, `docs/validacao_s02_rq04_rq05.md` |
| RQ03–RQ06 | #22 | `src/analysis/validate_s02_rq03_rq06.py`, `docs/validacao_s02_rq03_rq06.md` |

Critério de outliers: Tukey (1,5 × IQR).

### 2.6. Processo (Kanban)

- GitHub Projects v2 com Status: `Backlog → To Do → Doing → Review → Done`.
- Issues reais com **Assignee**; commits referenciam `#Issue`.
- Snapshots GraphQL do board em `snapshots/` (série para Labs 04/05).
- WIP documentado no README do repositório (ajustar para trio quando aplicável).

---

## 3. Resultados preliminares (S02)

Valores descritivos dos **1000** repositórios (validações #20–#22). Análise completa e visualizações: **S03**.

### 3.1. Resumo numérico

| RQ | Métrica | N | Mediana | Observação rápida |
|---|---|---:|---:|---|
| 01 | `age_days` | 1000 | 2826 | ~7,7 anos; sem outliers Tukey |
| 02 | `merged_prs` | 1000 | 768 | 124 outliers (cauda de mega-projetos) |
| 03 | `releases` | 1000 | 40 | 277 repos com 0 releases |
| 04 | `days_since_push` | 1000 | 1 | 196 outliers pouco ativos |
| 05 | `language` | 1000 | — | Python 22,7%; TS 17,3%; JS 11,1%; sem lang. 8,7% |
| 06 | `closed_ratio` | 957* | 0,875 | *exclui 43 sem issues |
| 07 | cruzamento | — | — | pendente S03 |

### 3.2. Contagem por linguagem (top 10 da amostra)

| Linguagem | Repos | % |
|---|---:|---:|
| Python | 227 | 22,7% |
| TypeScript | 173 | 17,3% |
| JavaScript | 111 | 11,1% |
| Sem linguagem | 87 | 8,7% |
| Go | 77 | 7,7% |
| Rust | 58 | 5,8% |
| C++ | 41 | 4,1% |
| Java | 41 | 4,1% |
| Jupyter Notebook | 24 | 2,4% |
| C | 21 | 2,1% |

---

## 4. Discussão preliminar: hipótese × observação

| RQ | Hipótese | Leitura preliminar (S02) |
|---|---|---|
| 01 | Maduros | **Alinhada** — mediana ~7,7 anos |
| 02 | Muita contribuição | **Alinhada** — mediana alta + cauda extrema |
| 03 | Releases frequentes | **Parcial** — muitos com 0 releases |
| 04 | Atualizados | **Alinhada** — mediana 1 dia desde push |
| 05 | Linguagens populares | **Alinhada** — domínio Octoverse na amostra |
| 06 | Alto % fechadas | **Alinhada** — mediana 87,5% (com tracker ativo) |
| 07 | Cruzamento por linguagem | **A testar na S03** |

A discussão aprofundada (causas, vieses de popularidade, listas awesome-*, limites da Search API) será expandida no relatório final e na S03.

---

## 5. Configuração do processo

### 5.1. GitHub Projects

- Board: [Lab Experimentação de Software](https://github.com/users/CaioVKodato/projects/6)
- Colunas mínimas: Backlog, To Do, Doing, Review, Done
- Cartões = Issues do repositório (não draft), com Assignee
- Commits no formato `#N mensagem`

### 5.2. Política de WIP

Documentada no README do repositório. Com a entrada do terceiro integrante, o grupo deve manter WIP coerente (sugestão: ~2 cartões por pessoa em Doing) e justificar no board/README.

### 5.3. Snapshots

Export via `python -m src.snapshot --sprint Lab01S02` → `snapshots/`.  
A S01 já possui `snapshots/lab01s01-2026-08-13.csv`.

### 5.4. Print do board

*(Anexar print do Projects ao final do Lab01 / após fechar a S02 — pendente no relatório final.)*

---

## 6. Próximos passos (S03 e relatório final)

1. Análise e visualização das **7 RQs** (medianas, gráficos, cruzamento RQ07).  
2. Discutir hipótese vs. resultado com profundidade.  
3. Regenerar CSV se necessário para persistir `closed_ratio` vazio quando `total_issues = 0`.  
4. Snapshot Lab01S02 e print do board no anexo final.  
5. Entrega do **Relatório Final** (3 pontos) com estrutura completa do enunciado.

---

## Referências rápidas do repositório

| Artefato | Caminho / link |
|---|---|
| CSV S02 | `data/repositories_top1000.csv` |
| Coleta | `src/collect/` |
| Cliente GraphQL | `src/github/` |
| Validações S02 | `docs/validacao_s02_*.md` |
| Hipóteses (fontes) | `docs/Hipóteses Informais — *` |
| Octoverse | `docs/fonte_linguagens_rq07.md` |
| RQ extra | `docs/rq_extra_stars_vs_closed_ratio.md` |

---

*Documento gerado na Issue **#26** — montagem da 1ª versão do relatório (esqueleto + hipóteses).*
