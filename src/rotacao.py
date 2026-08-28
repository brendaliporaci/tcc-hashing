from PIL import Image

def aplicar_rotacao(caminho_original, caminho_saida, angulo):
    """
    Gera uma nova versão da imagem aplicando uma rotação.

    A imagem original não é modificada. O parâmetro angulo determina,
    em graus, a rotação aplicada à imagem.
    """
    with Image.open(caminho_original) as imagem:
        imagem_rotacionada = imagem.rotate(
            angulo,
            expand=True #Usado para evitar que parte da imagem seja cortada ao rotacionar
        )

        imagem_rotacionada.save(caminho_saida)