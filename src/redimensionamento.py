import csv
from PIL import Image

from hashes import calcular_sha256, calcular_phash


def aplicar_redimensionamento(
    caminho_original,
    caminho_saida,
    percentual
):
    """
    Redimensiona a imagem mantendo sua proporção.
    """
    with Image.open(caminho_original) as imagem:
        largura, altura = imagem.size

        nova_largura = int(largura * percentual / 100)
        nova_altura = int(altura * percentual / 100)

        imagem_redimensionada = imagem.resize(
            (nova_largura, nova_altura),
            Image.Resampling.LANCZOS
        )

        imagem_redimensionada.save(caminho_saida)


def executar_experimento_redimensionamento(
    imagens,
    pasta_modificadas,
    pasta_resultados,
    percentuais
):
    """
    Executa o experimento de redimensionamento.
    """

    resultados = []

    for percentual in percentuais:

        # Cria uma pasta para cada percentual.
        pasta_percentual = pasta_modificadas / str(percentual)
        pasta_percentual.mkdir(parents=True, exist_ok=True)

        for caminho_original in imagens:

            caminho_modificado = (
                pasta_percentual / caminho_original.name
            )

            # Aplica o redimensionamento.
            aplicar_redimensionamento(
                caminho_original,
                caminho_modificado,
                percentual
            )

            # Calcula os hashes.
            sha_original = calcular_sha256(caminho_original)
            sha_modificado = calcular_sha256(caminho_modificado)

            phash_original = calcular_phash(caminho_original)
            phash_modificado = calcular_phash(caminho_modificado)

            # Calcula a distância entre os pHashes.
            distancia_hamming = (
                phash_original - phash_modificado
            )

            resultados.append([
                caminho_original.name,
                percentual,
                sha_original == sha_modificado,
                str(phash_original),
                str(phash_modificado),
                distancia_hamming
            ])

    # Salva os resultados em CSV.
    pasta_resultados.mkdir(parents=True, exist_ok=True)

    arquivo_resultados = (
        pasta_resultados / "redimensionamento.csv"
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
            "percentual",
            "sha256_igual",
            "phash_original",
            "phash_modificado",
            "distancia_hamming"
        ])

        escritor.writerows(resultados)

    print("Experimento de redimensionamento concluído.")
    print(f"Comparações: {len(resultados)}")
    print(f"Resultados salvos em: {arquivo_resultados}")