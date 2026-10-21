import random


def selecaoTorneio(populacao, listaAptidao, tamanhoTorneio=3):
    #sorteia uns individuos e pega o que tem o menor custo entre eles
    sorteados = random.sample(range(len(populacao)), tamanhoTorneio)
    vencedor = min(sorteados, key=lambda k: listaAptidao[k])
    return populacao[vencedor]


def cruzamentoOX(pai1, pai2):
    #order crossover: o filho pega um trecho do pai1 na mesma posicao
    #e o resto vem do pai2, na ordem que as cidades aparecem nele
    i, j = sorted(random.sample(range(len(pai1)), 2))
    trecho = pai1[i:j + 1]
    resto = [cidade for cidade in pai2 if cidade not in trecho]
    return resto[:i] + trecho + resto[i:]


def mutacaoInversao(individuo):
    #escolhe um trecho da rota e inverte a ordem dele
    i, j = sorted(random.sample(range(len(individuo)), 2))
    individuo[i:j + 1] = individuo[i:j + 1][::-1]
