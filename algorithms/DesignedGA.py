from .algorithm_interface import Algorithm
import ioh 
import numpy as np




class DesignedGA(Algorithm):
    '''
    Applying a genetic algorithm to find the optimum solution of some predefined problem 'func'. 
    The GA follows the generic framework involving uniform crossover, mutation, and a parent population 
    of at least 10 individuals. 
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
        


