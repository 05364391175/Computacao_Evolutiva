import math
import random
import matplotlib.pyplot as plt
import copy

function1_values = []
function2_values = []


class Individuo():
    def __init__(self, x, ngeracao, fronteira, dummy_fitness):
        self.x = x
        self.f1 = x ** 2
        self.f2 = (x - 2) ** 2
        self.ngeracao = ngeracao
        self.fronteira = fronteira
        self.dummy_fitness = dummy_fitness


class AG():
    def __init__(self, tamanhoPop, ngeracao):
        self.tamanhoPop = tamanhoPop
        self.ngeracao = ngeracao
        self.populacao = []

    # Cria a populção inicial
    def init_populacao(self, dummy_fitness):
        for i in range(self.tamanhoPop):
            valor = random.uniform(-2, 2)
            valorc = round(valor, ndigits=2)
            x = Individuo(valor, self.ngeracao, 0, dummy_fitness)
            self.populacao.append(x)

    def classificar_fronteira(self):
        npop = copy.deepcopy(self.populacao)
        self.populacao.clear()
        fronteira = 1
        final = len(npop)
        while final > 0:
            frente = self.frente_paredo(npop)
            for i in frente:
                i.fronteira = fronteira
                self.populacao.append(i)
                print(len(npop))
                npop.remove(i)
                print(len(npop))
            final = len(npop)
            fronteira+=1

        # gerar a frente ótima de paredo

    def frente_paredo(self, npop):
        frente_otima = []
        comparando = 0
        while comparando < len(npop):
            print()
            dominado = 0
            comparado_hh = 0
            while comparado_hh < len(npop):
                if (npop[comparando].f1 > npop[comparado_hh].f1 or npop[comparando].f2 > npop[
                    comparado_hh].f2) and comparando != comparado_hh:
                    t = 0
                    print("aqui porra")
                elif (comparando == comparado_hh):
                    t =0
                    print("o mesmo")
                else:
                    print("Dominado")
                    dominado = 1
                    comparado_hh = len(npop)
                comparado_hh += 1
            if (dominado == 0):
                frente_otima.append(npop[comparando])
            comparando += 1
        return frente_otima

    # Ordena a população para que o menor fica em primeiro
    def ordena_populacao_menor(self):
        self.populacao = sorted(self.populacao, key=lambda populacao: populacao.fronteira, reverse=False)


def main():
    tamanho_pop = 5
    ngeracao = 1
    totalgeracao = 1
    a = AG(tamanho_pop, ngeracao)
    a.init_populacao(tamanho_pop)
    for i in a.populacao:
        print("X ",i.x, " F1 ", i.f1, " F2 ", i.f2,)
    a.classificar_fronteira()
    for i in a.populacao:
        print("X ",i.x, " F1 ", i.f1, " F2 ", i.f2," Fronteira ",i.fronteira)

    '''
    a.ordena_populacao_menor()
    contador_que_recebeu = 0
    ponteiro = 1 #ver qual fronteira está recebendo os valores
    cont_por_fonteira = 0
    valor = len(a.populacao)
    for i in range(len(a.populacao)):
        if(ponteiro != a.populacao[i].fronteira):
            valor = valor - cont_por_fonteira
            ponteiro+=1
            cont_por_fonteira = 0
        a.populacao[i].dummy_fitness = valor
        cont_por_fonteira+=1

        print(a.populacao[i].x, " X ", a.populacao[i].f1, " F1 ", a.populacao[i].f2, " F2 ", a.populacao[i].fronteira, " dummy_fitness ",a.populacao[i].dummy_fitness)
    '''

main()

'''
# Colocando no gráfico apenas a função ótima de paredo
function1 = [i * -1 for i in function1_values]
function2 = [j * -1 for j in function2_values]
plt.xlabel('F1', fontsize=15)
plt.ylabel('F2', fontsize=15)
plt.scatter(function1, function2)
plt.show()
'''