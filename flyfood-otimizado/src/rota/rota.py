import random
from itertools import permutations

from deap import algorithms, base, creator, tools

TAMANHO_POPULACAO = 500
NUM_GERACOES = 200
PROB_CROSSOVER = 0.8
PROB_MUTACAO = 0.2

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individuo", list, fitness=creator.FitnessMin)


def distancia(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def custo_da_rota(rota, origem, pontos):
    custo = 0
    atual = origem
    for letra in rota:
        custo += distancia(atual, pontos[letra])
        atual = pontos[letra]
    custo += distancia(atual, origem)
    return custo


def forca_bruta(origem, pontos):
    melhor_rota = None
    menor_custo = None

    for rota in permutations(pontos):
        custo = custo_da_rota(rota, origem, pontos)
        if menor_custo is None or custo < menor_custo:
            menor_custo = custo
            melhor_rota = rota

    return melhor_rota, menor_custo


def preparar_genetico(origem, pontos):
    letras = list(pontos)
    n = len(letras)

    def avaliar(individuo):
        rota = [letras[i] for i in individuo]
        return (custo_da_rota(rota, origem, pontos),)

    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(n), n)
    toolbox.register("individuo", tools.initIterate, creator.Individuo, toolbox.indices)
    toolbox.register("populacao", tools.initRepeat, list, toolbox.individuo)
    toolbox.register("evaluate", avaliar)
    toolbox.register("mate", tools.cxPartialyMatched)  # PMX
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1.0 / n)  # troca de posições
    toolbox.register("select", tools.selTournament, tournsize=3)

    return toolbox, letras


def genetico(origem, pontos):
    toolbox, letras = preparar_genetico(origem, pontos)
    populacao = toolbox.populacao(n=TAMANHO_POPULACAO)
    melhores = tools.HallOfFame(1)  # guarda o melhor indivíduo de todas as gerações

    algorithms.eaSimple(populacao, toolbox, cxpb=PROB_CROSSOVER, mutpb=PROB_MUTACAO,
                        ngen=NUM_GERACOES, halloffame=melhores, verbose=False)

    melhor = melhores[0]
    rota = tuple(letras[i] for i in melhor)
    return rota, int(melhor.fitness.values[0])
