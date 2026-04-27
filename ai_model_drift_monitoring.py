import logging
import numpy as np


class ModelDriftMonitoring:
    """
    Provides functionality to monitor and detect statistical drift in data distributions.

    This class is designed for monitoring significant changes (drift) in the statistical properties
    of new data compared to a reference dataset. It helps ensure model reliability by identifying
    situations where the incoming data significantly deviates from the training or reference data.

    :ivar threshold: Maximum allowed drift as a percentage before being flagged. Default is 0.1 (10%).
    :type threshold: float
    :ivar logger: Logger instance for logging drift detection results and debugging information.
    :type logger: logging.Logger
    """

    def __init__(self, threshold=0.1):
        """
        Initialize the ModelDriftMonitoring instance with a threshold for drift detection.

        :param threshold: Maximum allowed drift as a percentage (default is 0.1 or 10%).
        """
        self.threshold = threshold
        self.logger = logging.getLogger("ModelDriftMonitoring")
        self.logger.setLevel(logging.INFO)

    def detect_drift(self, new_data, reference_data):
        """
        Detect statistical drift between incoming data and reference data.

        This method computes the mean percentage drift between datasets and flags significant drift based on
        the configured threshold.

        :param new_data: Incoming data distribution (list or 1-dimensional array of numerical values).
        :param reference_data: Reference data distribution (list or 1-dimensional array of numerical values).
        :return: Boolean indicating whether drift was detected (True) or not (False).
        """
        self.logger.info("Starting drift detection...")
        try:
            if len(new_data) == 0 or len(reference_data) == 0:
                raise ValueError("New data or reference data cannot be empty.")

            # Calculate the mean drift percentage
            mean_diff = abs(np.mean(new_data) - np.mean(reference_data))
            drift_percentage = mean_diff / np.mean(reference_data)

            if drift_percentage > self.threshold:
                self.logger.warning(f"Model drift detected: {drift_percentage:.2%} > {self.threshold:.2%}")
                return True

            self.logger.info(f"No significant drift detected. Drift percentage: {drift_percentage:.2%}")
            return False

        except Exception as e:
            self.logger.error(f"Drift detection failed: {e}")
            return False

    def detect_drift_stats(self, new_data, reference_data):
        """
        Detect drift using advanced statistical metrics such as standard deviation.

        This method calculates and logs both the mean and standard deviation drift percentages for a comprehensive
        assessment.

        :param new_data: Incoming data distribution (list or 1-dimensional array of numerical values).
        :param reference_data: Reference data distribution (list or 1-dimensional array of numerical values).
        :return: Dictionary containing detailed drift statistics (mean drift and std dev drift).
        """
        self.logger.info("Starting detailed statistical drift detection...")
        try:
            if len(new_data) == 0 or len(reference_data) == 0:
                raise ValueError("New data or reference data cannot be empty.")

            # Calculate drift statistics
            mean_diff = abs(np.mean(new_data) - np.mean(reference_data))
            mean_drift = mean_diff / np.mean(reference_data)
            std_diff = abs(np.std(new_data) - np.std(reference_data))
            std_drift = std_diff / np.std(reference_data)

            self.logger.info(f"Mean drift: {mean_drift:.2%}, Std dev drift: {std_drift:.2%}")

            drift_detected = mean_drift > self.threshold
            if drift_detected:
                self.logger.warning(f"Drift detected: Mean drift={mean_drift:.2%}, Threshold={self.threshold:.2%}")
            else:
                self.logger.info("No significant drift detected.")

            return {
                "mean_drift": mean_drift,
                "std_drift": std_drift,
                "drift_detected": drift_detected
            }

        except Exception as e:
            self.logger.error(f"Drift detection failed: {e}")
            return {
                "mean_drift": None,
                "std_drift": None,
                "drift_detected": False
            }


# Example usage of the ModelDriftMonitoring class
if __name__ == "__main__":
    import random

    # Configure logger
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Sample reference data (typically from training)
    reference_data = [random.uniform(10, 12) for _ in range(100)]

    # Sample new incoming data
    new_data = [random.uniform(12, 14) for _ in range(100)]

    # Initialize ModelDriftMonitoring with a custom threshold (e.g., 15%)
    drift_monitor = ModelDriftMonitoring(threshold=0.15)

    # Basic drift detection
    has_drifted = drift_monitor.detect_drift(new_data, reference_data)
    print(f"Drift Detected: {has_drifted}")

    # Get detailed drift statistics
    detailed_stats = drift_monitor.detect_drift_stats(new_data, reference_data)
    print("Detailed Drift Stats:", detailed_stats)