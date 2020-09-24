from __future__ import division
import random
import warnings
"""
    #Método de teste para implementar o crossover baseado em ordem, o oxCrossover é uma variação em testes, o oxCrossover_02 é o OX tradicional. 
    #Ambos utiliza a função avaliar_ox para ver se há o genis dentro do corte
"""


def oxCrossover(cro1, cro2):
    print(cro1)
    print(cro2)
    p1 = random.randint(1, len(cro1) - 1)
    p2 = random.randint(1, len(cro2) - 1)
    p1 = 3
    p2 = 6
    filho1 = cro1.copy()
    filho2 = cro2.copy()
    posicaoI = 0
    listaTroca1 = []
    listaTroca2 = []
    posicaoF1 = 0
    posicaoF2 = 0
    while posicaoI < p1:
        # pega do filho2, verifica se há dentro do corte de filho1, se não tiver coloca nele
        aux = cro2[posicaoI]
        aux2 = cro1[posicaoI]
        pode = avalia_ox(cro1, aux, p1, p2)
        pode2 = avalia_ox(cro2, aux2, p1, p2)
        if (pode == -1):
            print(posicaoI, " ", aux)
            listaTroca2.append(posicaoI)
        if (pode2 == -1):
            listaTroca1.append(posicaoI)
        posicaoI += 1
    print("-------")
    posicaoI = p2 + 1
    while posicaoI < len(cro1):
        # pega do filho2, verifica se há dentro do corte de filho1, se não tiver coloca nele
        aux = cro2[posicaoI]
        aux2 = cro1[posicaoI]
        pode = avalia_ox(cro1, aux, p1, p2)
        pode2 = avalia_ox(cro2, aux2, p1, p2)
        if (pode == -1):
            listaTroca2.append(posicaoI)
        if (pode2 == -1):
            listaTroca1.append(posicaoI)
        posicaoI += 1
    print("--Pode trocar da 1--")
    for i in range(len(listaTroca1)):
        filho1[listaTroca1[i]] = cro2[listaTroca2[i]]
        filho2[listaTroca2[i]] = cro1[listaTroca1[i]]
    print("--Pode trocar da 2--")
    for i in range(len(listaTroca2)):
        print(listaTroca1[i])
        print(listaTroca2[i])
    print(filho1)
    print(filho2)

def oxCrossover_02(cro1,cro2):
    print(cro1)
    print(cro2)
    filho1 = cro1.copy()
    filho2 = cro2.copy()
    p1 = random.randint(0, len(cro1) - 2)
    p2 = random.randint(p1, len(cro2) - 1)
    p1 = 2
    p2 = 4
    print(p1)
    print(p2)
    posicao = p1
    #fazer até o início do corte
    while posicao <=p2:
        filho1[posicao] = cro2[posicao]
        filho2[posicao] = cro1[posicao]
        posicao+=1
    posicaoV = 0
    inserir = 0
    while inserir < p1:
        #print("V ",posicaoV, " Inserir ",inserir)
        aux = cro1[posicaoV];
        r = avalia_ox(cro2,aux,p1,p2)
        if(r == -1):
            #print(aux)
            filho1[inserir] = cro1[posicaoV]
            inserir+=1
        posicaoV+=1

    inserir = p2+1
    #fazer após o corte do filho 1
    while inserir < len(cro1):
        print("V ",posicaoV, " Inserir ",inserir)
        aux = cro1[posicaoV];
        r = avalia_ox(cro2, aux, p1, p2)
        if (r == -1):
            # print(aux)
            filho1[inserir] = cro1[posicaoV]
            inserir += 1
        posicaoV += 1


    #Inicio do filho 2
    posicaoV = 0
    inserir = 0
    while inserir < p1:
        #print("V ", posicaoV, " Inserir ", inserir)
        aux = cro2[posicaoV];
        r = avalia_ox(cro1, aux, p1, p2)
        if (r == -1):
            #print(aux)
            filho2[inserir] = cro2[posicaoV]
            inserir += 1
        posicaoV += 1

    inserir = p2 + 1
    # fazer após o corte do filho 2
    while inserir < len(cro2):
        #print("V ", posicaoV, " Inserir ", inserir)
        aux = cro2[posicaoV];
        r = avalia_ox(cro1, aux, p1, p2)
        if (r == -1):
            # print(aux)
            filho2[inserir] = cro2[posicaoV]
            inserir += 1
        posicaoV += 1
    print(filho1)
    print(filho2)


# Utilizado para ver as repetições que precisam ser trocadas
def avalia_ox(cromossomo, valor, corte1, corte2):
    # Ver posicao que precisa trocar
    i = corte1
    while i <= corte2:
        if (cromossomo[i] == valor):
            return i
        i += 1
    return -1




def cxOrdered(ind1, ind2):
    """Executes an ordered crossover (OX) on the input
    individuals. The two individuals are modified in place. This crossover
    expects :term:`sequence` individuals of indices, the result for any other
    type of individuals is unpredictable.
    :param ind1: The first individual participating in the crossover.
    :param ind2: The second individual participating in the crossover.
    :returns: A tuple of two individuals.
    Moreover, this crossover generates holes in the input
    individuals. A hole is created when an attribute of an individual is
    between the two crossover points of the other individual. Then it rotates
    the element so that all holes are between the crossover points and fills
    them with the removed elements in order. For more details see
    [Goldberg1989]_.
    This function uses the :func:`~random.sample` function from the python base
    :mod:`random` module.
    .. [Goldberg1989] Goldberg. Genetic algorithms in search,
       optimization and machine learning. Addison Wesley, 1989
    """
    size = min(len(ind1), len(ind2))
    a, b = random.sample(range(size), 2)
    if a > b:
        a, b = b, a

    holes1, holes2 = [True] * size, [True] * size
    for i in range(size):
        if i < a or i > b:
            holes1[ind2[i]] = False
            holes2[ind1[i]] = False

    # We must keep the original values somewhere before scrambling everything
    temp1, temp2 = ind1, ind2
    k1, k2 = b + 1, b + 1
    for i in range(size):
        if not holes1[temp1[(i + b + 1) % size]]:
            ind1[k1 % size] = temp1[(i + b + 1) % size]
            k1 += 1

        if not holes2[temp2[(i + b + 1) % size]]:
            ind2[k2 % size] = temp2[(i + b + 1) % size]
            k2 += 1

    # Swap the content between a and b (included)
    for i in range(a, b + 1):
        ind1[i], ind2[i] = ind2[i], ind1[i]

    return ind1, ind2


c1 = [8, 0, 9, 1, 2, 6, 3, 5, 7, 4]
c2 = [4, 8, 9, 0, 1, 6, 7, 3, 5, 2]
oxCrossover_02(c1,c2)
