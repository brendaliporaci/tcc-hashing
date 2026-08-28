import csv
from PIL import Image
from hashes import calcular_sha256, calcular_phash

def aplicar_rotacao(caminho_original, caminho_saida, angulo):
    """
    Gera uma nova versão da imagem aplicando uma rotação

    A imagem original não é modificada. O parâmetro angulo determina,
    em graus, a rotação aplicada à imagem
    """
    with Image.open(caminho_original) as imagem:
        imagem_rotacionada = imagem.rotate(
            angulo,
            expand=True
        )

        imagem_rotacionada.save(caminho_saida)
        
def executar_experimento_rotacao(
    imagens,
    pasta_rotacao,
    pasta_resultados,
    angulos
):
    """
    Executa o experimento de robustez do pHash à rotação

    Para cada imagem original, gera versões rotacionadas nos ângulos
    definidos, calcula os hashes e registra os resultados em CSV
    """

    # Armazena os resultados das comparações
    resultados = []

    # Percorre todas as imagens originais do dataset
    for imagem_original in imagens:

        # Calcula os hashes da imagem original.
        sha_original = calcular_sha256(imagem_original)
        phash_original = calcular_phash(imagem_original)

        print(f"Imagem: {imagem_original.name}")

        # Aplica cada ângulo de rotação definido para o experimento
        for angulo in angulos:

            # Cria uma pasta específica para cada ângulo
            pasta_saida = pasta_rotacao / str(angulo)
            pasta_saida.mkdir(parents=True, exist_ok=True)

            # Define o nome e o caminho da imagem modificada
            nome_saida = (
                f"{imagem_original.stem}_rotacao_{angulo}.png"
            )
            imagem_modificada = pasta_saida / nome_saida

            # Gera a versão rotacionada da imagem
            aplicar_rotacao(
                imagem_original,
                imagem_modificada,
                angulo
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
                "angulo": angulo,
                "sha256_igual": sha_original == sha_modificado,
                "phash_original": str(phash_original),
                "phash_modificado": str(phash_modificado),
                "distancia_hamming": distancia_hamming
            })

            print(f"  Rotação {angulo}°")
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

    # Define o arquivo CSV do experimento de rotação
    arquivo_rotacao = pasta_resultados / "rotacao.csv"

    # Salva todas as comparações realizadas no arquivo CSV
    with open(
        arquivo_rotacao,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        campos = [
            "imagem",
            "angulo",
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
        f"Resultados de rotação salvos em: "
        f"{arquivo_rotacao}"
    )