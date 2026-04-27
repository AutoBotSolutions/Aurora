import logging
import numpy as np


class EdgeCaseHandler:
    """
    Handles edge cases in data processing, anomaly detection, and edge case logging.

    The class is designed to provide utility functions for anomaly detection, data source
    validation, missing value handling, and specific edge case management. It includes
    methods to manage operational logs and configurable parameters for these tasks.

    :ivar anomaly_threshold: Threshold for anomaly detection in terms of standard deviations.
    :type anomaly_threshold: float
    :ivar logger: Logger instance for recording operational logs and issues.
    :type logger: logging.Logger
    """

    def __init__(self, anomaly_threshold=3.0):
        """
        Initializes the EdgeCaseHandler with anomaly detection threshold and logging setup.

        :param anomaly_threshold: Number of standard deviations for anomaly detection.
        """
        self.anomaly_threshold = anomaly_threshold
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """
        Configures logging for tracking operations and edge case handling steps.

        :return: Configured logger instance.
        """
        logger = logging.getLogger("EdgeCaseHandler")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def check_data_source_availability(self, file_path):
        """
        Validates that the specified data source is accessible.

        :param file_path: Path to the data file.
        :return: True if the file is accessible, False otherwise.
        """
        try:
            with open(file_path, 'r'):
                self.logger.info(f"Data source available: {file_path}")
                return True
        except FileNotFoundError:
            self.logger.error(f"Data source not found: {file_path}")
            return False

    def detect_outliers(self, data):
        """
        Detects outliers in a numerical dataset using the standard deviation method.

        :param data: List or NumPy array of numerical values.
        :return: List of indices of the detected outliers.
        """
        if not isinstance(data, (list, np.ndarray)):
            self.logger.error("Input data must be a list or NumPy array.")
            return []

        try:
            mean, std = np.mean(data), np.std(data)
            outliers = [i for i, x in enumerate(data) if abs(x - mean) > self.anomaly_threshold * std]
            if outliers:
                self.logger.warning(f"Detected outliers at indices: {outliers}")
            return outliers
        except Exception as e:
            self.logger.error(f"Error during outlier detection: {e}")
            return []

    def handle_missing_values(self, data, strategy="mean"):
        """
        Handles missing values in a dataset using the specified strategy.

        Supported strategies:
          - "mean": Replaces missing values with the mean of available data.
          - "zero": Replaces missing values with 0.
          - "remove": Removes entries with missing values.

        :param data: A list of dictionaries or a pandas DataFrame.
        :param strategy: Strategy for handling missing values ("mean", "zero", "remove").
        :return: Processed dataset with missing values handled.
        """
        self.logger.info("Handling missing values...")
        try:
            if not isinstance(data, list):
                raise ValueError("Input data must be a list of dictionaries.")

            if strategy == "mean":
                values = [d.get("value") for d in data if "value" in d]
                avg_value = sum(values) / len(values) if values else 0
                for record in data:
                    if "value" not in record:
                        record["value"] = avg_value

            elif strategy == "zero":
                for record in data:
                    if "value" not in record:
                        record["value"] = 0

            elif strategy == "remove":
                data = [record for record in data if "value" in record]

            else:
                self.logger.warning(f"Unknown strategy: {strategy}. No changes were made.")

            self.logger.info("Missing value handling complete.")
            return data
        except Exception as e:
            self.logger.error(f"Error during missing value handling: {e}")
            return data

    def handle_edge_case(self, case_id, action="log"):
        """
        Handles specific edge cases using predefined actions.

        Supported actions:
          - "log": Log the edge case occurrence.
          - "notify": Notify an external monitoring system (mocked for now).
          - "fallback": Trigger a fallback mechanism.

        :param case_id: Unique identifier for the edge case.
        :param action: Action to perform ("log", "notify", "fallback").
        """
        if action == "log":
            self.logger.error(f"[Edge Case ID: {case_id}] Logged and flagged.")
        elif action == "notify":
            self.logger.info(f"[Edge Case ID: {case_id}] Notification sent to administrator.")
        elif action == "fallback":
            self.logger.critical(f"[Edge Case ID: {case_id}] Fallback mechanism activated!")
        else:
            self.logger.error(f"Invalid action specified for case {case_id}")


if __name__ == "__main__":
    # Example usage
    handler = EdgeCaseHandler(anomaly_threshold=2.5)

    # Example 1: Check for data file availability
    file_path = "data/missing_file.csv"
    print(f"File Exists: {handler.check_data_source_availability(file_path)}")

    # Example 2: Detect outliers in numerical data
    sample_data = [10, 12, 14, 11, 60, 100, 15]
    outliers = handler.detect_outliers(sample_data)
    print(f"Outlier Indices: {outliers}")

    # Example 3: Handle missing values in a dataset
    dataset = [
        {"id": 1, "value": 10},
        {"id": 2},
        {"id": 3, "value": 30},
    ]
    cleaned_data = handler.handle_missing_values(dataset, strategy="mean")
    print(f"Cleaned Data: {cleaned_data}")

    # Example 4: Respond to an edge case
    handler.handle_edge_case(case_id=42, action="fallback")