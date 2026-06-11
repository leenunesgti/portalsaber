from flask import Flask, request, redirect, session, render_template_string
import sqlite3
import os
from datetime import datetime

# ==========================
# CONFIGURAÇÃO
# ==========================

app = Flask(__name__)
app.secret_key = "victoria_maldonado_2026"

DB = "portal_escola.db"

ESCOLA = "EMEF Victoria Maldonado Cazarini"

WHATSAPP_DIRECAO = "5517996537933"
TELEFONE = "(17) 99653-7933"
EMAIL_ESCOLA = "contato@victoriamaldonado.edu.br"
ENDERECO = "Severínia - SP"

UPLOAD_FOLDER = "static/uploads"

os.makedirs("static", exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================
# BANCO DE DADOS
# ==========================

def conectar():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def criar_banco():

    conn = conectar()
    c = conn.cursor()

    # Usuários

    c.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        usuario TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        tipo TEXT NOT NULL
    )
    """)

    # Informativos

    c.execute("""
    CREATE TABLE IF NOT EXISTS informativos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        mensagem TEXT NOT NULL,
        imagem TEXT,
        data TEXT
    )
    """)

    # Dúvidas

    c.execute("""
    CREATE TABLE IF NOT EXISTS duvidas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        pergunta TEXT,
        resposta TEXT,
        data TEXT
    )
    """)

    # Sugestões

    c.execute("""
    CREATE TABLE IF NOT EXISTS sugestoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        sugestao TEXT,
        data TEXT
    )
    """)

    # Mensagens Direção

    c.execute("""
    CREATE TABLE IF NOT EXISTS mensagens(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        mensagem TEXT,
        resposta TEXT,
        data TEXT
    )
    """)

    # Professores

    c.execute("""
    CREATE TABLE IF NOT EXISTS professores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        materia TEXT
    )
    """)

    # Agendamentos

    c.execute("""
    CREATE TABLE IF NOT EXISTS agendamentos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pai TEXT,
        professor TEXT,
        data TEXT,
        status TEXT
    )
    """)

    # Galeria

    c.execute("""
    CREATE TABLE IF NOT EXISTS galeria(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        imagem TEXT,
        data TEXT
    )
    """)

    # Verifica Admin

    c.execute("""
    SELECT * FROM usuarios
    WHERE usuario='admin'
    """)

    admin = c.fetchone()

    if not admin:

        c.execute("""
        INSERT INTO usuarios(
            nome,
            email,
            usuario,
            senha,
            tipo
        )
        VALUES(?,?,?,?,?)
        """,
        (
            "Administrador",
            "admin@portal.com",
            "admin",
            "supremo00",
            "admin"
        ))

    conn.commit()
    conn.close()

# ==========================
# FUNÇÕES AUXILIARES
# ==========================

def logado():

    return "usuario" in session


def admin():

    return session.get("tipo") == "admin"


# Cria banco ao iniciar

criar_banco()
# ==========================
# TEMPLATE PRINCIPAL
# ==========================

def pagina(titulo, conteudo):

    return render_template_string(f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="utf-8">

<title>{titulo}</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">

<style>

body{{
background:
linear-gradient(
rgba(0,40,100,.85),
rgba(0,60,130,.85)
),
url('https://images.unsplash.com/photo-1522202176988-66273c2fd55f');

background-size:cover;
background-attachment:fixed;
}}

.sidebar{{
position:fixed;
left:0;
top:0;
width:260px;
height:100%;
background:#002f6c;
padding:20px;
overflow:auto;
}}

.sidebar a{{
display:block;
color:white;
padding:12px;
margin-top:5px;
text-decoration:none;
border-radius:8px;
}}

.sidebar a:hover{{
background:#0d6efd;
}}

.content{{
margin-left:280px;
padding:20px;
}}

.card{{
border:none;
border-radius:15px;
box-shadow:0 0 20px rgba(0,0,0,.15);
}}

.topo{{
background:white;
padding:20px;
border-radius:15px;
margin-bottom:20px;
}}

.whatsapp{{
position:fixed;
right:20px;
bottom:20px;
background:#25D366;
padding:15px;
border-radius:50%;
font-size:28px;
color:white;
z-index:999;
text-decoration:none;
}}

</style>

</head>

<body>

<div class="sidebar">

<center>

<img
src="/static/logo.png"
width="120">

<h4 class="text-white mt-3">
Portal Escolar
</h4>

</center>

<hr style="color:white;">

<a href="/dashboard">
<i class="bi bi-house"></i>
Dashboard
</a>

<a href="/informativos">
<i class="bi bi-megaphone"></i>
Informativos
</a>

<a href="/duvidas">
<i class="bi bi-question-circle"></i>
Tire sua dúvida
</a>

<a href="/sugestoes">
<i class="bi bi-lightbulb"></i>
Sugestões
</a>

<a href="/galeria">
<i class="bi bi-images"></i>
Galeria
</a>

{
'''
<a href="/admin">
<i class="bi bi-gear"></i>
Administração
</a>

<a href="/professores">
<i class="bi bi-person-workspace"></i>
Professores
</a>
'''
if session.get("tipo") == "admin"
else ""
}

{
'''
<a href="/mensagens_direcao">
<i class="bi bi-chat-dots"></i>
Falar com a Direção
</a>

<a href="/agendar">
<i class="bi bi-calendar-check"></i>
Agendar Professor
</a>
'''
if session.get("tipo") == "pai"
else ""
}

<a href="/logout">
<i class="bi bi-box-arrow-right"></i>
Sair
</a>
</a>

</div>

<a
class="whatsapp"
target="_blank"
href="https://wa.me/{WHATSAPP_DIRECAO}">
<i class="bi bi-whatsapp"></i>
</a>

<div class="content">

<div class="topo">

<h2>{ESCOLA}</h2>

<p>
📞 {TELEFONE}
|
✉ {EMAIL_ESCOLA}
|
📍 {ENDERECO}
</p>

</div>

{conteudo}

</div>

</body>
</html>
""")


