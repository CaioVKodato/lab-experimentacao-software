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
│   └── graphql_client.py   # Auth + cliente HTTP GraphQL
├── data/                   # CSVs da mineração (repos)
├── snapshots/              # Snapshots CSV do GitHub Projects
├── docs/                   # Relatório e documentação
├── requirements.txt
├── .env.example            # Modelo de variáveis de ambiente
└── README.md
```

## Setup rápido (S01)

1. Clone o repositório.
2. Crie um [Personal Access Token](https://github.com/settings/tokens) no GitHub
   (classic com `public_repo`, ou fine-grained com leitura de metadados públicos).
3. Copie `.env.example` para `.env` e preencha `GITHUB_TOKEN`.
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Teste a autenticação GraphQL (Issue #3):
   ```bash
   python -m src.graphql_client
   ```
   Se estiver ok, aparece: `Autenticação OK. Usuário autenticado: <seu-user>`.

## Commits e Issues

Todo commit deve referenciar a Issue correspondente, por exemplo:

```text
#1 cria estrutura inicial de pastas
```
