import csv
from pathlib import Path
from itertools import combinations

from hashes import calcular_phash

# Define o diretório raiz do projeto
PASTA_BASE = Path(__file__).parent.parent

# Diretórios utilizados no experimento
PASTA_ORIGINAIS = PASTA_BASE / "dataset" / "img-original"
PASTA_RESULTADOS = PASTA_BASE / "resultados"


def executar_experimento_discriminacao():
    """
    Compara o pHash de todas as combinações de imagens originais
    para avaliar a capacidade de discriminação do algoritmo.
    """

    imagens = sorted(PASTA_ORIGINAIS.glob("*.png"))

    # Garante que a pasta de resultados exista
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)

    arquivo_resultados = PASTA_RESULTADOS / "discriminacao.csv"

    # Calcula o pHash de cada imagem uma única vez
    hashes = {}

    for imagem in imagens:
        hashes[imagem] = calcular_phash(imagem)

    resultados = []

    # Gera todos os pares únicos de imagens
    for imagem_a, imagem_b in combinations(imagens, 2):
        phash_a = hashes[imagem_a]
        phash_b = hashes[imagem_b]

        # O operador "-" do ImageHash calcula a distância de Hamming
        distancia_hamming = phash_a - phash_b

        resultados.append([
            imagem_a.name,
            imagem_b.name,
            str(phash_a),
            str(phash_b),
            distancia_hamming
        ])

    # Salva as comparações em CSV
    with open(
        arquivo_resultados,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        escritor = csv.writer(arquivo)

        escritor.writerow([
            "imagem_a",
            "imagem_b",
            "phash_a",
            "phash_b",
            "distancia_hamming"
        ])

        escritor.writerows(resultados)

    print("Experimento de discriminação concluído.")
    print(f"Imagens: {len(imagens)}")
    print(f"Comparações: {len(resultados)}")
    print(f"Resultados salvos em: {arquivo_resultados}")


if __name__ == "__main__":
    executar_experimento_discriminacao()