# ==========================
# LOGIN
# ==========================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        acesso = request.form["acesso"]
        senha = request.form["senha"]

        conn = conectar()
        c = conn.cursor()

        c.execute("""
        SELECT *
        FROM usuarios
        WHERE usuario=? OR email=?
        """,
        (
            acesso,
            acesso
        ))

        usuario = c.fetchone()

        conn.close()

        if usuario and usuario["senha"] == senha:

            session["id"] = usuario["id"]
            session["nome"] = usuario["nome"]
            session["usuario"] = usuario["usuario"]
            session["email"] = usuario["email"]
            session["tipo"] = usuario["tipo"]

            return redirect("/dashboard")

    return """
<!DOCTYPE html>
<html>

<head>

<title>Portal Escolar</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<style>

body{
background:
linear-gradient(
rgba(0,40,100,.85),
rgba(0,60,130,.85)
),
url('https://images.unsplash.com/photo-1522202176988-66273c2fd55f');

background-size:cover;
}

</style>

</head>

<body>

<div class="container" style="max-width:500px;margin-top:100px;">

<div class="card">

<div class="card-body">

<center>

<img
src="/static/logo.png"
width="120">

<h3 class="mt-3">
Portal Escolar
</h3>

</center>

<form method="post">

<input
name="acesso"
class="form-control"
placeholder="Usuário ou E-mail">

<br>

<input
type="password"
name="senha"
class="form-control"
placeholder="Senha">

<br>

<button class="btn btn-primary w-100">
Entrar
</button>

</form>

<hr>

<a href="/cadastro">
Criar Conta
</a>

</div>

</div>

</div>

</body>

</html>
"""


