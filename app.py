from flask import Flask, request, redirect, session, render_template_string
from werkzeug.utils import secure_filename
import sqlite3
import os
from datetime import datetime
UPLOAD_FOLDER = "static/uploads"

# ==========================
# CONFIGURAÇÃO
# ==========================

app = Flask(__name__)
app.secret_key = "victoria_maldonado_2026"

DB = "portal_escola.db"
ARQUIVO_RESET = "ultimo_reset.txt"

ESCOLA = "EMEF Victoria Maldonado Cazarini"

WHATSAPP_DIRECAO = "(17)99231-2155"
TELEFONE = "(17) 992312155"
EMAIL_ESCOLA = "contato.victoriamaldonado@gmail.com"
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
def limpar_dados_7_dias():

    hoje = datetime.now()

    if not os.path.exists(ARQUIVO_RESET):

        with open(ARQUIVO_RESET, "w") as f:
            f.write(hoje.strftime("%Y-%m-%d"))

        return

    with open(ARQUIVO_RESET, "r") as f:
        ultima_data = f.read().strip()

    try:
        ultima_data = datetime.strptime(
            ultima_data,
            "%Y-%m-%d"
        )

    except:
        ultima_data = hoje

    dias = (hoje - ultima_data).days

    if dias >= 7:

        conn = conectar()
        c = conn.cursor()

        # Limpeza automática
        c.execute("DELETE FROM informativos")
        c.execute("DELETE FROM galeria")
        c.execute("DELETE FROM duvidas")
        c.execute("DELETE FROM mensagens")
        c.execute("DELETE FROM sugestoes")

        conn.commit()
        conn.close()




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

# Cria banco ao iniciar

criar_banco()
limpar_dados_7_dias()

# ==========================
# TEMPLATE PRINCIPAL
# ==========================
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
<a href="https://wa.me/5517992312155?text=Olá,%20gostaria%20de%20falar%20com%20a%20direção"
   target="_blank">
<i class="bi bi-whatsapp"></i>
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
<a href="/desenvolvedor">
<i class="bi bi-code-square"></i>
Fale com o Desenvolvedor
</a>

<a href="/logout">
<i class="bi bi-box-arrow-right"></i>
Sair
</a>
</a>

</div>



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

