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
├── src/          # Scripts de coleta GraphQL
├── data/         # CSVs da mineração (repos)
├── snapshots/    # Snapshots CSV do GitHub Projects
├── docs/         # Relatório e documentação
├── .env.example  # Modelo de variáveis de ambiente
└── README.md
```

## Setup rápido (S01)

1. Clone o repositório.
2. Crie um Personal Access Token no GitHub.
3. Copie `.env.example` para `.env` e preencha `GITHUB_TOKEN`.
4. (Em breve) rode o script de coleta em `src/`.

## Commits e Issues

Todo commit deve referenciar a Issue correspondente, por exemplo:

```text
#1 cria estrutura inicial de pastas
```
