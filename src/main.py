import time
from pathlib import Path

from jpeg import executar_experimento_jpeg
from rotacao import executar_experimento_rotacao
from crop import executar_experimento_crop
from espelhamento import executar_experimento_espelhamento
from redimensionamento import executar_experimento_redimensionamento


# Diretórios para definir os caminhos

# Raiz
PASTA_BASE = Path(__file__).parent.parent

# Imagens originais
PASTA_ORIGINAIS = PASTA_BASE / "dataset" / "img-original"

# Imagens modificadas
PASTA_MODIFICADAS = PASTA_BASE / "dataset" / "img-modificada"

# Resultados armazenados em tabelas csv
PASTA_RESULTADOS = PASTA_BASE / "resultados"


# Parâmetros utilizados no experimento de compressão JPEG
QUALIDADES_JPEG = [90, 65, 40]

# Parâmetros utilizados no experimento de rotação
ANGULOS_ROTACAO = [2, 5, 10]

# Parâmetros utilizados no experimento de recorte
PERCENTUAIS_CROP = [5, 10, 20]

# Parâmetros utilizados no experimento de redimensionamento
PERCENTUAIS_REDIMENSIONAMENTO = [80, 120]


def main():
    """
    Executa os experimentos de robustez utilizando as imagens
    do dataset piloto.
    """

    # Inicia a medição do tempo total de execução
    inicio = time.perf_counter()

    # Localiza e ordena as imagens originais
    imagens = sorted(PASTA_ORIGINAIS.glob("*.png"))

    print(f"Imagens encontradas: {len(imagens)}\n")

    # Executa o experimento de compressão JPEG
    executar_experimento_jpeg(
        imagens,
        PASTA_MODIFICADAS / "jpeg",
        PASTA_RESULTADOS,
        QUALIDADES_JPEG
    )

    # Executa o experimento de rotação
    executar_experimento_rotacao(
        imagens,
        PASTA_MODIFICADAS / "rotacao",
        PASTA_RESULTADOS,
        ANGULOS_ROTACAO
    )

    # Executa o experimento de recorte
    executar_experimento_crop(
        imagens,
        PASTA_MODIFICADAS / "crop",
        PASTA_RESULTADOS,
        PERCENTUAIS_CROP
    )

    # Executa o experimento de espelhamento
    executar_experimento_espelhamento(
        imagens,
        PASTA_MODIFICADAS / "espelhamento",
        PASTA_RESULTADOS
    )

    # Executa o experimento de redimensionamento
    executar_experimento_redimensionamento(
        imagens,
        PASTA_MODIFICADAS / "redimensionamento",
        PASTA_RESULTADOS,
        PERCENTUAIS_REDIMENSIONAMENTO
    )

    # Finaliza a medição e calcula o tempo total
    fim = time.perf_counter()
    tempo_execucao = fim - inicio

    print(f"\nTempo total de execução: {tempo_execucao:.2f} segundos")


# Garante que os experimentos sejam executados apenas quando
# este arquivo for executado diretamente
if __name__ == "__main__":
    main()