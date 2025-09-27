from ioh import get_problem, ProblemClass
from ioh import logger
import sys
import numpy as np

'''
Applying a genetic algorithm to find the optimum solution of some predefined problem 'func'. 
The GA uses uniform crossover, mutation, and a parent population of at least 10 individuals. 
'''

def roulette_select(func, pop: np.ndarray) -> np.ndarray:
    '''
    Roulette wheel selection on a 2D population array (p_size, n_variables).
    Returns a parent population of the same shape.
    '''
    # Ensure 2D
    if pop.ndim != 2:
        pop = np.stack(pop.tolist(), axis=0)

    # Calculate fitness and probabilities
    fitness = np.array([func(ind) for ind in pop], dtype=float)
    total = fitness.sum()
    if total <= 0:
        probs = np.full(len(pop), 1.0 / len(pop))
    else:
        probs = fitness / total

    # Sample indices (not arrays) to avoid "a must be 1-dimensional"
    idx = np.random.choice(len(pop), size=len(pop), p=probs, replace=True)
    parent_pop = pop[idx].copy()
    return parent_pop

def uniform_crossover(func, pop: np.ndarray) -> np.ndarray: 
    '''
    Uniform crossover on consecutive pairs in a 2D population (p_size, n_variables).
    Child2 is defined as the bitwise complement of Child1 (as in your original).
    '''
    if pop.ndim != 2:
        pop = np.stack(pop.tolist(), axis=0)

    n = func.meta_data.n_variables
    crsd_pop = np.empty_like(pop)
    for i in range(0, len(pop) - 1, 2):
        p1, p2 = pop[i], pop[i + 1]
        mask = np.random.randint(0, 2, size=n, dtype=bool)
        child1 = np.where(mask, p1, p2)
        child2 = 1 - child1
        crsd_pop[i] = child1
        crsd_pop[i + 1] = child2
    # If len(pop) is odd (shouldn't be), copy last one through
    if len(pop) % 2 == 1:
        crsd_pop[-1] = pop[-1]
    return crsd_pop 

def mutate(func, pop: np.ndarray) -> np.ndarray:
    '''
    Bit mutation per bit with rate 1/n on a 2D population array.
    '''
    if pop.ndim != 2:
        pop = np.stack(pop.tolist(), axis=0)

    n = func.meta_data.n_variables
    mutation_rate = 1 / n
    mutated = pop.copy()
    for i in range(len(pop)):
        flip = (np.random.rand(n) < mutation_rate)
        mutated[i, flip] = 1 - mutated[i, flip]
    return mutated

def genetic_algorithm(func, budget=None, p_size=4): 
    # Validate population size
    if p_size % 2 != 0 or p_size < 1:
        raise ValueError("Invalid population size. Must be even and >= 2")

    # Define budget (number of function evaluations)
    if budget is None:
        budget = int(pow(10, 5))

    # Determine known optimum
    if func.meta_data.problem_id == 18 and func.meta_data.n_variables == 32:
        optimum = 8
    else:
        optimum = func.optimum.y 
    print(optimum)
    
    n = func.meta_data.n_variables

    # Randomly initialise population of shape (p_size, n)
    pop = np.random.randint(2, size=(p_size, n), dtype=int)

    # 10 independent runs
    for r in range(10):
        f_opt = -np.inf
        x_opt = None

        # Each iteration = one generation here
        for _ in range(budget):
            # Selection
            parent_pop = roulette_select(func, pop)

            # Crossover
            offspring_pop = uniform_crossover(func, parent_pop)

            # Mutation
            pop = mutate(func, offspring_pop)

            # Evaluate population and keep best (maximization)
            fitness = np.array([func(ind) for ind in pop], dtype=float)
            j_best = int(np.argmax(fitness))
            f = float(fitness[j_best])
            x = pop[j_best].copy()

            if f > f_opt:
                f_opt = f
                x_opt = x

            if f_opt >= optimum:
                break
        
        func.reset() 
        print(f"Run {r + 1} of complete!")

    return f_opt, x_opt



# Declaration of problems to be tested; F1 = OneMax; F2 = LeadingOnes; F18 = LABS: 
# dimension = number of variables
# om = get_problem(fid = 1, dimension=100, instance=1, problem_class = ProblemClass.PBO)
# lo = get_problem(fid = 2, dimension=100, instance=1, problem_class = ProblemClass.PBO)
# labs = get_problem(fid = 18, dimension=100, instance=1, problem_class = ProblemClass.PBO)


# Create default logger compatible with IOHanalyzer
# `root` indicates where the output files are stored.
# `folder_name` is the name of the folder containing all output. You should compress this folder and upload it to IOHanalyzer
# l = logger.Analyzer(root="data", 
#     folder_name="run", 
#     algorithm_name="random_search", 
#     algorithm_info="test of IOHexperimenter in python")


# print("Optimising F1: ")
# om.attach_logger(l)
# genetic_algorithm(om)

# ##print("Optimising F2: ")
# lo.attach_logger(l)
# ##genetic_algorithm(lo)

# ##print("Optimising F18: ")
# labs.attach_logger(l)
# ##genetic_algorithm(labs)

# # This statemenet is necessary in case data is not flushed yet.
# del l