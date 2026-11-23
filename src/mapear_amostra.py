import csv
import filecmp
import random
from collections import Counter
from pathlib import Path

from preparar_dataset import (
    CSV_TRAIN,
    CSV_VAL,
    PASTA_DESTINO,
    PASTA_FAIRFACE,
    QUANTIDADE,
    SEED,
    carregar_adultos,
)

PASTA_RESULTADOS = Path(__file__).resolve().parent.parent / "resultados" / "fairface"


def carregar_metadados():
    metadados = {}

    for caminho_csv in (CSV_TRAIN, CSV_VAL):
        with open(caminho_csv, newline="", encoding="utf-8-sig") as arquivo:
            for linha in csv.DictReader(arquivo):
                metadados[linha["file"]] = linha

    return metadados


def main():
    # Reproduz a selecao original sem copiar ou modificar imagens.
    disponiveis = carregar_adultos(CSV_TRAIN) + carregar_adultos(CSV_VAL)
    selecionadas = random.Random(SEED).sample(disponiveis, QUANTIDADE)
    metadados = carregar_metadados()
    registros = []

    for numero, caminho_relativo in enumerate(selecionadas, start=1):
        origem = PASTA_FAIRFACE / caminho_relativo
        destino = PASTA_DESTINO / f"{numero:04d}.jpg"

        if not origem.is_file() or not destino.is_file():
            raise FileNotFoundError(f"Imagem ausente: {origem} ou {destino}")

        # Confere o conteudo para evitar associar metadados incorretos.
        if not filecmp.cmp(origem, destino, shallow=False):
            raise ValueError(
                f"A imagem {destino.name} nao corresponde a {caminho_relativo}. "
                "Nenhum resultado foi salvo."
            )

        dados = metadados[caminho_relativo]
        registros.append({
            "imagem_amostra": destino.name,
            "arquivo_fairface": caminho_relativo,
            "conjunto": Path(caminho_relativo).parts[0],
            "age": dados["age"],
            "gender": dados["gender"],
            "race": dados["race"],
            "service_test": dados["service_test"],
        })

    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    caminho_amostra = PASTA_RESULTADOS / "amostra_demografica.csv"
    with open(caminho_amostra, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(registros[0]))
        escritor.writeheader()
        escritor.writerows(registros)

    contagem = Counter((r["gender"], r["race"]) for r in registros)
    caminho_resumo = PASTA_RESULTADOS / "resumo_grupos_demograficos.csv"
    with open(caminho_resumo, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["gender", "race", "quantidade_imagens", "pares_possiveis"])
        for (genero, raca), quantidade in sorted(contagem.items()):
            escritor.writerow([genero, raca, quantidade, quantidade * (quantidade - 1) // 2])

    origens = Counter(r["conjunto"] for r in registros)
    print(f"Imagens verificadas: {len(registros)}")
    print(f"Origem: train={origens['train']}, val={origens['val']}")
    print("\nDistribuicao por grupo:")
    for (genero, raca), quantidade in sorted(contagem.items()):
        print(f"  {genero} / {raca}: {quantidade}")
    print(f"\nMetadados: {caminho_amostra}")
    print(f"Resumo: {caminho_resumo}")


if __name__ == "__main__":
    main()
