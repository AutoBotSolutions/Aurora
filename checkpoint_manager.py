"""
===============================================================================
Checkpoint Manager for G.O.D Framework
===============================================================================
A Python-based checkpointing system to save, verify, and clear pipeline execution
stages. Provides fault tolerance, resumability, and optimized workflows in ML
pipelines, ETL processes, and more.

GitHub Repository: <Insert Repository URL here>
License: MIT License
Maintainer: G.O.D Framework Team
===============================================================================
"""

import os
import logging


class CheckpointManager:
    """
    Manages pipeline stage checkpoints by saving, verifying, clearing, and listing
    checkpoint files in a specified directory. This helps in tracking completed stages
    in processes that can be resumed or iteratively performed.

    :ivar checkpoint_dir: Directory where checkpoints are stored.
    :type checkpoint_dir: str
    """

    def __init__(self, checkpoint_dir="checkpoints/"):
        """
        Initializes the CheckpointManager with a designated directory for checkpoints.

        Args:
            checkpoint_dir (str): Directory where checkpoints are stored.
        """
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        logging.info(f"CheckpointManager initialized with directory: {self.checkpoint_dir}")

    def save_checkpoint(self, stage_name):
        """
        Marks a pipeline stage as completed by saving a checkpoint file.

        Args:
            stage_name (str): Name of the pipeline stage to mark as completed.

        Returns:
            str: The path of the created checkpoint file.

        Raises:
            Exception: If the checkpoint file cannot be created.
        """
        try:
            checkpoint_file = os.path.join(self.checkpoint_dir, f"{stage_name}.checkpoint")
            with open(checkpoint_file, "w") as f:
                f.write("COMPLETED")
            logging.info(f"Checkpoint saved: {checkpoint_file}")
            return checkpoint_file
        except Exception as e:
            logging.error(f"Error saving checkpoint for stage '{stage_name}': {e}")
            raise

    def has_checkpoint(self, stage_name):
        """
        Checks if a checkpoint exists for the specified pipeline stage.

        Args:
            stage_name (str): Name of the pipeline stage.

        Returns:
            bool: True if the checkpoint exists, False otherwise.
        """
        checkpoint_file = os.path.join(self.checkpoint_dir, f"{stage_name}.checkpoint")
        exists = os.path.exists(checkpoint_file)
        logging.info(f"Checkpoint exists for stage '{stage_name}': {exists}")
        return exists

    def clear_checkpoints(self):
        """
        Deletes all checkpoint files from the checkpoint directory.

        Returns:
            int: The number of checkpoints deleted.

        Raises:
            Exception: If checkpoint files cannot be removed.
        """
        try:
            count = 0
            for checkpoint_file in os.listdir(self.checkpoint_dir):
                os.remove(os.path.join(self.checkpoint_dir, checkpoint_file))
                count += 1
            logging.info(f"All checkpoints cleared. Total deleted: {count}")
            return count
        except Exception as e:
            logging.error(f"Error clearing checkpoints: {e}")
            raise

    def list_checkpoints(self):
        """
        Lists all checkpoints available in the checkpoint directory.

        Returns:
            list: A list of checkpoint file names (without directory path).
        """
        try:
            checkpoints = [f for f in os.listdir(self.checkpoint_dir) if f.endswith(".checkpoint")]
            logging.info(f"Available checkpoints: {checkpoints}")
            return checkpoints
        except Exception as e:
            logging.error(f"Error listing checkpoints: {e}")
            raise


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

# Example Usage
if __name__ == "__main__":
    def fetch_data_from_source():
        """
        Fetches data from a predefined source.

        This function logs a message indicating the start of the data fetching
        process and then retrieves mock data from a predefined source. The
        mock data is returned as a dictionary.

        :raises: This function does not raise any errors.
        :returns: A dictionary containing the mock data.
        :rtype: dict
        """
        logging.info("Fetching data from source...")
        return {"data": [1, 2, 3]}


    def preprocess_data(data):
        """
        Preprocesses the input data by squaring each element in the list provided
        under the "data" key in the input dictionary. The function assumes that the
        dictionary contains a key named "data" with a list of numerical values.

        :param data: Dictionary containing a key "data" with a list of numbers to
            be processed.
        :type data: dict
        :return: A dictionary with a single key "processed_data" that holds a list
            of squared numbers corresponding to the input data.
        :rtype: dict
        """
        logging.info("Preprocessing data...")
        return {"processed_data": [x ** 2 for x in data["data"]]}


    def train_model(processed_data):
        """
        Trains a machine learning model using the provided processed data.

        This function takes preprocessed data as input and trains a model based on it.
        It logs the progress of the training process and returns the trained model
        alongside the processed data.

        :param processed_data: The data that has been preprocessed and is ready for
            model training.
        :type processed_data: dict
        :return: A dictionary containing the trained model and the processed data.
        :rtype: dict
        """
        logging.info("Training model...")
        return {"model": "trained_model_with_data", "data": processed_data}


    logging.info("Starting pipeline execution...")

    # Initialize checkpoint manager
    checkpoint_manager = CheckpointManager()

    # Example pipeline execution with checkpoints
    try:
        # Stage 1: Data ingestion
        if not checkpoint_manager.has_checkpoint("data_ingestion"):
            raw_data = fetch_data_from_source()
            checkpoint_manager.save_checkpoint("data_ingestion")
        else:
            logging.info("Skipping data ingestion; already completed.")

        # Stage 2: Data preprocessing
        if not checkpoint_manager.has_checkpoint("data_preprocessing"):
            processed_data = preprocess_data(raw_data)
            checkpoint_manager.save_checkpoint("data_preprocessing")
        else:
            logging.info("Skipping data preprocessing; already completed.")

        # Stage 3: Model training
        if not checkpoint_manager.has_checkpoint("model_training"):
            model = train_model(processed_data)
            checkpoint_manager.save_checkpoint("model_training")
        else:
            logging.info("Skipping model training; already completed.")
    except Exception as e:
        logging.error(f"An error occurred during pipeline execution: {e}")

    # Example: List all checkpoints
    checkpoints = checkpoint_manager.list_checkpoints()
    logging.info(f"Available checkpoints: {checkpoints}")

    # Example: Clear all checkpoints
    checkpoint_manager.clear_checkpoints()