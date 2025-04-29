"""
AI Life Connection
===================

This module connects AI systems to real-world physiological and natural data,
helping analyze patterns of life such as heartbeat intervals or other biological signals.

The system provides actionable insights, identifies anomalies, and interprets rhythms
through AI-powered computation.

License: MIT
Author: G.O.D Framework Team
"""

import numpy as np
import logging

# Initialize logger
logger = logging.getLogger("LifeConnection")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)


class LifeConnection:
    """
    Manage and analyze biological rhythm data for detecting stability and
    interpreting patterns.

    This class is designed to handle heartbeat or similar biological signal data,
    providing the ability to detect average rates, measure variability, and assess
    stability based on a customizable threshold.

    :ivar stability_threshold: Variability threshold used to determine stability.
    :type stability_threshold: int
    """

    def __init__(self, stability_threshold=10):
        """
        Initialize LifeConnection with a customizable threshold for stability detection.
        
        :param stability_threshold: Variability threshold considered "stable". Default is 10.
        """
        self.stability_threshold = stability_threshold
        logger.info(f"Initialized LifeConnection with stability threshold: {self.stability_threshold}")

    def read_heartbeat_pattern(self, data):
        """
        Detects patterns in heartbeats or other biological data.

        :param data: List or array of heartbeat intervals or other biological signals (numeric).
        :return: Dictionary with insights into average rate, variability, and stability.
        """
        if not isinstance(data, (list, np.ndarray)) or len(data) == 0:
            logger.error("Data provided for analysis is invalid or empty.")
            raise ValueError("Input data must be a non-empty list or NumPy array of numeric values.")

        try:
            avg_rate = np.mean(data)
            variability = np.var(data)

            is_stable = variability < self.stability_threshold
            logger.info(
                f"Heartbeat analysis - Avg Rate: {avg_rate:.2f}, Variability: {variability:.2f}, Stable: {is_stable}")

            return {
                "average_rate": avg_rate,
                "variability": variability,
                "is_stable": is_stable
            }
        except Exception as e:
            logger.error(f"Error analyzing heartbeat patterns: {e}")
            raise RuntimeError("Error processing heartbeat data for analysis.") from e

    def describe_living_element(self, data):
        """
        Provides semantic insights about the rhythm of life in the given data.

        :param data: List or array of heartbeat intervals or biological signals.
        :return: A human-readable string interpreting the rhythm of the system being analyzed.
        """
        try:
            result = self.read_heartbeat_pattern(data)
            if result["is_stable"]:
                return "This organism exhibits a balanced and steady rhythm of life."
            else:
                return "Unstable rhythm detected—might indicate distress in this organism."
        except ValueError as e:
            return str(e)
        except Exception as e:
            logger.error(f"Error generating semantic insights: {e}")
            raise RuntimeError("Unable to describe the living element due to an error.") from e


# ===== Example Usage =====
if __name__ == "__main__":
    # Sample heartbeat intervals in milliseconds
    sample_data = [800, 810, 795, 803, 802]  # Replace with real data if needed

    # Initialize LifeConnection system with a stability threshold
    life_connector = LifeConnection(stability_threshold=10)

    # Analyze the data and generate insights
    try:
        insight = life_connector.describe_living_element(sample_data)
        print(insight)
    except Exception as e:
        logger.error(f"An error occurred during analysis: {e}")