# ==========================
# CADASTRO
# ==========================

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        tipo = "aluno" if request.form["tipo"] == "aluno" else "pai"
        conn = conectar()
        c = conn.cursor()

        try:

            c.execute("""
            INSERT INTO usuarios(
                nome,
                email,
                usuario,
                senha,
                tipo
            )
            VALUES(?,?,?,?,?)
            """,
            (
                nome,
                email,
                usuario,
                senha,
                tipo
            ))

            conn.commit()
            conn.close()

            return redirect("/")

        except:

            conn.close()
            return "Usuário ou e-mail já cadastrado"

    return """
    <!DOCTYPE html>
    <html>

    <head>

    <title>Cadastro</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>

    body{
    background:
    linear-gradient(
    rgba(0,40,100,.85),
    rgba(0,60,130,.85)
    ),
    url('https://images.unsplash.com/photo-1522202176988-66273c2fd55f');

    background-size:cover;
    background-position:center;
    background-attachment:fixed;
    height:100vh;
    }

    .card{
    border:none;
    border-radius:15px;
    box-shadow:0 0 20px rgba(0,0,0,.15);
    }

    </style>

    </head>

    <body>

    <div class="container" style="max-width:500px;margin-top:70px;">

    <div class="card">

    <div class="card-body">

    <center>

    <img
    src="/static/logo.png"
    width="120">

    <h3 class="mt-3">
    Portal Escolar
    </h3>

    <p>
    Criar Conta
    </p>

    </center>

    <form method="post">

    <input
    name="nome"
    class="form-control"
    placeholder="Nome Completo"
    required>

    <br>

    <input
    name="email"
    type="email"
    class="form-control"
    placeholder="E-mail"
    required>

    <br>

    <input
    name="usuario"
    class="form-control"
    placeholder="Usuário"
    required>

    <br>

    <input
    name="senha"
    type="password"
    class="form-control"
    placeholder="Senha"
    required>

    <br>

    <select
    name="tipo"
    class="form-control">

    <option value="aluno">
    Aluno
    </option>

    <option value="pai">
    Responsável
    </option>

    </select>

    <br>

    <button class="btn btn-primary w-100">
    Cadastrar
    </button>

    </form>

    <hr>

    <a href="/">
    Voltar para Login
    </a>

    </div>

    </div>

    </div>

    </body>

    </html>
    """


# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():

    if not logado():
        return redirect("/")

    html = f"""

    <div class='card mb-4'>

        <div class='card-body'>

            <h2>
            Bem-vindo(a), {session['nome']}
            </h2>

            <p>

            Perfil:
            <b>{session['tipo'].upper()}</b>

            </p>

        </div>

    </div>

    <div class='row'>

        <div class='col-md-4'>

            <div class='card'>

                <div class='card-body'>

                    <h4>📚 Informativos</h4>

                    <p>
                    Avisos da escola.
                    </p>

                </div>

            </div>

        </div>

        <div class='col-md-4'>

            <div class='card'>

                <div class='card-body'>

                    <h4>🎓 Jornada Acadêmica</h4>

                    <p>
                    Eventos e atividades.
                    </p>

                </div>

            </div>

        </div>

        <div class='col-md-4'>

            <div class='card'>

                <div class='card-body'>

                    <h4>💬 Comunicação</h4>

                    <p>
                    Direção e professores.
                    </p>

                </div>

            </div>

        </div>

    </div>

    <br>

    <div class='card'>

        <div class='card-body'>

            <h3>
            Missão da Escola
            </h3>

            <p>

            Promover educação de qualidade,
            inclusão e desenvolvimento social.

            </p>

        </div>

    </div>

    """

    return pagina("Dashboard", html)


# ==========================
# INFORMATIVOS
# ==========================

