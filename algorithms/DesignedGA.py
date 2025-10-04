from .algorithm_interface import Algorithm
import ioh 
import numpy as np




class DesignedGA(Algorithm):
    '''
    Applying a genetic algorithm to find the optimum solution of some predefined problem 'func'. 
    The GA uses uniform crossover, mutation, and a parent population of at least 10 individuals. 
    '''
    def __init__(self, budget: int, population_size: int = 20, mutation_rate: float = 0.01):
        super().__init__(budget, name="Designed Genetic Algorithm", algorithm_info="A simple genetic algorithm with uniform crossover, mutation and a population of at least 10 individuals.")
        self.population_size = max(population_size, 10)  # Ensure at least 10 individuals
        self.mutation_rate = mutation_rate

    def initialize_population(self, n_variables: int) -> np.ndarray:
        """Initialize a random population."""
        return np.random.randint(2, size=(self.population_size, n_variables))

    def roulette_select(self, population: np.ndarray, fitness: np.ndarray) -> np.ndarray:
        """Roulette wheel selection."""
        fitness_sum = np.sum(fitness)
        if fitness_sum == 0:
            probabilities = np.ones(len(fitness)) / len(fitness)
        else:
            probabilities = fitness / fitness_sum
        selected_indices = np.random.choice(len(population), size=self.population_size, p=probabilities)
        return population[selected_indices]

    def uniform_crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> np.ndarray:
        """
        Perform uniform crossover between two parents. 
        """
        mask = np.random.rand(len(parent1)) < 0.5
        offspring = np.where(mask, parent1, parent2)
        return offspring
    
    
    def mutate(self, individual: np.ndarray) -> np.ndarray:
        mutation_mask = np.random.rand(len(individual)) < self.mutation_rate
        individual[mutation_mask] = 1 - individual[mutation_mask]  # Flip bits
        return individual

    def __call__(self, func: ioh.problem.PBO):
        n = func.meta_data.n_variables
        # if self.budget is None or self.budget <= 0:
        #     self.budget = int(50 * (n ** 2))  # Default budget = 50n^2 if not set or invalid (n is the dimension or size of the problem)
        # p_id = func.meta_data.problem_id
        # optimum = 0
        # if p_id == 18 or p_id == 32:
        #     optimum = 8
        # else: 
        #     optimum = func.optimum.y
        # print(f"Initial optimum for problem {p_id}: {optimum}")

        # population = self.initialize_population(self.population_size)

        # for _ in range(self.budget):
        #     X: np.ndarray = np.random.randint(2, size=func.meta_data.n_variables)
        #     func(X.tolist()) # evaluate the random solution

        #     # evaluate fitness for each individual in the population
        #     fitness = np.array([func(ind.tolist()) for ind in population])
        #     # define a population of parents by roulette wheel selection
        #     parent_pop = self.roulette_select(population, fitness)

        #     # perform uniform crossover on each consecutive pair in the new parent population 
        #     offspring_pop = self.uniform_crossover(parent_pop[::2], parent_pop[1::2])


        #     # mutate the offspring population by some probability 1/p_size 
        #     mutated_offspring_pop = np.array([self.mutate(ind) for ind in offspring_pop])
        #     population = mutated_offspring_pop  # redefine the population for the next generation

        #     X = population[0]  # take the first individual in the population
        #     f = func(X.tolist())
        #     for j in range(1, self.population_size):
        #         f = func(population[j].tolist())
        #         if f >= optimum:
        #             print(f"Optimum {optimum} found for problem {p_id}")
        #             return
        


