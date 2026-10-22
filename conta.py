from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from autenticacao import login_obrigatorio, usuario_atual
from banco import atualizar_senha
from emails import enviar_email
from validacao import validar_troca_senha

conta_bp = Blueprint("conta", __name__, url_prefix="/conta")


@conta_bp.route("/senha", methods=["GET", "POST"])
@login_obrigatorio
def senha():
    usuario = usuario_atual()
    erros = {}

    if request.method == "POST":
        atual, nova, erros = validar_troca_senha(request.form, usuario["email"])

        if "senha_atual" not in erros and not check_password_hash(usuario["senha_hash"], atual):
            erros["senha_atual"] = "Senha atual incorreta."

        if not erros:
            atualizar_senha(usuario["id"], generate_password_hash(nova))
            enviar_email(
                usuario["email"],
                "Sua senha foi alterada - OTDR Analyzer",
                "Olá!\n\nA senha da sua conta no OTDR Analyzer acabou de ser alterada. "
                "Se não foi você, avise o administrador do sistema imediatamente.",
            )
            session.clear()
            session["usuario_id"] = usuario["id"]
            flash("Senha alterada com sucesso.", "ok")
            return redirect(url_for("analise"))

    return render_template("senha.html", erros=erros)