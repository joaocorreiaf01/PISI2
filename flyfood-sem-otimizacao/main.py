import os
import random
import signal
import sys
import time
from datetime import datetime

PASTA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PASTA, "src"))

from matriz.matriz import LETRAS, encontrar_origem, ler_matriz, sortear_pontos
from rota.rota import forca_bruta

ARQUIVO_ENTRADA = os.path.join(PASTA, "data", "entrada", "matriz.txt")


def escrever(log, texto):
    # Escreve no terminal e no log ao mesmo tempo, para acompanhar o andamento
    try:
        print(texto, end="", flush=True)
    except OSError:
        # Terminal já foi fechado: segue gravando só no log
        pass
    log.write(texto)
    log.flush()


def main():
    # Fechar o terminal não para o programa; só o Ctrl+C interrompe
    signal.signal(signal.SIGHUP, signal.SIG_IGN)

    matriz = ler_matriz(ARQUIVO_ENTRADA)
    origem = encontrar_origem(matriz)

    seed = random.randint(0, 999999)
    random.seed(seed)

    nome_log = "execucao_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"
    log = open(os.path.join(PASTA, "data", "saida", nome_log), "w")

    escrever(log, f"seed: {seed}\n")
    total_colisoes = 0
    quantidade = 2

    try:
        while quantidade <= len(LETRAS):
            pontos, colisoes = sortear_pontos(matriz, quantidade)
            total_colisoes += colisoes
            escrever(log, f"{quantidade:>2} pontos... ")

            inicio = time.time()
            rota, custo = forca_bruta(origem, pontos)
            tempo = time.time() - inicio

            escrever(log, f"{' '.join(rota)} | custo {custo} | {colisoes} colisões | {tempo:.3f} s\n")
            quantidade += 1

    except KeyboardInterrupt:
        escrever(log, "interrompido\n")

    escrever(log, f"total de colisões: {total_colisoes}\n")
    log.close()


if __name__ == "__main__":
    main()
