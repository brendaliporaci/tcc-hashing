from pathlib import Path
from PIL import Image

# Define o caminho da pasta que contém as imagens originais do dataset
PASTA_IMAGENS = Path(__file__).parent.parent / "dataset" / "img-original"

# Localiza todos os arquivos PNG do dataset e os ordena pelo nome
imagens = sorted(PASTA_IMAGENS.glob("*.png"))

print(f"Imagens encontradas: {len(imagens)}\n")

# Percorre as imagens para verificar se todas podem ser abertas corretamente
# e exibe suas dimensões e modo de cor
for caminho in imagens:
    with Image.open(caminho) as imagem:
        print(
            f"{caminho.name}: "
            f"{imagem.size[0]}x{imagem.size[1]} - "
            f"{imagem.mode}"
        )