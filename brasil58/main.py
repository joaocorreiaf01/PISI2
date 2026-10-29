import os
import random
import time
from datetime import datetime

from genetico import algoritmoGenetico
from lerBrasil58 import distancias

PASTA = os.path.dirname(os.path.abspath(__file__))
PASTA_SAIDA = os.path.join(PASTA, "data", "saida")
QTDE_CIDADES = 58
OTIMO_CONHECIDO = 25395
SEED = 42


def main():
    random.seed(SEED)

    inicio = time.time()
    rota, custo = algoritmoGenetico(distancias, QTDE_CIDADES)
    tempo = time.time() - inicio
    #quantos % ficou acima da melhor solucao conhecida
    acima = (custo - OTIMO_CONHECIDO) / OTIMO_CONHECIDO * 100

    linhas = [
        f"seed: {SEED}",
        f"OX + inversão + inserção | custo {custo} | ótimo {OTIMO_CONHECIDO} | {acima:.1f}% acima | {tempo:.1f} s",
        f"rota: {' '.join(str(cidade) for cidade in rota)}",
    ]
    print("\n".join(linhas))

    #salva o mesmo resultado num log
    nomeLog = "execucao_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"
    with open(os.path.join(PASTA_SAIDA, nomeLog), "w") as log:
        log.write("\n".join(linhas) + "\n")


if __name__ == "__main__":
    main()
