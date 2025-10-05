import ioh
import numpy as np
from .algorithm_interface import Algorithm


class ACO(Algorithm):
    """
    Ant Colony Optimization (ACO) algorithm implementation.
    """
    def __init__(self,
                 budget: int, # number of iteration
                 name: str = "CustomACO",
                 algorithm_info: str = "Custom Ant Colony Optimization Algorithm",
                 number_of_ants: int = 10, # at least 10 ants
                 C: float = 1.0, # pheromone deposit ,
                 evaporate_rate: float = 0.01, # pheromone evaporation rate (rho)
                 local_search_prob: float = 0.6, # probability of applying local search on a solution
                 top_ants_rate: float = 0.2 # fraction of best ants will be used to update pheromone
                 ):
        super().__init__(budget, name, algorithm_info)
        self.number_of_ants = number_of_ants
        self.C = C
        self.evaporation_rate = evaporate_rate
        self._local_search_prob = local_search_prob
        self.top_ants_rate = top_ants_rate


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


        while True:
            max_neighbor_fitness = pivot_fitness
            best_neighbor = pivot_solution.copy()
            improve = False


            # check all n neighbors
            for i in range(n):
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


        ### main loop
        while problem.state.evaluations < self.budget:
            ant_solutions = []
            ant_fitnesses = []


            for ant in range(self.number_of_ants):
                # solution construction
                solution = np.zeros(n, dtype=int)


                # probabiltic construction
                for i in range(n):
                    # calculate probabilities for bit 0 and 1
                    sum_tau = tau[i,0] + tau[i,1]
                    p = tau[i,1] / sum_tau  # calcualte probability of bit being 1


                    # probabilitic selection
                    if np.random.rand() < p:
                        solution[i] = 1


                # evaluate and apply local search based on probability
                if np.random.rand() < self._local_search_prob:
                    solution_vec, solution_fitness = self._local_search(solution, problem)
                else:
                    solution_vec = solution
                    solution_fitness = problem(solution_vec.tolist())
               
                ant_solutions.append(solution_vec)
                ant_fitnesses.append(solution_fitness)


                # update global best if needed
                if solution_fitness > global_best_fitness:
                    global_best_solution = solution_vec.copy()
                    global_best_fitness = solution_fitness


                # check budget, if exceeded break before pheromone update
                if problem.state.evaluations >= self.budget:
                    break
               
            ### pheromone update (with multiple ants)
            # evaporation
            tau = (1 - self.evaporation_rate) * tau


            # pick top ants
            num_top_ants = max(1, int(self.top_ants_rate * len(ant_fitnesses)))
            top_indices = np.argsort(ant_fitnesses)[-num_top_ants:] # indices of the best ants


            for index in top_indices:
                sol = ant_solutions[index]
                for i in range(n):
                    tau[i, sol[i]] += self.C / num_top_ants # distribute pheromone deposit among top ants


            # apply pheromone limits
            np.clip(tau, tau_min, tau_max, out=tau)




