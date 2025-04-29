import logging
import pandas as pd
from scipy.stats import zscore
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN


class DataDetection:
    """
    Provides functionality for detecting data quality issues and anomalies
    in datasets. Includes logging for progress tracking and debugging.

    The class encapsulates methods to identify missing values, duplicate rows,
    and anomalies in data using different detection techniques. The logger setup is
    integrated to provide real-time feedback on operations.

    :ivar logger: Logger instance used for logging operations in the class.
    :type logger: logging.Logger
    """

    def __init__(self):
        """
        Initialize the DataDetection class with logging setup.
        """
        self.logger = self._setup_logger()

    @staticmethod
    def _setup_logger():
        """
        Configures and returns a logger instance.
        :return: Configured logger for DataDetection.
        """
        logger = logging.getLogger("DataDetection")
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def has_issues(self, data):
        """
        Checks for common data quality issues in the dataset, including missing values
        and duplicate rows.

        :param data: The dataset (Pandas DataFrame) to validate.
        :return: True if any issues are detected, False otherwise.
        """
        try:
            self.logger.info("Checking for data quality issues...")

            # Check for missing values
            if data.isnull().values.any():
                self.logger.warning("Data contains missing values.")
                return True

            # Check for duplicate rows
            if data.duplicated().any():
                self.logger.warning("Data contains duplicate rows.")
                return True

            self.logger.info("No data quality issues detected.")
            return False
        except Exception as e:
            self.logger.error(f"Error during data quality checks: {e}")
            raise

    def detect_anomalies(self, data, method="zscore", threshold=3):
        """
        Detects anomalies using the specified method.

        :param data: Dataset (Pandas DataFrame or NumPy array).
        :param method: The anomaly detection method ('zscore', 'isolation_forest', 'dbscan').
        :param threshold: (Optional) Applicable only to 'zscore', represents the threshold for anomalies.
        :return: An array or list indicating anomalous data points.
        """
        try:
            self.logger.info(f"Detecting anomalies using the {method} method...")

            # Ensure the data is a DataFrame or array
            if isinstance(data, pd.DataFrame):
                data = data.select_dtypes(include=["number"])  # Use only numeric columns
            elif not isinstance(data, (pd.DataFrame, pd.Series, list, tuple)):
                raise ValueError("Input data must be a Pandas DataFrame, Series, or array.")

            # Detect anomalies using the specified method
            if method == "zscore":
                z_scores = zscore(data, nan_policy="omit")
                anomalies = abs(z_scores) > threshold
                self.logger.info("Anomaly detection using Z-Score completed.")
                return anomalies

            elif method == "isolation_forest":
                model = IsolationForest(contamination=0.1)
                labels = model.fit_predict(data)  # -1 = anomaly, 1 = normal
                self.logger.info("Anomaly detection using Isolation Forest completed.")
                return labels

            elif method == "dbscan":
                model = DBSCAN(eps=1.5, min_samples=5)
                labels = model.fit_predict(data)  # -1 = anomaly/noise
                self.logger.info("Anomaly detection using DBSCAN completed.")
                return labels

            else:
                raise ValueError("Invalid method specified. Use 'zscore', 'isolation_forest', or 'dbscan'.")

        except Exception as e:
            self.logger.error(f"Error during anomaly detection: {e}")
            raise


if __name__ == "__main__":
    # Example Usage
    # Create a sample dataset
    data = pd.DataFrame({
        "A": [1, 2, None, 4],
        "B": ['a', 'b', 'b', 'd'],
        "C": [10, 20, 20, None]
    })

    # Initialize the DataDetection class
    detector = DataDetection()

    # Check for data quality issues (missing values, duplicates)
    print("\n=== Data Quality Detection ===")
    if detector.has_issues(data):
        print("The dataset has quality issues.")
    else:
        print("The dataset is clean.")

    # Generate a random dataset for anomaly detection
    import numpy as np

    random_data = np.random.rand(100, 2)  # 100 samples, 2 features

    # Detect anomalies using Z-Score
    print("\n=== Anomaly Detection: Z-Score ===")
    detector_zscore = DataDetection()
    anomalies_zscore = detector_zscore.detect_anomalies(data=random_data, method="zscore", threshold=2.5)
    print("Z-Score Results:", anomalies_zscore)

    # Detect anomalies using Isolation Forest
    print("\n=== Anomaly Detection: Isolation Forest ===")
    detector_if = DataDetection()
    anomalies_if = detector_if.detect_anomalies(data=random_data, method="isolation_forest")
    print("Isolation Forest Results:", anomalies_if)

    # Detect anomalies using DBSCAN
    print("\n=== Anomaly Detection: DBSCAN ===")
    detector_dbscan = DataDetection()
    anomalies_dbscan = detector_dbscan.detect_anomalies(data=random_data, method="dbscan")
    print("DBSCAN Results:", anomalies_dbscan)