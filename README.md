# OTDR Analyzer

Ferramenta em Python com interface web que lê eventos de medições OTDR
e identifica emendas e conectores com perda acima de limites configuráveis.

## Por quê

Trabalho com fibra óptica e sou formado em Análise e Desenvolvimento
de Sistemas. Este projeto junta os dois mundos e foi construído em
público, etapa por etapa.

## O que faz

- Lê um arquivo CSV com os eventos de uma medição
- Compara a perda de cada emenda e conector com o limite definido
- Mostra na tela os eventos fora do padrão
- Também funciona pelo terminal, gerando o arquivo `relatorio.csv`

## Tecnologias

Python, Flask, HTML e CSV.

## Como rodar

1. Instale as dependências:

```
python -m pip install flask
```

2. Inicie o servidor:

```
python app.py
```

3. Abra no navegador: http://127.0.0.1:5000

4. Envie o arquivo `eventos.csv`, ajuste os limites e clique em **Analisar**.

### Pelo terminal

```
python analisador.py
```

## Formato do CSV

```
distancia_km,tipo,perda_db,reflectancia_db
0.00,inicio,0.00,-45
2.35,emenda,0.08,-60
5.10,conector,0.62,-48
```

Os tipos analisados são `emenda` e `conector`.

## Estrutura do projeto

- `analisador.py`: lógica de leitura e análise dos eventos
- `app.py`: servidor