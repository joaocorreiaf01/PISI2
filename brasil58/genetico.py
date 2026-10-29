from deap import algorithms, base, creator, tools

from lerBrasil58 import custoCaminho, inicializaPopulacao
from operadores import cruzamentoOX, mutacao

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individuo", list, fitness=creator.FitnessMin)


def algoritmoGenetico(dicDistancias, qtdeCidades, tamanhoPopulacao=200, geracoes=1000,
                      probCruzamento=0.3, probMutacao=0.7):
    toolbox = base.Toolbox()
    toolbox.register("evaluate", lambda individuo: (custoCaminho(individuo, dicDistancias),))
    toolbox.register("mate", cruzamentoOX)
    toolbox.register("mutate", mutacao)
    toolbox.register("select", tools.selTournament, tournsize=3)

    populacao = [creator.Individuo(rota) for rota in inicializaPopulacao(tamanhoPopulacao, qtdeCidades)]
    melhor = tools.HallOfFame(1)
    algorithms.eaMuPlusLambda(populacao, toolbox, mu=tamanhoPopulacao, lambda_=tamanhoPopulacao,
                              cxpb=probCruzamento, mutpb=probMutacao, ngen=geracoes,
                              halloffame=melhor, verbose=False)

    return list(melhor[0]), int(melhor[0].fitness.values[0])
