"""
Model Monitoring Framework

This script provides the ModelMonitoring class, a flexible and extensible
framework for tracking, analyzing, and enhancing the performance of machine
learning models in production. It computes critical metrics such as accuracy,
precision, recall, F1-score, and confusion matrix while offering extensibility
for custom metrics and configurations.

License: MIT
"""

import logging
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import json

# Configure basic logging for monitoring
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)


class ModelMonitoring:
    """
    Class responsible for monitoring machine learning model performance.

    This class provides functionalities to initialize monitoring with a given
    configuration, start the monitoring process for a trained model, and compute
    evaluation metrics for a model's performance based on actual and predicted
    values.

    :ivar config: Dictionary containing configuration settings for monitoring
        (e.g., alert thresholds). Defaults to an empty dictionary if not provided.
    :type config: dict
    """

    def __init__(self, config=None):
        """
        Initialize the model monitoring component with optional configuration.

        :param config: Optional dictionary for monitoring settings (e.g., alert thresholds).
        """
        self.config = config or {}
        logging.info("ModelMonitoring initialized with configuration: {}".format(self.config))

    def start_monitoring(self, model):
        """
        Placeholder method to initiate monitoring for a trained model.

        :param model: Trained model to be monitored (for future integration).
        """
        if not model:
            raise ValueError("A trained model is required for monitoring.")
        logging.info(f"Monitoring started for model: {type(model).__name__}.")
        if self.config:
            logging.info("Monitoring configuration: {}".format(self.config))

    def monitor_metrics(self, actuals, predictions):
        """
        Compare actual versus predicted values and compute evaluation metrics.

        :param actuals: Ground truth labels (actual values).
        :param predictions: Predicted labels from the model.
        :return: Dictionary containing evaluation metrics.
        """
        try:
            logging.info("Computing evaluation metrics...")

            # Compute evaluation metrics
            accuracy = accuracy_score(actuals, predictions) * 100
            precision = precision_score(actuals, predictions, pos_label="yes", zero_division=0)
            recall = recall_score(actuals, predictions, pos_label="yes", zero_division=0)
            f1 = f1_score(actuals, predictions, pos_label="yes", zero_division=0)
            conf_matrix = confusion_matrix(actuals, predictions, labels=["yes", "no"]).tolist()

            # Log metrics for transparency
            logging.info(f"Accuracy: {accuracy:.2f}%")
            logging.info(f"Precision: {precision:.2f}")
            logging.info(f"Recall: {recall:.2f}")
            logging.info(f"F1-Score: {f1:.2f}")
            logging.info(f"Confusion Matrix: {conf_matrix}")

            # Return metrics in a JSON-compatible format
            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "confusion_matrix": json.dumps(conf_matrix),
            }

        except Exception as e:
            logging.error(f"Error while computing metrics: {e}")
            raise


class AlertingMonitor(ModelMonitoring):
    """
    Monitors evaluation metrics and generates alerts when thresholds are breached.

    This class extends the functionality of a general model monitoring system by
    focusing on threshold-based alerting. It checks predefined metric thresholds
    and logs warnings if any computed evaluation metric fails to meet the required
    values.

    :ivar config: Configuration dictionary containing alert thresholds and other settings.
    :type config: dict
    """

    def alert_on_threshold(self, metrics):
        """
        Alerts when evaluation metrics fall below specified thresholds.

        :param metrics: Dictionary containing computed evaluation metrics.
        """
        thresholds = self.config.get("alert_thresholds", {})
        alerts = {}

        for metric, threshold in thresholds.items():
            if metrics.get(metric) < threshold:
                alerts[metric] = f"Alert: {metric.title()} below threshold of {threshold}"

        # Log alerts if any thresholds were breached
        if alerts:
            for alert in alerts.values():
                logging.warning(alert)
        else:
            logging.info("All metrics meet the defined thresholds.")


# Example usage
if __name__ == "__main__":
    # Set hypothetical actual and predicted labels
    actual_labels = ["yes", "no", "yes", "no", "yes", "no", "yes"]
    predicted_labels = ["yes", "no", "no", "no", "yes", "yes", "yes"]

    # Example 1: Basic monitoring
    logging.info("\n===== Example 1: Basic Monitoring =====")
    monitor = ModelMonitoring()
    metrics = monitor.monitor_metrics(actuals=actual_labels, predictions=predicted_labels)
    print("Metrics:\n", metrics)

    # Example 2: Monitoring with alerts
    logging.info("\n===== Example 2: Monitoring with Alerts =====")
    config_with_alerts = {
        "alert_thresholds": {
            "accuracy": 80.0,
            "precision": 0.8,
            "recall": 0.7
        }
    }
    alert_monitor = AlertingMonitor(config=config_with_alerts)
    metrics = alert_monitor.monitor_metrics(actuals=actual_labels, predictions=predicted_labels)
    alert_monitor.alert_on_threshold(metrics)