@app.route("/informativos", methods=["GET", "POST"])
def informativos():

    if not logado():
        return redirect("/")

    conn = conectar()
    c = conn.cursor()

    if request.method == "POST" and admin():

        titulo = request.form["titulo"]
        mensagem = request.form["mensagem"]
        imagem = request.form["imagem"]

        c.execute("""
        INSERT INTO informativos(
            titulo,
            mensagem,
            imagem,
            data
        )
        VALUES(?,?,?,?)
        """,
        (
            titulo,
            mensagem,
            imagem,
            str(datetime.now())
        ))

        conn.commit()

    c.execute("""
    SELECT *
    FROM informativos
    ORDER BY id DESC
    """)

    dados = c.fetchall()

    html = "<h2>Informativos</h2><br>"

    if admin():

        html += """

        <div class='card mb-4'>

            <div class='card-body'>

            <h4>Novo Informativo</h4>

            <form method='post'>

                <input
                name='titulo'
                class='form-control'
                placeholder='Título'>

                <br>

                <textarea
                name='mensagem'
                class='form-control'
                placeholder='Mensagem'>
                </textarea>

                <br>

                <input
                name='imagem'
                class='form-control'
                placeholder='URL da Imagem'>

                <br>

                <button
                class='btn btn-success'>
                Publicar
                </button>

            </form>

            </div>

        </div>

        """

    for item in dados:

        html += f"""

        <div class='card mb-4'>

            <div class='card-body'>

                {'<img src="' + item['imagem'] + '" style="width:100%;border-radius:10px;margin-bottom:15px;">' if item['imagem'] else ''}

                <h4>
                {item['titulo']}
                </h4>

                <p>
                {item['mensagem']}
                </p>

                <small>
                {item['data']}
                </small>
                {
    f'''
    <br><br>

    <a
    href="/apagar_informativo/{item["id"]}"
    class="btn btn-danger">
    Excluir
    </a>
    '''
    if admin()
    else ""
}

            </div>

        </div>

        """

    conn.close()

    return pagina(
        "Informativos",
        html
    )

@app.route("/apagar_informativo/<int:id>")
def apagar_informativo(id):

    if not admin():
        return redirect("/dashboard")

    conn = conectar()
    c = conn.cursor()

    c.execute("""
    DELETE FROM informativos
    WHERE id=?
    """,
    (id,))

    conn.commit()
    conn.close()

    return redirect("/informativos")
# ==========================
# GALERIA
# ==========================

@app.route("/galeria")
def galeria():

    if not logado():
        return redirect("/")

    conn = conectar()
    c = conn.cursor()

    c.execute("""
    SELECT *
    FROM galeria
    ORDER BY id DESC
    """)

    fotos = c.fetchall()

    html = """

    <h2>
    Galeria da Escola
    </h2>

    <div class='row'>

    """

    for foto in fotos:

        html += f"""

        <div class='col-md-4'>

            <div class='card mb-3'>

                <img
                src="{foto['imagem']}"
                class="card-img-top">

                <div class='card-body'>

                    <b>
                    {foto['titulo']}
                    </b>

                </div>

            </div>

        </div>

        """

    html += "</div>"

    conn.close()

    return pagina(
        "Galeria",
        html
    )


# ==========================
# CADASTRAR FOTO
# ==========================

@app.route("/nova_foto", methods=["GET", "POST"])
def nova_foto():

    if not admin():
        return redirect("/dashboard")

    conn = conectar()
    c = conn.cursor()

    if request.method == "POST":

        titulo = request.form["titulo"]
        imagem = request.form["imagem"]

        c.execute("""
        INSERT INTO galeria(
            titulo,
            imagem,
            data
        )
        VALUES(?,?,?)
        """,
        (
            titulo,
            imagem,
            str(datetime.now())
        ))

        conn.commit()

        return redirect("/galeria")

    html = """

    <div class='card'>

        <div class='card-body'>

            <h2>
            Nova Foto
            </h2>

            <form method='post'>

                <input
                name='titulo'
                class='form-control'
                placeholder='Título'>

                <br>

                <input
                name='imagem'
                class='form-control'
                placeholder='URL da imagem'>

                <br>

                <button
                class='btn btn-success'>
                Salvar
                </button>

            </form>

        </div>

    </div>

    """

    return pagina(
        "Nova Foto",
        html
    )
