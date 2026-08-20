# Lab Experimentação de Software

Repositório do **Laboratório 01** — Características de repositórios populares + Setup do Kanban.

Disciplina: Laboratório de Experimentação de Software  
Curso: Engenharia de Software

## Integrantes

- [CaioVKodato](https://github.com/CaioVKodato)
- [Henrique-volponi](https://github.com/Henrique-volponi)

## GitHub Projects

Board Kanban (Projects v2):  
https://github.com/users/CaioVKodato/projects/6

> Se o número do project for outro, atualize este link.

### Processo (colunas e WIP)

| Coluna   | Uso                                      |
|----------|------------------------------------------|
| Backlog  | Ideias / tarefas ainda não priorizadas   |
| To Do    | Pronto para começar nesta sprint         |
| Doing    | Em andamento (**WIP = 4**, ~2 por pessoa)|
| Review   | Aguardando revisão do par                |
| Done     | Concluído                                |

**Justificativa do WIP:** limite de 4 cartões em Doing para a dupla manter foco, evitar trabalho paralelo excessivo e forçar passagem por Review.

## Estrutura do repositório

```text
.
├── src/
│   ├── github/             # Auth, retry, rateLimit, cliente GraphQL
│   ├── collect/            # Coleta paginada (S01=100, S02=1000) → CSV
│   │   ├── query.py        # Query GraphQL
│   │   ├── transform.py    # Nó API → linha CSV (métricas RQs)
│   │   ├── fetch.py        # Paginação
│   │   ├── export.py       # Escrita CSV
│   │   └── __main__.py     # CLI (--n, --out)
│   ├── snapshot.py         # Snapshot GraphQL do GitHub Projects → CSV
│   ├── validate.py         # Roda as duas fatias de validação (#7 e #8)
│   └── __main__.py         # CLI de teste de autenticação
├── data/
│   ├── repositories.csv           # S01 — 100 repositórios
│   └── repositories_top1000.csv   # S02 — 1000 repositórios
├── snapshots/              # Fotos do board (um CSV por data/sprint)
├── docs/
├── validate_rq01_rq03.py
├── validate_rq04_rq06.py
├── requirements.txt
├── .env.example
└── README.md
```

## Validação das fatias (S01)

Cada integrante valida os campos da sua parte em uma amostra de 5–10 repositórios **antes** de tratar a coleta dos 100 como fechada.

```bash
python -m src.validate
```

Isso executa, nesta ordem, as Issues #7 e #8:

```bash
python validate_rq01_rq03.py   # Issue #7 — RQ01–RQ03
python validate_rq04_rq06.py   # Issue #8 — RQ04–RQ06
```

Documentação das conferências: `docs/validacao_rq01_rq03.md` e `docs/validacao_rq04_rq06.md`.

**RQ04:** métrica = `pushedAt` (não `updatedAt`).  
**RQ05:** métrica = `primaryLanguage`; fonte de ranking proposta = [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/) (Issue #9).  
**RQ06:** `issues(states: CLOSED|OPEN)` no GraphQL (sem pull requests).

## Coleta de dados (S01: 100 | S02: 1000)

Pacote modular `src/collect/` (query, transform, paginação, CSV).  
A Search API limita cada query a **1000** hits; nós nulos são descartados e a
coleta abre novas janelas (`stars:<mínimo`) até completar **1000 válidos**.

```bash
# S02 — 1000 repos → data/repositories_top1000.csv
python -m src.collect
python -m src.collect --n 1000

# S01 — 100 repos → data/repositories.csv
python -m src.collect --n 100

# Caminho customizado
python -m src.collect --n 1000 --out data/repositories_top1000.csv
```

### Colunas do CSV

| Coluna | RQ | Descrição |
|---|---|---|
| `name` | — | `owner/repo` |
| `stars` | — | Número de estrelas |
| `created_at` | RQ01 | Data de criação (ISO-8601) |
| `age_days` | RQ01 | Idade em dias |
| `pushed_at` | RQ04 | Data do último push (ISO-8601) |
| `days_since_push` | RQ04 | Dias desde o último push |
| `merged_prs` | RQ02 | Total de pull requests aceitas (merged) |
| `releases` | RQ03 | Total de releases |
| `closed_issues` | RQ06 | Issues fechadas |
| `open_issues` | RQ06 | Issues abertas |
| `total_issues` | RQ06 | Total de issues |
| `closed_ratio` | RQ06 | Razão issues fechadas / total |
| `language` | RQ05/RQ07 | Linguagem primária |

## Snapshot do Kanban (fechamento de sprint / semanal)

O GitHub Projects v2 não guarda histórico de coluna consultável via API. O script abaixo
tira uma foto do board (Issue, Status, Assignee) e grava um CSV **novo** em `snapshots/`.
Não sobrescreva arquivos antigos — a série é a base dos Labs 04 e 05.

```bash
python -m src.snapshot
python -m src.snapshot --sprint Lab01S01
```

Saída: `snapshots/lab01s01-AAAA-MM-DD.csv`.

O token precisa do escopo `read:project`. Rode no fim de cada sprint e a cada aula.

### Colunas do snapshot

| Coluna | Descrição |
|---|---|
| `snapshot_at` | Data/hora da foto (fuso do computador) |
| `sprint` | Ex.: Lab01S01 |
| `issue_number` | Número da Issue no repositório |
| `title` | Título do card |
| `status` | Coluna do board (Backlog, To Do, Doing, Review, Done) |
| `assignees` | Responsáveis (separados por `;`) |
| `state` | OPEN ou CLOSED |
| `labels` | Labels da Issue |
| `url` | Link da Issue |

## Setup rápido (S01)

1. Clone o repositório.
2. Crie um [Personal Access Token](https://github.com/settings/tokens) no GitHub
   (classic: `public_repo` **e** `read:project` para o snapshot do Kanban;
   ou fine-grained com leitura de metadados públicos + Projects Read).
3. Copie `.env.example` para `.env` e preencha `GITHUB_TOKEN`.
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Teste autenticação + rateLimit (Issues #3 e #4):
   ```bash
   python -m src
   ```
   Se estiver ok, aparece o login e o `rateLimit` (remaining / resetAt).
   O cliente faz retry automático em erros de rede/5xx/429 e pausa se o
   `remaining` estiver baixo.

## Commits e Issues

Todo commit deve referenciar a Issue correspondente, por exemplo:

```text
#1 cria estrutura inicial de pastas
```
