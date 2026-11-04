from deap import algorithms, base, creator, tools

from lerBrasil58 import custoCaminho, inicializaPopulacao
from operadores import cruzamentoOX, mutacaoCom2opt

#objetivo é minimizar o custo, por isso o peso -1
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individuo", list, fitness=creator.FitnessMin)


def algoritmoGenetico(dicDistancias, qtdeCidades, tamanhoPopulacao=200, geracoes=20,
                      probCruzamento=0.3, probMutacao=0.7):
    toolbox = base.Toolbox()
    toolbox.register("evaluate", lambda individuo: (custoCaminho(individuo, dicDistancias),))
    toolbox.register("mate", cruzamentoOX)
    #a py2opt usa matriz de distancias, entao monta ela a partir do dicionario
    matrizDistancias = [[0] * qtdeCidades for _ in range(qtdeCidades)]
    for (i, j), peso in dicDistancias.items():
        matrizDistancias[i - 1][j - 1] = peso
    toolbox.register("mutate", mutacaoCom2opt, matrizDistancias=matrizDistancias)
    toolbox.register("select", tools.selTournament, tournsize=3)

    populacao = [creator.Individuo(rota) for rota in inicializaPopulacao(tamanhoPopulacao, qtdeCidades)]
    melhor = tools.HallOfFame(1)
    #laco do AG junta pais e filhos e escolhe os sobreviventes pelo torneio
    algorithms.eaMuPlusLambda(populacao, toolbox, mu=tamanhoPopulacao, lambda_=tamanhoPopulacao,
                              cxpb=probCruzamento, mutpb=probMutacao, ngen=geracoes,
                              halloffame=melhor, verbose=False)

    return list(melhor[0]), int(melhor[0].fitness.values[0])
