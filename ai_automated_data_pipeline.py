import os
import pandas as pd
import logging
from typing import Tuple, Dict


class DataPipeline:
    """
    Manages the data pipeline workflow, including configuration validation, logging setup,
    and data fetching/preprocessing for analytics or machine learning tasks.

    This class is designed to simplify the management and preprocessing of data, ensuring
    that the input dataset is correctly structured and validated before being processed
    for downstream operations. It handles file loading, missing value imputation, and
    feature/target separation.

    :ivar config: Configuration dictionary for the pipeline. Must include a valid `data_path`.
    :type config: Dict
    """

    def __init__(self, config: Dict):
        """
        Initializes the DataPipeline with configuration parameters.

        :param config: Dictionary containing configuration details. Must include:
            - `data_path`: Path to the dataset file (CSV format).
        """
        self.config = config
        self.validate_config()
        self._setup_logging()

    @staticmethod
    def _setup_logging(log_file: str = "data_pipeline.log") -> None:
        """
        Configures logging for the pipeline.

        :param log_file: File to save logs. Default: "data_pipeline.log".
        """
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        logging.getLogger().addHandler(logging.StreamHandler())  # Log to console as well

    def validate_config(self) -> None:
        """
        Validates the configuration dictionary for required keys.

        :raises KeyError: If `data_path` is missing or empty in the configuration.
        """
        if not self.config.get("data_path"):
            logging.error("The 'data_path' key is missing or empty in the configuration.")
            raise KeyError("The 'data_path' key is missing or improperly configured in the data pipeline.")

    def fetch_and_preprocess(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Fetches and preprocesses the dataset.

        - Validates data file existence and structure.
        - Handles missing values in features and target columns.
        - Logs key steps for debugging and monitoring.

        :return: Tuple containing processed features (DataFrame) and labels (Series).
        :raises:
            - FileNotFoundError: If the dataset file does not exist.
            - ValueError: If the required `target` column is missing.
        """
        try:
            # Load dataset
            data_path = self.config["data_path"]
            if not os.path.exists(data_path):
                logging.error(f"The specified data file '{data_path}' does not exist.")
                raise FileNotFoundError(f"Data file '{data_path}' not found at the specified path.")

            logging.info(f"Loading data from '{data_path}'...")
            raw_data = pd.read_csv(data_path)

            # Validate the presence of the 'target' column
            if "target" not in raw_data.columns:
                logging.error("The required 'target' column is missing from the dataset.")
                raise ValueError("The 'target' column is required but is missing in the dataset.")

            # Preprocess target and features
            logging.info("Preprocessing data: handling missing values...")
            target = raw_data.pop("target").fillna("unknown")  # Replace missing target values with 'unknown'
            features = raw_data.fillna(0)  # Replace missing feature values with 0

            logging.info("Data fetching and preprocessing completed successfully.")
            return features, target

        except Exception as error:
            logging.error(f"Error during data fetching and preprocessing: {error}")
            raise


if __name__ == "__main__":
    # Example configuration dictionary
    config = {
        "data_path": "data/customer_data.csv"  # Update with file path
    }

    # Initialize the pipeline
    try:
        logging.info("Initializing DataPipeline...")
        pipeline = DataPipeline(config)

        # Fetch and preprocess data
        features, target = pipeline.fetch_and_preprocess()

        # Output processed data for demonstration
        print("Processed Features:")
        print(features.head())
        print("\nProcessed Target:")
        print(target.head())

    except Exception as e:
        logging.error(f"DataPipeline execution failed: {e}")