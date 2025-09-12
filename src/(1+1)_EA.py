import ioh 
import numpy as np


class OnePlusOneEA: 
    """
    (1+1) EA implementation for pseudo-Boolean optimization
    """
    def __init__(self, budget: int): 
        self.budget = budget
    
    # this __call__() method makes an instance of the class callable like a function. So instead of writing EA_obj.__call__(problem), you can simply write EA_obj(problem).
    def __call__(self, problem: ioh.problem.PBO) -> None:
        current = np.random.randint(0, 2, size=problem.meta_data.n_variables)
        current_fitness: float = problem(current.tolist())
        num_evaluations: int = 1

        while num_evaluations < self.budget:
            offspring = current.copy() 
            for i in range(problem.meta_data.n_variables):
                if np.random.rand() < 1.0 / problem.meta_data.n_variables:
                    offspring[i] = 1 - offspring[i]  # Flip bit

                offspring_fitness = problem(offspring.tolist())
                num_evaluations += 1


                # if the offspring is better or equal, replace parent
                if offspring_fitness >= current_fitness:
                    current, current_fitness = offspring, offspring_fitness
    

