import ioh
import numpy as np
from .algorithm_interface import Algorithm

class MaxMinAS(Algorithm):
    """
    Max-Min Ant System (MMAS) algorithm implementation.
    """
    def __init__(self, 
                 budget: int, # number of iteration 
                 name: str = "MaxMinAS",
                 algorithm_info: str = "Max-Min Ant System Algorithm",
                 number_of_ants: int = 10, # at least 10 ants
                 C: float = 1.0, # pheromone deposit ,
                 evaporate_rate: float = 1 # pheromone evaporation rate (rho)
                 ):
        super().__init__(budget, name, algorithm_info)
        self.number_of_ants = number_of_ants
        self.C = C
        self.evaporation_rate = evaporate_rate

        
    def _local_search(self, solution, problem: ioh.problem.PBO) -> tuple[np.ndarray, float]:
        """
        Perform a greedy local search on the given solution.
        
        Args:
            solution (np.ndarray): The current solution to be improved.
        
        Returns:
            tuple: A tuple containing the improved solution and its fitness.
        """
        n = len(solution)
        pivot_solution = solution.copy()
        pivot_fitness = problem(pivot_solution.tolist())

        while problem.state.evaluations < self.budget:
            max_neighbor_fitness = pivot_fitness
            best_neighbor = pivot_solution.copy()
            improve = False

            # check all n neighbors 
            for i in range(n):
                if problem.state.evaluations >= self.budget: # this check is to ensure we do not exceed the budget
                    break
                neighbor = pivot_solution.copy()
                neighbor[i] = 1 - neighbor[i]  # flip the i-th bit

                neighbor_fitness = problem(neighbor.tolist())
                if neighbor_fitness > max_neighbor_fitness:
                    max_neighbor_fitness = neighbor_fitness
                    best_neighbor = neighbor
                    improve = True

            # if a striclty better neighbor is found, move to that neighbor
            if improve and max_neighbor_fitness > pivot_fitness:
                pivot_solution = best_neighbor
                pivot_fitness = max_neighbor_fitness
            else:
                break # local optima found
        return pivot_solution, pivot_fitness

    def __call__(self, problem: ioh.problem.PBO) -> None:
        # Implement the ACO algorithm logic here
        n = problem.meta_data.n_variables

        ### initialise setup
        # use a common MMAS heeuristic for phermone limits 
        tau_max = 1 / self.evaporation_rate 
        tau_min = tau_max / (2 * n)

        # pheromone matrix (n x 2), initialise to tau_max to encourage exploration
        tau = np.full((n,2), tau_max, dtype=float)

        # global best solution initialisation
        global_best_solution = np.random.randint(0, 2, size=n)
        global_best_fitness = problem(global_best_solution.tolist())


        delta_tau = -np.inf
        
        
        ### main loop
        while problem.state.evaluations < self.budget:
            for _ in range(self.number_of_ants):
                # solution construction
                solution = np.zeros(n, dtype=int)

                # probabiltic construction
                for i in range(n):
                    if problem.state.evaluations >= self.budget:
                        break
                    # calculate probabilities for bit 0 and 1
                    sum_tau = tau[i,0] + tau[i,1]
                    p = tau[i,1] / sum_tau  # calcualte probability of bit being 1

                    # probabilitic selection
                    if np.random.rand() < p:
                        solution[i] = 1
                    
                # evaluate and apply local search
                solution_vec, solution_fitness = self._local_search(solution, problem)

                # update global best if needed
                if solution_fitness > global_best_fitness:
                    global_best_solution = solution_vec.copy()
                    global_best_fitness = solution_fitness

                # check budget, if exceeded break before pheromone update
                if problem.state.evaluations >= self.budget:
                    break
                
                ### pheromone update (only for the current ant)
                # evaporation
                tau = (1 - self.evaporation_rate) * tau

                # deposit / reinforment (only on the bits used in the solution)
                delta_tau = self.C # this sets the amount of new pheromone to add

            # pheromone deposit for the global best solution found so far
            for i in range(n):
                if problem.state.evaluations >= self.budget:
                    break
                bit = global_best_solution[i] # 0 or 1
                tau[i, bit] += delta_tau

            # apply pheromone limits
            np.clip(tau, tau_min, tau_max, out=tau)