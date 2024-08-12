from copy import deepcopy
from sys import argv, stdin
import numpy as np

class TSP:
    class Solution(np.array):
        def swap(self, i, j):
            copy = deepcopy(self)
            copy[i],copy[j] = copy[j],copy[i]
            return copy

        def random_swap(self):
            i = np.random.randint(0,len(self)-1)
            j = np.random.randint(0,len(self)-1)
            return self.flip(i,j)
        
        @staticmethod
        def empty(size):
            return TSP.Solution([0]*size)

        @staticmethod
        def random(size):
            return np.random.permutation(size)

    def __init__(self, n, cities):
        self.n = n
        self.cities = cities
        self.distances = np.array([
            [np.linalg.norm(cities[i]-cities[j]) for j in range(n) ]
            for i in range(n)])

    def tabu_search(self,
                    initial_solution,
                    max_iterations,
                    tabu_duration):
        assert(tabu_duration < self.ncities)

        solution = initial_solution
        best_solution = initial_solution
        best_fitness = self.fitness(initial_solution)

        tabu_list = np.zeros((self.ncities,self.ncities))
        iteration = 0

        def get_next(solution):
            best_swap = None
            eldest_swap = None
            best_fitness = float("inf")
            eldest_time = float('inf')
            for i in range(self.ncities):
                for j in range(i+1,self.ncities):
                    if tabu_list[i,j] < eldest_time:
                        eldest_swap = (i,j)
                        eldest_time = tabu_list[i,j]
                    if tabu_list[i,j] >= iteration:
                        continue
                    neighbor = solution.swap(i,j)
                    fitness = self.fitness(neighbor, invalidate = False)
                    if fitness > best_fitness:
                        best_fitness = fitness
                        best_swap = i
            if best_swap is None:
                best_swap = eldest_swap
            tabu_list[best_swap[0],best_swap[1]] = iteration+tabu_duration
            return solution.swap(best_swap[0], best_swap[1])

        while iteration < max_iterations:
            iteration += 1
            solution = get_next(solution)
            fitness = self.fitness(solution, invalidate = True)
            if fitness < best_fitness:
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
                neighbor = solution.random_swap()
                neighbor_fitness = self.fitness(neighbor)

                if neighbor_fitness < solution_fitness:
                    solution = neighbor
                    solution_fitness = neighbor_fitness
                    if solution_fitness < best_fitness:
                        best_solution = solution
                        best_fitness = solution_fitness
                else:
                    bound = np.exp((neighbor_fitness - solution_fitness) / current_temperature)
                    if np.random.random() < bound:
                        solution = neighbor
                        solution_fitness = neighbor_fitness
                        
            current_temperature *= cooling_rate

        return best_solution, best_fitness
    
    def greedy(self):
        city = np.random.randint(self.ncities)
        solution = TSP.Solution.empty()
        visited = set()

        for i in range(self.ncities):
            assert city is not None

            solution[i] = city
            visited.add(city)
            best_distance = None
            best = None

            for candidate in range(self.ncities):
                if visited[candidate]: continue
                candidate_distance = self.distances[city][candidate]
                if best is None or best_distance > candidate_distance:
                    best_distance = candidate_distance
                    best = candidate

            city = best

        return solution
    
    def fitness(self, solution, invalidate = True):
        distance_sum = 0
        for i in range(0,len(solution)):
            a = solution[i]
            b = solution[(i+1)%len(solution)]
            distance_sum += self.distances[a,b]
        return distance_sum

    @classmethod
    def read(cls, stream):
        n = int(stream.readline())
        cities = np.array([
            [float(i) for i in stream.readline().split()]
            for _ in range(n)])
        
        return TSP(n, cities)

from itertools import permutations

if __name__ == "__main__":
    instance = TSP.read(stdin)
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