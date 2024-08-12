import numpy as np

class SimulatedAnnealingSolver:
    def __init__(self, 
                 initial_temperature,
                 cooling_rate,
                 max_iterations,
                 initial_solution,
                 fitness,
                 neighbor):
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.max_iterations = max_iterations
        self.initial_solution = initial_solution
        self.fitness = fitness
        self.neighbor = neighbor

    def solve(self):
        solution = self.initial_solution
        best_solution = solution
        current_temperature = self.initial_temperature

        while current_temperature > 0.01:
            for _ in range(self.max_iterations):
                neighbor = self.neighbor(solution)

                neighbor_cost = self.fitness(neighbor)
                solution_cost = self.fitness(solution)
                best_cost = self.fitness(best_solution)

                if neighbor_cost < solution_cost:
                    solution = neighbor
                    if solution_cost < best_cost:
                        best_solution = solution
                else:
                    bound = np.exp((solution_cost - neighbor_cost) / current_temperature)
                    if np.random.random() < bound:
                        solution = neighbor
                        
            current_temperature *= self.cooling_rate

        return best_solution, self.fitness(best_solution)