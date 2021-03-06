"""
Module Docstring:
A description of your program goes here
"""

from copy import deepcopy
import numpy as np

class Chromosome():
    """
    Description of class `Chromosome` goes here
    """
    def __init__(self, genes, id_=None, fitness=-1):
        self.id_ = id_
        self.genes = genes
        self.fitness = fitness

    def describe(self):
        """
        Prints the ID, fitness, and genes
        """
        #print('ID=#{}, fitenss={}, \ngenes=\n{}'.format(self.id, self.fitness, self.genes))
        print(f"ID=#{self.id_}, Fitness={self.fitness}, \nGenes=\n{self.genes}")

    def get_chrom_length(self):
        """
        Returns the length of `self.genes`
        """
        return len(self.genes)

def cycle_crossover(pc):
    """
    This function takes two parents, and performs Cycle crossover on them.
    pc: The probability of crossover (control parameter)
    """
    parent_one = Chromosome(genes=np.array([8, 4, 2, 6, 1, 3, 5, 9, 0, 7]), id_=0, fitness=125.2)
    parent_two = Chromosome(genes=np.array([8, 4, 2, 6, 1, 3, 5, 9, 0, 7]), id_=1, fitness=125.2)
    chrom_length = Chromosome.get_chrom_length(parent_one)
    print("\nParents")
    print("=================================================")
    Chromosome.describe(parent_one)
    Chromosome.describe(parent_two)
    child_one = Chromosome(genes=np.array([-1] * chrom_length), id_=0, fitness=125.2)
    child_two = Chromosome(genes=np.array([-1] * chrom_length), id_=1, fitness=125.2)

    if np.random.random() < pc:  # if pc is greater than random number
        p1_copy = parent_one.genes.tolist()
        p2_copy = parent_two.genes.tolist()
        swap = True
        count = 0
        pos = 0

        while True:
            if count > chrom_length:
                break
            for i in range(chrom_length):
                if child_one.genes[i] == -1:
                    pos = i
                    break

            if swap:
                while True:
                    child_one.genes[pos] = parent_one.genes[pos]
                    count += 1
                    pos = parent_two.genes.tolist().index(parent_one.genes[pos])
                    if p1_copy[pos] == -1:
                        swap = False
                        break
                    p1_copy[pos] = -1
            else:
                while True:
                    child_one.genes[pos] = parent_two.genes[pos]
                    count += 1
                    pos = parent_one.genes.tolist().index(parent_two.genes[pos])
                    if p2_copy[pos] == -1:
                        swap = True
                        break
                    p2_copy[pos] = -1

        for i in range(chrom_length): #for the second child
            if child_one.genes[i] == parent_one.genes[i]:
                child_two.genes[i] = parent_two.genes[i]
            else:
                child_two.genes[i] = parent_one.genes[i]

        for i in range(chrom_length): #Special mode
            if child_one.genes[i] == -1:
                if p1_copy[i] == -1: #it means that the ith gene from p1 has been already transfered
                    child_one.genes[i] = parent_two.genes[i]
                else:
                    child_one.genes[i] = parent_one.genes[i]

    else:  # if pc is less than random number then don't make any change
        child_one = deepcopy(parent_one)
        child_two = deepcopy(parent_two)
    return child_one, child_two

if __name__ == '__main__':

    CROSS = cycle_crossover(1)
    print("\nChildren")
    print("=================================================")
    for index, _ in enumerate(CROSS):
        Chromosome.describe(CROSS[index])