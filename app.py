from flask import Flask, render_template, request

from analisador import LIMITES_PERDA_DB, encontrar_problemas, ler_eventos_de_linhas

app = Flask(__name__)


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
            resultado = {"total": len(eventos), "problemas": problemas}
        except (KeyError, ValueError, UnicodeDecodeError):
            erro = "Não foi possível ler o arquivo. Use um CSV com as colunas distancia_km, tipo, perda_db e reflectancia_db."

    return render_template("index.html", resultado=resultado, erro=erro, limites=limites)


if __name__ == "__main__":
    app.run(debug=True)