import sqlite3
from admin import admin_bp  
from conta import conta_bp

from flask import (
    Flask, abort, flash, redirect, render_template, request, session, url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

import config
from analisador import LIMITES_PERDA_DB, encontrar_problemas, ler_eventos_de_linhas
from autenticacao import (
    gerar_token_confirmacao,
    ler_token_confirmacao,
    login_obrigatorio,
    usuario_atual,
)
from banco import (
    buscar_leitura,
    buscar_usuario_por_email,
    confirmar_email,
    criar_tabelas,
    criar_usuario,
    listar_leituras,
    salvar_leitura,
)
from emails import enviar_email
from validacao import validar_cadastro

if not config.SECRET_KEY:
    raise RuntimeError("Defina SECRET_KEY no arquivo .env antes de iniciar.")

app = Flask(__name__)
app.config.update(
    SECRET_KEY=config.SECRET_KEY,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
criar_tabelas()
app.register_blueprint(admin_bp)
app.register_blueprint(conta_bp)

# Usado para gastar o mesmo tempo quando o e-mail não existe no login
HASH_FALSO = generate_password_hash("senha-falsa-para-igualar-o-tempo")


@app.context_processor
def dados_globais():
    return {"usuario": usuario_atual()}


def enviar_confirmacao(email, nome):
    token = gerar_token_confirmacao(email)
    link = config.BASE_URL + url_for("confirmar", token=token)
    texto = (
        f"Olá, {nome}!\n\n"
        "Para ativar sua conta no OTDR Analyzer, confirme seu e-mail pelo "
        "link abaixo (válido por 24 horas):\n\n"
        f"{link}\n\n"
        "Se você não criou essa conta, ignore esta mensagem."
    )
    return enviar_email(email, "Confirme seu e-mail - OTDR Analyzer", texto)


# ---------- entrada, login e logout ----------

@app.route("/")
def inicio():
    if usuario_atual() is not None:
        return redirect(url_for("analise"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if usuario_atual() is not None:
        return redirect(url_for("analise"))

    erro = None
    pendente = False
    email = ""

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        registro = buscar_usuario_por_email(email)

        hash_guardado = registro["senha_hash"] if registro else HASH_FALSO
        senha_ok = check_password_hash(hash_guardado, senha)

        if registro is None or not senha_ok:
            erro = "E-mail ou senha incorretos."
        elif not registro["email_confirmado"]:
            erro = "Confirme seu e-mail antes de entrar. Procure a mensagem que enviamos para a sua caixa de entrada."
            pendente = True
        else:
            session.clear()
            session["usuario_id"] = registro["id"]
            return redirect(url_for("analise"))

    return render_template("login.html", erro=erro, pendente=pendente, email=email)


@app.route("/sair", methods=["POST"])
def sair():
    session.clear()
    return redirect(url_for("login"))


# ---------- cadastro e confirmação de e-mail ----------

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if usuario_atual() is not None:
        return redirect(url_for("analise"))

    erros = {}
    valores = {"nome": "", "email": ""}

    if request.method == "POST":
        dados, erros = validar_cadastro(request.form)
        valores = {
            "nome": request.form.get("nome", "").strip(),
            "email": request.form.get("email", "").strip(),
        }

        if not erros:
            existente = buscar_usuario_por_email(dados["email"])
            if existente is None:
                try:
                    criar_usuario(
                        dados["nome"],
                        dados["email"],
                        generate_password_hash(dados["senha"]),
                    )
                    enviar_confirmacao(dados["email"], dados["nome"])
                except sqlite3.IntegrityError:
                    pass  # e-mail criado em paralelo; a resposta continua a mesma
            elif not existente["email_confirmado"]:
                enviar_confirmacao(existente["email"], existente["nome"])
            else:
                enviar_email(
                    existente["email"],
                    "Tentativa de cadastro - OTDR Analyzer",
                    "Alguém tentou criar uma conta com este e-mail, mas ele já "
                    "está cadastrado. Se foi você, é só entrar pelo login. "
                    "Se não foi, ignore esta mensagem.",
                )

            # A resposta é a mesma nos três casos: não revela quem já tem conta
            flash(
                f"Cadastro recebido! Enviamos um e-mail para {dados['email']}. "
                "Verifique sua caixa de entrada (e o spam) e clique no link "
                "para aprovar sua conta. Você só poderá entrar depois disso.",
                "ok",
            )
            return redirect(url_for("login"))

    return render_template(
        "cadastro.html", erros=erros, valores=valores, email_enviado=None
    )


@app.route("/confirmar/<token>")
def confirmar(token):
    email = ler_token_confirmacao(token)
    registro = buscar_usuario_por_email(email) if email else None

    if registro is None:
        flash("Link inválido ou expirado. Peça um novo link de confirmação.", "erro")
        return redirect(url_for("reenviar"))

    confirmar_email(registro["id"])
    flash("E-mail confirmado! Agora você já pode entrar.", "ok")
    return redirect(url_for("login"))


@app.route("/reenviar", methods=["GET", "POST"])
def reenviar():
    enviado = False
    if request.method == "POST":
        registro = buscar_usuario_por_email(request.form.get("email", ""))
        if registro is not None and not registro["email_confirmado"]:
            enviar_confirmacao(registro["email"], registro["nome"])
        enviado = True
    return render_template("reenviar.html", enviado=enviado)


# ---------- páginas protegidas ----------

@app.route("/analise", methods=["GET", "POST"])
@login_obrigatorio
def analise():
    resultado = None
    erro = None
    limites = dict(LIMITES_PERDA_DB)

    if request.method == "POST":
        try:
            limites = {
                "emenda": float(request.form["limite_emenda"]),
                "conector": float(request.form["limite_conector"]),
            }
            arquivo = request.files["arquivo"]
            linhas = arquivo.stream.read().decode("utf-8").splitlines()
            eventos = ler_eventos_de_linhas(linhas)
            problemas = encontrar_problemas(eventos, limites)
            salvar_leitura(arquivo.filename, limites, eventos, problemas, usuario_atual()["id"])
            resultado = {"total": len(eventos), "problemas": problemas, "eventos": eventos}
        except (KeyError, ValueError, UnicodeDecodeError):
            erro = "Não foi possível ler o arquivo. Use um CSV com as colunas distancia_km, tipo, perda_db e reflectancia_db."

    return render_template("index.html", resultado=resultado, erro=erro, limites=limites)


@app.route("/historico")
@login_obrigatorio
def historico():
    return render_template("historico.html", leituras=listar_leituras(usuario_atual()["id"]))


@app.route("/leitura/<int:leitura_id>")
@login_obrigatorio
def leitura(leitura_id):
    registro, eventos = buscar_leitura(leitura_id, usuario_atual()["id"])
    if registro is None:
        abort(404)

    limites = {
        "emenda": registro["limite_emenda"],
        "conector": registro["limite_conector"],
    }
    problemas = encontrar_problemas(eventos, limites)
    resultado = {"total": len(eventos), "problemas": problemas, "eventos": eventos}

    return render_template(
        "leitura.html", leitura=registro, resultado=resultado, limites=limites, erro=None
    )


if __name__ == "__main__":
    app.run(debug=True)