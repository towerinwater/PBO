import config 
import ioh 


def main():
    """
    Main execution function to **run** all configured algorithms on specified problems.
    """

    print("Starting experiments...")

    for algorithm in config.ALGORITHMS:
        print(f"=========== Running experiments for algorithm: {algorithm.name} ========== ")
        # create a new experiment for the current algorithm 
        experiment = ioh.Experiment(
            algorithm=algorithm,
            algorithm_name=algorithm.name,
            algorithm_info=algorithm.algorithm_info,
            fids = config.PROBLEM_IDS,
            iids = [1], 
            dims=[config.DIMENSION],
            reps=config.REPETITIONS,
            problem_class=config.PROBLEMS_TYPE,  # Use the configured problem class # type: ignore
            old_logger=False,  # type: ignore
            output_directory="./data/",
            # folder_name=f"ioh-data-{algorithm.name}-{algorithm.evaporation_rate}", ======= This is temp for MMAS family only
            folder_name=f"ioh-data-{algorithm.name}",
            zip_output=True, 
        )

        experiment.run()
        print(f"=========== Completed experiments for algorithm: {algorithm.name} ========== ")
    print("All experiments completed.")
    print(f"Results are saved in the './data/' directory.")


if __name__ == "__main__":
    main()




# Example usage:
# Suppose we want to test 2 algorithms: Random Search and RLS on 3 problems: OneMax, LeadingOnes, and N-Queens.
# 2 * 3 = 6 data files will be generated. 
# To pass ALL of this data into the IOHProfiler (https://iohanalyzer.liacs.nl/), the following procedure can be used:
# Simplest: Compress the /data directory into a single zip file. And then pass the zip file to the IOHProfiler. Then we just need to click on the "Fixed Budget Results" tab to see the results.
# Or, we can zip each data file one by one and then pass them into (in no particular order) the IOHProfiler ... 
#