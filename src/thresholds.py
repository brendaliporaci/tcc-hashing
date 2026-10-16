import csv
from pathlib import Path

# Define o diretório raiz do projeto
PASTA_BASE = Path(__file__).parent.parent
PASTA_RESULTADOS = PASTA_BASE / "resultados"

# Limiares de distância de Hamming avaliados
THRESHOLDS = [5, 10, 15, 20, 25, 30]

def carregar_distancias_por_parametro(
    nome_arquivo,
    coluna_parametro
):
    """
    Lê um CSV de robustez e agrupa as distâncias
    pelo parâmetro da transformação.
    """

    caminho_arquivo = PASTA_RESULTADOS / nome_arquivo
    distancias = {}

    with open(
        caminho_arquivo,
        "r",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            parametro = int(linha[coluna_parametro])
            distancia = int(linha["distancia_hamming"])

            if parametro not in distancias:
                distancias[parametro] = []

            distancias[parametro].append(distancia)

    return distancias

def carregar_distancias_discriminacao():
    """
    Lê as distâncias entre imagens originais diferentes.
    """

    caminho_arquivo = (
        PASTA_RESULTADOS / "discriminacao.csv"
    )

    distancias = []

    with open(
        caminho_arquivo,
        "r",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            distancias.append(
                int(linha["distancia_hamming"])
            )

    return distancias

def calcular_reconhecimento(distancias, threshold):
    """
    Calcula quantas imagens modificadas foram reconhecidas
    como correspondentes às imagens originais.
    """

    reconhecidas = sum(
        distancia <= threshold
        for distancia in distancias
    )

    percentual = (
        reconhecidas / len(distancias)
    ) * 100

    return reconhecidas, percentual

def calcular_classificacao(
    distancias_positivas,
    distancias_negativas,
    threshold
):
    """
    Calcula TP, FN, FP e TN para um determinado threshold.
    """

    tp = sum(
        distancia <= threshold
        for distancia in distancias_positivas
    )

    fn = sum(
        distancia > threshold
        for distancia in distancias_positivas
    )

    fp = sum(
        distancia <= threshold
        for distancia in distancias_negativas
    )

    tn = sum(
        distancia > threshold
        for distancia in distancias_negativas
    )

    return tp, fn, fp, tn

# Cálculo de recall
def calcular_recall(tp, fn):
    """
    Calcula a proporção de casos positivos que foram
    corretamente reconhecidos.
    """
    total = tp + fn
    return tp / total if total > 0 else 0.0


# Cálculo de precisão
def calcular_precisao(tp, fp):
    """
    Calcula a proporção de correspondências identificadas
    que realmente pertencem aos casos positivos.
    """
    total = tp + fp
    return tp / total if total > 0 else 0.0


# Cálculo da taxa de falsos positivos
def calcular_fpr(fp, tn):
    """
    Calcula a proporção de casos negativos que foram
    incorretamente classificados como correspondências.
    """
    total = fp + tn
    return fp / total if total > 0 else 0.0

def exibir_transformacao(
    nome,
    grupos,
    threshold,
    unidade=""
):
    """
    Exibe a taxa de reconhecimento de cada intensidade
    de uma transformação.
    """

    print(f"  {nome}")

    for parametro in sorted(grupos):

        distancias = grupos[parametro]

        reconhecidas, percentual = calcular_reconhecimento(
            distancias,
            threshold
        )

        print(
            f"    {parametro}{unidade}: "
            f"{reconhecidas}/{len(distancias)} "
            f"({percentual:.2f}%)"
        )

def carregar_distancias_espelhamento():
    caminho_arquivo = PASTA_RESULTADOS / "espelhamento.csv"
    distancias = []

    with open(
        caminho_arquivo,
        "r",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            distancias.append(
                int(linha["distancia_hamming"])
            )

    return distancias

def main():

    # Carrega os resultados de robustez separados
    # pelos parâmetros de cada transformação
    jpeg = carregar_distancias_por_parametro(
        "jpeg.csv",
        "qualidade"
    )

    rotacao = carregar_distancias_por_parametro(
        "rotacao.csv",
        "angulo"
    )

    crop = carregar_distancias_por_parametro(
        "crop.csv",
        "percentual"
    )

    redimensionamento = carregar_distancias_por_parametro(
        "redimensionamento.csv",
        "percentual"
    )

    # Carrega a distância de discriminação
    discriminacao = carregar_distancias_discriminacao()
    
    # Carrega a distância de espelhamento
    espelhamento = carregar_distancias_espelhamento()

    # Junta todas as distâncias das versões modificadas.
    # Elas representam os casos positivos do experimento.
    distancias_positivas = []
    
    resultados_thresholds = []

    for grupos in [jpeg, rotacao, crop, redimensionamento]:
        for distancias in grupos.values():
            distancias_positivas.extend(distancias)

    distancias_positivas.extend(espelhamento)

    print("\nAnálise de thresholds\n")

    for threshold in THRESHOLDS:

        print(f"Threshold: {threshold}")

        exibir_transformacao(
            "JPEG",
            jpeg,
            threshold
        )

        exibir_transformacao(
            "Rotação",
            rotacao,
            threshold,
            "°"
        )

        exibir_transformacao(
            "Crop",
            crop,
            threshold,
            "%"
        )
        
        exibir_transformacao(
            "Redimensionamento",
            redimensionamento,
            threshold,
            "%"
        )
        
        reconhecidas, percentual = calcular_reconhecimento(
            espelhamento,
            threshold
        )

        print("  Espelhamento")
        print(
            f"    {reconhecidas}/{len(espelhamento)} "
            f"({percentual:.2f}%)"
        )

        # Em imagens diferentes, uma distância menor ou igual
        # ao threshold representa um falso positivo
        falsos_positivos = sum(
            distancia <= threshold
            for distancia in discriminacao
        )

        percentual_falsos = (
            falsos_positivos / len(discriminacao)
        ) * 100

        print("  Discriminação")
        print(
            f"    Falsos positivos: "
            f"{falsos_positivos}/{len(discriminacao)} "
            f"({percentual_falsos:.2f}%)"
        )

        # Calcula TP, FN, FP e TN para o threshold atual.
        tp, fn, fp, tn = calcular_classificacao(
            distancias_positivas,
            discriminacao,
            threshold
        )
        
        # Calcula as métricas de avaliação para o threshold atual
        recall = calcular_recall(tp, fn)
        precisao = calcular_precisao(tp, fp)
        fpr = calcular_fpr(fp, tn)
        
        # Armazena as métricas calculadas para o threshold atual
        resultados_thresholds.append([
            threshold,
            tp,
            fn,
            fp,
            tn,
            recall * 100,
            precisao * 100,
            fpr * 100
        ])

        print("  Classificação")
        print(f"    TP: {tp}")
        print(f"    FN: {fn}")
        print(f"    FP: {fp}")
        print(f"    TN: {tn}")
        print(f"    Recall: {recall * 100:.2f}%")
        print(f"    Precisão: {precisao * 100:.2f}%")
        print(f"    FPR: {fpr * 100:.2f}%")
        print()
        
    # Salva o resumo da análise dos thresholds em CSV
    arquivo_saida = PASTA_RESULTADOS / "thresholds.csv"

    with open(
        arquivo_saida,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        escritor = csv.writer(arquivo)

        escritor.writerow([
            "threshold",
            "tp",
            "fn",
            "fp",
            "tn",
            "recall",
            "precisao",
            "fpr"
        ])

        escritor.writerows(resultados_thresholds)

    print(f"Resultados dos thresholds salvos em: {arquivo_saida}")


if __name__ == "__main__":
    main()