# ==========================
# DÚVIDAS
# ==========================

@app.route("/duvidas", methods=["GET", "POST"])
def duvidas():

    if not logado():
        return redirect("/")

    conn = conectar()
    c = conn.cursor()

    if request.method == "POST":

        pergunta = request.form["pergunta"]

        c.execute("""
        INSERT INTO duvidas(
            usuario,
            pergunta,
            resposta,
            data
        )
        VALUES(?,?,?,?)
        """,
        (
            session["usuario"],
            pergunta,
            "",
            str(datetime.now())
        ))

        conn.commit()

    if admin():
        c.execute("""
        SELECT *
        FROM duvidas
        ORDER BY id DESC
        """)
    else:
        c.execute("""
        SELECT *
        FROM duvidas
        WHERE usuario=?
        ORDER BY id DESC
        """,
        (session["usuario"],))

    dados = c.fetchall()

    html = """

    <h2>Tire sua Dúvida</h2>

    <form method="post">

        <textarea
        name="pergunta"
        class="form-control"
        placeholder="Digite sua dúvida"
        required>
        </textarea>

        <br>

        <button
        class="btn btn-primary">
        Enviar
        </button>

    </form>

    <hr>

    """

    for item in dados:

        html += f"""

        <div class="card mb-3">

            <div class="card-body">

                <b>Pergunta:</b>

                <p>
                {item["pergunta"]}
                </p>

                <hr>

                <b>Resposta:</b>

                <p>
                {item["resposta"] if item["resposta"] else "Aguardando resposta"}
                </p>

            </div>

        </div>

        """

    conn.close()

    return pagina(
        "Dúvidas",
        html
    )


# ==========================
# RESPONDER DÚVIDAS
# ==========================

@app.route("/responder_duvida/<int:id>", methods=["GET", "POST"])
def responder_duvida(id):

    if not logado():
        return redirect("/")

    # 🔒 só admin pode responder
    if not admin():
        return redirect("/duvidas")

    conn = conectar()
    c = conn.cursor()

    # ==========================
    # SALVAR RESPOSTA
    # ==========================
    if request.method == "POST":

        resposta = request.form["resposta"].strip()

        if resposta:

            c.execute("""
            UPDATE duvidas
            SET resposta = ?
            WHERE id = ?
            """, (resposta, id))

            conn.commit()

        conn.close()
        return redirect("/duvidas")

    # ==========================
    # BUSCAR DÚVIDA
    # ==========================
    c.execute("""
    SELECT *
    FROM duvidas
    WHERE id = ?
    """, (id,))

    duvida = c.fetchone()

    conn.close()

    # 🔒 evita erro se não existir
    if not duvida:
        return redirect("/duvidas")

    # ==========================
    # HTML DA TELA
    # ==========================
    html = f"""

    <div class="card">
        <div class="card-body">

            <h3>Responder Dúvida</h3>

            <hr>

            <strong>Usuário:</strong> {duvida["usuario"]}

            <br><br>

            <strong>Pergunta:</strong>
            <p>{duvida["pergunta"]}</p>

            <hr>

            <form method="post">

                <label><b>Resposta:</b></label>

                <textarea
                    name="resposta"
                    class="form-control"
                    rows="5"
                    required
                >{duvida["resposta"] or ""}</textarea>

                <br>

                <button class="btn btn-success">
                    Salvar Resposta
                </button>

            </form>

        </div>
    </div>

    """

    return pagina(
        "Responder Dúvida",
        html
    )
# ==========================
# SUGESTÕES
# ==========================

