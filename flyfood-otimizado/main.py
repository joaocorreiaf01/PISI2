import os
import random
import signal
import sys
import time
from datetime import datetime

PASTA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PASTA, "src"))

from matriz.matriz import LETRAS, encontrar_origem, ler_matriz, sortear_pontos
from rota.rota import genetico

ARQUIVO_ENTRADA = os.path.join(PASTA, "data", "entrada", "matriz.txt")
SAIDA_SEM_OTIMIZACAO = os.path.join(PASTA, "..", "flyfood-sem-otimizacao", "data", "saida")


def ler_seed_sem_otimizacao():
    # Pega a seed do log mais recente do não otimizado
    logs = sorted(nome for nome in os.listdir(SAIDA_SEM_OTIMIZACAO) if nome.endswith(".log"))
    if not logs:
        return None, None

    with open(os.path.join(SAIDA_SEM_OTIMIZACAO, logs[-1])) as arquivo:
        for linha in arquivo:
            if linha.startswith("seed:"):
                return logs[-1], int(linha.split()[1])

    return None, None


def escrever(log, texto):
    # Escreve no terminal e no log
    try:
        print(texto, end="", flush=True)
    except OSError:
        pass
    log.write(texto)
    log.flush()


def main():
    signal.signal(signal.SIGHUP, signal.SIG_IGN)

    matriz = ler_matriz(ARQUIVO_ENTRADA)
    origem = encontrar_origem(matriz)

    # Usa a mesma seed do não otimizado para cada rodada sortear os mesmos pontos
    log_origem, seed = ler_seed_sem_otimizacao()
    if seed is None:
        seed = random.randint(0, 999999)
    # Gerador só para o sorteio: o DEAP também usa o random e mudaria os pontos das rodadas seguintes
    sorteio = random.Random(seed)
    random.seed(seed)

    nome_log = "execucao_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"
    log = open(os.path.join(PASTA, "data", "saida", nome_log), "w")

    escrever(log, f"seed: {seed}\n")
    if log_origem:
        escrever(log, f"mesmos pontos do não otimizado: {log_origem}\n")
    total_colisoes = 0
    quantidade = 2

    try:
        while quantidade <= len(LETRAS):
            pontos, colisoes = sortear_pontos(matriz, quantidade, sorteio)
            total_colisoes += colisoes
            escrever(log, f"{quantidade:>2} pontos... ")

            inicio = time.time()
            rota, custo = genetico(origem, pontos)
            tempo = time.time() - inicio

            escrever(log, f"R {' '.join(rota)} R | custo {custo} | {colisoes} colisões | {tempo:.3f} s\n")
            quantidade += 1

    except KeyboardInterrupt:
        escrever(log, "interrompido\n")

    escrever(log, f"total de colisões: {total_colisoes}\n")
    log.close()


if __name__ == "__main__":
    main()
