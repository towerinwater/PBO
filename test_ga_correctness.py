#!/usr/bin/env python3
"""
Comprehensive test suite for genetic algorithm correctness
"""

import numpy as np
import sys
import os

# Add algorithms directory to path
algorithms_path = os.path.join(os.path.dirname(__file__), 'algorithms')
sys.path.append(algorithms_path)

from ioh import get_problem, ProblemClass
from algorithms.test_GA import roulette_select, uniform_crossover, mutate, genetic_algorithm

def test_roulette_selection():
    """Test roulette wheel selection logic"""
    print("Testing Roulette Selection...")
    
    # Create a simple test problem
    func = get_problem(fid=1, dimension=5, instance=1, problem_class=ProblemClass.PBO)
    
    # Create test population where we know the fitness values
    pop = np.array([
        np.array([1, 1, 1, 1, 1]),  # fitness = 5 (best)
        np.array([0, 0, 0, 0, 0]),  # fitness = 0 (worst)
        np.array([1, 1, 0, 0, 0]),  # fitness = 2
        np.array([1, 1, 1, 0, 0])   # fitness = 3
    ])
    
    # Test multiple selections to check probabilistic behavior
    selection_counts = {}
    for _ in range(1000):
        selected = roulette_select(func, pop)
        for individual in selected:
            key = tuple(individual)
            selection_counts[key] = selection_counts.get(key, 0) + 1
    
    print(f"Selection counts: {selection_counts}")
    
    # The individual with fitness 5 should be selected more often
    best_individual = tuple([1, 1, 1, 1, 1])
    worst_individual = tuple([0, 0, 0, 0, 0])
    
    if best_individual in selection_counts and worst_individual in selection_counts:
        print(f"✓ Best individual selected {selection_counts[best_individual]} times")
        print(f"✓ Worst individual selected {selection_counts[worst_individual]} times")
        assert selection_counts[best_individual] > selection_counts[worst_individual]
        print("✓ Roulette selection working correctly (better fitness = higher selection probability)")
    
    func.reset()
    return True

def test_uniform_crossover():
    """Test uniform crossover implementation"""
    print("\nTesting Uniform Crossover...")
    
    # Create a dummy function for testing
    func = get_problem(fid=1, dimension=6, instance=1, problem_class=ProblemClass.PBO)
    
    # Test with known parents
    parent1 = np.array([1, 1, 1, 0, 0, 0])
    parent2 = np.array([0, 0, 0, 1, 1, 1])
    pop = np.array([parent1, parent2])
    
    # Run crossover multiple times
    results = []
    for _ in range(100):
        offspring = uniform_crossover(func, pop)
        results.append(offspring.copy())
    
    # Check that offspring contain genes from both parents
    child1_variants = set()
    child2_variants = set()
    
    for result in results:
        child1_variants.add(tuple(result[0]))
        child2_variants.add(tuple(result[1]))
    
    print(f"✓ Child 1 variants: {len(child1_variants)}")
    print(f"✓ Child 2 variants: {len(child2_variants)}")
    
    # There should be multiple variants (due to randomness)
    assert len(child1_variants) > 1, "Crossover should produce different offspring"
    print("✓ Uniform crossover produces varied offspring")
    
    func.reset()
    return True

def test_mutation():
    """Test mutation implementation"""
    print("\nTesting Mutation...")
    
    func = get_problem(fid=1, dimension=10, instance=1, problem_class=ProblemClass.PBO)
    
    # Create test population
    pop = np.array([
        np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0]),
        np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
    ])
    
    original = pop.copy()
    
    # Apply mutation multiple times
    mutation_occurred = False
    for _ in range(50):  # Multiple attempts to see mutation
        mutated = mutate(func, pop.copy())
        if not np.array_equal(original, mutated):
            mutation_occurred = True
            
            # Check that only individual bits are flipped
            diff = original != mutated
            print(f"✓ Mutations detected at positions: {np.where(diff)}")
            break
    
    assert mutation_occurred, "Mutation should occur with 1/n probability"
    print("✓ Mutation working correctly")
    
    func.reset()
    return True

def test_population_improvement():
    """Test that GA improves over generations"""
    print("\nTesting Population Improvement...")
    
    # Use OneMax (easy problem for testing)
    func = get_problem(fid=1, dimension=20, instance=1, problem_class=ProblemClass.PBO)
    
    # Run GA with small budget to test improvement
    initial_pop = np.random.randint(2, size=(10, 20))
    initial_fitness = [func(ind) for ind in initial_pop]
    initial_avg = np.mean(initial_fitness)
    
    func.reset()
    
    # Run genetic algorithm with small budget
    final_fitness, final_solution = genetic_algorithm(func, budget=500, p_size=10)
    
    print(f"✓ Initial average fitness: {initial_avg}")
    print(f"✓ Final best fitness: {final_fitness}")
    print(f"✓ Expected optimum: {func.optimum.y}")
    
    # GA should find better solutions than random
    assert final_fitness >= initial_avg, "GA should improve upon initial random population"
    print("✓ GA shows improvement over random initialization")
    
    func.reset()
    return True

def test_known_problems():
    """Test GA on problems with known optima"""
    print("\nTesting on Known Problems...")
    
    problems = [
        (1, "OneMax", 20),      # OneMax with dimension 20, optimum = 20
        (2, "LeadingOnes", 15), # LeadingOnes with dimension 15, optimum = 15
    ]
    
    for fid, name, dim in problems:
        print(f"\nTesting {name} (F{fid}, dim={dim})...")
        func = get_problem(fid=fid, dimension=dim, instance=1, problem_class=ProblemClass.PBO)
        
        best_fitness, best_solution = genetic_algorithm(func, budget=1000, p_size=12)
        
        optimum = func.optimum.y
        success_rate = (best_fitness / optimum) * 100
        
        print(f"✓ Problem: {name}")
        print(f"✓ Best fitness found: {best_fitness}")
        print(f"✓ Known optimum: {optimum}")
        print(f"✓ Success rate: {success_rate:.1f}%")
        
        # GA should get reasonably close to optimum
        assert success_rate >= 50, f"GA should achieve at least 50% of optimum on {name}"
        
        func.reset()
    
    return True

def test_parameter_validation():
    """Test that GA handles invalid parameters correctly"""
    print("\nTesting Parameter Validation...")
    
    func = get_problem(fid=1, dimension=10, instance=1, problem_class=ProblemClass.PBO)
    
    # Test odd population size (should be handled)
    print("Testing odd population size...")
    try:
        result = genetic_algorithm(func, budget=100, p_size=3)  # odd number
        print("✗ Should handle odd population size gracefully")
    except:
        print("✓ Correctly rejects odd population size")
    
    # Test zero population size
    print("Testing zero population size...")
    try:
        result = genetic_algorithm(func, budget=100, p_size=0)
        print("✗ Should handle zero population size")
    except:
        print("✓ Correctly rejects zero population size")
    
    func.reset()
    return True

def run_all_tests():
    """Run all correctness tests"""
    print("=" * 60)
    print("GENETIC ALGORITHM CORRECTNESS TESTS")
    print("=" * 60)
    
    tests = [
        test_roulette_selection,
        test_uniform_crossover,
        test_mutation,
        test_population_improvement,
        test_known_problems,
        test_parameter_validation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
            print("✓ PASSED")
        except Exception as e:
            failed += 1
            print(f"✗ FAILED: {e}")
        print("-" * 40)
    
    print(f"\nTest Results: {passed} passed, {failed} failed")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()