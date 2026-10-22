import sqlite3
from datetime import datetime

CAMINHO_BANCO = "otdr.db"


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas():
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
                FOREIGN KEY (leitura_id) REFERENCES leituras (id) ON DELETE CASCADE
            );
        """)
        migrar_leituras(conexao)


def migrar_leituras(conexao):
    # Bancos criados antes do login não têm a coluna usuario_id
    colunas = [c["name"] for c in conexao.execute("PRAGMA table_info(leituras)")]
    if "usuario_id" not in colunas:
        conexao.execute(
            "ALTER TABLE leituras ADD COLUMN usuario_id INTEGER REFERENCES usuarios (id)"
        )


# ---------- usuários ----------

def criar_usuario(nome, email, senha_hash):
    """Cria o usuário. Se o e-mail já existir, levanta sqlite3.IntegrityError."""
    with conectar() as conexao:
        cursor = conexao.execute(
            "INSERT INTO usuarios (nome, email, senha_hash, criado_em) VALUES (?, ?, ?, ?)",
            (nome, email.strip().lower(), senha_hash, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        return cursor.lastrowid


def buscar_usuario_por_email(email):
    with conectar() as conexao:
        return conexao.execute(
            "SELECT * FROM usuarios WHERE email = ?", (email.strip().lower(),)
        ).fetchone()


def buscar_usuario_por_id(usuario_id):
    with conectar() as conexao:
        return conexao.execute(
            "SELECT * FROM usuarios WHERE id = ?", (usuario_id,)
        ).fetchone()


# ---------- leituras ----------

def salvar_leitura(nome_arquivo, limites, eventos, problemas, usuario_id=None):
    with conectar() as conexao:
        cursor = conexao.execute(
            "INSERT INTO leituras (nome_arquivo, data_analise, limite_emenda, "
            "limite_conector, total_eventos, total_problemas, usuario_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                nome_arquivo,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                limites["emenda"],
                limites["conector"],
                len(eventos),
                len(problemas),
                usuario_id,
            ),
        )
        leitura_id = cursor.lastrowid
        conexao.executemany(
            "INSERT INTO eventos (leitura_id, distancia_km, tipo, perda_db, reflectancia_db) "
            "VALUES (?, ?, ?, ?, ?)",
            [
                (leitura_id, e["distancia_km"], e["tipo"], e["perda_db"], e["reflectancia_db"])
                for e in eventos
            ],
        )
    return leitura_id


def listar_leituras():
    with conectar() as conexao:
        return conexao.execute(
            "SELECT * FROM leituras ORDER BY id DESC"
        ).fetchall()


def buscar_leitura(leitura_id):
    with conectar() as conexao:
        leitura = conexao.execute(
            "SELECT * FROM leituras WHERE id = ?", (leitura_id,)
        ).fetchone()
        if leitura is None:
            return None, []
        eventos = conexao.execute(
            "SELECT distancia_km, tipo, perda_db, reflectancia_db "
            "FROM eventos WHERE leitura_id = ? ORDER BY distancia_km, id",
            (leitura_id,),
        ).fetchall()
    return leitura, [dict(e) for e in eventos]


if __name__ == "__main__":
    criar_tabelas()
    with conectar() as conexao:
        tabelas = conexao.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()
        colunas = conexao.execute("PRAGMA table_info(leituras)").fetchall()
    print("Tabelas:", [t["name"] for t in tabelas])
    print("Colunas de leituras:", [c["name"] for c in colunas])