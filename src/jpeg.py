from PIL import Image

def aplicar_compressao_jpeg(caminho_original, caminho_saida, qualidade):
    """
    Gera uma nova versão da imagem utilizando compressão JPEG.

    A imagem original não é modificada. O parâmetro qualidade determina
    o nível de qualidade utilizado na compressão da imagem.
    """
    with Image.open(caminho_original) as imagem:
        imagem.save(
            caminho_saida,
            format="JPEG",
            quality=qualidade
        )