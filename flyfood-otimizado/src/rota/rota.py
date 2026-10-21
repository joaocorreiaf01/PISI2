import random

from deap import algorithms, base, creator, tools

TAMANHO_POPULACAO = 500
NUM_GERACOES = 200
PROB_CROSSOVER = 0.8
PROB_MUTACAO = 0.2

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individuo", list, fitness=creator.FitnessMin)


def distancia(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def custo_da_rota(rota, origem):
    custo = 0
    atual = origem
    for posicao in rota:
        custo += distancia(atual, posicao)
        atual = posicao
    custo += distancia(atual, origem)
    return custo


def genetico(origem, pontos):
    letras = list(pontos)
    posicoes = list(pontos.values())
    n = len(letras)

    def nova_rota():
        return random.sample(range(n), n)

    def avaliar(individuo):
        rota = [posicoes[i] for i in individuo]
        return (custo_da_rota(rota, origem),)

    toolbox = base.Toolbox()
    toolbox.register("individuo", tools.initIterate, creator.Individuo, nova_rota)
    toolbox.register("evaluate", avaliar)
    toolbox.register("mate", tools.cxPartialyMatched)  # PMX
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1.0 / n)  # troca de posições
    toolbox.register("select", tools.selTournament, tournsize=3)

    populacao = [toolbox.individuo() for _ in range(TAMANHO_POPULACAO)]
    melhor = tools.HallOfFame(1)  # guarda o melhor indivíduo de todas as gerações
    algorithms.eaSimple(populacao, toolbox, cxpb=PROB_CROSSOVER, mutpb=PROB_MUTACAO,
                        ngen=NUM_GERACOES, halloffame=melhor, verbose=False)

    melhor_rota = [letras[i] for i in melhor[0]]
    melhor_custo = int(melhor[0].fitness.values[0])
    return melhor_rota, melhor_custo
