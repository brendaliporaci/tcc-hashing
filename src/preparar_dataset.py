import csv
import random
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

PASTA_FAIRFACE = BASE / "dataset" / "fairface"
PASTA_DESTINO = BASE / "dataset" / "img-original"

CSV_TRAIN = PASTA_FAIRFACE / "fairface_label_train.csv"
CSV_VAL = PASTA_FAIRFACE / "fairface_label_val.csv"

IDADES_ADULTAS = {
    "20-29",
    "30-39",
    "40-49",
    "50-59",
    "60-69",
    "more than 70",
}

QUANTIDADE = 1000
SEED = 42


def carregar_adultos(caminho_csv):
    imagens = []

    with open(caminho_csv, newline="", encoding="utf-8-sig") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            if linha["age"] in IDADES_ADULTAS:
                imagens.append(linha["file"])

    return imagens


def selecionar_imagens():
    imagens = carregar_adultos(CSV_TRAIN)
    imagens += carregar_adultos(CSV_VAL)

    print(f"Imagens adultas disponíveis: {len(imagens)}")

    random.seed(SEED)
    selecionadas = random.sample(imagens, QUANTIDADE)

    PASTA_DESTINO.mkdir(parents=True, exist_ok=True)

    for numero, caminho_relativo in enumerate(selecionadas, start=1):
        origem = PASTA_FAIRFACE / caminho_relativo
        destino = PASTA_DESTINO / f"{numero:04d}.jpg"

        shutil.copy2(origem, destino)

    print(f"Imagens selecionadas: {len(selecionadas)}")
    print(f"Salvas em: {PASTA_DESTINO}")


if __name__ == "__main__":
    selecionar_imagens()