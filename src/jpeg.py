import csv
from PIL import Image
from hashes import calcular_sha256, calcular_phash

def aplicar_compressao_jpeg(caminho_original, caminho_saida, qualidade):
    """
    Gera uma nova versão da imagem utilizando compressão JPEG.

    A imagem original não é modificada. O parâmetro qualidade determina
    o nível de qualidade utilizado na compressão.
    """
    with Image.open(caminho_original) as imagem:
        imagem.save(
            caminho_saida,
            format="JPEG",
            quality=qualidade
        )

def executar_experimento_jpeg(
    imagens,
    pasta_jpeg,
    pasta_resultados,
    qualidades
):
    """
    Executa o experimento de robustez do pHash à compressão JPEG.

    Para cada imagem original, gera versões comprimidas nas qualidades
    definidas, calcula os hashes e registra os resultados em CSV.
    """

    # Armazena os resultados das comparações
    resultados = []

    # Percorre todas as imagens originais do dataset
    for imagem_original in imagens:

        # Calcula os hashes da imagem original.
        sha_original = calcular_sha256(imagem_original)
        phash_original = calcular_phash(imagem_original)

        print(f"Imagem: {imagem_original.name}")
        print(f"pHash original: {phash_original}")

        # Aplica cada nível de qualidade JPEG definido no experimento
        for qualidade in qualidades:

            # Cria uma pasta específica para cada nível de qualidade
            pasta_saida = pasta_jpeg / str(qualidade)
            pasta_saida.mkdir(parents=True, exist_ok=True)

            # Define o nome e o caminho da imagem modificada
            nome_saida = (
                f"{imagem_original.stem}_jpeg_{qualidade}.jpg"
            )
            imagem_modificada = pasta_saida / nome_saida

            # Gera a versão comprimida da imagem
            aplicar_compressao_jpeg(
                imagem_original,
                imagem_modificada,
                qualidade
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
                "qualidade": qualidade,
                "sha256_igual": sha_original == sha_modificado,
                "phash_original": str(phash_original),
                "phash_modificado": str(phash_modificado),
                "distancia_hamming": distancia_hamming
            })

            print(f"  JPEG {qualidade}")
            print(
                f"    SHA-256 igual: "
                f"{sha_original == sha_modificado}"
            )
            print(f"    pHash: {phash_modificado}")
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

    # Define o arquivo CSV do experimento JPEG
    arquivo_jpeg = pasta_resultados / "jpeg.csv"

    # Salva todas as comparações realizadas no arquivo CSV
    with open(
        arquivo_jpeg,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        campos = [
            "imagem",
            "qualidade",
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
        f"Resultados JPEG salvos em: "
        f"{arquivo_jpeg}"
    )