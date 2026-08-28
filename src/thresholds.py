import csv
from pathlib import Path

# Define o diretório raiz do projeto
PASTA_BASE = Path(__file__).parent.parent
PASTA_RESULTADOS = PASTA_BASE / "resultados"

# Limiares de distância de Hamming avaliados
THRESHOLDS = [5, 10, 15, 20, 25, 30]

def carregar_distancias_por_parametro(
    nome_arquivo,
    coluna_parametro
):
    """
    Lê um CSV de robustez e agrupa as distâncias
    pelo parâmetro da transformação.
    """

    caminho_arquivo = PASTA_RESULTADOS / nome_arquivo
    distancias = {}

    with open(
        caminho_arquivo,
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

    return distancias

def carregar_distancias_discriminacao():
    """
    Lê as distâncias entre imagens originais diferentes.
    """

    caminho_arquivo = (
        PASTA_RESULTADOS / "discriminacao.csv"
    )

    distancias = []

    with open(
        caminho_arquivo,
        "r",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            distancias.append(
                int(linha["distancia_hamming"])
            )

    return distancias

def calcular_reconhecimento(distancias, threshold):
    """
    Calcula quantas imagens modificadas foram reconhecidas
    como correspondentes às imagens originais.
    """

    reconhecidas = sum(
        distancia <= threshold
        for distancia in distancias
    )

    percentual = (
        reconhecidas / len(distancias)
    ) * 100

    return reconhecidas, percentual

def exibir_transformacao(
    nome,
    grupos,
    threshold,
    unidade=""
):
    """
    Exibe a taxa de reconhecimento de cada intensidade
    de uma transformação.
    """

    print(f"  {nome}")

    for parametro in sorted(grupos):

        distancias = grupos[parametro]

        reconhecidas, percentual = calcular_reconhecimento(
            distancias,
            threshold
        )

        print(
            f"    {parametro}{unidade}: "
            f"{reconhecidas}/{len(distancias)} "
            f"({percentual:.2f}%)"
        )


def main():

    # Carrega os resultados de robustez separados
    # pelos parâmetros de cada transformação
    jpeg = carregar_distancias_por_parametro(
        "jpeg.csv",
        "qualidade"
    )

    rotacao = carregar_distancias_por_parametro(
        "rotacao.csv",
        "angulo"
    )

    crop = carregar_distancias_por_parametro(
        "crop.csv",
        "percentual"
    )

    # Carrega as comparações entre imagens diferentes
    discriminacao = carregar_distancias_discriminacao()

    print("\nAnálise de thresholds\n")

    for threshold in THRESHOLDS:

        print(f"Threshold: {threshold}")

        exibir_transformacao(
            "JPEG",
            jpeg,
            threshold
        )

        exibir_transformacao(
            "Rotação",
            rotacao,
            threshold,
            "°"
        )

        exibir_transformacao(
            "Crop",
            crop,
            threshold,
            "%"
        )

        # Em imagens diferentes, uma distância menor ou igual
        # ao threshold representa um falso positivo
        falsos_positivos = sum(
            distancia <= threshold
            for distancia in discriminacao
        )

        percentual_falsos = (
            falsos_positivos / len(discriminacao)
        ) * 100

        print("  Discriminação")
        print(
            f"    Falsos positivos: "
            f"{falsos_positivos}/{len(discriminacao)} "
            f"({percentual_falsos:.2f}%)"
        )

        print()

if __name__ == "__main__":
    main()