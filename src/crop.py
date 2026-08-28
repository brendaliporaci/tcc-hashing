import csv
from PIL import Image
from hashes import calcular_sha256, calcular_phash

def aplicar_crop(caminho_original, caminho_saida, percentual):
    """
    Gera uma nova versão da imagem removendo uma porcentagem
    de cada uma das quatro bordas

    A imagem original não é modificada
    """

    with Image.open(caminho_original) as imagem:
        largura, altura = imagem.size

        # Calcula quantos pixels serão removidos de cada lado.
        corte_x = int(largura * (percentual / 100))
        corte_y = int(altura * (percentual / 100))

        # Define a área da imagem que será mantida
        area_crop = (
            corte_x,
            corte_y,
            largura - corte_x,
            altura - corte_y
        )

        imagem_recortada = imagem.crop(area_crop)

        # Salva a imagem recortada sem alterar a original
        imagem_recortada.save(caminho_saida)

def executar_experimento_crop(
    imagens,
    pasta_crop,
    pasta_resultados,
    percentuais
):
    """
    Executa o experimento de robustez do pHash ao recorte.

    Para cada imagem original, gera versões recortadas nos percentuais
    definidos, calcula os hashes e registra os resultados em CSV.
    """

    # Armazena os resultados das comparações
    resultados = []

    # Percorre todas as imagens originais do dataset
    for imagem_original in imagens:

        # Calcula os hashes da imagem original
        sha_original = calcular_sha256(imagem_original)
        phash_original = calcular_phash(imagem_original)

        print(f"Imagem: {imagem_original.name}")

        # Aplica cada percentual de recorte definido no experimento
        for percentual in percentuais:

            # Cria uma pasta específica para cada percentual
            pasta_saida = pasta_crop / str(percentual)
            pasta_saida.mkdir(parents=True, exist_ok=True)

            # Define o nome e o caminho da imagem modificada
            nome_saida = (
                f"{imagem_original.stem}_crop_{percentual}.png"
            )
            imagem_modificada = pasta_saida / nome_saida

            # Gera a versão recortada da imagem
            aplicar_crop(
                imagem_original,
                imagem_modificada,
                percentual
            )

            # Calcula os hashes da imagem modificada
            sha_modificado = calcular_sha256(imagem_modificada)
            phash_modificado = calcular_phash(imagem_modificada)

            # Calcula a distância de Hamming entre os pHashes
            distancia_hamming = (
                phash_original - phash_modificado
            )

            # Armazena os dados da comparação
            resultados.append({
                "imagem": imagem_original.name,
                "percentual": percentual,
                "sha256_igual": sha_original == sha_modificado,
                "phash_original": str(phash_original),
                "phash_modificado": str(phash_modificado),
                "distancia_hamming": distancia_hamming
            })

            print(f"  Crop {percentual}%")
            print(
                f"    SHA-256 igual: "
                f"{sha_original == sha_modificado}"
            )
            print(
                f"    Distância de Hamming: "
                f"{distancia_hamming}"
            )

        print()

    # Cria a pasta de resultados caso ainda não exista
    pasta_resultados.mkdir(
        parents=True,
        exist_ok=True
    )

    # Define o arquivo CSV do experimento de crop
    arquivo_crop = pasta_resultados / "crop.csv"

    # Salva todas as comparações realizadas no arquivo CSV
    with open(
        arquivo_crop,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        campos = [
            "imagem",
            "percentual",
            "sha256_igual",
            "phash_original",
            "phash_modificado",
            "distancia_hamming"
        ]

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        escritor.writeheader()
        escritor.writerows(resultados)

    print(
        f"Resultados de crop salvos em: "
        f"{arquivo_crop}"
    )