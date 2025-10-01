import config_mmas_mmass as config
import ioh 
import time 

def main():
    """
    Main execution function to **run** all configured algorithms on specified problems.
    """

    print("Starting experiments...")
    # set timers
    start_time = time.time()
    for algorithm in config.ALGORITHMS:
        print(f"=========== Running experiments for algorithm: {algorithm.name} ========== ")
        # create a new experiment for the current algorithm 
        experiment = ioh.Experiment(
            algorithm=algorithm,
            algorithm_name=f"{algorithm.name}-r{algorithm.rho}",
            algorithm_info=algorithm.algorithm_info,
            fids = config.PROBLEM_IDS,
            iids = [1], 
            dims=[config.DIMENSION],
            reps=config.REPETITIONS,
            problem_class=config.PROBLEMS_TYPE,  # Use the configured problem class # type: ignore
            old_logger=False,  # type: ignore
            output_directory="./mmas-data/",
            folder_name=f"ioh-data-{algorithm.name}-r{algorithm.rho}",
            zip_output=True, 
            merge_output=False, # outputs each data file separately
        )

        experiment.run()
        print(f"=========== Completed experiments for algorithm: {algorithm.name} ========== ")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("All experiments completed.")
    print(f"Results are saved in the './mmas-data/' directory (in the root of this project).")
    print(f"Total elapsed time for all experiments: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()


