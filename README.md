# Lab Experimentação de Software

Repositório do **Laboratório 01** — Características de repositórios populares + Setup do Kanban.

Disciplina: Laboratório de Experimentação de Software  
Curso: Engenharia de Software

## Integrantes

- [CaioVKodato](https://github.com/CaioVKodato)
- [Henrique-volponi](https://github.com/Henrique-volponi)
- [Kjonps](https://github.com/Kjonps) (Jonas Martins)

## GitHub Projects

Board Kanban (Projects v2):  
https://github.com/users/CaioVKodato/projects/6

### Processo (colunas e WIP)

| Coluna   | Uso                                      |
|----------|------------------------------------------|
| Backlog  | Ideias / tarefas ainda não priorizadas   |
| To Do    | Pronto para começar nesta sprint         |
| Doing    | Em andamento (**WIP = 6**, ~2 por pessoa)|
| Review   | Aguardando revisão do par                |
| Done     | Concluído                                |

**Justificativa do WIP:** limite de 6 cartões em Doing para o trio manter foco, evitar trabalho paralelo excessivo e forçar passagem por Review.

## Entregas do Lab01

| Sprint | Entrega |
|--------|---------|
| **S01** | Cliente GraphQL, coleta de 100 repos, Kanban configurado, validação por fatia |
| **S02** | Coleta de 1.000 repos, hipóteses informais, validação dos dados, 1ª versão do relatório |
| **S03** | Análise e visualização das 7 RQs |
| **Final** | Relatório consolidado em PDF |

## Estrutura do repositório

```text
.
├── src/
│   ├── github/                  # Auth, retry, rateLimit, cliente GraphQL
│   ├── collect/                 # Coleta paginada (S01=100, S02=1000) → CSV
│   ├── analysis/                # Validações S02 e análises S03
│   │   ├── validate_s02_*.py
│   │   ├── analyze_s03_rq01_rq03.py
│   │   ├── analyze_s03_rq04_rq06.py
│   │   └── rq07_por_linguagem.py
│   ├── snapshot.py              # Snapshot GraphQL do GitHub Projects → CSV
│   ├── validate.py              # Validações S01 (RQ01–RQ06)
│   └── __main__.py              # Teste de autenticação
├── scripts/
│   ├── generate_relatorio_docx.py
│   └── generate_relatorio_final.py
├── data/
│   ├── repositories.csv              # S01 — 100 repositórios
│   └── repositories_top1000.csv      # S02 — 1000 repositórios
├── snapshots/                   # Fotos do board (um CSV por sprint)
│   ├── lab01s01-2026-08-13.csv
│   ├── lab01s02-2026-08-21.csv
│   └── lab01s03-2026-08-27.csv
├── docs/                        # Ver docs/README.md
│   ├── relatorios/
│   ├── s01/validacao/ + s01/caio/
│   ├── s02/henrique/ + s02/jonas/
│   └── s03/caio/ + s03/jonas/ + s03/henrique/
├── validate_rq01_rq03.py
├── validate_rq04_rq06.py
├── requirements.txt
├── .env.example
└── README.md
```

## Setup rápido

1. Clone o repositório.
2. Crie um [Personal Access Token](https://github.com/settings/tokens) no GitHub
   (classic: `public_repo` **e** `read:project` para o snapshot do Kanban;
   ou fine-grained com leitura de metadados públicos + Projects Read).
3. Copie `.env.example` para `.env` e preencha `GITHUB_TOKEN`.
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Teste autenticação + rateLimit:
   ```bash
   python -m src
   ```
   Se estiver ok, aparece o login e o `rateLimit` (remaining / resetAt).

## Validação das fatias (S01)

Cada integrante valida os campos da sua parte em uma amostra de 5–10 repositórios **antes** de tratar a coleta dos 100 como fechada.

```bash
python -m src.validate
```

Documentação: `docs/s01/validacao/rq01_rq03.md` e `docs/s01/validacao/rq04_rq06.md`.

**RQ04:** métrica = `pushedAt` (não `updatedAt`).  
**RQ05:** métrica = `primaryLanguage`; fonte de ranking = [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/).  
**RQ06:** `issues(states: CLOSED|OPEN)` no GraphQL (sem pull requests).

## Coleta de dados (S01: 100 | S02: 1000)

Pacote modular `src/collect/`. A Search API limita cada query a **1000** hits; nós nulos são descartados e a coleta abre novas janelas (`stars:<mínimo`) até completar **1000 válidos**.

```bash
# S02 — 1000 repos → data/repositories_top1000.csv
python -m src.collect
python -m src.collect --n 1000

# S01 — 100 repos → data/repositories.csv
python -m src.collect --n 100
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

## Validação dos 1000 repositórios (S02)

Scripts em `src/analysis/validate_s02_*.py` — conferência de idade/PRs, push/linguagens e releases/issues fechadas.

```bash
python -m src.analysis.validate_s02_rq01_rq02
python -m src.analysis.validate_s02_rq04_rq05
python -m src.analysis.validate_s02_rq03_rq06
```

Relatórios: `docs/s02/henrique/validacao_s02_*.md`.

## Análise e visualização (S03)

Scripts que leem `data/repositories_top1000.csv` e geram markdown + gráficos:

```bash
python -m src.analysis.analyze_s03_rq01_rq03   # RQ01, RQ02, RQ03
python src/analysis/analyze_s03_rq04_rq06.py   # RQ04, RQ05, RQ06
python -m src.analysis.rq07_por_linguagem      # RQ07
```

| RQ | Responsável | Documento |
|---|---|---|
| 01–03 | Caio | `docs/s03/caio/analise_rq01_rq03.md` |
| 04–06 | Jonas | `docs/s03/jonas/analise_rq04_rq06.md` |
| 07 | Henrique | `docs/s03/henrique/rq07_linguagens.md` |

## Relatórios

- **1ª versão (S02):** [`docs/relatorios/relatorio_lab01_s02.md`](docs/relatorios/relatorio_lab01_s02.md)
- **Final (Lab01):** [`docs/relatorios/relatorio_lab01_final.docx`](docs/relatorios/relatorio_lab01_final.docx)
- **PDF:** [`docs/relatorios/relatorio_lab01_final.pdf`](docs/relatorios/relatorio_lab01_final.pdf)

Para regenerar o DOCX:

```bash
python scripts/generate_relatorio_docx.py
```

Para regenerar o PDF:

```bash
python scripts/generate_relatorio_final.py
```

## Snapshot do Kanban (fechamento de sprint)

O GitHub Projects v2 não guarda histórico de coluna consultável via API. O script abaixo tira uma foto do board e grava um CSV **novo** em `snapshots/`. Não sobrescreva arquivos antigos — a série é a base dos Labs 04 e 05.

```bash
python -m src.snapshot --sprint Lab01S03
```

Saída: `snapshots/lab01s03-AAAA-MM-DD.csv`.

O token precisa do escopo `read:project`. Rode no fim de cada sprint.

### Colunas do snapshot

| Coluna | Descrição |
|---|---|
| `snapshot_at` | Data/hora da foto (fuso do computador) |
| `sprint` | Ex.: Lab01S03 |
| `issue_number` | Número da Issue no repositório |
| `title` | Título do card |
| `status` | Coluna do board (Backlog, To Do, Doing, Review, Done) |
| `assignees` | Responsáveis (separados por `;`) |
| `state` | OPEN ou CLOSED |
| `labels` | Labels da Issue |
| `url` | Link da Issue |

## Commits e Issues

Todo commit deve referenciar a Issue correspondente, por exemplo:

```text
#1 cria estrutura inicial de pastas
```
