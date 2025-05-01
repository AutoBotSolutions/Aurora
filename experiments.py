"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

import logging
import json
from datetime import datetime
import random
import uuid


class Experiment:
    """
    Manages the configuration, logging, and execution of an experiment.

    This class provides tools for repeatedly executing trials within an experiment and logging
    their results. It facilitates the tracking of experiment metadata, runtime, and outcomes.
    Additionally, it offers an extensible structure where subclasses can define specific trial logic.

    :ivar name: Name of the experiment.
    :type name: str
    :ivar metadata: Additional metadata associated with the experiment, such as environmental parameters or timestamps.
    :type metadata: dict
    :ivar logger: Logger instance for recording experiment activity and results.
    :type logger: logging.Logger
    :ivar start_time: Timestamp indicating when the experiment began execution.
    :type start_time: datetime.datetime or None
    :ivar end_time: Timestamp indicating when the experiment completed execution.
    :type end_time: datetime.datetime or None
    """

    def __init__(self, experiment_name, metadata=None):
        """
        Initializes the Experiment class with a name and optional metadata.

        :param experiment_name: Name of the experiment.
        :param metadata: Optional metadata to attach to the experiment (e.g., timestamp, environment details).
        """
        self.name = experiment_name
        self.metadata = metadata or {}
        self.logger = logging.getLogger(f"ExperimentLogger - {self.name}")
        self.setup_logger()
        self.start_time = None
        self.end_time = None

    def setup_logger(self):
        """
        Configures the logger for the experiment.
        """
        handler = logging.FileHandler(f"{self.name}_experiment.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def run(self, trials=10):
        """
        Executes the experiment for a specified number of trials.

        :param trials: Number of trials to run the experiment.
        :return: A list of results for all trials.
        """
        self.start_time = datetime.now()
        self.logger.info(f"Starting experiment: {self.name}")
        self.logger.info(f"Metadata: {self.metadata}")

        results = []
        for trial in range(trials):
            self.logger.info(f"Running trial {trial + 1} out of {trials}")
            try:
                result = self.run_trial(trial)
                results.append(result)
                self.logger.info(f"Trial {trial + 1} result: {result}")
            except Exception as e:
                self.logger.error(f"Error in trial {trial + 1}: {e}")

        self.end_time = datetime.now()
        self.logger.info(f"Experiment {self.name} completed in {self.end_time - self.start_time}")
        return results

    def run_trial(self, trial_number):
        """
        Placeholder for running a single trial. Can be extended by subclasses.

        :param trial_number: The number of the current trial.
        :return: Result of the trial.
        """
        raise NotImplementedError("Subclasses must implement this method to define trial logic.")


class SampleExperiment(Experiment):
    """
    Represents a sample experiment that runs trials and generates random results.

    This class is designed to execute individual trials, typically as part of an
    experimental process. Each trial produces a random integer as its result.

    :ivar trials: The list containing the results of all conducted trials.
    :type trials: list[int]
    :ivar name: The name of the experiment.
    :type name: str
    """

    def run_trial(self, trial_number):
        """
        Executes a single trial and returns a random result.

        :param trial_number: The number of the current trial.
        :return: A random integer as the trial result.
        """
        return random.randint(0, 100)


class ExperimentManager:
    """
    Manages experiment logging by saving configurations and results to a file.

    This class aims to facilitate the organization and tracking of experiments by
    recording their configurations, results, and associated metadata into a log
    file. It allows experiments to be reproducible and their data safely stored
    for further reference and analysis.

    """

    @staticmethod
    def log_experiment(config, results, file_path="experiment_logs.json"):
        """
        Logs configurations and results of an experiment.

        :param config: Dictionary containing experimental configurations.
        :param results: List or dictionary containing experimental results.
        :param file_path: Path to save the experiment logs.
        """
        logging.info("Logging experiment data...")
        try:
            # Add metadata for traceability
            experiment_data = {
                "config": config,
                "results": results,
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "experiment_id": str(uuid.uuid4())
                }
            }
            # Append to the log file in JSON format
            with open(file_path, "a") as log_file:
                json.dump(experiment_data, log_file, indent=4)
                log_file.write("\n")
            logging.info("Experiment data logged successfully.")
        except Exception as e:
            logging.error(f"Failed to log experiment data: {e}")


if __name__ == "__main__":
    # Example usage of the Experiment class
    logging.basicConfig(level=logging.INFO)

    # Define an example experiment
    example_experiment = SampleExperiment("ExampleExperiment", metadata={"author": "OpenSourceContributor"})
    results = example_experiment.run(trials=5)

    # Log the experiment's configuration and results using ExperimentManager
    experiment_config = {
        "name": "ExampleExperiment",
        "trials": 5,
        "metadata": example_experiment.metadata,
    }

    ExperimentManager.log_experiment(experiment_config, results, file_path="experiment_logs.json")

    print("Experiment completed. Results and logs are saved.")
