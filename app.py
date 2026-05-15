"""
Sistema de Feedback de Clientes
Backend: Flask + SQLite (biblioteca padrão do Python)
"""

import sqlite3
import os
from datetime import datetime
from functools import wraps
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, jsonify, flash
)

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "feedbackpro-secret-2024"

DB_PATH = os.path.join(os.path.dirname(__file__), "feedback.db")

# Credenciais do administrador (simples, sem banco, conforme escopo)
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"


# ---------------------------------------------------------------------------
# Banco de dados
# ---------------------------------------------------------------------------
def get_db():
    """Retorna uma conexão SQLite com Row Factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Cria a tabela de feedbacks se não existir."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feedbacks (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                nome      TEXT    NOT NULL,
                nota      INTEGER NOT NULL CHECK(nota BETWEEN 1 AND 5),
                comentario TEXT,
                criado_em TEXT    NOT NULL
            )
        """)
        conn.commit()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def login_required(f):
    """Decorador: redireciona para login se não autenticado."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


def get_star_label(nota: int) -> str:
    labels = {1: "Péssimo", 2: "Ruim", 3: "Regular", 4: "Bom", 5: "Excelente"}
    return labels.get(nota, "")


# ---------------------------------------------------------------------------
# Rotas públicas
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Página pública de envio de feedback."""
    return render_template("index.html")


@app.route("/enviar", methods=["POST"])
def enviar():
    """Recebe e persiste um feedback."""
    nome = request.form.get("nome", "").strip()
    nota_raw = request.form.get("nota", "").strip()
    comentario = request.form.get("comentario", "").strip()

    # Validação
    erros = []
    if not nome:
        erros.append("O campo <strong>Nome</strong> é obrigatório.")
    if not nota_raw or not nota_raw.isdigit() or not (1 <= int(nota_raw) <= 5):
        erros.append("A <strong>Nota</strong> deve ser um número inteiro entre 1 e 5.")

    if erros:
        return render_template("index.html", erros=erros, nome=nome, comentario=comentario)

    nota = int(nota_raw)
    criado_em = datetime.now().strftime("%d/%m/%Y %H:%M")

    with get_db() as conn:
        conn.execute(
            "INSERT INTO feedbacks (nome, nota, comentario, criado_em) VALUES (?, ?, ?, ?)",
            (nome, nota, comentario or None, criado_em)
        )
        conn.commit()

    return render_template("index.html", sucesso=True)


# ---------------------------------------------------------------------------
# Rotas administrativas
# ---------------------------------------------------------------------------
@app.route("/admin/login", methods=["GET", "POST"])
def login():
    """Tela de login do administrador."""
    erro = None
    if request.method == "POST":
        user = request.form.get("usuario", "")
        pwd = request.form.get("senha", "")
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))
        erro = "Usuário ou senha inválidos."
    return render_template("login.html", erro=erro)


@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/admin")
@login_required
def admin():
    """Painel administrativo com listagem e filtros."""
    nota_filtro = request.args.get("nota", "")
    query = "SELECT * FROM feedbacks"
    params = []

    if nota_filtro and nota_filtro.isdigit() and 1 <= int(nota_filtro) <= 5:
        query += " WHERE nota = ?"
        params.append(int(nota_filtro))

    query += " ORDER BY id DESC"

    with get_db() as conn:
        feedbacks = conn.execute(query, params).fetchall()
        total = conn.execute("SELECT COUNT(*) FROM feedbacks").fetchone()[0]
        media_row = conn.execute("SELECT AVG(nota) FROM feedbacks").fetchone()[0]
        media = round(media_row, 1) if media_row else 0

        # Distribuição por nota para gráfico inline
        dist = {}
        for n in range(1, 6):
            count = conn.execute(
                "SELECT COUNT(*) FROM feedbacks WHERE nota = ?", (n,)
            ).fetchone()[0]
            dist[n] = count

    feedbacks_list = [dict(row) for row in feedbacks]
    for fb in feedbacks_list:
        fb["label"] = get_star_label(fb["nota"])

    return render_template(
        "admin.html",
        feedbacks=feedbacks_list,
        total=total,
        media=media,
        nota_filtro=nota_filtro,
        dist=dist,
    )


@app.route("/admin/excluir/<int:feedback_id>", methods=["POST"])
@login_required
def excluir(feedback_id):
    """Exclui um feedback pelo ID."""
    with get_db() as conn:
        conn.execute("DELETE FROM feedbacks WHERE id = ?", (feedback_id,))
        conn.commit()
    return redirect(request.referrer or url_for("admin"))


# ---------------------------------------------------------------------------
# API JSON (bônus)
# ---------------------------------------------------------------------------
@app.route("/api/feedbacks")
@login_required
def api_feedbacks():
    """Endpoint JSON para consumo externo."""
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM feedbacks ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])


# ---------------------------------------------------------------------------
# Entrada
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    init_db()
    print("\n" + "="*50)
    print("  Sistema de Feedback de Clientes")
    print("  Acesse: http://127.0.0.1:5000")
    print("  Admin:  http://127.0.0.1:5000/admin/login")
    print("  Login:  admin / admin123")
    print("="*50 + "\n")
    app.run(debug=True)
