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
            folder_name=f"ioh-data-{algorithm.name}",
            zip_output=True, 
        )

        experiment.run()
        print(f"=========== Completed experiments for algorithm: {algorithm.name} ========== ")
    print("All experiments completed.")
    print(f"Results are saved in the './data/' directory.")


if __name__ == "__main__":
    main()
