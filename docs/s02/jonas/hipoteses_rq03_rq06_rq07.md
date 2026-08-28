# Hipóteses Informais — RQ03, RQ06 e nota da RQ07

Issue: #25
Dataset: `data/repositories_top1000.csv` (1000 repositórios)
Validação de referência: issue #22

## RQ03 — Sistemas populares lançam releases com frequência?

**Hipótese:** confirmação apenas parcial — releases frequentes são comuns, mas não universais.

**Justificativa:** era esperado um ciclo de release ativo, associado a equipes de manutenção maiores. Os dados mostram um quadro dividido: 27,7% da amostra não tem nenhuma release publicada, e a mediana geral é de apenas 40 releases, puxada por uma cauda de projetos com centenas delas (Q3 = 149, máximo de 1000). Releases frequentes aparecem mais entre os projetos populares mais estruturados, não como regra geral da popularidade.

## RQ06 — Sistemas populares possuem um alto percentual de issues fechadas?

**Hipótese:** sim, sistemas populares têm alta taxa de resolução de issues.

**Justificativa:** repositórios populares, por terem mais colaboradores e visibilidade, tendem a tratar e fechar issues com mais eficiência. A validação confirma: entre os 957 repositórios com pelo menos uma issue, a mediana de fechamento foi de 87,5%, com Q1 já em 70,4%. Os 43 repositórios sem nenhuma issue (4,3%) foram tratados à parte, já que zero issues não equivale a 0% de resolução.

## RQ07 — Cruzamento por linguagem (nota informal)

A RQ07 cruza os resultados de RQ02, RQ03 e RQ04 por linguagem primária, o que depende da segmentação desses valores por categoria de linguagem — ainda não calculada na validação atual (que trata cada métrica de forma agregada). Como Python, TypeScript e JavaScript concentram mais da metade da amostra (RQ05), é esperado que o comportamento agregado observado em RQ02/RQ03/RQ04 seja fortemente influenciado por esses três ecossistemas, com linguagens de nicho (Rust, C++, C) podendo apresentar padrões distintos ao serem isoladas. Análise completa fica pendente para a S03.
