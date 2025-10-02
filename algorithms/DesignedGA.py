from .algorithm_interface import Algorithm
import ioh 
import numpy as np
import sys




class DesignedGA(Algorithm):
    '''
    Applying a genetic algorithm to find the optimum solution of some predefined problem 'func'. 
    The GA follows the generic framework involving uniform crossover, mutation, and a parent population 
    of at least 10 individuals. 
    '''
    def __init__(self, budget: int, population_size: int = 20):
        super().__init__(budget, name="Designed Genetic Algorithm", algorithm_info="A simple genetic algorithm with uniform crossover, mutation and a population of at least 10 individuals.")
        self.population_size = max(population_size, 10)  # Ensure at least 10 individuals
        self.budget = budget 

    def tournament_select(self, func, pop: np.ndarray, sub_size = 8) -> np.ndarray:
        '''
        Helper function to perform tournament selection, given a population of
        individuals, then return p_size parents. 
        '''

        parent_pop = np.zeros(len(pop), dtype=np.ndarray)

        for i in range(len(pop)):
            # Randomly pick subset of individuals
            subset = np.random.choice(pop, size=sub_size, replace=False) 
            
            # Evaluate fitness of the subset
            sub_fitnesses = [func(ind.tolist()) for ind in subset]
            best_idx = np.argmax(sub_fitnesses)
            parent_pop[i] = subset[best_idx]

        return parent_pop

    def uniform_crossover(self, func, pop: np.ndarray, n) -> np.ndarray: 
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
            child1 = np.zeros(n, dtype = int)
            child2 = np.zeros(n, dtype = int)

            # Loop through each element of the parents
            for j in range(n):
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

    def mutate(self, func, pop: np.ndarray, n) -> np.ndarray:
        '''
        Helper function to perform bit mutation on each individual in a population, where 
        the mutation parameter determines chance of mutating each entire individual. 
        The mutated population is returned. 
        '''

        mutation_rate = 3 / n #mutation probability

        mutated = pop.copy()
        for i in range(len(pop)):
            for j in range(n):
                if np.random.rand() < mutation_rate:
                    mutated[i][j] = 1 - mutated[i][j]
        return mutated

    #def genetic_algorithm(func: ioh.problem.PBO, budget = None, p_size = 30): 

    def __call__(self, func: ioh.problem.PBO):

        n = func.meta_data.n_variables

        # Assure population size is even 
        if (self.population_size % 2 != 0 or self.population_size < 1): 
            print("Invalid population size. Must be even and non-zero")
            return 

        # Get optimum of the given problem 
        if func.meta_data.problem_id == 18 and n == 32: # for a known problem instance
            optimum = 8
        else:
            optimum = func.optimum.y 

        # An independent run for each algorithm on each problem. #
        #for r in range(10):
        
        # Randomly initialise population of self.population_size individuals
        pop = np.zeros(self.population_size, dtype = np.ndarray)
        for i in range(self.population_size):
            pop[i] = np.random.randint(2, size = n)
        
        f_opt = sys.float_info.min # initialise optimum as the lowest possible value  
        x_opt = np.zeros(n, dtype = int)    # initialise corresponding optimum array 

        # Loop of function evaluations: 
        while func.state.evaluations < self.budget:

            # Define new population of parents by roulette wheel selection 
            parent_pop = self.tournament_select(func, pop)

            # Perform uniform crossover on each consecutive pair in the new parent population
            offspring_pop = self.uniform_crossover(func, parent_pop, n)

            # Mutate the resulting offspring by some probability 1.5/self.population_size
            m_offspring_pop = self.mutate(func, offspring_pop, n)
            pop = m_offspring_pop # Redefine population

            # Assure elitism
            pop[0] = x_opt
            
            # Evaluate population for its optimum (i.e., the highest fitness/value of an individual in the population)
            fitnesses = [func(ind.tolist()) for ind in pop]
            best_idx = np.argmax(fitnesses)
            f = fitnesses[best_idx]
            x = pop[best_idx]

            if f > f_opt:
                f_opt = f
                x_opt = x

            if f_opt >= optimum:
                break
        
        # Reset function
        # func.reset() 

        # Return optimal fitness/value 'f_opt' and corresponding array 'x_opt' 
        #return f_opt, x_opt 

        
