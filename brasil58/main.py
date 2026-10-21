import os
import random
import time
from datetime import datetime

from genetico import algoritmoGenetico
from leitura import lerDistancias

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_ARESTAS = os.path.join(PASTA, "data", "edgesbrasil58.tsp")
PASTA_SAIDA = os.path.join(PASTA, "data", "saida")
QTDE_CIDADES = 58
OTIMO_CONHECIDO = 25395
SEED = 42


def main():
    #le as arestas do arquivo e monta o dicionario de distancias
    distancias = lerDistancias(ARQUIVO_ARESTAS)
    #obs: com a mesma seed o resultado sai sempre igual
    random.seed(SEED)

    inicio = time.time()
    rota, custo = algoritmoGenetico(distancias, QTDE_CIDADES)
    tempo = time.time() - inicio
    #quanto (em %) ficou acima da melhor solucao conhecida
    acima = (custo - OTIMO_CONHECIDO) / OTIMO_CONHECIDO * 100

    linhas = [
        f"seed: {SEED}",
        f"OX + inversão | custo {custo} | ótimo {OTIMO_CONHECIDO} | {acima:.1f}% acima | {tempo:.1f} s",
        f"rota: {' '.join(str(cidade) for cidade in rota)}",
    ]
    print("\n".join(linhas))

    #salva o mesmo resultado num log, com a data e hora no nome
    nomeLog = "execucao_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"
    with open(os.path.join(PASTA_SAIDA, nomeLog), "w") as log:
        log.write("\n".join(linhas) + "\n")


if __name__ == "__main__":
    main()
