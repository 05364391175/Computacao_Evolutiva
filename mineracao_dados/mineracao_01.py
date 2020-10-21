import random
import copy

totalGenes = 34
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
    def __init__(self, regra, listaGenes, listaPresente, fitness):
        self.regra = regra
        self.listaGenes = listaGenes
        self.listaPresente = listaPresente
        self.fitness = fitness

    def calcularFitness(self, genes, listaPresente):
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        t = 0
        for linha in base_treinamento:
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
        # print("TP ",tp)
        # print("FP ",fp)
        # print("TN ",tn)
        # print("FN ",fn)
        sensibilidade = tp / (tp + fn)
        especialidade = tn / (tn + fp)
        fitnessRetorno = sensibilidade * especialidade
        # print("Fitness ",fitnessRetorno)
        return fitnessRetorno


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
            fitness = Individuo.calcularFitness(self, listGenes, listaPresente)
            self.populacao.append(Individuo(regra, listGenes, listaPresente, fitness))

        # Ordena a população para que o maior fica em primeiro

    def ordena_populacao_maior(self):
        self.populacao = sorted(self.populacao, key=lambda populacao: populacao.fitness, reverse=True)

    def geracoes(self):
        melhor = copy.deepcopy(self.populacao[0])
        print("O melhor é ",melhor.fitness)
        totalCrssocer = int(txcrossover*len(self.populacao)/2)
        for i in range(totalCrssocer):
            print("Fazendo o crossover ",i)
        print(len(self.populacao))
        totalMutacao = int(txmutacao * len(self.populacao))
        print(totalMutacao)
        for mutacao in range(totalMutacao):
            print("Fazendo o mutacao ",mutacao)



def main():
    tamanoPop = 50
    geracao = 50
    ngeracao = 0
    a = AG(tamanoPop);
    a.populacao.clear()
    a.init_populacao()
    a.ordena_populacao_maior()
    for i in range(len(a.populacao)):
        print(a.populacao[i].fitness)
    while ngeracao < geracao:
        a.geracoes()

        ngeracao+=1


file = open('dermatology.data', 'r')
results = []
for line in file:
    columns = line.split(",")
    results.append(columns)

# print('Total de %d resultados encontrados: ' % len(results))
# for register in results:
# print(register)
base_treinamento = copy.deepcopy(results[0:172])
base_teste = copy.deepcopy(results[173:258])

# for register in base_treinamento:
# print(register[0])


main()
