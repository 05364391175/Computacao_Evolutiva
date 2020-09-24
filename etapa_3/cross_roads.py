import random
import datetime
import copy

taxaCrossover = 0.8
taxaMutacao = 0.02
geracaoSucesso = 0
ngeracao = 0
pior = 100000


class Individuo():
    def __init__(self, cromossomo, fitness, fitness2, gen=0):
        self.cromossomo = cromossomo
        self.fitness = fitness
        self.fitness2 = fitness2
        self.gen = gen

    # Criar cromossomo
    def criarCromossomo(tamanho):  # criar indivíduo para inserir na população
        cromossomo = random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], tamanho)
        return cromossomo  # Gera o vetor com os valores aleatórios sem repetição

    # Calcula a avaliação de um cromossomo individual
    def calcula_fitness(cromossomo):
        send = int(str(cromossomo[0]) + str(cromossomo[1]) + str(cromossomo[2]) + str(
            cromossomo[3]))  # concatena as posições do SEND
        # print("SEND ", send)
        more = int(str(cromossomo[4]) + str(cromossomo[5]) + str(cromossomo[6]) + str(
            cromossomo[1]))  # concatena as posições do MORE
        # print("MORE", more)
        money = int(str(cromossomo[4]) + str(cromossomo[5]) + str(cromossomo[2]) + str(cromossomo[1]) + str(
            cromossomo[7]))  # concatena as posições do MONEY
        # print("MONEY", money)
        # print( abs((send + more) - money))
        # a ideia e inverter, o mais perto de 1000000 é o melhor, antes era o mais perto de 0
        # Falta refinar a ideia do ABS
        fitness1 = abs((send + more) - money)  # Calcula a avaliação Avaliação
        # print(fitness1)
        return fitness1

    # Calcula a avaliação de um cromossomo individual
    def calcula_fitness_invertido(cromossomo):
        global pior
        send = int(str(cromossomo[0]) + str(cromossomo[1]) + str(cromossomo[2]) + str(
            cromossomo[3]))  # concatena as posições do SEND
        # print("SEND ", send)
        more = int(str(cromossomo[4]) + str(cromossomo[5]) + str(cromossomo[6]) + str(
            cromossomo[1]))  # concatena as posições do MORE
        # print("MORE", more)
        money = int(str(cromossomo[4]) + str(cromossomo[5]) + str(cromossomo[2]) + str(cromossomo[1]) + str(
            cromossomo[7]))  # concatena as posições do MONEY
        # print("MONEY", money)
        # print( abs((send + more) - money))
        # a ideia e inverter, o mais perto de 1000000 é o melhor, antes era o mais perto de 0
        # Falta refinar a ideia do ABS
        ##print(pior)
        fitness1 = (pior + 1) - abs((send + more) - money)  # Calcula a avaliação Avaliação
        # print(fitness1)
        return fitness1


