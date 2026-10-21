import sqlite3

CAMINHO_BANCO = "otdr.db"


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas():
    with conectar() as conexao:
        conexao.executescript("""
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


if __name__ == "__main__":
    criar_tabelas()
    with conectar() as conexao:
        tabelas = conexao.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()
    print("Banco criado: otdr.db")
    print("Tabelas:", [t["name"] for t in tabelas])