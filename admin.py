from flask import Blueprint, render_template

from autenticacao import admin_obrigatorio, eh_admin, usuario_atual
from banco import listar_usuarios

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.app_context_processor
def dados_admin():
    # Deixa a variável eh_admin disponível em todos os templates
    return {"eh_admin": eh_admin(usuario_atual())}


@admin_bp.route("/")
@admin_obrigatorio
def painel():
    usuarios = listar_usuarios()
    confirmados = sum(1 for u in usuarios if u["email_confirmado"])
    resumo = {
        "total": len(usuarios),
        "confirmados": confirmados,
        "pendentes": len(usuarios) - confirmados,
    }
    return render_template("admin.html", usuarios=usuarios, resumo=resumo)