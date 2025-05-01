"""
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT (or choose your open-source license)
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

import logging
from typing import List


def setup_logging(level: int = logging.INFO, log_file: str = None) -> None:
    """
    Configures the logging system for the application.

    This function sets up the logging system with a specified logging level and
    optional log file. If a log file is provided, log messages will be written
    both to the file and to the console. Otherwise, log messages will only be
    displayed in the console. The logging format includes the timestamp, log
    level, and the log message.

    :param level: The logging level for the logger.
    :param log_file: The file path for the log file. If None, logs will only
        be written to the console.
    :return: None
    """
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=handlers
    )


def detect_anomalies(data: List[float], threshold: float = 3.0) -> List[float]:
    """
    Detect anomalies in a given dataset by identifying values that deviate significantly
    from the mean, using a specified threshold. This function calculates the mean
    and standard deviation of the input data and flags values beyond a certain limit
    as anomalies. Results and process details are logged for transparency and traceability.

    :param data: The dataset to analyze, represented as a list of floating-point numbers.
    :type data: List[float]
    :param threshold: The sensitivity threshold for anomaly detection (default is 3.0).
                      Higher values reduce sensitivity while lower values increase it.
    :type threshold: float, optional
    :return: A list of anomalies detected in the input data. Anomalies are values that
             lie outside the range of `mean ± threshold * standard deviation`. If the
             input data is empty, an empty list is returned.
    :rtype: List[float]
    """
    logging.info("Starting anomaly detection...")

    if not data:
        logging.warning("Input data is empty. No anomalies detected.")
        return []

    try:
        # Calculate statistical parameters (mean and standard deviation)
        mean = sum(data) / len(data)
        variance = sum((x - mean) ** 2 for x in data) / len(data)
        std_dev = variance ** 0.5

        # Detect anomalies (values outside the range of threshold * std_dev from mean)
        anomalies = [x for x in data if abs(x - mean) > threshold * std_dev]

        # Log results
        logging.info(f"Data mean: {mean:.2f}, Standard deviation: {std_dev:.2f}")
        logging.info(f"Anomalies detected: {anomalies}")

        return anomalies

    except Exception as e:
        logging.error(f"An error occurred during anomaly detection: {e}")
        return []


if __name__ == "__main__":
    # Configure default logging
    setup_logging(log_file="anomaly_detection.log")

    # Example dataset with anomalies
    example_data = [10, 12, 15, 10, 11, 14, 120, 12, 9, -45]

    logging.info("Example dataset loaded. Running anomaly detection...")
    detected_anomalies = detect_anomalies(example_data, threshold=3.0)

    if detected_anomalies:
        logging.info(f"Final detected anomalies: {detected_anomalies}")
    else:
        logging.info("No anomalies were detected in the dataset.")
