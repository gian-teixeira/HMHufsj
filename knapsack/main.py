from copy import deepcopy
from random import random, randint
from math import exp
from sys import stdin, argv

class Knapsack:
    class Item:
        def __init__(self, 
                     value,
                     weight, 
                     id):
            self.weight = float(weight)
            self.value = float(value)
            self.id = int(id)

    class Solution(list):
        def flip(self, i):
            copy = deepcopy(self)
            copy[i] = int(not copy[i])
            return copy

        def random_flip(self):
            i = randint(0,len(self)-1)
            return self.flip(i)
        
        @staticmethod
        def empty(size):
            return Knapsack.Solution([0]*size)

        @staticmethod
        def random(size):
            prob = [random() for _ in range(size)]
            discrete = [0 if x < 0.5 else 1 for x in prob]
            return Knapsack.Solution(discrete)
    
    def __init__(self, 
                 items, 
                 max_weight,
                 penaulty):
        self.items = items
        self.nitems = len(items)
        self.max_weight = max_weight
        self.penaulty = penaulty

    def tabu_search(self,
                    initial_solution,
                    max_iterations,
                    tabu_duration):
        assert(tabu_duration < self.nitems)

        solution = initial_solution
        best_solution = initial_solution
        best_fitness = self.fitness(initial_solution)

        tabu_list = [0]*self.nitems
        iteration = 0

        def get_next(solution):
            best_flip = None
            eldest_flip = None
            best_fitness = float("-inf")
            eldest_time = float('inf')
            for i in range(self.nitems):
                if tabu_list[i] < eldest_time:
                    eldest_flip = i
                    eldest_time = tabu_list[i]
                if tabu_list[i] >= iteration:
                    continue
                neighbor = solution.flip(i)
                fitness = self.fitness(neighbor, invalidate = False)
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_flip = i
            if best_flip is None:
                best_flip = eldest_flip
            tabu_list[best_flip] = iteration+tabu_duration
            return solution.flip(best_flip)

        while iteration < max_iterations:
            iteration += 1
            solution = get_next(solution)
            fitness = self.fitness(solution, invalidate = True)
            if fitness > best_fitness:
                best_solution = solution
                best_fitness = fitness
        
        return best_solution, best_fitness

    def simulated_annealing(self, 
                            initial_temperature,
                            cooling_rate,
                            max_iterations,
                            initial_solution):
        solution = initial_solution
        solution_fitness = self.fitness(solution)
        best_solution = solution
        best_fitness = solution_fitness
        current_temperature = initial_temperature

        while current_temperature > 0.01:
            for _ in range(max_iterations):
                neighbor = solution.random_flip()
                neighbor_fitness = self.fitness(neighbor)

                if neighbor_fitness > solution_fitness:
                    solution = neighbor
                    solution_fitness = neighbor_fitness
                    if solution_fitness > best_fitness:
                        best_solution = solution
                        best_fitness = solution_fitness
                else:
                    bound = exp((neighbor_fitness - solution_fitness) / current_temperature)
                    if random() < bound:
                        solution = neighbor
                        solution_fitness = neighbor_fitness
                        
            current_temperature *= cooling_rate

        return best_solution, best_fitness

    def greedy(self):
        sorted_items = sorted(self.items, key = lambda i : -i.value/i.weight)
        weight_counter = 0
        solution = Knapsack.Solution.empty(self.nitems)

        for item in sorted_items:
            if weight_counter + item.weight > self.max_weight:
                break
            weight_counter += item.weight
            solution[item.id] = 1

        return solution
    
    def fitness(self, solution, invalidate = True):
        INVALID = float('-inf')
        value_sum = 0
        weight_sum = 0
        for i in range(self.nitems):
            if solution[i] == 0: continue
            value_sum += self.items[i].value
            weight_sum += self.items[i].weight
        if invalidate and weight_sum > self.max_weight:
            return INVALID
        return value_sum-self.penaulty*max(0,weight_sum-self.max_weight)

    @classmethod
    def read(cls, stream):
        N,W = [int(i) for i in stream.readline().split()]
        items = [Knapsack.Item(*stream.readline().split(),i) for i in range(N)]
        return cls(items,W,0.7)

if __name__ == "__main__":
    instance = Knapsack.read(stdin)
    s0 = instance.greedy()

    if argv[1] == "SA":
        solution = instance.simulated_annealing(initial_temperature = 100,
                                                cooling_rate = 0.95,
                                                max_iterations = 100,
                                                initial_solution = s0)
    else:
        solution = instance.tabu_search(initial_solution = s0,
                                        max_iterations = 100,
                                        tabu_duration = instance.nitems//2+1)
    
    print(solution[1])