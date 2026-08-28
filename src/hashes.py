import hashlib

import imagehash
from PIL import Image


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

    O pHash representa características perceptuais da imagem e permite
    medir a similaridade entre uma imagem e suas versões modificadas.
    """
    with Image.open(caminho) as imagem:
        return imagehash.phash(imagem)