@app.route("/sugestoes", methods=["GET", "POST"])
def sugestoes():

    if not logado():
        return redirect("/")

    conn = conectar()
    c = conn.cursor()

    if request.method == "POST":

        sugestao = request.form["sugestao"]

        c.execute("""
        INSERT INTO sugestoes(
            usuario,
            sugestao,
            data
        )
        VALUES(?,?,?)
        """,
        (
            session["usuario"],
            sugestao,
            str(datetime.now())
        ))

        conn.commit()

    c.execute("""
    SELECT *
    FROM sugestoes
    ORDER BY id DESC
    """)

    dados = c.fetchall()

    html = """

    <h2>Sugestões de Melhoria</h2>

    <form method="post">

        <textarea
        name="sugestao"
        class="form-control"
        required>
        </textarea>

        <br>

        <button
        class="btn btn-success">
        Enviar Sugestão
        </button>

    </form>

    <hr>

    """

    if admin():

        for item in dados:
            html += f"""

            <div class="card mb-3">

                <div class="card-body">

                    <b>Usuário:</b>
                    {item["usuario"]}

                    <hr>

                    <b>Pergunta:</b>

                    <p>
                    {item["pergunta"]}
                    </p>

                    <hr>

                    <b>Resposta:</b>

                    <p>
                    {item["resposta"] if item["resposta"] else "Aguardando resposta"}
                    </p>

                    {
            f'''
                        <a
                        href="/responder_duvida/{item["id"]}"
                        class="btn btn-primary">
                        Responder
                        </a>
                        '''
            if admin()
            else ""
            }

                </div>

            </div>

            """

    conn.close()

    return pagina(
        "Sugestões",
        html
    )


# ==========================
# MENSAGENS DIREÇÃO
# ==========================

@app.route("/mensagens_direcao", methods=["GET", "POST"])
def mensagens_direcao():

    if session.get("tipo") != "pai":
        return redirect("/dashboard")

    conn = conectar()
    c = conn.cursor()

    if request.method == "POST":

        mensagem = request.form["mensagem"]

        c.execute("""
        INSERT INTO mensagens(
            usuario,
            mensagem,
            resposta,
            data
        )
        VALUES(?,?,?,?)
        """,
        (
            session["usuario"],
            mensagem,
            "",
            str(datetime.now())
        ))

        conn.commit()

    c.execute("""
    SELECT *
    FROM mensagens
    WHERE usuario=?
    ORDER BY id DESC
    """,
    (session["usuario"],))

    dados = c.fetchall()

    html = """

    <h2>Comunicação com a Direção</h2>

    <form method="post">

        <textarea
        name="mensagem"
        class="form-control"
        required>
        </textarea>

        <br>

        <button
        class="btn btn-primary">
        Enviar
        </button>

    </form>

    <hr>

    """

    for item in dados:

        html += f"""

        <div class="card mb-3">

            <div class="card-body">

                <b>Mensagem:</b>

                <p>
                {item["mensagem"]}
                </p>

                <hr>

                <b>Resposta:</b>

                <p>
                {item["resposta"] if item["resposta"] else "Aguardando resposta"}
                </p>

            </div>

        </div>

        """

    conn.close()

    return pagina(
        "Direção",
        html
    )
# ==========================
# PROFESSORES
# ==========================

@app.route("/professores", methods=["GET", "POST"])
def professores():

    if not admin():
        return redirect("/dashboard")

    conn = conectar()
    c = conn.cursor()

    if request.method == "POST":

        nome = request.form["nome"]
        materia = request.form["materia"]

        c.execute("""
        INSERT INTO professores(
            nome,
            materia
        )
        VALUES(?,?)
        """,
        (
            nome,
            materia
        ))

        conn.commit()

    c.execute("""
    SELECT *
    FROM professores
    ORDER BY nome
    """)

    dados = c.fetchall()

    html = """

    <h2>Professores</h2>

    <div class="card mb-4">

        <div class="card-body">

            <form method="post">

                <input
                name="nome"
                class="form-control"
                placeholder="Nome do Professor"
                required>

                <br>

                <input
                name="materia"
                class="form-control"
                placeholder="Matéria"
                required>

                <br>

                <button
                class="btn btn-success">
                Cadastrar
                </button>

            </form>

        </div>

    </div>

    """

    for p in dados:

        html += f"""

        <div class="card mb-2">

            <div class="card-body">

                <b>{p['nome']}</b>

                <br>

                {p['materia']}

            </div>

        </div>

        """

    conn.close()

    return pagina(
        "Professores",
        html
    )


