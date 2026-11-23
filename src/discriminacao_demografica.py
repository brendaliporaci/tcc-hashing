import csv
from bisect import bisect_right
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

from thresholds import THRESHOLDS

BASE = Path(__file__).resolve().parent.parent
PASTA_RESULTADOS = BASE / "resultados" / "fairface"
CSV_AMOSTRA = PASTA_RESULTADOS / "amostra_demografica.csv"
CSV_DISCRIMINACAO = PASTA_RESULTADOS / "discriminacao.csv"


def carregar_amostra():
    # Associa cada imagem renomeada aos grupos do FairFace.
    imagens = {}
    grupos = Counter()

    with open(CSV_AMOSTRA, newline="", encoding="utf-8-sig") as arquivo:
        for linha in csv.DictReader(arquivo):
            nome = linha["imagem_amostra"]
            grupo = (linha["gender"], linha["race"])

            if nome in imagens:
                raise ValueError(f"Imagem repetida no mapeamento: {nome}")

            imagens[nome] = grupo
            grupos[grupo] += 1

    if not imagens:
        raise ValueError("O CSV de mapeamento esta vazio.")

    return imagens, grupos


def carregar_pares_intragrupo(imagens, grupos):
    # Reaproveita as distancias ja calculadas no experimento original.
    pares = defaultdict(list)
    pares_vistos = set()
    total = 0

    with open(CSV_DISCRIMINACAO, newline="", encoding="utf-8-sig") as arquivo:
        leitor = csv.DictReader(arquivo)
        colunas = {"imagem_a", "imagem_b", "distancia_hamming"}
        if not colunas.issubset(leitor.fieldnames or []):
            raise ValueError("O CSV de discriminacao nao possui as colunas esperadas.")

        for linha in leitor:
            a = linha["imagem_a"]
            b = linha["imagem_b"]

            if a not in imagens or b not in imagens:
                raise ValueError(f"Imagem sem metadados: {a} ou {b}")
            if a == b:
                raise ValueError(f"Comparacao de uma imagem consigo mesma: {a}")

            chave = tuple(sorted((a, b)))
            if chave in pares_vistos:
                raise ValueError(f"Par repetido: {a} e {b}")
            pares_vistos.add(chave)
            total += 1

            distancia = int(linha["distancia_hamming"])
            if distancia < 0:
                raise ValueError(f"Distancia invalida no par: {a} e {b}")

            if imagens[a] == imagens[b]:
                pares[imagens[a]].append((a, b, distancia))

    esperado_total = len(imagens) * (len(imagens) - 1) // 2
    if total != esperado_total:
        raise ValueError(
            f"Esperadas {esperado_total} comparacoes, mas encontradas {total}."
        )

    for grupo, quantidade in grupos.items():
        esperado = quantidade * (quantidade - 1) // 2
        encontrado = len(pares[grupo])
        if encontrado != esperado:
            raise ValueError(
                f"Grupo {grupo}: esperados {esperado} pares, encontrados {encontrado}."
            )

    return pares, total


def salvar_resultados(grupos, pares):
    arquivo_pares = PASTA_RESULTADOS / "pares_intragrupo.csv"
    arquivo_resumo = PASTA_RESULTADOS / "discriminacao_demografica.csv"
    arquivo_distribuicao = PASTA_RESULTADOS / "distancias_demograficas.csv"

    with open(arquivo_pares, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["gender", "race", "imagem_a", "imagem_b", "distancia_hamming"])
        for (genero, raca), registros in sorted(pares.items()):
            for a, b, distancia in sorted(registros, key=lambda item: item[2]):
                escritor.writerow([genero, raca, a, b, distancia])

    with open(arquivo_resumo, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow([
            "gender", "race", "quantidade_imagens", "quantidade_pares",
            "threshold", "falsos_positivos", "verdadeiros_negativos",
            "fpr_percentual", "distancia_minima", "distancia_media",
            "distancia_mediana", "distancia_maxima"
        ])

        for (genero, raca), quantidade in sorted(grupos.items()):
            distancias = sorted(item[2] for item in pares[(genero, raca)])
            total_pares = len(distancias)

            for threshold in THRESHOLDS:
                fp = bisect_right(distancias, threshold)
                tn = total_pares - fp
                fpr = 100 * fp / total_pares if total_pares else 0.0

                escritor.writerow([
                    genero, raca, quantidade, total_pares, threshold, fp, tn,
                    round(fpr, 4),
                    min(distancias) if distancias else "",
                    round(mean(distancias), 4) if distancias else "",
                    median(distancias) if distancias else "",
                    max(distancias) if distancias else ""
                ])

    with open(arquivo_distribuicao, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["gender", "race", "distancia_hamming", "quantidade_pares"])
        for (genero, raca), registros in sorted(pares.items()):
            frequencias = Counter(item[2] for item in registros)
            for distancia, quantidade in sorted(frequencias.items()):
                escritor.writerow([genero, raca, distancia, quantidade])

    return arquivo_pares, arquivo_resumo, arquivo_distribuicao


def main():
    for caminho in (CSV_AMOSTRA, CSV_DISCRIMINACAO):
        if not caminho.is_file():
            raise FileNotFoundError(f"Arquivo nao encontrado: {caminho}")

    imagens, grupos = carregar_amostra()
    pares, total = carregar_pares_intragrupo(imagens, grupos)
    arquivos = salvar_resultados(grupos, pares)

    print(f"Imagens analisadas: {len(imagens)}")
    print(f"Comparacoes originais verificadas: {total}")
    print(f"Comparacoes dentro dos grupos: {sum(map(len, pares.values()))}")
    print(f"Grupos demograficos: {len(grupos)}")
    print("\nFalsos positivos por grupo (threshold = 5):")

    for (genero, raca), registros in sorted(pares.items()):
        total_grupo = len(registros)
        fp = sum(distancia <= 5 for _, _, distancia in registros)
        fpr = 100 * fp / total_grupo if total_grupo else 0
        print(f"  {genero} / {raca}: {fp}/{total_grupo} ({fpr:.4f}%)")

    print("\nArquivos gerados:")
    for arquivo in arquivos:
        print(f"  {arquivo}")


if __name__ == "__main__":
    main()
