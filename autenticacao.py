from functools import wraps

from flask import abort, g, redirect, session, url_for
from itsdangerous import BadSignature, URLSafeTimedSerializer

import config
from banco import buscar_usuario_por_id

VALIDADE_CONFIRMACAO = 60 * 60 * 24  # 24 horas


def _serializador():
    return URLSafeTimedSerializer(config.SECRET_KEY, salt="confirmar-email")


def gerar_token_confirmacao(email):
    return _serializador().dumps(email)


def ler_token_confirmacao(token):
    """Devolve o e-mail do token, ou None se for inválido ou tiver expirado."""
    try:
        return _serializador().loads(token, max_age=VALIDADE_CONFIRMACAO)
    except BadSignature:  # inclui token expirado
        return None


def usuario_atual():
    if "usuario" not in g:
        usuario_id = session.get("usuario_id")
        g.usuario = buscar_usuario_por_id(usuario_id) if usuario_id is not None else None
    return g.usuario


def eh_admin(usuario):
    return (
        usuario is not None
        and bool(config.ADMIN_EMAIL)
        and bool(usuario["email_confirmado"])
        and usuario["email"] == config.ADMIN_EMAIL
    )


def login_obrigatorio(funcao):
    @wraps(funcao)
    def protegida(*args, **kwargs):
        if usuario_atual() is None:
            session.clear()
            return redirect(url_for("login"))
        return funcao(*args, **kwargs)
    return protegida


def admin_obrigatorio(funcao):
    @wraps(funcao)
    def protegida(*args, **kwargs):
        usuario = usuario_atual()
        if usuario is None:
            session.clear()
            return redirect(url_for("login"))
        if not eh_admin(usuario):
            abort(404)  # não revela que a página existe
        return funcao(*args, **kwargs)
    return protegida