# ==========================
# AGENDAMENTOS
# ==========================

@app.route("/agendar", methods=["GET", "POST"])
def agendar():

    if session.get("tipo") != "pai":
        return redirect("/dashboard")

    conn = conectar()
    c = conn.cursor()

    if request.method == "POST":

        professor = request.form["professor"]
        data = request.form["data"]

        c.execute("""
        INSERT INTO agendamentos(
            pai,
            professor,
            data,
            status
        )
        VALUES(?,?,?,?)
        """,
        (
            session["usuario"],
            professor,
            data,
            "Pendente"
        ))

        conn.commit()

    c.execute("""
    SELECT *
    FROM professores
    ORDER BY nome
    """)

    professores_lista = c.fetchall()

    html = """

    <h2>Agendar Reunião</h2>

    <div class="card">

        <div class="card-body">

            <form method="post">

                <select
                name="professor"
                class="form-control">

    """

    for professor in professores_lista:

        html += f"""

        <option>
        {professor['nome']} - {professor['materia']}
        </option>

        """

    html += """

                </select>

                <br>

                <input
                type="date"
                name="data"
                class="form-control"
                required>

                <br>

                <button
                class="btn btn-success">
                Solicitar Agendamento
                </button>

            </form>

        </div>

    </div>

    """

    conn.close()

    return pagina(
        "Agendamento",
        html
    )


# ==========================
# PAINEL ADMINISTRATIVO
# ==========================

@app.route("/admin")
def painel_admin():

    if not admin():
        return redirect("/dashboard")

    conn = conectar()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) as total FROM usuarios")
    usuarios = c.fetchone()["total"]

    c.execute("""
    SELECT COUNT(*) as total
    FROM usuarios
    WHERE tipo='aluno'
    """)
    alunos = c.fetchone()["total"]

    c.execute("""
    SELECT COUNT(*) as total
    FROM usuarios
    WHERE tipo='pai'
    """)
    pais = c.fetchone()["total"]

    c.execute("""
    SELECT COUNT(*) as total
    FROM professores
    """)
    professores_total = c.fetchone()["total"]

    c.execute("""
    SELECT COUNT(*) as total
    FROM informativos
    """)
    informativos_total = c.fetchone()["total"]

    conn.close()

    html = f"""

    <h2>Painel Administrativo</h2>

    <div class="row">

        <div class="col-md-3">

            <div class="card">

                <div class="card-body">

                    <h3>{usuarios}</h3>

                    Usuários

                </div>

            </div>

        </div>

        <div class="col-md-3">

            <div class="card">

                <div class="card-body">

                    <h3>{alunos}</h3>

                    Alunos

                </div>

            </div>

        </div>

        <div class="col-md-3">

            <div class="card">

                <div class="card-body">

                    <h3>{pais}</h3>

                    Responsáveis

                </div>

            </div>

        </div>

        <div class="col-md-3">

            <div class="card">

                <div class="card-body">

                    <h3>{professores_total}</h3>

                    Professores

                </div>

            </div>

        </div>

    </div>

    <br>

    <div class="card">

        <div class="card-body">

            <h4>Resumo Geral</h4>

            <p>
            Informativos cadastrados:
            <b>{informativos_total}</b>
            </p>

        </div>

    </div>

    <br>

    <a href="/professores" class="btn btn-primary">
    Gerenciar Professores
    </a>

    <a href="/nova_foto" class="btn btn-success">
    Gerenciar Galeria
    </a>

    """

    return pagina(
        "Administração",
        html
    )


# ==========================
# EXECUÇÃO
# ==========================

if __name__ == "__main__":

    criar_banco()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )