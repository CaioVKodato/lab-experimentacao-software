"""
Gera o relatório final consolidado do Lab01 em PDF (Arial).
Uso: python scripts/generate_relatorio_final.py
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = DOCS / "relatorios" / "relatorio_lab01_final.pdf"

FONT_DIR = Path(r"C:\Windows\Fonts")
pdfmetrics.registerFont(TTFont("Arial", str(FONT_DIR / "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONT_DIR / "arialbd.ttf")))


def style_sheet() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            fontName="Arial-Bold",
            fontSize=14,
            leading=18,
            spaceAfter=10,
            alignment=TA_LEFT,
        ),
        "h1": ParagraphStyle(
            "h1",
            fontName="Arial-Bold",
            fontSize=12,
            leading=15,
            spaceBefore=14,
            spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName="Arial-Bold",
            fontSize=11,
            leading=14,
            spaceBefore=10,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Arial",
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "small",
            fontName="Arial",
            fontSize=9,
            leading=12,
            spaceAfter=4,
        ),
    }


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def table(data: list[list[str]], col_widths: list[float] | None = None) -> Table:
    t = Table(data, colWidths=col_widths, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, 0), "Arial-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Arial"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def fig(path: Path, width: float = 15 * cm) -> Image | Paragraph:
    if path.is_file():
        img = Image(str(path))
        ratio = img.imageWidth / img.imageHeight
        img.drawWidth = width
        img.drawHeight = width / ratio
        return img
    return p(f"[Figura não encontrada: {path.name}]", style_sheet()["small"])


def build_story() -> list:
    s = style_sheet()
    story: list = []

    story.append(p("Laboratório 01 — Relatório Final", s["title"]))
    story.append(
        p(
            "Laboratório de Experimentação de Software · Engenharia de Software · PUC Minas<br/>"
            "Prof. Danilo Maia",
            s["body"],
        )
    )
    story.append(Spacer(1, 0.2 * cm))
    story.append(
        table(
            [
                ["Integrante", "GitHub"],
                ["Caio Victor Kodato Teixeira", "CaioVKodato"],
                ["Henrique Volponi", "Henrique-volponi"],
                ["Jonas Martins", "Kjonps"],
            ],
            [7 * cm, 8 * cm],
        )
    )
    story.append(Spacer(1, 0.3 * cm))
    story.append(
        p(
            "<b>Repositório:</b> github.com/CaioVKodato/lab-experimentacao-software<br/>"
            "<b>GitHub Projects:</b> github.com/users/CaioVKodato/projects/6",
            s["body"],
        )
    )

    # 1. Introdução
    story.append(p("1. Introdução", s["h1"]))
    story.append(
        p(
            "Este trabalho analisa características de repositórios open-source populares no GitHub. "
            "Coletamos os 1.000 repositórios com mais estrelas e respondemos sete questões de pesquisa "
            "(RQ01–RQ07) sobre maturidade, contribuição externa, releases, atualização de código, "
            "linguagem primária, taxa de issues fechadas e o cruzamento dessas métricas por linguagem.",
            s["body"],
        )
    )
    story.append(
        p(
            "Na <b>S01</b> montamos o cliente GraphQL próprio e coletamos 100 repositórios; na <b>S02</b> "
            "escalamos para 1.000, validamos os dados e registramos hipóteses informais; na <b>S03</b> "
            "fizemos a análise descritiva com gráficos. O Kanban (GitHub Projects v2) foi quem nos manteve "
            "organizado e ciente das tarefas para cada atuante no projeto.",
            s["body"],
        )
    )

    # 2. Hipóteses
    story.append(p("2. Hipóteses informais", s["h1"]))
    story.append(
        table(
            [
                ["RQ", "Hipótese resumida"],
                ["01", "Repositórios populares tendem a ser antigos/maduros."],
                ["02", "Recebem muita contribuição externa (PRs aceitas)."],
                ["03", "Lançam releases com frequência — mas não em todos."],
                ["04", "São atualizados com frequência (último push recente)."],
                ["05", "Concentram-se nas linguagens mais usadas no GitHub."],
                ["06", "Quem usa o tracker de issues tem alta taxa de fechamento."],
                [
                    "07",
                    "Linguagens do top-10 Octoverse têm mais PRs, releases e pushes recentes.",
                ],
            ],
            [1.2 * cm, 14 * cm],
        )
    )
    story.append(
        p(
            "As hipóteses foram redigidas por Jonas Martins nos documentos de hipóteses informais "
            "(idade/PRs, atualização/linguagens, releases/issues) e conferidas contra "
            "<i>data/repositories_top1000.csv</i>. Para RQ05 e RQ07 usamos o ranking do "
            "GitHub Octoverse 2025 como referência de linguagens populares.",
            s["small"],
        )
    )

    # 3. Metodologia
    story.append(p("3. Metodologia", s["h1"]))
    story.append(
        p(
            "A coleta usa a API GraphQL do GitHub com script próprio em Python (<i>src/collect/</i>, "
            "<i>src/github/</i>), sem bibliotecas que encapsulam a API. O token fica no arquivo <i>.env</i>. "
            "Como a Search API limita cada busca a 1.000 resultados e alguns nós vêm nulos, abrimos janelas "
            "sucessivas por faixa de estrelas até completar 1.000 repositórios válidos.",
            s["body"],
        )
    )
    story.append(
        table(
            [
                ["Coluna", "RQ", "Origem na API"],
                ["age_days", "01", "createdAt"],
                ["merged_prs", "02", "pullRequests(MERGED)"],
                ["releases", "03", "releases.totalCount"],
                ["days_since_push", "04", "pushedAt (não updatedAt)"],
                ["language", "05/07", "primaryLanguage"],
                ["closed_ratio", "06", "issues CLOSED/OPEN (sem PRs)"],
            ],
            [3.5 * cm, 1.5 * cm, 10 * cm],
        )
    )
    story.append(
        p(
            "Cada integrante validou sua fatia de RQs na S02 — conferência de idade e PRs, "
            "de push e linguagens, de releases e taxa de issues fechadas — com scripts em "
            "<i>src/analysis/</i> e relatórios em <i>docs/s02/henrique/validacao_s02_*.md</i>. Outliers foram "
            "marcados pelo critério de Tukey (1,5 × IQR). Repositórios com <i>total_issues = 0</i> "
            "ficam fora da análise da RQ06.",
            s["body"],
        )
    )

    # 4. Resultados
    story.append(p("4. Resultados", s["h1"]))

    story.append(p("4.1. RQ01 — Idade do repositório", s["h2"]))
    story.append(
        p(
            "Mediana de <b>2.826 dias</b> (~7,7 anos); Q1–Q3 entre 3,5 e 11,4 anos. "
            "676 repositórios (67,6%) têm 5 anos ou mais. Ainda assim, 82 (8,2%) têm menos de 1 ano — "
            "casos de viralidade recente (IA, listas, tutoriais). Nenhum outlier pelo Tukey.",
            s["body"],
        )
    )
    story.append(fig(DOCS / "s03" / "caio" / "analise_s03_rq01_idade.png", 14 * cm))
    story.append(Spacer(1, 0.2 * cm))

    story.append(p("4.2. RQ02 — PRs aceitas", s["h2"]))
    story.append(
        p(
            "Mediana de <b>768</b> PRs merged; Q3 = 3.415. Há 124 outliers acima de 8.275 PRs "
            "(12,4% da amostra). Vinte repositórios têm zero PRs no GitHub — em geral listas, "
            "ou projetos que não usam pull request na plataforma (ex.: Linux).",
            s["body"],
        )
    )

    story.append(p("4.3. RQ03 — Releases", s["h2"]))
    story.append(
        p(
            "Mediana geral = <b>40</b> releases; 277 repositórios (27,7%) nunca publicaram release. "
            "Entre quem usa Releases, a mediana sobe para 95. Listas e guias costumam ficar em zero.",
            s["body"],
        )
    )

    story.append(p("4.4. RQ04 — Última atualização", s["h2"]))
    story.append(
        p(
            "Mediana de <b>1 dia</b> desde o último push; 75% da amostra receberam commit em até "
            "<b>48 dias</b>. A distribuição concentra-se perto de zero, com cauda de repositórios parados.",
            s["body"],
        )
    )
    story.append(fig(DOCS / "s03" / "jonas" / "rq04_days_since_push_hist.png", 14 * cm))
    story.append(Spacer(1, 0.2 * cm))

    story.append(p("4.5. RQ05 — Linguagem primária", s["h2"]))
    story.append(
        p(
            "Python (22,7%), TypeScript (17,3%) e JavaScript (11,1%) somam mais da metade da amostra. "
            "As três aparecem no Octoverse 2025. Outros 8,7% não têm linguagem detectável (listas em Markdown).",
            s["body"],
        )
    )
    story.append(fig(DOCS / "s03" / "jonas" / "rq05_language_bar.png", 14 * cm))
    story.append(Spacer(1, 0.2 * cm))

    story.append(p("4.6. RQ06 — Issues fechadas", s["h2"]))
    story.append(
        p(
            "Entre os 957 repositórios com pelo menos uma issue, a mediana de <i>closed_ratio</i> é "
            "<b>87,5%</b> (Q1 = 70,4%). Os 43 sem issues foram excluídos — não representam 0% de fechamento.",
            s["body"],
        )
    )

    story.append(p("4.7. RQ07 — Cruzamento por linguagem", s["h2"]))
    story.append(
        p(
            "Separamos repositórios em linguagens do top-10 Octoverse (760 repos) e demais (240). "
            "No grupo popular, as medianas são: <b>1.075 PRs</b>, <b>66,5 releases</b> e "
            "<b>0,5 dias</b> desde o último push. No outro grupo: 290 PRs, 0 releases e 19 dias.",
            s["body"],
        )
    )
    story.append(Spacer(1, 0.2 * cm))
    story.append(fig(DOCS / "s03" / "henrique" / "rq07_por_linguagem.png", 17 * cm))

    # 5. Discussão
    story.append(PageBreak())
    story.append(p("5. Discussão: hipótese × resultado", s["h1"]))
    story.append(
        table(
            [
                ["RQ", "Hipótese", "Resultado"],
                ["01", "Maduros", "Confirmada no centro da distribuição (~7,7 anos)"],
                ["02", "Muita contribuição", "Confirmada (mediana alta); 2% sem PR no GitHub"],
                ["03", "Releases frequentes", "Parcial — 27,7% sem nenhuma release"],
                ["04", "Atualizados", "Confirmada — mediana de 1 dia desde push"],
                ["05", "Linguagens populares", "Confirmada — domínio de Python/TS/JS"],
                ["06", "Alto % fechadas", "Confirmada — mediana 87,5%"],
                ["07", "Cruzamento", "Confirmada nas 3 métricas; Shell e listas puxam para baixo"],
            ],
            [1.2 * cm, 4.5 * cm, 9.5 * cm],
        )
    )
    story.append(Spacer(1, 0.3 * cm))
    story.append(
        p(
            "No geral, repositórios muito estrelados costumam ser antigos, ativos e com comunidade grande — "
            "mas a amostra mistura frameworks de produção com listas, tutoriais e projetos que não usam "
            "Releases ou PRs como a maioria. Isso pesa nas RQs 02, 03 e 07.",
            s["body"],
        )
    )
    story.append(
        p(
            "Também há viés na coleta: ordenar por estrelas favorece ecossistemas grandes (TypeScript, Go, Rust) "
            "e conteúdo que viraliza sem ciclo de software tradicional. Mesmo assim, com 1.000 repositórios "
            "a leitura descritiva fica consistente.",
            s["body"],
        )
    )

    # 6. Processo
    story.append(p("6. Configuração do processo", s["h1"]))
    story.append(
        p(
            "O grupo usa GitHub Projects v2 com colunas Backlog → To Do → Doing → Review → Done. "
            "Cada tarefa virou Issue com responsável (Assignee), com commits vinculados à tarefa "
            "correspondente no repositório. O limite de WIP em Doing é <b>4 cartões</b> (~2 por pessoa), "
            "para evitar trabalho paralelo demais e garantir passagem por Review.",
            s["body"],
        )
    )
    story.append(
        p(
            "Ao fim de cada sprint exportamos o board com <i>python -m src.snapshot --sprint Lab01S0N</i>. "
            "Os CSVs ficam em <i>snapshots/</i> (S01: 2026-08-13; S02: 2026-08-21). Essa série será "
            "usada nos Labs 04 e 05 porque o Projects não guarda histórico de coluna via API.",
            s["body"],
        )
    )
    story.append(
        p(
            "<b>Board ao final do Lab01:</b> ver Projects em "
            "github.com/users/CaioVKodato/projects/6 — tarefas das três sprints em Done, "
            "com fluxo Backlog → Done documentado nos snapshots.",
            s["body"],
        )
    )

    return story


def main() -> None:
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Lab01 — Relatório Final",
        author="Grupo Lab Experimentação de Software",
    )
    doc.build(build_story())
    print(f"PDF gerado: {OUT}")


if __name__ == "__main__":
    main()
