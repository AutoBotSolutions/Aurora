"""
AI Insert Training Data
========================

This module provides a streamlined integration of training data into machine learning pipelines. With features
that support data validation, deduplication, and preprocessing, it is a powerful utility for managing and scaling
training datasets.

License: MIT
Author: G.O.D Framework Team
"""

import os
import json
import logging
from typing import List, Union


class TrainingDataInsert:
    """
    Represents a utility for managing and manipulating training datasets, including
    adding new data, deduplicating, validating, saving, and loading datasets.

    The purpose of this class is to facilitate the management of datasets used in training
    models or other data-driven processes. It provides a set of operations through which
    datasets can be modified, validated, and stored.

    :ivar log_file: Path for the log file used to record actions.
    :type log_file: str
    """

    def __init__(self, log_file: str = "training_data_insert.log"):
        """
        Initializes the TrainingDataInsert utility and configures logging.

        :param log_file: Path for the log file to record actions.
        """
        self.log_file = log_file
        # Configure logging
        logging.basicConfig(
            filename=self.log_file,
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )
        logging.info("TrainingDataInsert initialized successfully.")

    @staticmethod
    def add_data(new_data: List, existing_data: List) -> List:
        """
        Adds new data points to the existing dataset.

        :param new_data: A list of new data points to be added.
        :param existing_data: An existing dataset as a list.
        :return: An updated dataset with the new data included.
        """
        logging.info("Adding new data to the existing training dataset...")
        try:
            updated_data = existing_data + new_data
            logging.info("New training data added successfully.")
            return updated_data
        except Exception as e:
            logging.error(f"Failed to add data: {str(e)}")
            raise

    @staticmethod
    def deduplicate_data(dataset: List) -> List:
        """
        Removes duplicate entries from the dataset.

        :param dataset: A list representing the dataset.
        :return: A cleaned dataset with duplicates removed.
        """
        logging.info("Performing deduplication on the dataset...")
        unique_data = list(set(dataset))
        logging.info("Deduplication completed.")
        return unique_data

    @staticmethod
    def validate_data(dataset: List, validation_fn=None) -> bool:
        """
        Validates the dataset using a provided validation function.

        :param dataset: The dataset to be validated.
        :param validation_fn: A custom function that validates each data entry.
                              If None, performs a basic check to ensure the dataset is not empty.
        :return: True if the dataset is valid, False otherwise.
        """
        logging.info("Starting dataset validation...")
        try:
            if validation_fn:
                valid = all(validation_fn(data) for data in dataset)
            else:
                valid = bool(dataset)  # Basic validation: Dataset is not empty.

            if valid:
                logging.info("Validation passed.")
                return True
            else:
                raise ValueError("Validation failed: Dataset contains invalid entries.")
        except Exception as e:
            logging.error(f"Validation error: {str(e)}")
            return False

    def save_data(self, dataset: List, file_path: str) -> str:
        """
        Saves the dataset to a JSON file.

        :param dataset: The dataset to be saved.
        :param file_path: The file path where the dataset should be stored.
        :return: Confirmation message indicating the success or failure of the save operation.
        """
        try:
            with open(file_path, "w") as file:
                json.dump(dataset, file)
            logging.info(f"Dataset saved successfully to {file_path}.")
            return f"Dataset saved successfully to {file_path}."
        except Exception as e:
            logging.error(f"Failed to save the dataset: {str(e)}")
            raise

    def load_data(self, file_path: str) -> Union[List, None]:
        """
        Loads a dataset from a JSON file.

        :param file_path: The file path to load the dataset from.
        :return: The loaded dataset as a list if successful, or None if an error occurred.
        """
        try:
            with open(file_path, "r") as file:
                dataset = json.load(file)
            logging.info(f"Dataset loaded successfully from {file_path}.")
            return dataset
        except Exception as e:
            logging.error(f"Failed to load the dataset: {str(e)}")
            return None

    def insert_data(
            self, new_data: List, existing_file: str, save_file: str = None
    ) -> str:
        """
        Inserts new data into an existing dataset stored in a file and optionally saves it to a specified file.

        :param new_data: New data to be added to the dataset.
        :param existing_file: Path to the existing dataset file.
        :param save_file: Path to the file where the updated dataset will be saved.
                          If None, the original file will be updated.
        :return: A message indicating success or failure of the operation.
        """
        logging.info("Inserting new training data into the existing dataset...")

        save_file = save_file or existing_file

        try:
            # Load existing dataset
            existing_data = self.load_data(existing_file)
            if existing_data is None:
                raise ValueError("Failed to load existing dataset.")

            # Add new data
            updated_data = self.add_data(new_data, existing_data)

            # Deduplicate new dataset
            updated_data = self.deduplicate_data(updated_data)

            # Save the updated dataset
            self.save_data(updated_data, save_file)

            return f"Data successfully inserted and saved to {save_file}."
        except Exception as e:
            logging.error(f"Failed to insert data: {str(e)}")
            return f"Failed to insert data: {str(e)}."


# ===== Usage Example =====
if __name__ == "__main__":
    # Initialize the utility
    inserter = TrainingDataInsert()

    # Example datasets
    existing_dataset_file = "existing_dataset.json"
    new_data_points = ["data_point_4", "data_point_5", "data_point_6"]

    # Save an initial dataset for testing
    stub_dataset = ["data_point_1", "data_point_2", "data_point_3"]
    inserter.save_data(stub_dataset, existing_dataset_file)

    # Insert new data into the existing dataset
    result = inserter.insert_data(new_data_points, existing_dataset_file)
    print(result)

    # Validate the updated dataset
    updated_dataset = inserter.load_data(existing_dataset_file)
    print("Updated Dataset:", updated_dataset)