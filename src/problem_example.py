from ioh import get_problem, ProblemClass
from ioh import logger
import sys
import numpy as np

# Please replace this `random search` by your `genetic algorithm`.
def random_search(func, budget = None) -> tuple[int, int, int]:
    # budget of each run: 50n^2
    if budget is None:
        budget = int(func.meta_data.n_variables * func.meta_data.n_variables * 50)

    if func.meta_data.problem_id == 18 and func.meta_data.n_variables == 32:
        optimum = 8
    else:
        optimum = func.optimum.y
    print(optimum)
    # 10 independent runs for each algorithm on each problem.
    for r in range(10):
        f_opt = sys.float_info.min
        x_opt = None
        for i in range(budget):
            x = np.random.randint(2, size = func.meta_data.n_variables)
            f = func(x)
            if f > f_opt:
                f_opt = f
                x_opt = x
            if f_opt >= optimum:
                break
        func.reset()
    return f_opt, x_opt, optimum

# Declaration of problems to be tested.
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

# This is used for exporting the .csv result to the IOHanalyzer
results = []

om.attach_logger(l)
results.append(random_search(om)[2])

lo.attach_logger(l)
results.append(random_search(lo)[2])

labs.attach_logger(l)
results.append(random_search(labs)[2])

np.savetxt("data.csv", results, fmt = "%1.3f", delimiter = ',', newline = '\n')

# This statemenet is necessary in case data is not flushed yet.
del l