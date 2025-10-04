from .algorithm_interface import Algorithm
import ioh
import numpy as np


class OnePlusOneEA(Algorithm):
    def __init__(self, budget: int):
        super().__init__(budget, name="(1+1)_EA", algorithm_info="(1+1) Evolutionary Algorithm.")

    def __call__(self, problem: ioh.problem.PBO):
        # Implement the (1+1) EA algorithm logic here
        n = problem.meta_data.n_variables
        # Initialize a random solution
        current = np.random.randint(0, 2, size=n)
        current_fitness = problem(current.tolist())
        
        
        num_evaluations = 0
        while num_evaluations < self.budget:
            offspring = current.copy()
            # flip n bits 
            for i in range(n):
                if np.random.rand() < 1/n:
                    offspring[i] = 1 - offspring[i]

            offspring_fitness = problem(offspring.tolist())
            num_evaluations += 1

            if offspring_fitness >= current_fitness:
                current = offspring
                current_fitness = offspring_fitness