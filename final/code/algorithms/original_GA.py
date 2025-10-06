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
    Helper function to perform roulette wheel selection, given a population of
    individuals, then return p_size parents. 
    '''
        
    # Calculate sum of fitnesses of each individual 
    fit_sum = 0         
    for i in range(len(pop)): 
        fit_sum += func(pop[i]) 

    # Define probabilities of selection
    problt = []
    for i in range(len(pop)): 
        problt.append(func(pop[i])/fit_sum)      

    # Select parents by roulette wheel selection w/ replacement
    parent_pop = np.random.choice(pop, size = len(pop), p = problt, replace = True)

    return parent_pop

def uniform_crossover(func, pop: np.ndarray) -> np.ndarray: 
    '''
    Helper function to perform uniform crossover on each consecutive pair of a
    given population, returning a population where 
    parents are replaced by offspring. 
    '''

    # Initialise population of offspring and loop counter
    crsd_pop = np.zeros(len(pop), dtype = np.ndarray)
    i = 0

    # Loop through each pair in the given parent population 
    while i < len(pop) - 1: 

        # Initialise pair of offsprings 
        child1 = np.zeros(func.meta_data.n_variables, dtype = int)
        child2 = np.zeros(func.meta_data.n_variables, dtype = int)

        # Loop through each element of the parents
        for j in range(func.meta_data.n_variables):
            # Randomly pick each gene of the first offspring from parent pair 
            child1[j] = np.random.choice([pop[i][j], pop[i + 1][j]])

            # Construct second offspring as the inverse of the first 
            if child1[j] == 0: 
                child2[j] = 1
            else: 
                child2[j] = 0

            # Add children to population of offspring 
            crsd_pop[i] = child1 
            crsd_pop[i + 1] = child2 

        # Increment counter
        i += 2

    return crsd_pop 

def mutate(func, ind: np.ndarray) -> np.ndarray:
    '''
    Helper function to perform bit mutation on each individual in a population, where 
    the mutation parameter determines chance of mutating each entire individual. 
    The mutated population is returned. 
    # ('ind' should be 'pop')!
    '''
    pop_size = len(ind)
    n = func.meta_data.n_variables
    mutation_rate = 1 / n #mutation probability

    mutated = ind.copy()
    for i in range(pop_size):
        for j in range(n):
            if np.random.rand() < mutation_rate:
                mutated[i][j] = 1 - mutated[i][j]  # Flip bit
    return mutated

def genetic_algorithm(func, budget = None, p_size = 4): 
    # Assure population size is even 
    if (p_size % 2 != 0 or p_size < 1): 
        print("Invalid population size. Must be even and non-zero")
        return 

    # Define budget (number of function evaluations) of each run: 10^5
    if budget is None:
        budget = int(pow(10, 5))

    # Print default optimum of the given problem 
    if func.meta_data.problem_id == 18 and func.meta_data.n_variables == 32: # for a known problem instance
        optimum = 8
    else:
        optimum = func.optimum.y 
    print(optimum)
    

    # Randomly initialise population of p_size individuals
    pop = np.zeros(p_size, dtype = np.ndarray)
    for i in range(p_size):
        pop[i] = np.random.randint(2, size = func.meta_data.n_variables)

    # 10 independent runs for each algorithm on each problem. 
    for r in range(10):
        f_opt = sys.float_info.min # initialise optimum as the lowest possible value  
        x_opt = None    # initialise corresponding optimum array 

        # Loop of function evaluations: 
        for i in range(budget):
            x = np.random.randint(2, size = func.meta_data.n_variables)  # random array of size n_variables in the range [0, 2)
                                                                         # i.e., randomised binary string
            # f = func(x) # evaluate array x, finding it's optimum

            # Define new population of parents by roulette wheel selection 
            parent_pop = roulette_select(func, pop)

            # Perform uniform crossover on each consecutive pair in the new parent population
            offspring_pop = uniform_crossover(func, parent_pop)

            # Mutate the resulting offspring by some probability 1/p_size 
            m_offspring_pop = mutate(func, offspring_pop)
            pop = m_offspring_pop # Redefine population
            
            # Evaluate population for its optimum (i.e., the highest fitness/value of an individual in the population)
            f = func(pop[0])
            x = pop[0]
            for j in range(p_size):
                if f > func(pop[j]): 
                    f = func(pop[j])
                    x = pop[j]

            if f > f_opt:
                f_opt = f
                x_opt = x

            if f_opt >= optimum:
                break
        
        # Reset function
        func.reset() 

        print(f"Run {r + 1} of complete!")

    # Return optimal fitness/value 'f_opt' and corresponding array 'x_opt' 
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