<b>
{
"Responsável pelo Aluno"
if session["tipo"] == "pai"
else session["tipo"].upper()
}
</b>

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
        imagem = ""

        c.execute("""
        INSERT INTO informativos(
            titulo,
            mensagem,
            data
        )
        VALUES(?,?,?)
        """,
                  (
                      titulo,
                      mensagem,
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

                <h4>
                Novo Informativo
                </h4>

                <form method='post'>

                    <input
                    name='titulo'
                    class='form-control'
                    placeholder='Título'
                    required>

                    <br>

                    <textarea
                    name='mensagem'
                    class='form-control'
                    placeholder='Mensagem'
                    rows='5'
                    required>
                    </textarea>

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

        <div style="
    background:white;
    padding:25px;
    border-radius:15px;
    margin-bottom:20px;
    box-shadow:0 4px 12px rgba(0,0,0,0.15);
    border-left:6px solid #0d6efd;
        ">

            <h4 style="
            color:#0d6efd;
            font-weight:bold;
            margin-bottom:15px;
            ">
{item['titulo']}
</h4>

            <hr>

            <p style="white-space:pre-wrap;">
            {item['mensagem']}
            </p>

            <div style="
            margin-top:15px;
            color:#6c757d;
            font-size:12px;
            ">
{item['data']}
</div>

            {
        f'''
            <br><br>

            <a
            href="/apagar_informativo/{item["id"]}"
            class="btn btn-danger btn-sm">
            Excluir
            </a>
            '''
        if admin()
        else ""
        }

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

    """

    if not admin():
        html += """

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

                    <b>Sugestão:</b>

                    <p>
                    {item["sugestao"]}
                    </p>

                    <hr>

                    <small>
                    Enviada em: {item["data"]}
                    </small>

                </div>

            </div>

            """

    conn.close()

    return pagina(
        "Sugestões",
        html
    )
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

    <h2 class='mb-4'>
    Galeria da Escola
    </h2>

    """

    if admin():

        html += """

        <a
        href="/nova_foto"
        class="btn btn-success mb-4">
        ➕ Nova Foto
        </a>

        """

    html += """

    <div class="row">

    """

    for foto in fotos:

        html += f"""

        <div class="col-md-4 mb-4">

            <div class="card shadow-sm h-100">

                <a
                href="{foto['imagem']}"
                target="_blank">

                    <img
                    src="{foto['imagem']}"
                    class="card-img-top"
                    style="
                    height:250px;
                    object-fit:cover;
                    cursor:pointer;
                    ">

                </a>

                <div class="card-body">

                    <h5>
                    {foto['titulo']}
                    </h5>

                    {
                    f'''
                    <a
                    href="/excluir_foto/{foto["id"]}"
                    class="btn btn-danger btn-sm"
                    onclick="return confirm('Deseja excluir esta foto?')">
                    Excluir
                    </a>
                    '''
                    if admin()
                    else ""
                    }

                </div>

            </div>

        </div>

        """

    html += """

    </div>

    """

    conn.close()

    return pagina(
        "Galeria",
        html
    )
# ==========================
# NOVA FOTO
# ==========================

@app.route("/nova_foto", methods=["GET", "POST"])
def nova_foto():

    if not admin():
        return redirect("/dashboard")

    conn = conectar()
    c = conn.cursor()

    if request.method == "POST":

        titulo = request.form["titulo"]

        arquivo = request.files["imagem"]

        if arquivo and arquivo.filename:

            nome_original = secure_filename(
                arquivo.filename
            )

            nome_arquivo = (
                f"{int(datetime.now().timestamp())}_"
                f"{nome_original}"
            )

            caminho = os.path.join(
                UPLOAD_FOLDER,
                nome_arquivo
            )

            arquivo.save(caminho)

            imagem = (
                f"/static/uploads/{nome_arquivo}"
            )

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

        conn.close()

        return redirect("/galeria")

    html = """

    <div class="card">

        <div class="card-body">

            <h2>
            Nova Foto
            </h2>

            <form
            method="post"
            enctype="multipart/form-data">

                <input
                name="titulo"
                class="form-control"
                placeholder="Título"
                required>

                <br>

                <input
                type="file"
                name="imagem"
                class="form-control"
                accept="image/*"
                required>

                <br>

                <button
                class="btn btn-success">
                Salvar Foto
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
# EXCLUIR FOTO
# ==========================

@app.route("/excluir_foto/<int:id>")
def excluir_foto(id):

    if not admin():
        return redirect("/dashboard")

    conn = conectar()
    c = conn.cursor()

    c.execute("""
    DELETE FROM galeria
    WHERE id=?
    """,
    (id,))

    conn.commit()
    conn.close()

    return redirect("/galeria")
# ==========================
# DÚVIDAS
# ==========================

@app.route("/duvidas", methods=["GET", "POST"])
def duvidas():

    if not logado():
        return redirect("/")

    conn = conectar()
    c = conn.cursor()

    # Usuário envia pergunta
    if request.method == "POST" and not admin():

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

    # Admin vê todas
    if admin():

        c.execute("""
        SELECT *
        FROM duvidas
        ORDER BY id DESC
        """)

    # Usuário vê apenas as dele
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

    """

    if not admin():

        html += """

        <div class="card mb-3">
            <div class="card-body">

                <form method="post">

                    <textarea
                    name="pergunta"
                    class="form-control"
                    placeholder="Digite sua dúvida"
                    required></textarea>

                    <br>

                    <button class="btn btn-primary">
                        Enviar Pergunta
                    </button>

                </form>

            </div>
        </div>

        """

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

        """

        if admin():

            html += f"""

                <a
                href="/responder_duvida/{item['id']}"
                class="btn btn-primary">
                Responder
                </a>

            """

        html += """

            </div>

        </div>

        """

    conn.close()

    return pagina(
        "Dúvidas",
        html
    )
# ==========================
# RESPONDER DÚVIDA
# ==========================

@app.route("/responder_duvida/<int:id>", methods=["GET", "POST"])
def responder_duvida(id):

    if not logado():
        return redirect("/")

    if not admin():
        return redirect("/duvidas")

    conn = conectar()
    c = conn.cursor()

    if request.method == "POST":

        resposta = request.form["resposta"]

        c.execute("""
        UPDATE duvidas
        SET resposta = ?
        WHERE id = ?
        """,
        (
            resposta,
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/duvidas")

    c.execute("""
    SELECT *
    FROM duvidas
    WHERE id = ?
    """,
    (id,))

    duvida = c.fetchone()

    conn.close()

    if not duvida:
        return redirect("/duvidas")

    html = f"""

    <div class="card">

        <div class="card-body">

            <h3>Responder Dúvida</h3>

            <hr>

            <b>Usuário:</b>
            {duvida["usuario"]}

            <br><br>

            <b>Pergunta:</b>

            <p>
            {duvida["pergunta"]}
            </p>

            <hr>

            <form method="post">

                <textarea
                name="resposta"
                class="form-control"
                rows="5"
                required>{duvida["resposta"] or ""}</textarea>

                <br>

                <button
                class="btn btn-success">
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
    )# ==========================
# DESENVOLVEDOR
# ==========================

@app.route("/desenvolvedor")
def desenvolvedor():

    if not logado():
        return redirect("/")

    html = """

    <div class="card">

        <div class="card-body text-center">

            <h2>Fale com o Desenvolvedor</h2>

            <p>
            Precisa de suporte técnico ou melhorias no sistema?
            </p>

            <a
            href="https://wa.me/5517996537933"
            target="_blank"
            class="btn btn-success btn-lg">

            <i class="bi bi-whatsapp"></i>
            Chamar no WhatsApp

            </a>

        </div>

    </div>

    """

    return pagina("Desenvolvedor", html)


    if not admin():
        return redirect("/dashboard")

    conn = conectar()
    c = conn.cursor()

    c.execute("""
    SELECT *
    FROM agendamentos
    ORDER BY id DESC
    """)

    dados = c.fetchall()

    html = """

    <h2>Agendamentos Solicitados</h2>

    """

    for item in dados:

        html += f"""

        <div class="card mb-3">

            <div class="card-body">

                <b>Responsável:</b>
                {item['pai']}

                <br>

                <b>Professor:</b>
                {item['professor']}

                <br>

                <b>Data:</b>
                {item['data']}

                <br>

                <b>Status:</b>
                {item['status']}

                <hr>

                <a
                href="/aprovar_agendamento/{item['id']}"
                class="btn btn-success btn-sm">
                Aprovar
                </a>

                <a
                href="/rejeitar_agendamento/{item['id']}"
                class="btn btn-danger btn-sm">
                Rejeitar
                </a>

            </div>

        </div>

        """

    conn.close()

    return pagina(
        "Agendamentos",
        html
    )
@app.route("/agendamentos_admin")
def agendamentos_admin():

    if not admin():
        return redirect("/dashboard")

    conn = conectar()
    c = conn.cursor()

    c.execute("""
    SELECT *
    FROM agendamentos
    ORDER BY id DESC
    """)

    dados = c.fetchall()

    html = """

    <h2>Agendamentos Solicitados</h2>

    """

    for item in dados:

        html += f"""

        <div class="card mb-3">

            <div class="card-body">

                <b>Responsável:</b>
                {item['pai']}

                <br>

                <b>Professor:</b>
                {item['professor']}

                <br>

                <b>Data:</b>
                {item['data']}

                <br>

                <b>Status:</b>
                {item['status']}

                <hr>

                <a
                href="/aprovar_agendamento/{item['id']}"
                class="btn btn-success btn-sm">
                Aprovar
                </a>

                <a
                href="/rejeitar_agendamento/{item['id']}"
                class="btn btn-danger btn-sm">
                Rejeitar
                </a>

            </div>

        </div>

        """

    conn.close()

    return pagina(
        "Agendamentos",
        html
    )
@app.route("/aprovar_agendamento/<int:id>")
def aprovar_agendamento(id):

    if not admin():
        return redirect("/dashboard")

    conn = conectar()
    c = conn.cursor()

    c.execute("""
    UPDATE agendamentos
    SET status='Aprovado'
    WHERE id=?
    """,
    (id,))

    conn.commit()
    conn.close()

    return redirect("/agendamentos_admin")
@app.route("/rejeitar_agendamento/<int:id>")
def rejeitar_agendamento(id):

    if not admin():
        return redirect("/dashboard")

    conn = conectar()
    c = conn.cursor()

    c.execute("""
    UPDATE agendamentos
    SET status='Rejeitado'
    WHERE id=?
    """,
    (id,))

    conn.commit()
    conn.close()

    return redirect("/agendamentos_admin")
    c.execute("""
    SELECT *
    FROM agendamentos
    WHERE pai=?
    ORDER BY id DESC
    """,
              (session["usuario"],))
    historico = c.fetchall()
    html += "<hr><h3>Meus Agendamentos</h3>"
    for item in historico:
        html += f"""
    <div class='card mb-2'>
        <div class='card-body'>

            <b>Professor:</b>
            {item['professor']}

            <br>

            <b>Data:</b>
            {item['data']}

            <br>

            <b>Status:</b>
            {item['status']}

        </div>
    </div>
    """


    @app.route("/agendamentos_admin")
    def agendamentos_admin():

        if not admin():
            return redirect("/dashboard")

        conn = conectar()
        c = conn.cursor()

        c.execute("""
        SELECT *
        FROM agendamentos
        ORDER BY id DESC
        """)

        dados = c.fetchall()

        html = """

        <h2>Agendamentos Solicitados</h2>

        """

        for item in dados:
            html += f"""

            <div class="card mb-3">

                <div class="card-body">

                    <b>Responsável:</b>
                    {item['pai']}

                    <br>

                    <b>Professor:</b>
                    {item['professor']}

                    <br>

                    <b>Data:</b>
                    {item['data']}

                    <br>

                    <b>Status:</b>
                    {item['status']}

                    <hr>

                    <a
                    href="/aprovar_agendamento/{item['id']}"
                    class="btn btn-success btn-sm">
                    Aprovar
                    </a>

                    <a
                    href="/rejeitar_agendamento/{item['id']}"
                    class="btn btn-danger btn-sm">
                    Rejeitar
                    </a>

                </div>

            </div>

            """

        conn.close()

        return pagina(
            "Agendamentos",
            html
        )


    @app.route("/aprovar_agendamento/<int:id>")
    def aprovar_agendamento(id):

        if not admin():
            return redirect("/dashboard")

        conn = conectar()
        c = conn.cursor()

        c.execute("""
        UPDATE agendamentos
        SET status='Aprovado'
        WHERE id=?
        """,
                  (id,))

        conn.commit()
        conn.close()

        return redirect("/agendamentos_admin")


    @app.route("/rejeitar_agendamento/<int:id>")
    def rejeitar_agendamento(id):

        if not admin():
            return redirect("/dashboard")

        conn = conectar()
        c = conn.cursor()

        c.execute("""
        UPDATE agendamentos
        SET status='Rejeitado'
        WHERE id=?
        """,
                  (id,))

        conn.commit()
        conn.close()

        return redirect("/agendamentos_admin")


    c.execute("""
    SELECT *
    FROM agendamentos
    WHERE pai=?
    ORDER BY id DESC
    """,
              (session["usuario"],))

    historico = c.fetchall()

    html += "<hr><h3>Meus Agendamentos</h3>"
    for item in historico:
        html += f"""
        <div class='card mb-2'>
            <div class='card-body'>

                <b>Professor:</b>
                {item['professor']}

                <br>

                <b>Data:</b>
                {item['data']}

                <br>

                <b>Status:</b>
                {item['status']}

            </div>
        </div>
        """
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

                Matéria: {p['materia']}

                <br><br>

                <a
                href="/excluir_professor/{p['id']}"
                class="btn btn-danger btn-sm"
                onclick="return confirm('Deseja excluir este professor?')">
                🗑 Excluir Professor
                </a>

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
    usuarios_total = c.fetchone()["total"]

    c.execute("SELECT COUNT(*) as total FROM usuarios WHERE tipo='aluno'")
    alunos = c.fetchone()["total"]

    c.execute("SELECT COUNT(*) as total FROM usuarios WHERE tipo='pai'")
    pais = c.fetchone()["total"]

    c.execute("SELECT COUNT(*) as total FROM professores")
    professores_total = c.fetchone()["total"]

    c.execute("SELECT COUNT(*) as total FROM informativos")
    informativos_total = c.fetchone()["total"]

    c.execute("""
    SELECT *
    FROM usuarios
    ORDER BY nome
    """)
    lista_usuarios = c.fetchall()

    html = f"""

    <h2>Painel Administrativo</h2>

    <div class="row">

        <div class="col-md-3">
            <div class="card">
                <div class="card-body">
                    <h3>{usuarios_total}</h3>
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

    <div class="card">
        <div class="card-body">

            <h4>Usuários Cadastrados</h4>

            <table class="table table-striped">

                <tr>
                    <th>ID</th>
                    <th>Nome</th>
                    <th>Usuário</th>
                    <th>Tipo</th>
                </tr>

    """

    for u in lista_usuarios:

        html += f"""
        <tr>
            <td>{u['id']}</td>
            <td>{u['nome']}</td>
            <td>{u['usuario']}</td>
            <td>{u['tipo']}</td>
        </tr>
        """

    html += """

            </table>

        </div>
    </div>

    <br>

    <a href="/professores" class="btn btn-primary">
    Gerenciar Professores
    </a>
    <a href="/agendamentos_admin" class="btn btn-warning">
Agendamentos Pendentes
</a>

    """

    conn.close()

    return pagina("Administração", html)
@app.route("/excluir_professor/<int:id>")
def excluir_professor(id):

    if not admin():
        return redirect("/dashboard")

    conn = conectar()
    c = conn.cursor()

    c.execute("""
    DELETE FROM professores
    WHERE id=?
    """,
    (id,))

    conn.commit()
    conn.close()
    return redirect("/professores")
    for p in dados:
        html += f"""
        <div class="card mb-2">
        <div class="card-body">
        <b>{p['nome']}</b>
        <br>
        Matéria: {p['materia']}
        <br><br>
        <a
        href="/excluir_professor/{p['id']}"
        class="btn btn-danger btn-sm"
        onclick="return confirm('Deseja excluir este professor?')">
        🗑 Excluir Professor
        </a>
        </div>
        </div>
"""

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