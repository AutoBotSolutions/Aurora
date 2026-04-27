import logging
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import pandas as pd


class DataPreparation:
    """
    Provides functionality for data preparation including cleaning, normalization, and splitting.

    The DataPreparation class is designed to preprocess datasets through a series of steps,
    including cleaning invalid entries, normalizing numerical data, and splitting data into
    training and testing sets. The class can handle both pandas DataFrame and list inputs,
    with optional configuration for scaling and other preprocessing parameters.

    :ivar config: Configuration dictionary for preprocessing (e.g., scaling type,
                  missing data strategy).
    :type config: dict
    :ivar logger: Logger instance for tracking preprocessing steps and errors.
    :type logger: logging.Logger
    """

    def __init__(self, config=None):
        """
        Initialize the DataPreparation class with optional configurations.
        :param config: A dictionary to configure preprocessing steps (e.g., scaling type, missing data strategy).
        """
        self.config = config or {}
        self.logger = self._setup_logger()

    @staticmethod
    def _setup_logger():
        """
        Sets up the logger for tracking preprocessing steps.
        :return: Configured logger instance.
        """
        logger = logging.getLogger("DataPreparation")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def clean_data(self, data):
        """
        Cleans the dataset by removing `None` or invalid entries.
        :param data: Iterable data (list or DataFrame) to clean.
        :return: Cleaned data (list or DataFrame, depending on input type).
        """
        self.logger.info("Cleaning data...")
        try:
            if isinstance(data, pd.DataFrame):
                cleaned_data = data.dropna()  # Drop rows with missing values
            elif isinstance(data, list):
                cleaned_data = [item for item in data if item is not None]  # Remove None values
            else:
                raise TypeError("Data type not supported. Use pandas DataFrame or list.")

            self.logger.info(f"Cleaned data: {cleaned_data}")
            return cleaned_data
        except Exception as e:
            self.logger.error(f"Error during data cleaning: {e}")
            raise

    def normalize_data(self, data):
        """
        Normalizes numerical data using Min-Max scaling (default) or standard scaling.
        :param data: Input data as a pandas DataFrame or list.
        :return: Normalized data.
        """
        self.logger.info("Normalizing data...")
        try:
            scaling_type = self.config.get('scaling', 'minmax')

            if isinstance(data, pd.DataFrame):
                numerical_cols = data.select_dtypes(include=['float64', 'int64']).columns
                scaler = StandardScaler() if scaling_type == 'standard' else MinMaxScaler()
                data[numerical_cols] = scaler.fit_transform(data[numerical_cols])
                self.logger.info("Data normalized successfully (DataFrame).")
                return data
            elif isinstance(data, list):
                min_value, max_value = min(data), max(data)
                if max_value > min_value:
                    normalized_data = [(x - min_value) / (max_value - min_value) for x in data]
                    self.logger.info(f"Normalized data: {normalized_data}")
                    return normalized_data
                else:
                    self.logger.warning("Normalization skipped: Min and Max values are equal.")
                    return data
            else:
                raise TypeError("Data type not supported. Use pandas DataFrame or list.")

        except Exception as e:
            self.logger.error(f"Error during normalization: {e}")
            raise

    def split_data(self, data, test_size=0.2, random_state=42):
        """
        Splits data into training and testing subsets.
        :param data: pandas DataFrame to split.
        :param test_size: Proportion of data to reserve for the test set.
        :param random_state: Seed for random splitting.
        :return: Training and testing dataframes.
        """
        self.logger.info("Splitting data into train and test sets...")
        try:
            if not isinstance(data, pd.DataFrame):
                raise TypeError("Input data must be a pandas DataFrame for splitting.")

            train_data, test_data = train_test_split(data, test_size=test_size, random_state=random_state)
            self.logger.info("Data split successfully.")
            return train_data, test_data
        except Exception as e:
            self.logger.error(f"Error during data splitting: {e}")
            raise

    def prepare(self, data):
        """
        Executes the entire data preparation pipeline: cleaning, normalization, and splitting.
        :param data: Input dataset (as a pandas DataFrame or list).
        :return: Prepared data (if DataFrame, training and testing sets; otherwise cleaned and normalized data).
        """
        self.logger.info("Starting data preparation pipeline...")
        try:
            cleaned_data = self.clean_data(data)
            normalized_data = self.normalize_data(cleaned_data)

            if isinstance(normalized_data, pd.DataFrame):
                # Split only if DataFrame is provided
                train_set, test_set = self.split_data(normalized_data)
                self.logger.info("Data preparation pipeline completed successfully.")
                return train_set, test_set

            self.logger.info("Data preparation pipeline completed successfully for non-DataFrame input.")
            return normalized_data
        except Exception as e:
            self.logger.error(f"Error in data preparation pipeline: {e}")
            raise


if __name__ == "__main__":
    # Example usage of DataPreparation class

    # Logging setup
    logging.basicConfig(level=logging.INFO)

    # Example configuration
    config = {
        'scaling': 'standard'  # Options: 'minmax' or 'standard'
    }

    # Example 1: List-based dataset
    data_list = [12, None, 18, 24, 30, 36, None, 40]

    prep = DataPreparation(config)

    cleaned_list = prep.clean_data(data_list)
    normalized_list = prep.normalize_data(cleaned_list)
    print("Cleaned List:", cleaned_list)
    print("Normalized List:", normalized_list)

    # Example 2: DataFrame-based dataset
    df = pd.DataFrame({
        'Feature1': [12, None, 18, 24, 30, None, 36],
        'Feature2': [1, 2, None, 4, 5, None, None]
    })

    cleaned_df, test_df = prep.prepare(df)
    print("\nCleaned DataFrame:\n", cleaned_df.head())
    print("\nTest Set:\n", test_df.head())