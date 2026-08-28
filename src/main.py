from pathlib import Path
from PIL import Image
from jpeg import aplicar_compressao_jpeg
from rotacao import aplicar_rotacao

import hashlib
import imagehash
import csv


# Define os caminhos das imagens no experimento
PASTA_ORIGINAIS = (
    Path(__file__).parent.parent / "dataset" / "img-original"
)

PASTA_MODIFICADAS = (
    Path(__file__).parent.parent / "dataset" / "img-modificada" / "jpeg"
)

QUALIDADES_JPEG = [90, 65, 40]

PASTA_ROTACAO = (
    Path(__file__).parent.parent
    / "dataset"
    / "img-modificada"
    / "rotacao"
)

ANGULOS_ROTACAO = [2, 5, 10]

# Cria a pasta de saída caso ela ainda não exista
PASTA_MODIFICADAS.mkdir(parents=True, exist_ok=True)

# Localiza todos os arquivos PNG do dataset e os ordena pelo nome
imagens = sorted(PASTA_ORIGINAIS.glob("*.png"))

print(f"Imagens encontradas: {len(imagens)}\n")


def calcular_sha256(caminho):
    """
    Calcula o hash criptográfico SHA-256 de um arquivo.

    O cálculo utiliza os bytes do arquivo, portanto qualquer alteração
    no arquivo pode resultar em um hash completamente diferente.
    """
    sha256 = hashlib.sha256()

    with open(caminho, "rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(4096), b""):
            sha256.update(bloco)

    return sha256.hexdigest()


def calcular_phash(caminho):
    """
    Calcula o hash perceptual pHash de uma imagem.

    Diferentemente do SHA-256, o pHash representa características
    perceptuais da imagem e permite posteriormente medir a similaridade
    entre a imagem original e suas versões modificadas.
    """
    with Image.open(caminho) as imagem:
        return imagehash.phash(imagem)


# Calcula os hashes de todas as imagens originais do dataset piloto
#for caminho in imagens:
#    sha256 = calcular_sha256(caminho)
#    phash = calcular_phash(caminho)
#
#    print(f"{caminho.name}")
#    print(f"  SHA-256: {sha256}")
#    print(f"  pHash:   {phash}")
#    print()

# Localiza todas as imagens originais do dataset piloto
imagens = sorted(PASTA_ORIGINAIS.glob("*.png"))

print(f"Imagens encontradas: {len(imagens)}\n")

# Armazena os resultados das comparações realizadas
resultados = []

# Percorre todas as imagens originais
for imagem_original in imagens:

    # Calcula os hashes da imagem original
    sha_original = calcular_sha256(imagem_original)
    phash_original = calcular_phash(imagem_original)

    print(f"Imagem: {imagem_original.name}")
    print(f"pHash original: {phash_original}")

    # Aplica cada nível de compressão JPEG
    for qualidade in QUALIDADES_JPEG:

        pasta_saida = PASTA_MODIFICADAS / str(qualidade)
        pasta_saida.mkdir(parents=True, exist_ok=True)

        # Mantém o nome da imagem original na versão modificada
        nome_saida = f"{imagem_original.stem}_jpeg_{qualidade}.jpg"
        imagem_modificada = pasta_saida / nome_saida

        aplicar_compressao_jpeg(
            imagem_original,
            imagem_modificada,
            qualidade
        )

        # Calcula os hashes da imagem modificada
        sha_modificado = calcular_sha256(imagem_modificada)
        phash_modificado = calcular_phash(imagem_modificada)

        # Calcula a distância de Hamming entre os pHashes
        distancia_hamming = phash_original - phash_modificado
        
        #Adiciona a lista de resultados para a tabela jpeg.py
        resultados.append({
            "imagem": imagem_original.name,
            "qualidade": qualidade,
            "sha256_igual": sha_original == sha_modificado,
            "phash_original": str(phash_original),
            "phash_modificado": str(phash_modificado),
            "distancia_hamming": distancia_hamming
        })

        print(f"  JPEG {qualidade}")
        print(f"    SHA-256 igual: {sha_original == sha_modificado}")
        print(f"    pHash: {phash_modificado}")
        print(f"    Distância de Hamming: {distancia_hamming}")

    print()
    
# Define a pasta onde serão armazenados os resultados
PASTA_RESULTADOS = (
    Path(__file__).parent.parent / "resultados"
)

PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)

arquivo_resultados = PASTA_RESULTADOS / "jpeg.csv"

# Salva os resultados do experimento em CSV
with open(arquivo_resultados, "w", newline="", encoding="utf-8") as arquivo:
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

print(f"\nResultados salvos em: {arquivo_resultados}")

# Lista que armazenará os resultados da rotação
resultados_rotacao = []

for imagem_original in imagens:

    sha_original = calcular_sha256(imagem_original)
    phash_original = calcular_phash(imagem_original)

    print(f"Imagem: {imagem_original.name}")

    for angulo in ANGULOS_ROTACAO:

        pasta_saida = PASTA_ROTACAO / str(angulo)
        pasta_saida.mkdir(parents=True, exist_ok=True)

        nome_saida = f"{imagem_original.stem}_rotacao_{angulo}.png"
        imagem_modificada = pasta_saida / nome_saida

        # Gera a imagem rotacionada
        aplicar_rotacao(
            imagem_original,
            imagem_modificada,
            angulo
        )

        # Calcula os hashes
        sha_modificado = calcular_sha256(imagem_modificada)
        phash_modificado = calcular_phash(imagem_modificada)

        distancia_hamming = phash_original - phash_modificado

        # Armazena o resultado
        resultados_rotacao.append({
            "imagem": imagem_original.name,
            "angulo": angulo,
            "sha256_igual": sha_original == sha_modificado,
            "phash_original": str(phash_original),
            "phash_modificado": str(phash_modificado),
            "distancia_hamming": distancia_hamming
        })

        print(f"  Rotação {angulo}°")
        print(f"    SHA-256 igual: {sha_original == sha_modificado}")
        print(f"    Distância de Hamming: {distancia_hamming}")

    print()
arquivo_rotacao = PASTA_RESULTADOS / "rotacao.csv"

with open(arquivo_rotacao, "w", newline="", encoding="utf-8") as arquivo:
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
    escritor.writerows(resultados_rotacao)

print(f"Resultados de rotação salvos em: {arquivo_rotacao}")