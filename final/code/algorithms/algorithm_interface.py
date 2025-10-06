import ioh 


class Algorithm:
    """
    Base class (interface/abstract class) for all other algorithms classes in the next exercises.
    """
    def __init__(self, budget: int, name: str = "algorithm_name", algorithm_info: str = "algorithm_info"):
        self.name = name
        self.budget = budget
        self.algorithm_info = algorithm_info

    def __call__(self, problem: ioh.problem.PBO) -> None:
        # This method should be overridden by subclasses to implement specific algorithm logic.
        raise NotImplementedError(f"This method should be overridden by subclasses's __call__() method with the given problem: {problem}.")