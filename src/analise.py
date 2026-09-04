import csv
import statistics
from pathlib import Path


# Define o diretório raiz do projeto.
PASTA_BASE = Path(__file__).parent.parent

# Diretório onde estão armazenados os resultados dos experimentos.
PASTA_RESULTADOS = PASTA_BASE / "resultados"


def calcular_estatisticas(valores):
    """
    Calcula as estatísticas descritivas das distâncias de Hamming
    """

    return {
        "comparacoes": len(valores),
        "media": statistics.mean(valores),
        "mediana": statistics.median(valores),
        "minimo": min(valores),
        "maximo": max(valores),
        "desvio_padrao": statistics.stdev(valores),
        "quantidade_zero": valores.count(0)
    }


def exibir_estatisticas(valores):
    """
    Exibe as estatísticas descritivas das distâncias de Hamming.
    """

    estatisticas = calcular_estatisticas(valores)

    percentual_zero = (
        estatisticas["quantidade_zero"]
        / estatisticas["comparacoes"]
    ) * 100

    print(f"  Comparações: {estatisticas['comparacoes']}")
    print(f"  Média: {estatisticas['media']:.2f}")
    print(f"  Mediana: {estatisticas['mediana']:.2f}")
    print(f"  Mínimo: {estatisticas['minimo']}")
    print(f"  Máximo: {estatisticas['maximo']}")
    print(
        f"  Desvio-padrão: "
        f"{estatisticas['desvio_padrao']:.2f}"
    )
    print(
        f"  Distância 0: "
        f"{estatisticas['quantidade_zero']} "
        f"({percentual_zero:.2f}%)"
    )


def analisar_resultados(
    nome_arquivo,
    coluna_parametro,
    nome_experimento
):
    """
    Analisa os resultados de um experimento de robustez,
    agrupando as distâncias pelo parâmetro da transformação
    """

    arquivo_resultados = PASTA_RESULTADOS / nome_arquivo
    distancias = {}

    with open(
        arquivo_resultados,
        "r",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            parametro = int(linha[coluna_parametro])
            distancia = int(linha["distancia_hamming"])

            if parametro not in distancias:
                distancias[parametro] = []

            distancias[parametro].append(distancia)

    print(f"\nAnálise do experimento: {nome_experimento}\n")

    for parametro in sorted(distancias):

        print(f"Parâmetro: {parametro}")

        exibir_estatisticas(distancias[parametro])

        print()


def analisar_discriminacao():
    """
    Analisa as distâncias de Hamming entre imagens
    originais diferentes.
    """

    arquivo_resultados = (
        PASTA_RESULTADOS / "discriminacao.csv"
    )

    distancias = []

    with open(
        arquivo_resultados,
        "r",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            distancia = int(linha["distancia_hamming"])
            distancias.append(distancia)

    print("\nAnálise do experimento: Discriminação\n")

    exibir_estatisticas(distancias)

    print()

def analisar_espelhamento():
    arquivo_resultados = PASTA_RESULTADOS / "espelhamento.csv"
    distancias = []

    with open(
        arquivo_resultados,
        "r",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            distancias.append(
                int(linha["distancia_hamming"])
            )

    print("\nAnálise do experimento: Espelhamento\n")
    exibir_estatisticas(distancias)
    print()

def main():
    analisar_resultados(
        "jpeg.csv",
        "qualidade",
        "Compressão JPEG"
    )

    analisar_resultados(
        "rotacao.csv",
        "angulo",
        "Rotação"
    )

    analisar_resultados(
        "crop.csv",
        "percentual",
        "Crop"
    )
    
    analisar_resultados(
        "redimensionamento.csv",
        "percentual",
        "Redimensionamento"
    )

    analisar_espelhamento()
    analisar_discriminacao()
if __name__ == "__main__":
    main()