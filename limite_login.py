
import hashlib
import hmac
import math
import time
from contextlib import closing

from werkzeug.security import check_password_hash

import config
from banco import conectar


INTERVALO_SEGUNDOS = 30 * 60
LIMITE_INICIAL = 2


def _identificador(email):
    normalizado = email.strip().lower()

    return hmac.new(
        config.SECRET_KEY.encode("utf-8"),
        normalizado.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def preparar_controle_login():
    """Cria a tabela que armazena os bloqueios."""

    with closing(conectar()) as conexao:
        with conexao:
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS tentativas_login (
                    identificador TEXT PRIMARY KEY,
                    falhas INTEGER NOT NULL DEFAULT 0,
                    bloqueado_ate INTEGER NOT NULL DEFAULT 0,
                    atualizado_em INTEGER NOT NULL
                )
            """)

            agora = int(time.time())

            conexao.execute("""
                DELETE FROM tentativas_login
                WHERE atualizado_em < ?
                AND bloqueado_ate <= ?
            """, (
                agora - 90 * 24 * 60 * 60,
                agora
            ))


def autenticar_com_limite(
    email, senha, registro, hash_falso, *, agora=None
):
    """Verifica a senha e aplica o bloqueio progressivo."""

    instante = int(time.time()) if agora is None else int(agora)
    identificador = _identificador(email)

    with closing(conectar()) as conexao:
        with conexao:
            conexao.execute("BEGIN IMMEDIATE")

            estado = conexao.execute("""
                SELECT falhas, bloqueado_ate
                FROM tentativas_login
                WHERE identificador = ?
            """, (identificador,)).fetchone()

            if estado is not None:
                if estado["bloqueado_ate"] > instante:
                    restante = math.ceil(
                        (estado["bloqueado_ate"] - instante) / 60
                    )
                    return "bloqueado", restante

            hash_guardado = (
                registro["senha_hash"]
                if registro is not None
                else hash_falso
            )

            senha_valida = check_password_hash(
                hash_guardado, senha
            )

            if registro is not None and senha_valida:
                if not registro["email_confirmado"]:
                    return "pendente", 0

                conexao.execute("""
                    DELETE FROM tentativas_login
                    WHERE identificador = ?
                """, (identificador,))

                return "ok", 0

            falhas = (
                estado["falhas"] if estado is not None else 0
            ) + 1

            duracao = (
                max(0, falhas - LIMITE_INICIAL + 1)
                * INTERVALO_SEGUNDOS
            )

            bloqueado_ate = (
                instante + duracao if duracao else 0
            )

            conexao.execute("""
                INSERT INTO tentativas_login
                    (identificador, falhas, bloqueado_ate, atualizado_em)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(identificador) DO UPDATE SET
                    falhas = excluded.falhas,
                    bloqueado_ate = excluded.bloqueado_ate,
                    atualizado_em = excluded.atualizado_em
            """, (
                identificador,
                falhas,
                bloqueado_ate,
                instante
            ))

            if duracao:
                return "bloqueado", duracao // 60

            return "invalido", 0
