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


def ler_log_sem_otimizacao():
    # Pega a seed e o custo ótimo de cada rodada do log mais recente do não otimizado
    logs = sorted(nome for nome in os.listdir(SAIDA_SEM_OTIMIZACAO) if nome.endswith(".log"))
    if not logs:
        return None, None, {}

    nome_log = logs[-1]
    seed = None
    custos = {}
    with open(os.path.join(SAIDA_SEM_OTIMIZACAO, nome_log)) as arquivo:
        for linha in arquivo:
            if linha.startswith("seed:"):
                seed = int(linha.split()[1])
            elif "| custo " in linha:
                quantidade = int(linha.split()[0])
                custo = linha.split("| custo ")[1].split()[0]
                custos[quantidade] = int(custo)

    if seed is None:
        return None, None, {}
    return nome_log, seed, custos


def comparar(custo, otimo):
    if otimo is None:
        return "sem força bruta"
    if custo == otimo:
        return f"ótimo {otimo} (igual)"
    return f"ótimo {otimo} (+{custo - otimo})"


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
    log_origem, seed, custos_otimos = ler_log_sem_otimizacao()
    if seed is None:
        seed = random.randint(0, 999999)
    sorteio = random.Random(seed)
    random.seed(seed)

    nome_log = "execucao_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"
    with open(os.path.join(PASTA, "data", "saida", nome_log), "w") as log:
        escrever(log, f"seed: {seed}\n")
        if log_origem:
            escrever(log, f"mesmos pontos do não otimizado: {log_origem}\n")
        total_colisoes = 0

        try:
            for quantidade in range(2, len(LETRAS) + 1):
                pontos, colisoes = sortear_pontos(matriz, quantidade, sorteio)
                total_colisoes += colisoes
                escrever(log, f"{quantidade:>2} pontos... ")

                inicio = time.time()
                rota, custo = genetico(origem, pontos)
                tempo = time.time() - inicio

                comparacao = comparar(custo, custos_otimos.get(quantidade))
                escrever(log, f"R {' '.join(rota)} R | custo {custo} | {comparacao} | {colisoes} colisões | {tempo:.3f} s\n")

        except KeyboardInterrupt:
            escrever(log, "interrompido\n")

        escrever(log, f"total de colisões: {total_colisoes}\n")


if __name__ == "__main__":
    main()
