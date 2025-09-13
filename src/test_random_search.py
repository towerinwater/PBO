from algorithms import RandomSearch
import ioh
from ioh import ProblemClass
import numpy as np
from config import ALGORITHMS, DIMENSION, PROBLEM_IDS, PROBLEMS_TYPE, REPETITIONS

# Example usage of the RandomSearch algorithm
random_search_algorithm = RandomSearch(budget=1000)


# create a problem instance
problem = ioh.get_problem(
    fid=1, 
    dimension=DIMENSION,
    instance=1,
    problem_class=ProblemClass.PBO  # type: ignore # 
)


random_search_algorithm(problem)