import random

from aptidao import calculaAptidao
from operadores import cruzamentoOX, mutacaoInversao, selecaoTorneio


def inicializaPopulacao(tamanho, qtdeCidades):
    #criando uma lista com "tamanho" permutacoes aleatorias de cidades:
    lista = []
    for i in range(tamanho):
        individuo = list(range(1, qtdeCidades + 1))
        random.shuffle(individuo)
        lista.append(individuo)
    return lista


def algoritmoGenetico(dicDistancias, qtdeCidades, tamanhoPopulacao=200, geracoes=1000,
                      probCruzamento=0.9, probMutacao=0.2, qtdeElite=2):
    populacao = inicializaPopulacao(tamanhoPopulacao, qtdeCidades)
    listaAptidao = calculaAptidao(populacao, dicDistancias)

    for geracao in range(geracoes):
        #elitismo: os melhores passam direto pra proxima geracao, para nao perder eles
        ordem = sorted(range(tamanhoPopulacao), key=lambda k: listaAptidao[k])
        novaPopulacao = [populacao[k] for k in ordem[:qtdeElite]]

        #o resto da nova populacao vem dos filhos
        while len(novaPopulacao) < tamanhoPopulacao:
            pai1 = selecaoTorneio(populacao, listaAptidao)
            pai2 = selecaoTorneio(populacao, listaAptidao)

            #se nao cair no cruzamento, o filho eh so uma copia do pai1
            filho = cruzamentoOX(pai1, pai2) if random.random() < probCruzamento else pai1[:]
            if random.random() < probMutacao:
                mutacaoInversao(filho)

            novaPopulacao.append(filho)

        populacao = novaPopulacao
        listaAptidao = calculaAptidao(populacao, dicDistancias)

    #no final devolve a melhor rota e o custo dela
    menorCusto = min(listaAptidao)
    return populacao[listaAptidao.index(menorCusto)], menorCusto
