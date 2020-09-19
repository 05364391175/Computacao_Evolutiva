import random
import datetime
import copy



# Recebe dois cromossomos, faz o crossover PMX e retorna os novos cromossomo (filhos)
def crossover_pmx(cromo1, cromo2):
    print("-- Início do PMX")
    print("PAI 1 ",cromo1)
    print("PAI 2 ", cromo2)
    # Aleatório do 0 até uma posição a menos, não deixei pegar a ultima para obrigar o crossover acontecer
    p1 = random.randint(0, len(cromo1) - 2)
    p2 = random.randint(p1 + 1, len(cromo1) - 1)
    # print(p1)
    # print(p2)
    posicao = p1
    # realiza as trocas entre os corte
    while posicao <= p2:
        aux = cromo1[posicao]
        # print("AUX",aux)
        # print(cromo2[posicao])
        cromo1[posicao] = cromo2[posicao]
        cromo2[posicao] = aux
        posicao += 1
    # print(cromo1)
    # print(cromo2)
    # Até aqui ok
    # verificar quais precisa no cromo1
    atefim = p1
    pre_cro1trocar = []
    pre_cro2trocar = []
    while p2 >= atefim:
        # chama o método para ver quem pode trocar
        trocar_1 = avalia_repeticao_pmx(cromo1, atefim)
        trocar_2 = avalia_repeticao_pmx(cromo2, atefim)
        if (trocar_1 != -1):
            # mandar trocar por uma do cro2
            pre_cro1trocar.append(trocar_1)
        if (trocar_2 != -1):
            # mandar trocar por uma do cro2
            pre_cro2trocar.append(trocar_2)
        atefim += 1
    """"
    print("Precisa trocar do 1")
    for i in range(len(pre_cro1trocar)):
        print(cromo1[pre_cro1trocar[i]])
    print("Precisa trocar do 2")
    for i in range(len(pre_cro2trocar)):
        print(cromo2[pre_cro2trocar[i]])
    """
    # Realiza as trocas das posições externas
    for i in range(len(pre_cro1trocar)):
        aux = cromo1[pre_cro1trocar[i]]
        cromo1[pre_cro1trocar[i]] = cromo2[pre_cro2trocar[i]]
        cromo2[pre_cro2trocar[i]] = aux
    print(cromo1)
    print(cromo2)
    # print("-- Fim do crossover PMX--")
    return cromo1, cromo2


# Utilizado para ver as repetições que precisam ser trocadas

def avalia_repeticao_pmx(cromossomo, posicaoDele):
    valor_verificar = cromossomo[posicaoDele]
    # Ver posicao que precisa trocar
    for i in range(len(cromossomo)):
        if (cromossomo[i] == valor_verificar and i != posicaoDele):
            return i
    return -1

cro1 = [8, 3, 2, 4, 0, 9, 1, 7, 5, 6]
cro2 = [8, 3, 2, 4, 0, 9, 1, 7, 5, 6]
crossover_pmx(cro1,cro2)