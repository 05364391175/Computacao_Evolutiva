import random

def mutacao_teste(cromossomo):
    # print("--Início da mutação 2G")
    p1 = random.randint(1, len(cromossomo) - 1)
    if(p1 != len(cromossomo)-1):
        p2 = p1+1
    else:
        p1 = 0
    aux = cromossomo[p1]
    cromossomo[p1] = cromossomo[p2]
    cromossomo[p2] = aux
    # print("Cromossomo permutado", cromossomo)
    # print("Fim da Mutação 2g")

def mutacao_sim(cromossomo):
    c = cromossomo.copy()
    p1 = random.randint(0, len(cromossomo) - 2)
    p2 = random.randint(p1 + 1, len(cromossomo) - 1)
    vai = p1
    vem = p2
    while vai < vem:
        aux = c[vai]
        print(c[vai])
        c[vai] = c[vem]
        c[vem] = aux
        print(c)
        vai +=1
        vem -=1
    return c

c = mutacao_sim([9, 6, 2, 3, 5, 1, 8, 7, 4, 0])
print(c)