class AG():
    def __init__(self, tamanhoPop, geracoes):
        self.tamanhoPop = tamanhoPop
        self.geracoes = geracoes
        self.populacao = []

    # Cria a populção inicial
    def init_populacao(self):
        for i in range(self.tamanhoPop):
            cromossomo = Individuo.criarCromossomo(10)  # 10 é o tamanho do cromossomo
            fitness = Individuo.calcula_fitness(cromossomo)
            fitness2 = Individuo.calcula_fitness_invertido(cromossomo)
            self.populacao.append(Individuo(cromossomo, fitness, fitness2, ngeracao))

    # Ordena a população para que o maior fica em primeiro
    def ordena_populacao_maior(self):
        self.populacao = sorted(self.populacao, key=lambda populacao: populacao.fitness, reverse=True)

    # Ordena a população para que o menor fica em primeiro
    def ordena_populacao_menor(self):
        self.populacao = sorted(self.populacao, key=lambda populacao: populacao.fitness, reverse=False)

    # O objetivo é somar todos os fitness para fazer o calculo de probabilidade na roleta
    def soma_fitness(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.fitness2
        return soma

    # Roleta com implementação mais simples e leve que a anterior
    def roleta_leve(self, soma_fitness):
        selecionado = -1
        valor_sorteado = random.uniform(0, soma_fitness)
        soma = 0
        i = 0
        while i < len(self.populacao) and soma <= valor_sorteado:
            soma += self.populacao[i].fitness2
            selecionado += 1
            i += 1
        return selecionado

    # Método crossover cíclico, gerar os filhos com os genes dos pais
    def crossover_ciclico_ok(self, cro1, cro2):
        # print("cromossomo pai 1: ", cro1)
        # print("cromossomo pai 2: ", cro2)
        # sorteia uma posicao inicial no cromossomo de forma que o gene do pai 1 seja diferente do pai 2
        corte = random.randint(0, len(cro1) - 1)
        #print(corte)
        # while cro1[corte] == cro2[corte]:
        # print("Chegou")
        # corte = random.randint(0, len(cro1) - 1)
        # print("CORTE INICIAL ",corte)
        valor_corte = cro1[corte]
        # print("valor_inicial_gene_filho1: ", valor_inicial_gene_filho1)
        # faz a primeira troca
        aux = cro1[corte]
        cro1[corte] = cro2[corte]
        cro2[corte] = aux
        while (cro1[corte] != valor_corte):
            corte = AG.verifica_cromossomo(self, cro1, corte)
            # troca os genes entre os pais 1 e 2 na posicao 'pos'
            aux = cro1[corte]
            cro1[corte] = cro2[corte]
            cro2[corte] = aux
        # print("cromossomo filho 1: ", cro1)
        # print("cromossomo filho 2: ", cro2)
        return cro1, cro2

    # Utilizado no crossover cíclico para ver a repetição
    def verifica_cromossomo(self, cromossomo, genis):
        valor = cromossomo[genis]
        for i in range(0, len(cromossomo), 1):
            if cromossomo[i] == valor and i != genis:
                return (i)
        return (-1)

    # Recebe dois cromossomos, faz o crossover PMX e retorna os novos cromossomo (filhos)
    def crossover_pmx(self, cromo1, cromo2):
        # print("-- Início do PMX")
        # print("PAI 1 ",cromo1)
        # print("PAI 2 ", cromo2)
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
            trocar_1 = self.avalia_repeticao_pmx(cromo1, atefim)
            trocar_2 = self.avalia_repeticao_pmx(cromo2, atefim)
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
        # print(cromo1)
        # print(cromo2)
        # print("-- Fim do crossover PMX--")
        return cromo1, cromo2

    # Utilizado para ver as repetições que precisam ser trocadas
    def avalia_repeticao_pmx(self, cromossomo, posicaoDele):
        valor_verificar = cromossomo[posicaoDele]
        # Ver posicao que precisa trocar
        for i in range(len(cromossomo)):
            if (cromossomo[i] == valor_verificar and i != posicaoDele):
                return i
        return -1

    # faz a mutação de dois genes
    def mutacao_2g(self, cromossomo):
        # print("--Início da mutação 2G")
        p1 = random.randint(1, len(cromossomo) - 1)
        p2 = random.randint(1, len(cromossomo) - 1)
        while (p1 == p2):
            p2 = random.randint(0, len(cromossomo) - 1)
        # print("Sorteio 1", p1)
        # print(cromossomo[p1-1])
        # print("Sorteio 2", p2)
        # print(cromossomo[p2 - 1])
        aux = cromossomo[p1]
        cromossomo[p1] = cromossomo[p2]
        cromossomo[p2] = aux
        # print("Cromossomo permutado", cromossomo)
        # print("Fim da Mutação 2g")
        return cromossomo

    # Responsável por criar cada geração, sorteando, fazendo o crossover e mutação
    def criaGeracao(self, totalPares):
        global pior
        self.ordena_populacao_menor()
        pior = self.populacao[len(self.populacao) - 1].fitness
        #print("O pior é : ", pior)
        listaFilhosGerados = []
        listaFilhosGerados.clear()
        soma = AG.soma_fitness(self)
        for i in range(0, int(totalPares / 2)):
            valor1 = AG.roleta_leve(self, soma)
            # print(valor1)
            # print(valor1, " ",self.populacao[valor1].cromossomo)
            valor2 = AG.roleta_leve(self, soma)
            # print(valor2)
            # criei uma variável a mais só para não ficar mudando quando for trocar de método de seleção
            pai1 = copy.deepcopy(self.populacao[valor1].cromossomo)
            pai2 = copy.deepcopy(self.populacao[valor2].cromossomo)
            # print("PAI 1", pai1)
            # print("PAI 2", pai2)
            cro1, cro2 = copy.deepcopy(AG.crossover_ciclico_ok(self, pai1, pai2))
            fitness_do_primeiro = Individuo.calcula_fitness(cro1)
            fitness_do_primeiro2 = Individuo.calcula_fitness_invertido(cro1)
            listaFilhosGerados.append(Individuo(cro1, fitness_do_primeiro, fitness_do_primeiro2, ngeracao))
            fitness_do_segundo = Individuo.calcula_fitness(cro2)
            fitness_do_segundo2 = Individuo.calcula_fitness_invertido(cro2)
            listaFilhosGerados.append(Individuo(cro2, fitness_do_segundo, fitness_do_segundo2, ngeracao))
        # mutaçao
        qtdMutacao = int(round(float(len(listaFilhosGerados) * taxaMutacao)))
        while qtdMutacao > 0:
            mutar = random.randint(0, len(listaFilhosGerados) - 1)
            cromossomoMutado = copy.deepcopy(self.mutacao_2g(listaFilhosGerados[mutar].cromossomo))
            fitness_mutado = Individuo.calcula_fitness(cromossomoMutado)
            fitness_mutado2 = Individuo.calcula_fitness_invertido(cromossomoMutado)
            listaFilhosGerados.append(Individuo(cromossomoMutado, fitness_mutado, fitness_mutado2, ngeracao))
            qtdMutacao -= 1
        # Reiserção ordenada

        self.populacao.extend(listaFilhosGerados)
        self.ordena_populacao_menor()
        self.populacao = copy.deepcopy(self.populacao[0:99])
        """
        # Reiserção Elistica 20%
        self.ordena_populacao_menor()
        aux_pop = copy.deepcopy(self.populacao[0:20])
        aux_pop.extend(listaFilhosGerados)
        self.populacao.clear()
        self.populacao = copy.deepcopy(aux_pop)
        """




def main():
    tamanoPop = 100
    geracao = 1
    global ngeracao
    global geracaoSucesso
    global pior
    ngeracao = 0
    a = AG(tamanoPop, geracao);
    a.populacao.clear()
    a.init_populacao()
    a.ordena_populacao_menor()
    # print("-- Inicio da geração incial--")
    # for i in range(len(a.populacao)):
    # print(a.populacao[i].cromossomo, " ", a.populacao[i].fitness, " ", a.populacao[i].fitness2)
    # print("-- Fim da geração incial--")
    while ngeracao < 50:
        # print("Geração ",ngeracao)
        totalPares = len(a.populacao) * taxaCrossover
        # print(totalPares)
        a.criaGeracao(totalPares)
        # for i in range(len(a.populacao)):
        # print(a.populacao[i].cromossomo, " ", a.populacao[i].fitness)
        """
        for i in range(len(a.populacao)):
            cromo = a.populacao[i].cromossomo
            a.populacao[i].fitness2 = Individuo.calcula_fitness_invertido(cromo)
        a.populacao = copy.deepcopy(a.populacao[0:99])
        """

        if a.populacao[0].fitness == 0:
            geracaoSucesso += 1
            ngeracao = 50
            print("Achou parou!")
        # print("--Início da impressão da ", ngeracao, "º geração--")
        # for i in range(len(a.populacao)):
        # print(a.populacao[i].cromossomo, " ", a.populacao[i].fitness, " ", a.populacao[i].fitness2, " Geração ",
        # a.populacao[i].gen)
        # print("--Fim da impressão da primeira geração--")
        ngeracao += 1


"""
c1 = [7,5,1,4,3,6,8,2]
c2 = [3,4,8,7,5,2,6,1]
a = AG(100,1)
a.crossover_pmx(c1,c2)
"""
execucao = 0
datetime_inicio = datetime.datetime.now()
while execucao < 200:
    print("Execução ", execucao)
    main()
    execucao += 1
print("taxa de convergencia: ", (geracaoSucesso / execucao * 100), "%")
datetime_fim = datetime.datetime.now()
print(geracaoSucesso)
print(execucao)
print("inicio: ", datetime_inicio)
print("fim : ", datetime_fim)
