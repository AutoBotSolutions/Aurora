"""
AI Inference Monitor
=====================

This module provides real-time tracking and logging of inference metrics for AI systems, such as
latency and throughput. It helps developers monitor, debug, and optimize inference pipelines.

License: MIT
Author: G.O.D Team
"""

import time
import logging
import statistics


class InferenceMonitor:
    """
    Monitors inference operations, tracks latencies, computes statistics, and triggers alerts.

    This class is used to measure the performance of inference operations by tracking
    latency and throughput metrics. It logs metrics for auditability and sends alerts
    if the latency exceeds a predefined threshold.

    :ivar alert_threshold: Threshold for latency in milliseconds to trigger alerts.
    :type alert_threshold: int
    :ivar latencies: List of recorded latencies for inference operations.
    :type latencies: list[float]
    :ivar logger: Logger instance configured for logging metrics and alerts.
    :type logger: logging.Logger
    :ivar alerts: List of alert messages generated when latency exceeds the threshold.
    :type alerts: list[str]
    """

    def __init__(self, alert_threshold=500, log_file="inference_monitor.log"):
        """
        Initialize the monitor with alert thresholds and logging configurations.

        :param alert_threshold: The threshold for inference latency (in milliseconds) before sending alerts.
        :param log_file: The file to log metrics and alerts for auditability.
        """
        self.alert_threshold = alert_threshold
        self.latencies = []  # Stores latency values
        self.logger = self._setup_logger(log_file)
        self.alerts = []  # Stores alert messages for triggering notifications

    @staticmethod
    def _setup_logger(log_file: str):
        """
        Configures and returns a logger instance.

        :param log_file: Filepath for the log file.
        :return: Configured logger instance.
        """
        logger = logging.getLogger("InferenceMonitor")
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def log_inference(self, start_time: float, end_time: float, num_predictions: int):
        """
        Logs latency and throughput metrics for inference operations.

        :param start_time: Timestamp when inference started (in seconds).
        :param end_time: Timestamp when inference ended (in seconds).
        :param num_predictions: The number of predictions made during the inference run.
        """
        latency = (end_time - start_time) * 1000  # Convert latency to milliseconds
        throughput = num_predictions / (end_time - start_time)

        # Log the performance metrics
        self.latencies.append(latency)
        self.logger.info(
            f"Inference completed: {num_predictions} predictions in {latency:.2f} ms "
            f"(Throughput: {throughput:.2f} req/s)"
        )

        # Check for anomalies and trigger alerts
        if latency > self.alert_threshold:
            self._send_alert(latency)

    def _send_alert(self, latency: float):
        """
        Trigger an alert if latency exceeds the defined threshold.

        :param latency: The recorded latency that triggered the alert (in milliseconds).
        """
        alert_message = f"ALERT: High latency detected! Latency: {latency:.2f} ms"
        self.alerts.append(alert_message)
        self.logger.warning(alert_message)

    def get_average_latency(self) -> float:
        """
        Returns the average latency of recorded inference operations.

        :return: The average latency in milliseconds.
        """
        return statistics.mean(self.latencies) if self.latencies else 0.0

    def get_latency_statistics(self) -> dict:
        """
        Returns detailed statistics on the recorded latencies, such as min, max, and average.

        :return: A dictionary containing latency statistics.
        """
        if not self.latencies:
            return {"min": 0.0, "max": 0.0, "average": 0.0}
        return {
            "min": min(self.latencies),
            "max": max(self.latencies),
            "average": statistics.mean(self.latencies),
        }


# ======= Example Usage =======
if __name__ == "__main__":
    # Initialize the monitor with a latency alert threshold of 300 ms
    monitor = InferenceMonitor(alert_threshold=300)

    # Simulated data
    num_predictions_list = [10, 50, 100, 200]
    for i, num_predictions in enumerate(num_predictions_list):
        # Simulate inference timings with increasing latencies
        start = time.time()
        time.sleep(0.1 * (i + 1))  # Simulated delay (in seconds)
        end = time.time()

        # Log inference metrics
        monitor.log_inference(start_time=start, end_time=end, num_predictions=num_predictions)

    # Get average latency
    print(f"Average Latency: {monitor.get_average_latency():.2f} ms")

    # Get detailed latency statistics
    stats = monitor.get_latency_statistics()
    print(
        f"Latency Statistics - Min: {stats['min']:.2f} ms, Max: {stats['max']:.2f} ms, Avg: {stats['average']:.2f} ms")