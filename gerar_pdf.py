# -*- coding: utf-8 -*-
"""
Gera: Documento de Requisitos v2.0.pdf
- Todas as células usam Paragraph para wrap correto
- Layout limpo, semelhante ao original
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)

# ── Página ──────────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4          # 595.27 x 841.89 pt
L_MARGIN = R_MARGIN = 2*cm
USABLE_W = PAGE_W - L_MARGIN - R_MARGIN   # ≈ 17 cm

OUTPUT = "Documento de Requisitos v2.0.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=L_MARGIN, rightMargin=R_MARGIN,
    topMargin=2*cm, bottomMargin=2*cm,
    title="Documento de Requisitos v2.0 — Sistema de Feedback de Clientes",
)

# ── Cores ────────────────────────────────────────────────────────────────────
C_BLACK   = colors.HexColor("#000000")
C_DARK    = colors.HexColor("#1a1a1a")
C_HEADER  = colors.HexColor("#d9d9d9")   # cinza claro — igual ao original
C_ROW_ALT = colors.HexColor("#f5f5f5")
C_BORDER  = colors.HexColor("#999999")
C_PURPLE  = colors.HexColor("#6c63ff")
C_GREEN   = colors.HexColor("#00a884")
C_WHITE   = colors.white

# ── Estilos de parágrafo ─────────────────────────────────────────────────────
def ps(name, **kw):
    defaults = dict(fontName="Helvetica", fontSize=9, leading=13,
                    textColor=C_DARK, spaceAfter=0, spaceBefore=0)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

ST_TITLE   = ps("title",   fontName="Helvetica-Bold", fontSize=16,
                textColor=C_BLACK, leading=20, spaceAfter=2, alignment=TA_LEFT)
ST_SUBTITLE= ps("sub",     fontName="Helvetica", fontSize=11,
                textColor=C_DARK, leading=15, spaceAfter=12, alignment=TA_LEFT)
ST_H1      = ps("h1",      fontName="Helvetica-Bold", fontSize=13,
                textColor=C_BLACK, leading=17, spaceBefore=14, spaceAfter=6)
ST_H2      = ps("h2",      fontName="Helvetica-Bold", fontSize=11,
                textColor=C_DARK,  leading=15, spaceBefore=10, spaceAfter=4)
ST_BODY    = ps("body",    fontSize=9.5, leading=14, spaceAfter=6,
                alignment=TA_JUSTIFY)
ST_BULLET  = ps("bullet",  fontSize=9.5, leading=14, leftIndent=12, spaceAfter=3)
ST_NOTE    = ps("note",    fontSize=8.5, leading=13, textColor=colors.HexColor("#333"),
                leftIndent=6, spaceAfter=6)
ST_FOOTER  = ps("footer",  fontSize=8,  textColor=colors.HexColor("#888"),
                alignment=TA_CENTER, spaceAfter=0)

# Estilos para células de tabela
ST_TH      = ps("th",  fontName="Helvetica-Bold", fontSize=9, leading=12)
ST_TD      = ps("td",  fontName="Helvetica",       fontSize=9, leading=12)
ST_TD_BOLD = ps("tdb", fontName="Helvetica-Bold",  fontSize=9, leading=12)
ST_TD_NEW  = ps("tdn", fontName="Helvetica-Bold",  fontSize=9, leading=12,
                textColor=C_GREEN)

# ── Helpers ───────────────────────────────────────────────────────────────────
def sp(h=0.35):
    return Spacer(1, h * cm)

def hr_line(color=C_BORDER, thickness=0.6):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceAfter=4, spaceBefore=2)

def h1(text):
    return Paragraph(text, ST_H1)

def h2(text):
    return Paragraph(text, ST_H2)

def body(text):
    return Paragraph(text, ST_BODY)

def bullet(text):
    return Paragraph(f"• {text}", ST_BULLET)

def note(text):
    return Paragraph(f"Obs.: {text}", ST_NOTE)

def th(text):
    """Célula de cabeçalho."""
    return Paragraph(text, ST_TH)

def td(text, bold=False, new=False):
    """Célula de dado com wrap."""
    if new:
        return Paragraph(text, ST_TD_NEW)
    return Paragraph(text, ST_TD_BOLD if bold else ST_TD)

def make_table(headers, rows, col_widths, new_rows=None):
    """
    Constrói uma Table com Paragraphs em todas as células.
    new_rows: conjunto de índices (1-based, do dado) de linhas 'novas'.
    """
    new_rows = new_rows or set()

    # Linha de cabeçalho
    table_data = [[th(h) for h in headers]]

    # Linhas de dados
    for i, row in enumerate(rows, start=1):
        is_new = i in new_rows
        table_data.append([
            td(cell, bold=(j == 0), new=(is_new and j == 0))
            for j, cell in enumerate(row)
        ])

    # Estilo base
    style_cmds = [
        ("BACKGROUND",   (0, 0), (-1, 0),  C_HEADER),
        ("GRID",         (0, 0), (-1, -1), 0.5, C_BORDER),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]

    # Linhas alternadas
    for i in range(1, len(table_data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), C_ROW_ALT))

    # Destaque nas linhas novas
    for idx in new_rows:
        row_idx = idx  # 1-based já é o índice correto (header é 0)
        style_cmds.append(("BACKGROUND", (0, row_idx), (-1, row_idx),
                            colors.HexColor("#edfff7")))

    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle(style_cmds))
    return t

# ── STORY ─────────────────────────────────────────────────────────────────────
story = []

# ─────────────────────────────────────────────────────────────────────────────
# CAPA
# ─────────────────────────────────────────────────────────────────────────────
story.append(sp(0.3))
story.append(Paragraph("Documento de Requisitos: Sistema de", ST_TITLE))
story.append(Paragraph("Feedback de Clientes", ST_TITLE))
story.append(Paragraph("Versão 2.0", ST_SUBTITLE))
story.append(hr_line(C_BORDER, 1))
story.append(sp(0.2))

# ─────────────────────────────────────────────────────────────────────────────
# 1. INTRODUÇÃO
# ─────────────────────────────────────────────────────────────────────────────
story.append(h1("Introdução"))
story.append(body(
    "O Sistema de Feedback de Clientes é uma solução desenvolvida para coletar, organizar e "
    "analisar as percepções dos consumidores sobre os serviços ou produtos de uma organização."
))
story.append(body(
    "O projeto busca resolver o problema da falta de um canal estruturado para ouvir o cliente, "
    "o que muitas vezes resulta em perda de insights valiosos para a melhoria contínua. O "
    "desenvolvimento desta solução é importante para centralizar as opiniões, permitindo que a "
    "gestão identifique falhas e sucessos de forma rápida e baseada em dados reais."
))
story.append(sp(0.15))
story.append(Paragraph("Público-alvo:", ST_H2))
story.append(bullet(
    "Clientes: Usuários que desejam expressar sua satisfação ou descontentamento com o "
    "atendimento de forma ágil."
))
story.append(bullet(
    "Administradores/Gestores: Responsáveis por monitorar os feedbacks, gerenciar os "
    "dados e utilizar as informações para tomadas de decisão estratégicas."
))

# ─────────────────────────────────────────────────────────────────────────────
# 2. REQUISITOS FUNCIONAIS
# ─────────────────────────────────────────────────────────────────────────────
story.append(h1("Requisitos Funcionais"))

# Larguras: ID(1.4) + Requisito(3.4) + Descrição(9.5) + Prioridade(2.7) = 17cm
RF_COLS = [1.4*cm, 3.4*cm, 9.5*cm, 2.7*cm]
RF_HEADERS = ["ID", "Requisito", "Descrição", "Prioridade"]
RF_ROWS = [
    ["RF001", "Coleta de Feedback",
     "O sistema deve permitir que o cliente envie um feedback informando nome, "
     "nota (1 a 5) e um comentário.",
     "Essencial"],
    ["RF002", "Validação de Entrada",
     "O sistema deve realizar a validação de campos obrigatórios (nome e nota) "
     "antes do envio.",
     "Essencial"],
    ["RF003", "Autenticação Admin",
     "O sistema deve permitir o acesso do administrador a uma página restrita "
     "via login simples.",
     "Essencial"],
    ["RF004", "Visualização de Lista",
     "O sistema deve listar todos os feedbacks recebidos em uma tabela na área "
     "administrativa.",
     "Essencial"],
    ["RF005", "Exclusão de Dados",
     "O sistema deve permitir que o administrador exclua um feedback da lista.",
     "Importante"],
    ["RF006", "Contador de Registros",
     "O sistema deve exibir um contador total de feedbacks recebidos.",
     "Desejável"],
    ["RF007", "Filtro por Nota",
     "O sistema deve permitir filtrar a lista de feedbacks por nota "
     "(ex: exibir apenas notas 5).",
     "Importante"],
    ["RF008", "Notificação de Sucesso",
     "O sistema deve exibir uma mensagem de confirmação de sucesso após o "
     "envio do feedback pelo cliente.",
     "Essencial"],
]
story.append(make_table(RF_HEADERS, RF_ROWS, RF_COLS))

# ─────────────────────────────────────────────────────────────────────────────
# 3. REQUISITOS NÃO FUNCIONAIS
# ─────────────────────────────────────────────────────────────────────────────
story.append(h1("Requisitos Não Funcionais"))

RNF_COLS = [1.4*cm, 3.4*cm, 9.5*cm, 2.7*cm]
RNF_HEADERS = ["ID", "Requisito", "Descrição", "Prioridade"]
RNF_ROWS = [
    ["RNF001", "Interface Web",
     "O sistema deve possuir uma interface web simples e funcional.",
     "Essencial"],
    ["RNF002", "Persistência",
     "Os dados devem ser armazenados em um banco de dados relacional ou "
     "arquivo estruturado (JSON/CSV).",
     "Essencial"],
    ["RNF003", "Compatibilidade",
     "O sistema deve ser executável em navegadores modernos "
     "(Chrome, Firefox ou Edge).",
     "Importante"],
    ["RNF004", "Tecnologia",
     "O sistema deve ser desenvolvido utilizando tecnologias web padrão "
     "(HTML/JS/CSS e um backend simples).",
     "Essencial"],
]
story.append(make_table(RNF_HEADERS, RNF_ROWS, RNF_COLS))

# ─────────────────────────────────────────────────────────────────────────────
# 4. REGRAS DE NEGÓCIO
# ─────────────────────────────────────────────────────────────────────────────
story.append(h1("Regras de Negócio"))

RN_COLS = [1.4*cm, 3.4*cm, 8.0*cm, 4.2*cm]
RN_HEADERS = ["ID", "Regra", "Descrição", "Exceções"]
RN_ROWS = [
    ["RN001", "Intervalo de Notas",
     "A nota atribuída pelo cliente deve ser obrigatoriamente um número "
     "inteiro entre 1 e 5.",
     "Nenhuma"],
    ["RN002", "Obrigatoriedade de Comentário",
     "O campo de comentário é facultativo, permitindo que o cliente envie "
     "apenas a nota.",
     "Nenhuma"],
    ["RN003", "Irreversibilidade",
     "Uma vez que um feedback é excluído pelo administrador, os dados não "
     "podem ser recuperados via interface.",
     "Recuperação via backup do banco de dados (se disponível)."],
]
story.append(make_table(RN_HEADERS, RN_ROWS, RN_COLS))

# ─────────────────────────────────────────────────────────────────────────────
# 5. NOVAS IMPLEMENTAÇÕES (v2.0)  ← seção adicionada
# ─────────────────────────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(h1("Novas Implementações (v2.0)"))
story.append(body(
    "As funcionalidades abaixo foram implementadas além do escopo original. "
    "Todas mantêm o projeto simples de executar localmente."
))
story.append(sp(0.2))

# 5.1 Design System
story.append(h2("5.1 Design System — Dark Mode Profissional"))
story.append(body(
    "O frontend foi construído com um design system completo em CSS puro, "
    "baseado em variáveis CSS (tokens) para cores, bordas, sombras e transições. "
    "O tema dark mode utiliza uma paleta coesa com destaque em violeta (#6c63ff) "
    "e verde-água (#00d4aa)."
))
story.append(bullet("Tipografia Google Fonts — família Inter (pesos 300–800)."))
story.append(bullet("Gradientes radiais no hero e nos cards de estatísticas."))
story.append(bullet("Navbar fixa com backdrop-filter (efeito glassmorphism)."))
story.append(bullet("Responsividade com CSS Grid e a função clamp()."))
story.append(sp(0.15))

# 5.2 Scroll-Reveal
story.append(h2("5.2 Animações de Scroll (Intersection Observer)"))
story.append(body(
    "Todos os elementos de conteúdo recebem a classe .reveal, que inicia "
    "com opacity: 0 + translateY(36px). O Intersection Observer adiciona a "
    "classe .visible quando o elemento entra no viewport, disparando a animação "
    "de fade-in + slide-up. Cards de features têm delay escalonado (nth-child) "
    "para efeito cascata."
))
story.append(sp(0.15))

# 5.3 Star Rating
story.append(h2("5.3 Star Rating Interativo — CSS Puro"))
story.append(body(
    "O seletor de nota usa a técnica CSS de flex-direction: row-reverse "
    "combinado com seletores ~ para retroiluminar estrelas anteriores à "
    "selecionada. Não utiliza nenhuma linha de JavaScript. "
    "Hover adiciona escala (transform: scale(1.2)) à estrela ativa."
))
story.append(sp(0.15))

# 5.4 Dashboard Admin
story.append(h2("5.4 Painel Administrativo com Dashboard"))
story.append(body(
    "O painel administrativo foi expandido com:"
))
story.append(bullet("Sidebar fixa com links de navegação e botão de logout."))
story.append(bullet("Card — Total de Feedbacks: contador absoluto do banco de dados."))
story.append(bullet("Card — Média Geral: média aritmética das notas com ícone de estrela."))
story.append(bullet(
    "Card — Distribuição por Nota: mini gráfico de barras horizontal (CSS puro) "
    "mostrando a proporção de feedbacks para cada nota de 1 a 5."
))
story.append(bullet(
    "Badges coloridos na tabela: cada nota recebe uma cor distinta "
    "(verde=5, roxo=4, amarelo=3, laranja=2, vermelho=1) com rótulo textual."
))
story.append(bullet(
    "Estrelas visuais na tabela: representação gráfica da nota com estrelas "
    "preenchidas e vazias."
))
story.append(sp(0.15))

# 5.5 API JSON
story.append(h2("5.5 Endpoint de API JSON (Bônus)"))
story.append(body(
    "Foi adicionado o endpoint GET /api/feedbacks, protegido pela sessão do "
    "administrador, que retorna todos os feedbacks em formato JSON. "
    "Útil para integração com ferramentas de análise externas ou exportação de dados."
))
story.append(sp(0.15))

# 5.6 Preservação de campos
story.append(h2("5.6 Preservação de Campos Após Erro de Validação"))
story.append(body(
    "Ao enviar o formulário com dados inválidos, o backend retorna a página com "
    "os valores de nome e comentário preservados, evitando que o usuário precise "
    "redigitar tudo. Os erros são listados em um banner detalhado acima do formulário."
))
story.append(sp(0.3))

# ─────────────────────────────────────────────────────────────────────────────
# 6. STACK TECNOLÓGICO
# ─────────────────────────────────────────────────────────────────────────────
story.append(h1("Stack Tecnológico"))

ST_COLS = [4.0*cm, 7.5*cm, 5.5*cm]
ST_HEADERS = ["Camada", "Tecnologia", "Versão mínima"]
ST_ROWS = [
    ["Backend",        "Python + Flask",               "Python 3.9 / Flask 3.0"],
    ["Banco de Dados", "SQLite",                        "Biblioteca padrão do Python"],
    ["Frontend",       "HTML5 + CSS3 (puro)",           "—"],
    ["JavaScript",     "Intersection Observer API",     "Navegadores modernos"],
    ["Tipografia",     "Google Fonts — Inter",          "CDN público"],
]
story.append(make_table(ST_HEADERS, ST_ROWS, ST_COLS))

# ─────────────────────────────────────────────────────────────────────────────
# 7. ESTRUTURA DE ARQUIVOS
# ─────────────────────────────────────────────────────────────────────────────
story.append(h1("Estrutura de Arquivos do Projeto"))

ARQ_COLS = [5.5*cm, 11.5*cm]
ARQ_HEADERS = ["Arquivo / Pasta", "Responsabilidade"]
ARQ_ROWS = [
    ["app.py",               "Backend Flask: rotas, lógica, autenticação e queries SQLite"],
    ["requirements.txt",     "Dependências do projeto (apenas Flask)"],
    ["feedback.db",          "Banco de dados SQLite — criado automaticamente na 1ª execução"],
    ["static/style.css",     "Design system completo: tokens CSS, componentes e animações"],
    ["templates/index.html", "Página pública: formulário de envio de feedback com star rating"],
    ["templates/login.html", "Tela de login do administrador"],
    ["templates/admin.html", "Painel admin: dashboard, tabela, filtros e exclusão"],
]
story.append(make_table(ARQ_HEADERS, ARQ_ROWS, ARQ_COLS))

# ─────────────────────────────────────────────────────────────────────────────
# 8. ROTAS DA APLICAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
story.append(h1("Rotas da Aplicação"))

RT_COLS = [1.8*cm, 4.8*cm, 7.2*cm, 3.2*cm]
RT_HEADERS = ["Método", "Rota", "Descrição", "Acesso"]
RT_ROWS = [
    ["GET",  "/",                   "Formulário público de feedback",         "Público"],
    ["POST", "/enviar",             "Processa e salva o feedback no banco",   "Público"],
    ["GET",  "/admin/login",        "Tela de login do administrador",         "Público"],
    ["POST", "/admin/login",        "Autentica o administrador",              "Público"],
    ["GET",  "/admin/logout",       "Encerra a sessão admin",                 "Público"],
    ["GET",  "/admin",              "Painel com dashboard, lista e filtros",  "Admin"],
    ["POST", "/admin/excluir/<id>", "Exclui um feedback pelo ID",             "Admin"],
    ["GET",  "/api/feedbacks",      "Lista todos os feedbacks em JSON",       "Admin"],
]
story.append(make_table(RT_HEADERS, RT_ROWS, RT_COLS))

# ─────────────────────────────────────────────────────────────────────────────
# 9. MODELO DE DADOS
# ─────────────────────────────────────────────────────────────────────────────
story.append(h1("Modelo de Dados — Tabela feedbacks"))

DB_COLS = [2.5*cm, 2.2*cm, 5.5*cm, 6.8*cm]
DB_HEADERS = ["Coluna", "Tipo", "Constraint", "Descrição"]
DB_ROWS = [
    ["id",         "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Identificador único"],
    ["nome",       "TEXT",    "NOT NULL",                  "Nome do cliente"],
    ["nota",       "INTEGER", "NOT NULL, CHECK (1–5)",     "Nota de 1 a 5 estrelas"],
    ["comentario", "TEXT",    "NULL permitido",            "Comentário opcional"],
    ["criado_em",  "TEXT",    "NOT NULL",
     "Data e hora no formato DD/MM/AAAA HH:MM"],
]
story.append(make_table(DB_HEADERS, DB_ROWS, DB_COLS))

# ─────────────────────────────────────────────────────────────────────────────
# 10. COMO EXECUTAR
# ─────────────────────────────────────────────────────────────────────────────
story.append(h1("Como Executar o Projeto"))
story.append(note(
    "Pré-requisito: Python 3.9 ou superior instalado. "
    "Nenhum Docker, banco de dados externo ou arquivo .env é necessário."
))

EX_COLS = [1.5*cm, 15.5*cm]
EX_HEADERS = ["Passo", "Comando / Ação"]
EX_ROWS = [
    ["1", "Abrir o terminal na pasta do projeto:   cd \"Trabalho QA\""],
    ["2", "Instalar o Flask (apenas na 1ª vez):    pip install flask"],
    ["3", "Iniciar o servidor:                      python app.py"],
    ["4", "Abrir no navegador:                      http://127.0.0.1:5000"],
]
story.append(make_table(EX_HEADERS, EX_ROWS, EX_COLS))
story.append(sp(0.3))

story.append(h2("URLs do Sistema"))
URL_COLS = [4.5*cm, 7.5*cm, 5.0*cm]
URL_HEADERS = ["Página", "URL", "Credenciais"]
URL_ROWS = [
    ["Formulário público",    "http://127.0.0.1:5000",              "—"],
    ["Login administrador",   "http://127.0.0.1:5000/admin/login",  "admin / admin123"],
    ["Painel administrativo", "http://127.0.0.1:5000/admin",        "admin / admin123"],
    ["API JSON",              "http://127.0.0.1:5000/api/feedbacks","Sessão admin ativa"],
]
story.append(make_table(URL_HEADERS, URL_ROWS, URL_COLS))

# ── Rodapé ───────────────────────────────────────────────────────────────────
story.append(sp(0.8))
story.append(hr_line(C_BORDER, 0.6))
story.append(Paragraph(
    "FeedbackPro · Documento de Requisitos v2.0 · Projeto Acadêmico",
    ST_FOOTER
))

# ── Build ─────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF gerado com sucesso: {OUTPUT}")
