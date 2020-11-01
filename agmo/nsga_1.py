import math
import random
import matplotlib.pyplot as plt
import copy
import math

function1_values = []
function2_values = []


class Individuo():
    def __init__(self, x, ngeracao, fronteira, dummy_fitness,shared_fitness):
        self.x = x
        self.f1 = x ** 2
        self.f2 = (x - 2) ** 2
        self.ngeracao = ngeracao
        self.fronteira = fronteira
        self.dummy_fitness = dummy_fitness
        self. shared_fitness  = shared_fitness


class AG():
    def __init__(self, tamanhoPop, ngeracao):
        self.tamanhoPop = tamanhoPop
        self.ngeracao = ngeracao
        self.populacao = []

    # Cria a populção inicial
    def init_populacao(self):
        for i in range(self.tamanhoPop):
            valor = random.uniform(-2, 2)
            valorc = round(valor, ndigits=2)
            x = Individuo(valor, self.ngeracao, 0, 0,0)
            self.populacao.append(x)

    def lista_nao_dominados(self, lista_pop, fronteira_atual, dummy_fitness_atual):
        nao_dominados = []
        for x in lista_pop:
            verifica = 0
            analisando = 0
            while (analisando < len(lista_pop)):
                if (x.f1 >= lista_pop[analisando].f1 and x.f2 > lista_pop[analisando].f2) or (
                        x.f1 > lista_pop[analisando].f1 and x.f2 >= lista_pop[analisando].f2):
                    verifica = 1
                analisando += 1
            if (verifica == 0):
                x.fronteira = fronteira_atual
                x.fitness = dummy_fitness_atual
                nao_dominados.append(x)
        return nao_dominados

    def distancia_euclidiana(self,x1,x2):
        distancia = (x1-x2)** 2
        distancia = math.sqrt(distancia)

        return distancia

    def classificação(self):
        populacao_sem_classificao = copy.deepcopy(self.populacao)
        self.populacao.clear()
        fronteira_atual = 1
        dummy_fitness_atual = len(populacao_sem_classificao)
        cont = 0
        while(cont < len(populacao_sem_classificao)):
            nao_dominados = self.lista_nao_dominados(populacao_sem_classificao, fronteira_atual, dummy_fitness_atual)
            for n in nao_dominados:
                shared = 0
                for kk in nao_dominados:
                    shared += self.distancia_euclidiana(n.x,kk.x)
                n.shared_fitness = shared
            for n in nao_dominados:
                populacao_sem_classificao.remove(n)
            self.populacao.extend(nao_dominados)
            fronteira_atual+=1

    # Ordena a população para que o menor fica em primeiro
    def ordena_populacao_menor(self):
        self.populacao = sorted(self.populacao, key=lambda populacao: populacao.fronteira, reverse=False)


def main():
    tamanho_pop = 5
    ngeracao = 1
    totalgeracao = 1
    a = AG(tamanho_pop, ngeracao)
    a.init_populacao()
    for i in range(len(a.populacao)):
        print(a.populacao[i].x, " ", a.populacao[i].f1, " ", a.populacao[i].f2, " ", a.populacao[i].fronteira)
    a.classificação()
    print("População classificada")
    for i in range(len(a.populacao)):
        print(a.populacao[i].x, " ", a.populacao[i].f1, " ", a.populacao[i].f2, " ", a.populacao[i].fronteira," ", a.populacao[i].shared_fitness)



main()
# Colocando no gráfico apenas a função ótima de paredo
function1 = [i * -1 for i in function1_values]
function2 = [j * -1 for j in function2_values]
plt.xlabel('F1', fontsize=15)
plt.ylabel('F2', fontsize=15)
# plt.scatter(function1, function2)
# plt.show()
