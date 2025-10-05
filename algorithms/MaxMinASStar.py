import ioh
import numpy as np
from .algorithm_interface import Algorithm

class MaxMinASStar(Algorithm):
    """
    Max-Min Ant System (MMAS*) algorithm implementation.
    """
    def __init__(self, 
                 budget: int,
                 name: str = "MaxMinAS*",
                 algorithm_info: str = "Max-Min Ant System Star Algorithm",
                 number_of_ants: int = 10,
                 C: float = 1.0,
                 evaporate_rate: float = 0.01):
        super().__init__(budget, name, algorithm_info)
        self.number_of_ants = number_of_ants
        self.C = C
        self.evaporation_rate = evaporate_rate

    def _local_search(self, solution: np.ndarray, problem: ioh.problem.PBO) -> tuple[np.ndarray, float]:
        """
        Perform a greedy local search on the given solution.
        """
        n = len(solution)
        pivot_solution = solution.copy()
        pivot_fitness = problem(pivot_solution.tolist())

        while problem.state.evaluations < self.budget:
            max_neighbor_fitness = pivot_fitness
            best_neighbor = pivot_solution.copy()
            improve = False

            for i in range(n):
                if problem.state.evaluations >= self.budget:
                    break
                neighbor = pivot_solution.copy()
                neighbor[i] = 1 - neighbor[i]
                neighbor_fitness = problem(neighbor.tolist())

                if neighbor_fitness > max_neighbor_fitness:
                    max_neighbor_fitness = neighbor_fitness
                    best_neighbor = neighbor
                    improve = True

            if improve and max_neighbor_fitness > pivot_fitness:
                pivot_solution = best_neighbor
                pivot_fitness = max_neighbor_fitness
            else:
                break

        return pivot_solution, pivot_fitness

    def __call__(self, problem: ioh.problem.PBO) -> tuple[np.ndarray, float]:
        n = problem.meta_data.n_variables

        # MMAS* pheromone limits
        tau_max = 1 / self.evaporation_rate
        tau_min = tau_max / (2 * n)

        # initialize pheromones
        tau = np.full((n, 2), tau_max, dtype=float)

        # Step 2: construct initial global best
        global_best_solution = np.random.randint(0, 2, size=n)
        global_best_fitness = problem(global_best_solution.tolist())

        delta_tau = self.C

        while problem.state.evaluations < self.budget:
            # construct solutions for all ants
            for _ in range(self.number_of_ants):
                solution = np.zeros(n, dtype=int)
                for i in range(n):
                    if problem.state.evaluations >= self.budget:
                        break
                    p = tau[i, 1] / (tau[i, 0] + tau[i, 1])
                    if np.random.rand() < p:
                        solution[i] = 1

                # apply local search
                solution_vec, solution_fitness = self._local_search(solution, problem)

                # update global best only if strictly better
                if solution_fitness > global_best_fitness:
                    global_best_solution = solution_vec.copy()
                    global_best_fitness = solution_fitness

                if problem.state.evaluations >= self.budget:
                    break

            # update pheromones based on global best
            tau = (1 - self.evaporation_rate) * tau  # evaporation
            for i in range(n):
                bit = global_best_solution[i]
                tau[i, bit] += delta_tau

            # apply pheromone limits
            np.clip(tau, tau_min, tau_max, out=tau)
