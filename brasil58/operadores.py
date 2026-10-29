import random

from deap import tools


def cruzamentoOX(pai1, pai2):
    #order crossover: o filho pega um trecho do pai1 na mesma posicao
    #e o resto vem do pai2, na ordem que as cidades aparecem nele
    filho1 = [cidade - 1 for cidade in pai1]
    filho2 = [cidade - 1 for cidade in pai2]
    tools.cxOrdered(filho1, filho2)
    pai1[:] = [cidade + 1 for cidade in filho1]
    pai2[:] = [cidade + 1 for cidade in filho2]
    return pai1, pai2


def mutacaoInversao(individuo):
    #escolhe um trecho da rota e inverte a ordem dele
    i, j = sorted(random.sample(range(len(individuo)), 2))
    individuo[i:j + 1] = individuo[i:j + 1][::-1]
    return individuo,


def mutacaoInsercao(individuo):
    #tira uma cidade da rota e coloca ela em outra posicao
    i, j = random.sample(range(len(individuo)), 2)
    individuo.insert(j, individuo.pop(i))
    return individuo,


def mutacao(individuo):
    return random.choice([mutacaoInversao, mutacaoInsercao])(individuo)
