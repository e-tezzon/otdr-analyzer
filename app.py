from flask import Flask, abort, render_template, request

from analisador import LIMITES_PERDA_DB, encontrar_problemas, ler_eventos_de_linhas
from banco import buscar_leitura, criar_tabelas, listar_leituras, salvar_leitura

app = Flask(__name__)
criar_tabelas()


@app.route("/", methods=["GET", "POST"])
def inicio():
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
            salvar_leitura(arquivo.filename, limites, eventos, problemas)
            resultado = {"total": len(eventos), "problemas": problemas, "eventos": eventos}
        except (KeyError, ValueError, UnicodeDecodeError):
            erro = "Não foi possível ler o arquivo. Use um CSV com as colunas distancia_km, tipo, perda_db e reflectancia_db."

    return render_template("index.html", resultado=resultado, erro=erro, limites=limites)


@app.route("/historico")
def historico():
    return render_template("historico.html", leituras=listar_leituras())


@app.route("/leitura/<int:leitura_id>")
def leitura(leitura_id):
    registro, eventos = buscar_leitura(leitura_id)
    if registro is None:
        abort(404)

    limites = {
        "emenda": registro["limite_emenda"],
        "conector": registro["limite_conector"],
    }
    problemas = encontrar_problemas(eventos, limites)
    resultado = {"total": len(eventos), "problemas": problemas, "eventos": eventos}

    return render_template(
        "leitura.html",
        leitura=registro,
        resultado=resultado,
        limites=limites,
        erro=None,
    )


if __name__ == "__main__":
    app.run(debug=True)