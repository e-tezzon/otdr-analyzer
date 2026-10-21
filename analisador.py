import csv


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


if __name__ == "__main__":
    eventos = ler_eventos("eventos.csv")
    print(f"{len(eventos)} eventos lidos")
    for evento in eventos:
        print(evento)