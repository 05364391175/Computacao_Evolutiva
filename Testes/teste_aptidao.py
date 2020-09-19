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
        fitness1 = 100000 - abs((send + more) - money)  # Calcula a avaliação Avaliação
        # print(fitness1)
        return fitness1

a = calcula_fitness([7, 3, 1, 6, 0, 8, 2, 9, 4, 5])
print(a)
contador = 0
while contador < 5:
    print("Teste")
    contador +=1