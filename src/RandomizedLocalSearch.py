import ioh 
import numpy as np 

class RandomizedLocalSearch():
    def __init__(self, budget: int):
        self.budget = budget

    def __call__(self, problem: ioh.problem.PBO) -> None:
        current_sol = np.random.randint(0,2 , size=problem.meta_data.n_variables)
        current_fitness = problem(current_sol.tolist())


        for _ in range(self.budget):
            # create a neighbor by flipping one random bit
            neighbor = current_sol.copy()
            flip_index = np.random.randint(0, problem.meta_data.n_variables)
            neighbor[flip_index] = 1 - neighbor[flip_index]  # Flip a random bit
            neighbor_fitness = problem(neighbor.tolist())
            


            
            # if the neighbor is better or equal, replace current solution
            if neighbor_fitness >= current_fitness:
                current_sol, current_fitness = neighbor, neighbor_fitness



