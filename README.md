# FlyFood

Encontra a menor rota do drone usando distância de Manhattan, comparando duas abordagens:

- flyfood-sem-otimizacao/ -> força bruta (testa todas as ordens possíveis dos pontos)
- flyfood-otimizado/ -> algoritmo genético (DEAP)

Cada pasta é um projeto independente, com a mesma estrutura:

- main.py -> roda o programa
- src/matriz/matriz.py -> ler a matriz, achar a origem (R) e sortear os pontos
- src/rota/rota.py -> distância de Manhattan, custo da rota e o algoritmo de busca
- data/entrada/ -> matriz.txt (5x6, só com o R)
- data/saida/ -> um log por execução (resultados)

## Como rodar

O otimizado usa a biblioteca DEAP:

- pip install -r requirements.txt
- python3 flyfood-sem-otimizacao/main.py
- python3 flyfood-otimizado/main.py

O programa gera rodadas: 2 pontos, 3 pontos, 4 pontos...
Em cada rodada os pontos são sorteados na matriz. Se o sorteio cair numa posição já ocupada,
conta como colisão e sorteia de novo. Para parar antes do fim, aperte Ctrl+C.

Cada rodada é salva no log (data/saida/ da pasta que foi executada) com a rota, o custo,
as colisões e o tempo. No início fica a seed do sorteio e, no final, o total de colisões.

## Algoritmo genético

Cada indivíduo é uma ordem de visita dos pontos (uma permutação) e o fitness é o custo da rota,
que deve ser o menor possível.

- população -> 500 indivíduos
- gerações -> 200
- cruzamento -> PMX, com probabilidade 0.8
- mutação -> troca de posições, com probabilidade 0.2 (indpb = 1/n)
- seleção -> torneio de 3

O otimizado usa a mesma seed do log mais recente do não otimizado, então cada rodada sorteia os
mesmos pontos. No log, cada rodada mostra o custo ótimo encontrado pela força bruta e quanto o
genético ficou acima dele (ou sem força bruta, quando a força bruta não chegou naquela rodada).

