from .algorithm_interface import Algorithm
from .OnePlusOneEA import OnePlusOneEA
from .RLS import RandomizedLocalSearch
from .RandomSearch import RandomSearch
from .DesignedGA import DesignedGA
from .MaxMinAS import MaxMinAS
from .MaxMinASStar import MaxMinASStar
from .ACO import ACO



# Some comments: 
# This file will make the "algorithms" directory a package and 
# will allow us to import the classes from other files in this directory.

# It's useful because no matter which file we are in, we can always do:
# from algorithms import OnePlusOneEA, RandomizedLocalSearch, RandomSearch, DesignedGA
# instead of worrying about the relative paths ...


# Starting point for everyone completing the next exercises: 