"""
==================================================================================
AI Training Data Manager
==================================================================================

The AI Training Data Manager is a robust module for preparing training datasets 
in machine learning workflows. It provides functionalities such as data splitting 
into train/test/validation subsets, data cleansing, and extensibility for 
custom preprocessing pipelines.

Project Homepage: <https://github.com/<your-repo-link>> (Replace with your GitHub repo)
License: MIT (or preferred open-source license)
Maintainer: G.O.D Framework Team
==================================================================================
"""

import logging
import numpy as np
from sklearn.model_selection import train_test_split


class TrainingDataManager:
    """
    Manages training data operations, including splitting and validation.

    Provides functionalities to split input data into training and testing sets and validate
    the provided data and target for preprocessing. This class ensures data integrity
    and consistency before training machine learning models.

    :ivar None: This class does not maintain instance-level attributes as it only contains
        static methods.
    :type None: None
    """

    @staticmethod
    def split_data(data, target, test_size=0.2, random_state=42):
        """
        Splits input data into training and testing subsets.

        Args:
            data (np.ndarray or pd.DataFrame): Input features, should be aligned with `target`.
            target (np.ndarray or pd.Series): Target labels corresponding to the data input.
            test_size (float): Fraction of the dataset to reserve for testing (default is 0.2).
            random_state (int): Seed for random number generation for reproducibility.

        Returns:
            tuple: Split datasets: (X_train, X_test, y_train, y_test)

        Raises:
            ValueError: If data is empty, target is None, or lengths mismatch.
        """

        try:
            if target is None:
                logging.error("Target column is missing or None.")
                raise ValueError("Target column is missing or None.")

            if len(data) != len(target):
                logging.error("Data and target arrays must have the same length!")
                raise ValueError("Data and target arrays must have the same length.")

            if len(data) == 0 or len(target) == 0:
                logging.error("Data and target arrays cannot be empty.")
                raise ValueError("Data and target arrays cannot be empty.")

            logging.info(f"Data shape before splitting: {data.shape}")
            logging.info(f"Target length before splitting: {len(target)}")

            # Split the data using sklearn's train_test_split
            logging.info(f"Splitting data with test_size={test_size} and random_state={random_state}...")
            X_train, X_test, y_train, y_test = train_test_split(
                data, target, test_size=test_size, random_state=random_state
            )

            logging.info(f"Data split successful: "
                         f"X_train: {X_train.shape}, X_test: {X_test.shape}, "
                         f"y_train: {len(y_train)}, y_test: {len(y_test)}")

            return X_train, X_test, y_train, y_test

        except Exception as e:
            logging.error(f"An error occurred while splitting data: {e}")
            raise

    @staticmethod
    def validate_data(data, target):
        """
        Validates the data and target for preprocessing.

        Args:
            data (np.ndarray or pd.DataFrame): Input features.
            target (np.ndarray or pd.Series): Target labels.

        Returns:
            bool: True if validation is successful, raises ValueError otherwise.
        """

        if target is None:
            logging.error("Target labels are None.")
            raise ValueError("Target labels must not be None.")

        if len(data) != len(target):
            logging.error("Data length does not match target length.")
            raise ValueError("Length of data and target must be the same.")

        if len(data) == 0 or len(target) == 0:
            logging.error("Data or target arrays are empty.")
            raise ValueError("Data and target arrays cannot be empty.")

        logging.info("Data validation successful.")
        return True


# Example Usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Example Dataset
    data = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
    target = np.array([0, 1, 0, 1, 0])

    try:
        # Validate Data
        TrainingDataManager.validate_data(data, target)

        # Perform Train/Test Split
        X_train, X_test, y_train, y_test = TrainingDataManager.split_data(data, target)

        # Log Results
        logging.info(f"X_train:\n{X_train}\nX_test:\n{X_test}")
        logging.info(f"y_train:\n{y_train}\ny_test:\n{y_test}")

    except ValueError as ve:
        logging.error(f"Validation Error: {ve}")
    except Exception as ex:
        logging.error(f"Unexpected Error: {ex}")