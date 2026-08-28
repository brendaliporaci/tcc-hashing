from pathlib import Path
from PIL import Image
import hashlib
import imagehash


# Define o caminho da pasta que contém as imagens originais do dataset
PASTA_IMAGENS = Path(__file__).parent.parent / "dataset" / "img-original"

# Localiza todos os arquivos PNG do dataset e os ordena pelo nome
imagens = sorted(PASTA_IMAGENS.glob("*.png"))

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
for caminho in imagens:
    sha256 = calcular_sha256(caminho)
    phash = calcular_phash(caminho)

    print(f"{caminho.name}")
    print(f"  SHA-256: {sha256}")
    print(f"  pHash:   {phash}")
    print()