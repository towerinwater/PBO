from algorithms import RandomSearch, MaxMinAS
import ioh


# 3rd party imports
import numpy as np


# configuration parameters for the experiments
BUDGET = 100000   # maximum number of function evaluations per run (or number of iterations or generations for GAs)
n = DIMENSION = 100   # problem dimension/size (e.g., number of bits for OneMax and LeadingOnes)
REPETITIONS = 10  # number of independent repetitions or runs for each problem
# PROBLEM_IDS = [1, 2, 3, 18, 23, 24, 25]   # problem IDs to be used in the experiments (e.g., 1 -> OneMax, 2 -> LeadingOnes, etc.)
PROBLEM_IDS = [1, 2]   # problem IDs to be used in the experiments (e.g., 1 -> OneMax, 2 -> LeadingOnes, etc.)
PROBLEMS_TYPE = ioh.ProblemClass.PBO  # Pseudo-Boolean Optimization problems


# run mmas on the above problems with different values of rhos below: 
# rho = 1
# rho = 1/sqrt(n)
# rho = 1/n, where n is the problem dimension/size of the problem 

RHOS = [1, 1/(np.sqrt(n)), 1/n]



# a list of algorithm instances to run
# ALGORITHMS = [
#     MaxMinAS(budget=BUDGET,
#               name="MaxMinAS",
#               algorithm_info="Max-Min Ant System with Local Search",
#               number_of_ants=20,
#               Q=1.0,
#               rho=RHOS[0], # pheromone evaporation rate 
#               ),
# ]

# or we can put them all together into one list and run them all


# ALGORITHMS = [
#     MaxMinAS(budget=BUDGET,
#               name="MaxMinAS",
#               algorithm_info="Max-Min Ant System with Local Search",
#               number_of_ants=20,
#               Q=1.0,
#               rho=RHOS[1], # pheromone evaporation rate 
#               ),
# ]

ALGORITHMS = [
    MaxMinAS(budget=BUDGET,
              name="MaxMinAS",
              algorithm_info="Max-Min Ant System with Local Search",
              number_of_ants=20,
              Q=1.0,
              rho=RHOS[2], # pheromone evaporation rate 
              ),
]