import random
import copy
import datetime


totalGenes = 33
classeD = 1
txcrossover = 1
txmutacao = 0.3

nomes_colunas = ["erythema", "scaling", "definite borders", "itching", "koebner phenomenon", "polygonal papules",
                 "follicular papules", "oral mucosal involvement",
                 "knee and elbow involvement", "scalp involvement", "family history", "melanin incontinence",
                 "eosinophils in the infiltrate",
                 "PNL infiltrate", "fibrosis of the papillary dermis", "exocytosis", "acanthosis", "hyperkeratosis",
                 "parakeratosis",
                 "clubbing of the rete ridges", "elongation of the rete ridges",
                 "thinning of the suprapapillary epidermis", "spongiform pustule", "munro microabcess",
                 "focal hypergranulosis", "disappearance of the granular layer",
                 "vacuolisation and damage of basal layer", "spongiosis",
                 "saw-tooth appearance of retes", "follicular horn plug", "perifollicular parakeratosis",
                 "inflammatory monoluclear inflitrate",
                 "band-like infiltrate", "Oge"]


class Genes():
    def __init__(self, nome, peso, operador, valor):
        self.nome = nome
        self.peso = peso
        self.operador = operador
        self.valor = valor

    def criarGenes(self, posica):
        nome = nomes_colunas[posica]
        peso = random.random()
        valor = random.randint(0, 3)
        if (posica == 10):
            operador = "=="
            valor = random.randint(0, 1)
        else:
            op = random.randint(0, 3)
            if (op == 0):
                operador = "=="
            elif (op == 1):
                operador = "!="
            elif (op == 2):
                operador = ">="
            elif (op == 3):
                operador = "<"
        if (posica == 33):
            valor = random.randint(0, 79)
        genes = Genes(nome, peso, operador, valor)
        return genes


class Individuo():
    def __init__(self, regra, listaGenes, listaPresente, fitness, fitness2, fitness3, fitness4,fronteira,dummy_fitness, shared_fitness):
        self.regra = regra
        self.listaGenes = listaGenes
        self.listaPresente = listaPresente
        self.fitness = fitness
        self.fitness2 = fitness2
        self.fitness3 = fitness3
        self.fitness4 = fitness4
        self.fronteira = fronteira
        self.dummy_fitness = dummy_fitness
        self.shared_fitness = shared_fitness

    def calcularFitness(self, genes, listaPresente):
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        t = 0
        for linha in base_usar:
            classeDoenca = int(linha[34].strip())
            verifica = 0
            # print(classeDoenca)
            for coluna in listaPresente:
                g = genes[coluna]
                # print("Genes ",g.nome)
                valorBase = int(linha[coluna])
                if (g.operador == "=="):
                    if (valorBase == g.valor):
                        t += 1
                    else:
                        verifica = 1
                elif (g.operador == "!="):
                    if (valorBase != g.valor):
                        t += 1
                    else:
                        verifica = 1
                elif (g.operador == ">="):
                    if (valorBase >= g.valor):
                        t += 1
                    else:
                        verifica = 1
                elif (g.operador == "<"):
                    if (valorBase < g.valor):
                        t += 1
                    else:
                        verifica = 1
            if (verifica == 0 and classeDoenca == classeD):
                tp += 1
            elif (verifica == 0 and classeDoenca != classeD):
                fp += 1
            elif (verifica == 1 and classeDoenca == classeD):
                fn += 1
            elif (verifica == 1 and classeDoenca != classeD):
                tn += 1
        #print("TP ",tp)
        #print("FP ",fp)
        # print("TN ",tn)
        # print("FN ",fn)
        se = tp / (tp + fn)
        sp = tn / (tn + fp)
        if(tp == 0 and fp ==0):
            fitness2 = 0
        else:
            pr = tp / (tp + fp)
            if(pr == 0 and se ==0):
                fitness2 = 0
            else:
                fitness2 = (se * pr) / (se + pr)
        nm = totalGenes
        n = len(listaPresente)
        fitness3 = (nm-n+1)/nm
        fitnessRetorno = se * sp
        fitness4 = 0.7
        # print("Fitness ",fitnessRetorno)
        return fitnessRetorno,fitness2,fitness3,fitness4


