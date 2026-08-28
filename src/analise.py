import csv
import statistics
from pathlib import Path

# Define o diretório raiz do projeto
PASTA_BASE = Path(__file__).parent.parent

# Diretório onde estão armazenados os resultados dos experimentos
PASTA_RESULTADOS = PASTA_BASE / "resultados"


def analisar_resultados(
    nome_arquivo,
    coluna_parametro,
    nome_experimento
):
    """
    Analisa as distâncias de Hamming de um experimento

    Os resultados são agrupados pelo parâmetro da transformação
    e são calculadas estatísticas descritivas para cada grupo
    """

    arquivo_resultados = PASTA_RESULTADOS / nome_arquivo

    # Armazena as distâncias de Hamming agrupadas pelo parâmetro
    distancias = {}

    # Lê os resultados do experimento
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

            # Cria uma lista para o parâmetro caso ainda não exista
            if parametro not in distancias:
                distancias[parametro] = []

            distancias[parametro].append(distancia)

    print(f"\nAnálise do experimento: {nome_experimento}\n")

    # Calcula as estatísticas de cada parâmetro
    for parametro in sorted(distancias):

        valores = distancias[parametro]

        media = statistics.mean(valores)
        mediana = statistics.median(valores)
        minimo = min(valores)
        maximo = max(valores)
        desvio_padrao = statistics.stdev(valores) #desvio-padrão amostral

        # Calcula quantas comparações tiveram pHash idêntico
        quantidade_zero = valores.count(0)
        percentual_zero = (
            quantidade_zero / len(valores)
        ) * 100

        print(f"Parâmetro: {parametro}")
        print(f"  Comparações: {len(valores)}")
        print(f"  Média: {media:.2f}")
        print(f"  Mediana: {mediana:.2f}")
        print(f"  Mínimo: {minimo}")
        print(f"  Máximo: {maximo}")
        print(f"  Desvio-padrão: {desvio_padrao:.2f}")
        print(
            f"  Distância 0: {quantidade_zero} "
            f"({percentual_zero:.2f}%)"
        )
        print()

def main():
    """
    Executa a análise dos resultados de todos os experimentos
    realizados no dataset piloto.
    """

    # Analisa os resultados da compressão JPEG
    analisar_resultados(
        "jpeg.csv",
        "qualidade",
        "Compressão JPEG"
    )

    # Analisa os resultados da rotação
    analisar_resultados(
        "rotacao.csv",
        "angulo",
        "Rotação"
    )

    # Analisa os resultados do recorte
    analisar_resultados(
        "crop.csv",
        "percentual",
        "Crop"
    )

if __name__ == "__main__":
    main()