from ioh import get_problem, ProblemClass
from ioh import logger
import sys
import numpy as np

# Please replace this `random search` by your `genetic algorithm`.

def random_search(func, budget = None): # Here, func is a predefined optimisation problem, e.g, F1 = OneMax. 
    # budget (number of function evaluations) of each run: 50n^2
    if budget is None:
        budget = int(func.meta_data.n_variables * func.meta_data.n_variables * 50)

    # For a known problem 18 w/ 32 variables, we know optimum = 8
    if func.meta_data.problem_id == 18 and func.meta_data.n_variables == 32:
        optimum = 8
    else:
        optimum = func.optimum.y # otherwise, calculate optimum???
    print(optimum)


    # 10 independent runs for each algorithm on each problem.
    for r in range(10):
        f_opt = sys.float_info.min # initialise optimum value 
        x_opt = None    # initialise optimum array 
        
        # Loop of function evaluations: 
        for i in range(budget):
            x = np.random.randint(2, size = func.meta_data.n_variables)  # random array of size n_variables in the range [0, 2)
                                                                         # i.e., randomised binary string
            f = func(x) # evaluate array x, finding it's optimum
            
            if f > f_opt:
                f_opt = f
                x_opt = x

            if f_opt >= optimum:
                break
        func.reset()
    
    return f_opt, x_opt

# Declaration of problems to be tested; F1 = OneMax; F2 = LeadingOnes; F18 = LABS: 
# dimension = number of variables
om = get_problem(fid = 1, dimension=50, instance=1, problem_class = ProblemClass.PBO)
lo = get_problem(fid = 2, dimension=50, instance=1, problem_class = ProblemClass.PBO)
labs = get_problem(fid = 18, dimension=50, instance=1, problem_class = ProblemClass.PBO)




# Create default logger compatible with IOHanalyzer
# `root` indicates where the output files are stored.
# `folder_name` is the name of the folder containing all output. You should compress this folder and upload it to IOHanalyzer
l = logger.Analyzer(root="data", 
    folder_name="run", 
    algorithm_name="random_search", 
    algorithm_info="test of IOHexperimenter in python")


om.attach_logger(l)
random_search(om)

lo.attach_logger(l)
random_search(lo)

# labs.attach_logger(l)
# random_search(labs)

# This statemenet is necessary in case data is not flushed yet.
del l