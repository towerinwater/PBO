from algorithms import RandomSearch, MaxMinAS, DesignedGA, ACO
import ioh


# configuration parameters for the experiments
BUDGET = 100000   # maximum number of function evaluations per run (or number of iterations or generations for GAs)
DIMENSION = 100   # problem dimension/size (e.g., number of bits for OneMax and LeadingOnes)
REPETITIONS = 10  # number of independent repetitions or runs for each problem
# PROBLEM_IDS = [1, 2, 3, 18, 23, 24, 25]   # problem IDs to be used in the experiments (e.g., 1 -> OneMax, 2 -> LeadingOnes, etc.)
PROBLEM_IDS = [1, 2, 3, 18, 23, 24, 25]   # problem IDs to be used in the experiments (e.g., 1 -> OneMax, 2 -> LeadingOnes, etc.)
PROBLEMS_TYPE = ioh.ProblemClass.PBO  # Pseudo-Boolean Optimization problems





# a list of algorithm instances to run 
ALGORITHMS = [
    # # RandomSearch(budget=BUDGET),
    # # MaxMinAS(budget=BUDGET)
    # OnePlusOneEA(budget=BUDGET),
    # # RandomizedLocalSearch(budget=BUDGET),
    DesignedGA(budget=BUDGET, population_size=44, mutation_rate=0.01)
    ACO(budget=BUDGET)
]