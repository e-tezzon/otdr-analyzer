import csv

# Limites de perda por tipo de evento (em dB).
# Valores de exemplo: cada operadora define os seus.
LIMITES_PERDA_DB = {
    "emenda": 0.20,
    "conector": 0.50,
}


def ler_eventos(caminho):
    eventos = []
    with open(caminho, newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            eventos.append({
                "distancia_km": float(linha["distancia_km"]),
                "tipo": linha["tipo"],
                "perda_db": float(linha["perda_db"]),
                "reflectancia_db": float(linha["reflectancia_db"]),
            })
    return eventos


def encontrar_problemas(eventos, limites):
    problemas = []
    for evento in eventos:
        limite = limites.get(evento["tipo"])
        if limite is not None and evento["perda_db"] > limite:
            problemas.append(evento)
    return problemas


if __name__ == "__main__":
    eventos = ler_eventos("eventos.csv")
    problemas = encontrar_problemas(eventos, LIMITES_PERDA_DB)

    print(f"{len(eventos)} eventos analisados")
    print(f"{len(problemas)} fora do limite:")
    for p in problemas:
        limite = LIMITES_PERDA_DB[p["tipo"]]
        print(f"- {p['distancia_km']} km | {p['tipo']} | perda {p['perda_db']} dB (limite {limite} dB)")