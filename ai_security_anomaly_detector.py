"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

"""
ai_security_anomaly_detector.py

This module provides a lightweight and effective solution for detecting anomalies in access logs,
user behavior, and activity data. It uses statistical methods (Z-score) for outlier detection
and serves as a first line of defense against unauthorized or irregular activities.

Author: G.O.D Framework Team (Open Source Community)
License: MIT
Version: 1.0.0
"""

import numpy as np
import logging


class SecurityAnomalyDetector:
    """
    Detects and explains anomalies in numerical data using statistical methods.

    This class provides functionality to identify anomalies based on Z-scores,
    allowing for detection of outliers in given numerical datasets. It also
    offers detailed explanations for detected anomalies.

    :ivar logger: Logging instance used for logging system messages and errors.
    :type logger: logging.Logger
    """

    def __init__(self):
        """
        Initialize the SecurityAnomalyDetector with logging.
        """
        logging.info("SecurityAnomalyDetector initialized.")

    def detect_anomaly(self, data, threshold=3.0):
        """
        Identifies anomalies in numerical data using Z-score outlier detection.

        Args:
            data (list or numpy.ndarray): A list or array of numerical values.
            threshold (float): Z-score threshold beyond which data points are considered anomalies.

        Returns:
            list: A list of data values identified as anomalies.
        """
        try:
            data = np.array(data)
            mean = np.mean(data)
            std_dev = np.std(data)

            logging.info(f"Data mean: {mean}, Standard Deviation: {std_dev}")

            if std_dev == 0:
                logging.warning("Standard deviation is zero, unable to calculate Z-scores.")
                return []

            anomalies = [x for x in data if abs((x - mean) / std_dev) > threshold]
            logging.info(f"Detected {len(anomalies)} anomalies.")
            return anomalies
        except Exception as e:
            logging.error(f"Error during anomaly detection: {e}")
            return []

    def explain_anomalies(self, data, anomalies):
        """
        Provides an explanation of the anomalies in the given data set.

        Args:
            data (list or numpy.ndarray): The original data set.
            anomalies (list): A list of anomalies detected.

        Returns:
            dict: A dictionary containing details of the anomalies and their Z-scores.
        """
        try:
            data = np.array(data)
            mean = np.mean(data)
            std_dev = np.std(data)

            if std_dev == 0:
                logging.warning("Standard deviation is zero, explanation is not possible.")
                return {"message": "Standard deviation is zero, cannot calculate Z-scores."}

            result = {}
            for anomaly in anomalies:
                z_score = abs((anomaly - mean) / std_dev)
                result[anomaly] = {
                    "z_score": z_score,
                    "deviation_from_mean": abs(anomaly - mean)
                }

            logging.info(f"Explanation generated for {len(anomalies)} anomalies.")
            return result
        except Exception as e:
            logging.error(f"Error generating anomaly explanations: {e}")
            return {"error": str(e)}


if __name__ == "__main__":
    # Configuring logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Example data set representing user activity (e.g., login counts)
    data = [10, 12, 10, 11, 120, 11, 9, 10, 12, 11]

    # Initialize anomaly detector
    detector = SecurityAnomalyDetector()

    # Detect anomalies
    threshold = 3.0  # Default threshold
    anomalies = detector.detect_anomaly(data, threshold=threshold)
    print(f"Anomalies detected (Threshold {threshold}): {anomalies}")

    # Explain anomalies
    if anomalies:
        explanations = detector.explain_anomalies(data, anomalies)
        print("\nExplanation of anomalies:")
        for point, details in explanations.items():
            print(f"  - Value: {point}, Z-Score: {details['z_score']:.2f}, Deviation: {details['deviation_from_mean']}")
