
import sqlite3
from datetime import datetime


# ==========================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ==========================================

CAMINHO_BANCO = "otdr.db"


def conectar():
    """Cria uma conexão com o banco SQLite."""
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


# ==========================================
# CRIAÇÃO E MIGRAÇÃO DAS TABELAS
# ==========================================

def criar_tabelas():
    """Cria as tabelas necessárias ao sistema."""

    with conectar() as conexao:
        conexao.executescript("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL,
                email_confirmado INTEGER NOT NULL DEFAULT 0,
                criado_em TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS leituras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_arquivo TEXT NOT NULL,
                data_analise TEXT NOT NULL,
                limite_emenda REAL NOT NULL,
                limite_conector REAL NOT NULL,
                total_eventos INTEGER NOT NULL,
                total_problemas INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                leitura_id INTEGER NOT NULL,
                distancia_km REAL NOT NULL,
                tipo TEXT NOT NULL,
                perda_db REAL NOT NULL,
                reflectancia_db REAL NOT NULL,
                FOREIGN KEY (leitura_id)
                    REFERENCES leituras (id)
                    ON DELETE CASCADE
            );
        """)

        migrar_leituras(conexao)


def migrar_leituras(conexao):
    """
    Atualiza bancos antigos, adicionando usuario_id
    quando a coluna ainda não existir.
    """

    colunas = [
        coluna["name"]
        for coluna in conexao.execute(
            "PRAGMA table_info(leituras)"
        )
    ]

    if "usuario_id" not in colunas:
        conexao.execute("""
            ALTER TABLE leituras
            ADD COLUMN usuario_id INTEGER
            REFERENCES usuarios (id)
        """)


# ==========================================
# GERENCIAMENTO DE USUÁRIOS
# ==========================================

def criar_usuario(nome, email, senha_hash):
    """
    Cadastra um novo usuário.
    O e-mail deve ser único.
    """

    email = email.strip().lower()

    with conectar() as conexao:
        cursor = conexao.execute(
            """
            INSERT INTO usuarios (
                nome,
                email,
                senha_hash,
                criado_em
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                nome,
                email,
                senha_hash,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        return cursor.lastrowid


def buscar_usuario_por_email(email):
    """Busca um usuário pelo e-mail."""

    email = email.strip().lower()

    with conectar() as conexao:
        return conexao.execute(
            """
            SELECT *
            FROM usuarios
            WHERE email = ?
            """,
            (email,)
        ).fetchone()


def buscar_usuario_por_id(usuario_id):
    """Busca um usuário pelo ID."""

    with conectar() as conexao:
        return conexao.execute(
            """
            SELECT *
            FROM usuarios
            WHERE id = ?
            """,
            (usuario_id,)
        ).fetchone()


def confirmar_email(usuario_id):
    """Marca o e-mail do usuário como confirmado."""

    with conectar() as conexao:
        conexao.execute(
            """
            UPDATE usuarios
            SET email_confirmado = 1
            WHERE id = ?
            """,
            (usuario_id,)
        )


def atualizar_senha(usuario_id, senha_hash):
    """Atualiza o hash da senha de um usuário."""

    with conectar() as conexao:
        conexao.execute(
            """
            UPDATE usuarios
            SET senha_hash = ?
            WHERE id = ?
            """,
            (senha_hash, usuario_id)
        )


def listar_usuarios():
    """
    Retorna usuários e quantidade de leituras.
    Não retorna hashes de senhas.
    """

    with conectar() as conexao:
        return conexao.execute(
            """
            SELECT
                u.id,
                u.nome,
                u.email,
                u.email_confirmado,
                u.criado_em,
                COUNT(l.id) AS total_leituras

            FROM usuarios u

            LEFT JOIN leituras l
                ON l.usuario_id = u.id

            GROUP BY u.id

            ORDER BY u.id DESC
            """
        ).fetchall()


# ==========================================
# GERENCIAMENTO DE LEITURAS OTDR
# ==========================================

def salvar_leitura(
    nome_arquivo,
    limites,
    eventos,
    problemas,
    usuario_id
):
    """
    Salva uma análise OTDR e seus eventos.
    Relaciona a leitura ao usuário autenticado.
    """

    with conectar() as conexao:

        cursor = conexao.execute(
            """
            INSERT INTO leituras (
                nome_arquivo,
                data_analise,
                limite_emenda,
                limite_conector,
                total_eventos,
                total_problemas,
                usuario_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                nome_arquivo,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                limites["emenda"],
                limites["conector"],
                len(eventos),
                len(problemas),
                usuario_id
            )
        )

        leitura_id = cursor.lastrowid

        dados_eventos = [
            (
                leitura_id,
                evento["distancia_km"],
                evento["tipo"],
                evento["perda_db"],
                evento["reflectancia_db"]
            )
            for evento in eventos
        ]

        conexao.executemany(
            """
            INSERT INTO eventos (
                leitura_id,
                distancia_km,
                tipo,
                perda_db,
                reflectancia_db
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            dados_eventos
        )

    return leitura_id


def listar_leituras(usuario_id):
    """
    Lista o histórico de análises de um usuário.
    """

    with conectar() as conexao:
        return conexao.execute(
            """
            SELECT *
            FROM leituras
            WHERE usuario_id = ?
            ORDER BY id DESC
            """,
            (usuario_id,)
        ).fetchall()


def buscar_leitura(leitura_id, usuario_id):
    """
    Busca uma leitura e seus eventos.
    Somente permite acessar leituras do próprio usuário.
    """

    with conectar() as conexao:

        leitura = conexao.execute(
            """
            SELECT *
            FROM leituras
            WHERE id = ?
              AND usuario_id = ?
            """,
            (leitura_id, usuario_id)
        ).fetchone()

        if leitura is None:
            return None, []

        eventos = conexao.execute(
            """
            SELECT
                distancia_km,
                tipo,
                perda_db,
                reflectancia_db

            FROM eventos

            WHERE leitura_id = ?

            ORDER BY distancia_km, id
            """,
            (leitura_id,)
        ).fetchall()

    return leitura, [dict(evento) for evento in eventos]


# ==========================================
# EXECUÇÃO DIRETA / TESTE DO BANCO
# ==========================================

if __name__ == "__main__":

    criar_tabelas()

    with conectar() as conexao:
        tabelas = conexao.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            """
        ).fetchall()

    print("Banco de dados inicializado.")
    print("Tabelas encontradas:")

    for tabela in tabelas:
        print("-", tabela["name"])
