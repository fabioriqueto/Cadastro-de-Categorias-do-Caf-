from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "categorias.db"


# ================================
# Banco de Dados
# ================================
def criar_tabela():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        """)
        conn.commit()


def listar_categorias():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM categorias ORDER BY id")
        return cursor.fetchall()


def adicionar_categoria(nome):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
        conn.commit()


def buscar_categoria(id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM categorias WHERE id=?", (id,))
        return cursor.fetchone()


def atualizar_categoria(id, nome):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE categorias SET nome=? WHERE id=?", (nome, id))
        conn.commit()


def excluir_categoria(id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categorias WHERE id=?", (id,))
        conn.commit()


# ================================
# Rotas Flask
# ================================
@app.route("/")
def index():
    categorias = listar_categorias()
    return render_template("index.html", categorias=categorias)


@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if request.method == "POST":
        nome = request.form.get("nome")
        if nome:
            adicionar_categoria(nome)
            return redirect(url_for("index"))
    return render_template("adicionar.html")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    categoria = buscar_categoria(id)
    if request.method == "POST":
        nome = request.form.get("nome")
        if nome:
            atualizar_categoria(id, nome)
            return redirect(url_for("index"))
    return render_template("editar.html", categoria=categoria)


@app.route("/excluir/<int:id>")
def excluir(id):
    excluir_categoria(id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    criar_tabela()
    app.run(debug=True)
