import csv
from PIL import Image

from hashes import calcular_sha256, calcular_phash


def aplicar_espelhamento(caminho_original, caminho_saida):
    """
    Aplica espelhamento horizontal à imagem.
    """
    with Image.open(caminho_original) as imagem:
        imagem_espelhada = imagem.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        imagem_espelhada.save(caminho_saida)


def executar_experimento_espelhamento(
    imagens,
    pasta_modificadas,
    pasta_resultados
):
    """
    Executa o experimento de espelhamento horizontal.
    """

    pasta_modificadas.mkdir(parents=True, exist_ok=True)
    pasta_resultados.mkdir(parents=True, exist_ok=True)

    resultados = []

    for caminho_original in imagens:

        caminho_modificado = (
            pasta_modificadas / caminho_original.name
        )

        aplicar_espelhamento(
            caminho_original,
            caminho_modificado
        )

        sha_original = calcular_sha256(caminho_original)
        sha_modificado = calcular_sha256(caminho_modificado)

        phash_original = calcular_phash(caminho_original)
        phash_modificado = calcular_phash(caminho_modificado)

        distancia_hamming = phash_original - phash_modificado

        resultados.append([
            caminho_original.name,
            sha_original == sha_modificado,
            str(phash_original),
            str(phash_modificado),
            distancia_hamming
        ])

    arquivo_resultados = (
        pasta_resultados / "espelhamento.csv"
    )

    with open(
        arquivo_resultados,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        escritor = csv.writer(arquivo)

        escritor.writerow([
            "imagem",
            "sha256_igual",
            "phash_original",
            "phash_modificado",
            "distancia_hamming"
        ])

        escritor.writerows(resultados)

    print("Experimento de espelhamento concluído.")
    print(f"Imagens: {len(imagens)}")
    print(f"Resultados salvos em: {arquivo_resultados}")