class AG():
    def __init__(self, tamanhoPop):
        self.tamanhoPop = tamanhoPop
        self.populacao = []

    # Cria a populção inicial
    def init_populacao(self):
        for i in range(self.tamanhoPop):
            regra = ""
            and_meio = ""
            listGenes = []
            listaPresente = []
            for j in range(totalGenes):
                g = Genes.criarGenes(self, j)
                listGenes.append(g)
                if (g.peso < 0.3):
                    listaPresente.append(j)
                    regra = regra + str(and_meio) + str(g.nome) + str(g.operador) + str(g.valor)
                    and_meio = " AND "
            # for k in range(len(listGenes)):
            # print(listGenes[k].nome," Peso ",listGenes[k].peso," Operador ",listGenes[k].operador," Valor ",listGenes[k].valor)
            # print(regra)
            fitness,fitness2, fitness3,fitness4 = Individuo.calcularFitness(self, listGenes, listaPresente)
            fronteira = 0
            shared_fitness = 0
            dummy_fitness = 0
            self.populacao.append(Individuo(regra, listGenes, listaPresente, fitness,fitness2,fitness3,fitness4,fronteira,dummy_fitness,shared_fitness))

        # Ordena a população para que o maior fica em primeiro

    def classificar_fronteira(self):
        npop = copy.deepcopy(self.populacao)
        self.ordena_populacao_maior_fitness2()
        menor_fitness2 = self.populacao[len(self.populacao) - 1].fitness
        maior_fitness2 = self.populacao[0].fitness
        self.ordena_populacao_maior_fitness1()
        menor_fitness1 = self.populacao[len(self.populacao)-1].fitness
        maior_fitness1 = self.populacao[0].fitness
        self.populacao.clear()
        fronteira = 1
        final = len(npop)
        while final > 0:
            #print("Nova fronteira")
            frente = self.frente_paredo(npop)
            #print("Tamanho ",len(frente))
            tamanho = len(frente)
            cont = 0
            for i in frente:
                if(tamanho < 3 or cont == 0 or cont == (tamanho-1)):
                    #print(tamanho)
                    distancia = 10000
                else:
                    distancia = self.calcular_shared_distance(cont,frente,menor_fitness1,maior_fitness1,menor_fitness2,maior_fitness2)
                i.fronteira = fronteira
                i.shared_fitness = distancia
                self.populacao.append(i)
                #print(len(npop))
                npop.remove(i)
                cont+=1
                #print(len(npop))
            final = len(npop)
            fronteira += 1

        # gerar a frente ótima de paredo

    def frente_paredo(self, npop):
        frente_otima = []
        comparando = 0
        while comparando < len(npop):
            dominado = 0
            comparado_hh = 0
            while comparado_hh < len(npop):
                if (npop[comparando].fitness > npop[comparado_hh].fitness or npop[comparando].fitness2 > npop[
                    comparado_hh].fitness2):
                    t = 0
                    #print("aqui porra")
                elif((npop[comparando].fitness == npop[comparado_hh].fitness and npop[comparando].fitness2 == npop[
                    comparado_hh].fitness2)) and comparando != comparado_hh:
                    t = 0
                elif(comparando == comparado_hh):
                    t=0
                else:
                    #print("Dominado")
                    #print(npop[comparando].fitness," ",npop[comparando].fitness2)
                    #print(npop[comparado_hh].fitness, " ", npop[comparado_hh].fitness2)
                    dominado = 1
                    comparado_hh = len(npop)
                comparado_hh += 1
            if (dominado == 0):
                frente_otima.append(npop[comparando])
            comparando += 1
        return frente_otima

    def calcular_shared_distance(self, posicao, pop_fron,menor_fitness1,maior_fitness1,menor_fitness2,maior_fitness2):
        f1_dis = abs((pop_fron[posicao+1].fitness-pop_fron[posicao-1].fitness)) #/ maior_fitness1 - menor_fitness1
        f2_dis = abs((pop_fron[posicao + 1].fitness2 - pop_fron[posicao - 1].fitness2)) #/ maior_fitness2 - menor_fitness2
        distancia = f1_dis + f2_dis
        return distancia

    def ordena_populacao_maior_fitness1(self):
        self.populacao = sorted(self.populacao, key=lambda populacao: populacao.fitness, reverse=True)

    def ordena_populacao_maior_fitness2(self):
        self.populacao = sorted(self.populacao, key=lambda populacao: populacao.fitness2, reverse=True)

    def ordena_populacao_fronteira(self):
        self.populacao = sorted(self.populacao, key=lambda populacao: populacao.fronteira, reverse=True)

    # O objetivo é somar todos os fitness para fazer o calculo de probabilidade na roleta
    def soma_fitness(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.fitness
        return soma

    # Roleta com implementação mais simples e leve que a anterior
    def roleta_leve(self, soma_fitness):
        selecionado = -1
        valor_sorteado = random.uniform(0, soma_fitness)
        soma = 0
        i = 0
        while i < len(self.populacao) and soma <= valor_sorteado:
            soma += self.populacao[i].fitness
            selecionado += 1
            i += 1
        return selecionado

    def torneio_estocastico(self):
        maior = 0
        posicaoRetorno = 0
        soma_fitness = self.soma_fitness()
        cont = 0
        while cont < 3:
            p = self.roleta_leve(soma_fitness)
            individuo = self.populacao[p]
            if (maior <= individuo.fitness):
                maior = copy.deepcopy(self.populacao[p].fitness)
                posicaoRetorno = p
            cont += 1
        return posicaoRetorno

    def crossover_2p(self, pai1, pai2):
        filho1 = copy.deepcopy(pai1)
        filho2 = copy.deepcopy(pai2)
        ponto1 = random.randint(0, totalGenes)
        ponto2 = random.randint(0, totalGenes)
        while (ponto1 == ponto2):
            ponto2 = random.randint(0, totalGenes)
        if (ponto1 > ponto2):
            aux = ponto1
            ponto1 = ponto2
            ponto2 = aux
        while ponto1 < ponto2:
            peso1 = pai1.listaGenes[ponto1].peso
            peso2 = pai2.listaGenes[ponto1].peso
            filho1.listaGenes[ponto1].peso = peso2
            filho2.listaGenes[ponto1].peso = peso1

            operador1 = pai1.listaGenes[ponto1].operador
            operador2 = pai2.listaGenes[ponto1].operador
            filho1.listaGenes[ponto1].operador = operador2
            filho2.listaGenes[ponto1].operador = operador1

            valor1 = pai1.listaGenes[ponto1].valor
            valor2 = pai2.listaGenes[ponto1].valor
            filho1.listaGenes[ponto1].valor = valor2
            filho2.listaGenes[ponto1].valor = valor1

            ponto1 += 1

        filho1.listaPresente.clear
        filho2.listaPresente.clear
        regra1, listaPresente1 = self.calcularRegra(filho1.listaGenes)
        regra2, listaPresente2 = self.calcularRegra(filho2.listaGenes)
        filho1.regra = regra1
        filho1.listaPresente.extend(listaPresente1)
        filho2.regra = regra2
        filho2.listaPresente.extend(listaPresente2)

        f1_fitness1, f1_f2, f1_f3,f1_f4 = Individuo.calcularFitness(self, filho1.listaGenes, filho1.listaPresente)
        filho1.fitness = f1_fitness1
        filho1.fitness2 = f1_f2
        filho1.fitness3 = f1_f3
        filho1.fitness4 = f1_f4
        # print(fitness1)
        f2_fitness2, f2_f2, f2_f3,f2_f4 = Individuo.calcularFitness(self, filho2.listaGenes, filho2.listaPresente)
        filho2.fitness = f2_fitness2
        filho2.fitness2 = f2_f2
        filho2.fitness3 = f2_f3
        filho2.fitness4 = f2_f4
        # print(fitness2)
        filhos = []
        filhos.append(filho1)
        filhos.append(filho2)
        return filhos

    def calcularRegra(self, listaGenes):
        listaPresente = []
        regra = ""
        and_meio1 = ""
        cont = 0
        for i in listaGenes:
            if (i.peso < 0.3):
                listaPresente.append(cont)
                regra = regra + str(and_meio1) + str(i.nome) + str(i.operador) + str(i.valor)
                and_meio1 = " AND "
            cont += 1
        return regra, listaPresente

    def mutacaoPeso(self, valor):
        soma_subtrai = random.randint(0, 1)
        valoradd = random.random()
        if (soma_subtrai == 0):
            nvalor = valor - valoradd
        else:
            nvalor = valoradd + valor
        return nvalor

    def mutacaoOperador(self, posica):
        if (posica == 10):
            operador = "=="
        else:
            op = random.randint(0, 3)
            if (op == 0):
                operador = "=="
            elif (op == 1):
                operador = "!="
            elif (op == 2):
                operador = ">="
            elif (op == 3):
                operador = "<"
        return operador

    def mutacaoValor(self, posicao):
        valor = random.randint(0, 3)
        if (posicao == 33):
            valor = random.randint(0, 79)
        return valor

    def geracoes(self):
        melhor = copy.deepcopy(self.populacao[0])
        filhosR = []
        filhosR.clear()
        print("Fitness 1  ", melhor.fitness," F-score ",melhor.fitness2," simplicidade ",melhor.fitness3)
        totalCrssocer = int(txcrossover * len(self.populacao) / 2)
        totalMutacao = int(txmutacao * len(self.populacao))
        for i in range(totalCrssocer):
            posicao1 = self.torneio_estocastico()
            pai1 = copy.deepcopy(self.populacao[posicao1])
            del (self.populacao[posicao1])
            # print("Pai 1 ",pai1.fitness)

            posicao2 = self.torneio_estocastico()
            pai2 = copy.deepcopy(self.populacao[posicao2])
            del (self.populacao[posicao2])
            # print("Pai 2 ", pai2.fitness)
            filhosR.extend(self.crossover_2p(pai1, pai2))

        for mutacao in range(totalMutacao):
            idpeso = random.randint(0, len(filhosR) - 1)
            ps = random.randint(0, totalGenes - 1)
            valorps = filhosR[idpeso].listaGenes[ps].peso
            novovalor = self.mutacaoPeso(valorps)
            filhosR[idpeso].listaGenes[ps].peso = novovalor
            regraPeso, listaPeso = self.calcularRegra(filhosR[idpeso].listaGenes)
            filhosR[idpeso].regra = regraPeso
            filhosR[idpeso].listaPresente.clear()
            filhosR[idpeso].listaPresente.extend(listaPeso)
            f1, f2,f3,f4 = Individuo.calcularFitness(self, filhosR[idpeso].listaGenes, listaPeso)
            filhosR[idpeso].fitness = f1
            filhosR[idpeso].fitness2 = f2
            filhosR[idpeso].fitness3 = f3
            filhosR[idpeso].fitness4 = f4

            idoperador = random.randint(0, len(filhosR) - 1)
            op = random.randint(0, totalGenes - 1)
            filhosR[idoperador].listaGenes[op].operador = self.mutacaoOperador(op)
            regraOperador, listaOperador = self.calcularRegra(filhosR[idoperador].listaGenes)
            filhosR[idoperador].regra = regraOperador
            filhosR[idoperador].listaPresente.clear()
            filhosR[idoperador].listaPresente.extend(listaOperador)
            f1, f2,f3,f4 = Individuo.calcularFitness(self, filhosR[idoperador].listaGenes, listaOperador)
            filhosR[idoperador].fitness = f1
            filhosR[idoperador].fitness2 = f2
            filhosR[idoperador].fitness3 = f3
            filhosR[idoperador].fitness4 = f4


            idvalor = random.randint(0, len(filhosR) - 1)
            vl = random.randint(0, totalGenes - 1)
            filhosR[idvalor].listaGenes[vl].valor = self.mutacaoValor(vl)
            regraValor, listaValor = self.calcularRegra(filhosR[idvalor].listaGenes)
            filhosR[idvalor].regra = regraValor
            filhosR[idvalor].listaPresente.clear()
            filhosR[idvalor].listaPresente.extend(listaValor)
            f1,f2,f3,f4 = Individuo.calcularFitness(self, filhosR[idvalor].listaGenes, listaValor)
            filhosR[idvalor].fitness = f1
            filhosR[idvalor].fitness2 = f2
            filhosR[idvalor].fitness3 = f3
            filhosR[idvalor].fitness4 = f4
        self.populacao.clear()
        self.populacao.append(melhor)
        self.populacao.extend(filhosR)


def main():
    tamanoPop = 50
    geracao = 50
    ngeracao = 0
    a = AG(tamanoPop);
    a.populacao.clear()
    a.init_populacao()
    for i in a.populacao:
        print(" Fitness 1 ", i.fitness, " Fitness 2 ", i.fitness2)
    a.classificar_fronteira()
    for i in a.populacao:
        print("Fronteira ",i.fronteira, " Fitness 1 ",i.fitness, " Fitness 2 ",i.fitness2," Shared ",i.shared_fitness)


    a.ordena_populacao_fronteira()
    for i in range(len(a.populacao)):
        print(a.populacao[i].fitness)
    while ngeracao < geracao:
        a.classificar_fronteira()
        print("Geração ", ngeracao)
        a.geracoes()
        a.ordena_populacao_maior_fitness1()

        ngeracao += 1
    print(a.populacao[0].fitness, " ", a.populacao[0].regra)



def testarRegra():
    genesParaTeste = []
    genesParaTeste.append(Genes("erythema", 0.4, "!=", 0))
    genesParaTeste.append(Genes("scaling", 0.4, "==", 0))
    genesParaTeste.append(Genes("definite borders", 0.4, "==", 0))
    genesParaTeste.append(Genes("itching", 0.4, "==", 0))
    genesParaTeste.append(Genes("koebner phenomenon", 0.4, "<", 3))
    genesParaTeste.append(Genes("polygonal papules", 0.4, "==", 0))
    genesParaTeste.append(Genes("follicular papules", 0.4, "<", 1))
    genesParaTeste.append(Genes("oral mucosal involvement", 0.4, "<", 2))
    genesParaTeste.append(Genes("knee and elbow involvement", 0.1, "==", 0))
    genesParaTeste.append(Genes("scalp involvement", 0.1, "==", 0))
    genesParaTeste.append(Genes("family history", 0.4, "==", 0))
    genesParaTeste.append(Genes("melanin incontinence", 0.4, "==", 0))
    genesParaTeste.append(Genes("eosinophils in the infiltrate", 0.4, "==", 0))

    genesParaTeste.append(Genes("PNL infiltrate", 0.4, "!=", 3))
    genesParaTeste.append(Genes("fibrosis of the papillary dermis", 0.1, "<", 2))
    genesParaTeste.append(Genes("exocytosis", 0.4, ">=", 0))
    genesParaTeste.append(Genes("acanthosis", 0.4, "!=", 0))
    genesParaTeste.append(Genes("hyperkeratosis", 0.4, "==", 0))
    genesParaTeste.append(Genes("parakeratosis", 0.4, "<", 3))
    genesParaTeste.append(Genes("clubbing of the rete ridges", 0.4, "<", 1))

    genesParaTeste.append(Genes("elongation of the rete ridges", 0.1, "==", 0))
    genesParaTeste.append(Genes("thinning of the suprapapillary epidermis", 0.4, "==", 0))
    genesParaTeste.append(Genes("spongiform pustule", 0.4, "==", 0))
    genesParaTeste.append(Genes("munro microabcess", 0.4, ">=", 0))

    genesParaTeste.append(Genes("focal hypergranulosis", 0.1, "==", 0))
    genesParaTeste.append(Genes("disappearance of the granular layer", 0.4, "==", 0))
    genesParaTeste.append(Genes("vacuolisation and damage of basal layer", 0.4, "<", 1))
    genesParaTeste.append(Genes("spongiosis", 0.4, "!=", 1))

    genesParaTeste.append(Genes("saw-tooth appearance of retes", 0.4, "==", 0))
    genesParaTeste.append(Genes("follicular horn plug", 0.4, "==", 0))
    genesParaTeste.append(Genes("perifollicular parakeratosis", 0.4, "<", 2))
    genesParaTeste.append(Genes("inflammatory monoluclear inflitrate", 0.4, "!=", 0))
    genesParaTeste.append(Genes("band-like infiltrate", 0.4, "==", 0))

    a = AG(1);
    regra, listaPresente = a.calcularRegra(genesParaTeste)
    id = Individuo(regra, genesParaTeste, listaPresente, 0)
    fitness = id.calcularFitness(genesParaTeste, listaPresente)
    print("Fitness do teste ",fitness, " Regra ",regra)
    individuo = Individuo(regra, genesParaTeste, listaPresente, fitness)
    return individuo


file = open('dermatology.data', 'r')
results = []
for line in file:
    columns = line.split(",")
    results.append(columns)

# print('Total de %d resultados encontrados: ' % len(results))
# for register in results:
# print(register)
base_treinamento = copy.deepcopy(results[0:240])
base_teste = copy.deepcopy(results[241:len(results)])

base_usar = copy.deepcopy(base_treinamento)

# for register in base_treinamento:
# print(register[0])

datetime_inicio = datetime.datetime.now()
#testarRegra()
main()
datetime_fim = datetime.datetime.now()
print(datetime_fim - datetime_inicio)
