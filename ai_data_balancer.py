import logging
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTEENN


class DataBalancer:
    """
    Automates the process of balancing imbalanced datasets using specified sampling
    strategies.

    This class helps preprocess data by applying resampling techniques such as SMOTE,
    undersampling, and hybrid methods to address class imbalance problems in machine learning.

    :ivar strategy: The chosen strategy for balancing data, which can be "smote",
                    "undersample", or "hybrid".
    :type strategy: str
    :ivar logger: Logger instance used for recording events, errors, and information during
                  the balancing process.
    :type logger: logging.Logger
    """

    def __init__(self, strategy="smote"):
        """
        Initialize the DataBalancer with the chosen balancing strategy.

        :param strategy: The balancing strategy to use ("smote", "undersample", "hybrid").
        """
        self.strategy = strategy.lower()
        self.logger = self._setup_logger()

    @staticmethod
    def _setup_logger():
        """
        Configure and create a logger for the class.

        :return: Configured logger instance.
        """
        logger = logging.getLogger("DataBalancer")
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def balance_data(self, X, y):
        """
        Balances the dataset using the specified strategy.

        :param X: Feature matrix (numpy array or pandas DataFrame).
        :param y: Target vector (numpy array or pandas Series).
        :return: Balanced feature matrix and target vector.
        """
        self.logger.info(f"Starting data balancing using strategy: {self.strategy}...")
        try:
            # Select the balancing technique
            if self.strategy == "smote":
                sampler = SMOTE()
            elif self.strategy == "undersample":
                sampler = RandomUnderSampler()
            elif self.strategy == "hybrid":
                sampler = SMOTEENN()
            else:
                raise ValueError(f"Invalid strategy: {self.strategy}. Use 'smote', 'undersample', or 'hybrid'.")

            # Apply the chosen sampler
            X_resampled, y_resampled = sampler.fit_resample(X, y)

            self.logger.info("Data balancing completed successfully.")
            self.logger.info(f"Original class distribution: {dict(pd.Series(y).value_counts())}")
            self.logger.info(f"Balanced class distribution: {dict(pd.Series(y_resampled).value_counts())}")

            return X_resampled, y_resampled

        except Exception as e:
            self.logger.error(f"Error during data balancing: {e}")
            raise


if __name__ == "__main__":
    # Example Usage
    from sklearn.datasets import make_classification

    # Generate an imbalanced dataset
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_classes=2,
        weights=[0.9, 0.1],  # Class imbalance
        random_state=42
    )

    # Log the original distribution
    print("Original Class Distribution:", dict(pd.Series(y).value_counts()))

    # Balance the dataset using SMOTE
    print("\nUsing SMOTE:")
    balancer_smote = DataBalancer(strategy="smote")
    X_balanced_smote, y_balanced_smote = balancer_smote.balance_data(X, y)

    # Balance the dataset using undersampling
    print("\nUsing Undersampling:")
    balancer_undersample = DataBalancer(strategy="undersample")
    X_balanced_under, y_balanced_under = balancer_undersample.balance_data(X, y)

    # Balance the dataset using a hybrid approach (SMOTE+ENN)
    print("\nUsing Hybrid (SMOTE + ENN):")
    balancer_hybrid = DataBalancer(strategy="hybrid")
    X_balanced_hybrid, y_balanced_hybrid = balancer_hybrid.balance_data(X, y)