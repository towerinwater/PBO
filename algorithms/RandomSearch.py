from .algorithm_interface import Algorithm
import ioh
import numpy as np

class RandomSearch(Algorithm):
    def __init__(self, budget: int):
        super().__init__(budget, name="Random Search", algorithm_info="Naïve random search algorithm.")


    def __call__(self, problem: ioh.problem.PBO): # this overrides the __call__ method in the Algorithm class
        for _ in range(self.budget):
            X: np.ndarray = np.random.randint(2, size=problem.meta_data.n_variables)
            problem(X.tolist())




# RS_obj = RandomSearch(budget=1000)
# n = 10 
# # print(RS_obj.name)
# p1 = ioh.get_problem(fid=1, 
#                     dimension=n,
#                     instance=1,
#                     problem_class=ProblemClass.PBO)  # type: ignore # 
# RS_obj(p1)  # calling the __call__ method of the RandomSearch class (will not work if the __call__ method is not implemented)
# if the __call__ method is not implemented, it will call the __call__ method of the Algorithm class which raises NotImplementedError