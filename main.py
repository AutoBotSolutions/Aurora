"""
G.O.D Framework - Main Entry Point
==================================

This script initializes and manages the lifecycle of the G.O.D Framework, acting as the central entry point for execution. 
It orchestrates vital components and workflows, ensuring smooth and reliable operation.

Core Features:
    - Configuration Loader: Flexible and validated YAML-based setup.
    - Logging: JSON-configurable logging for debugging and runtime insights.
    - Data Pipeline: Integration with preprocessing, training, and monitoring modules.
    - Orchestration: Centralized workflow management for AI processes.
    - Error Handling: Graceful error catching and logging.

GitHub Repository: <Insert Repository URL>
License: MIT License
Maintainer: G.O.D Framework Team
"""

import logging
import yaml
import logging.config
import json
import os

from ai_automated_data_pipeline import DataPipeline
from ai_training_data import TrainingDataManager
from ai_training_model import ModelTrainer
from ai_monitoring import ModelMonitoring
from ai_inference_service import InferenceService
from ai_data_detection import DataDetection
from manage_database import DatabaseManagerSQL


def setup_logging(config_file="config/config_logging.json"):
    """
    Initializes logging configuration based on a JSON configuration file. If the specified configuration file
    is not found or contains an error, it falls back to a default logging setup with INFO level logging.

    :param config_file: Path to the logging configuration file in JSON format. Defaults to
        "config/config_logging.json".
    :type config_file: str
    :return: None
    """
    if not os.path.exists(config_file):
        logging.basicConfig(level=logging.INFO)
        logging.warning(f"Logging configuration file '{config_file}' not found. Default logging applied.")
        return

    try:
        with open(config_file, "r") as file:
            config = json.load(file)
        logging.config.dictConfig(config)
        logging.info("Logging initialized successfully.")
    except (json.JSONDecodeError, Exception) as e:
        logging.basicConfig(level=logging.INFO)
        logging.error(f"Failed to configure logging: {e}. Default logging applied.")


def load_config(config_file="config/config.yaml"):
    """
    Loads and validates a YAML configuration file, ensuring that required configuration
    keys are present. This function is used to initialize system or application-level
    settings necessary for proper execution.

    :param config_file: Path to the YAML configuration file.
    :type config_file: str, optional
    :return: Parsed and validated configuration as a dictionary.
    :rtype: dict
    :raises FileNotFoundError: If the specified configuration file does not exist.
    :raises KeyError: If any of the required keys are missing from the configuration file.
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file '{config_file}' does not exist.")

    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
        logging.info("Configuration loaded successfully.")

        # Validate required keys
        required_keys = ["data_pipeline", "data_path", "database_path"]
        for key in required_keys:
            if key not in config:
                raise KeyError(f"Missing required configuration key: {key}")

    return config


def main():
    """
    Main entry point for initializing and executing the AI pipeline.

    This function orchestrates various components involved in the pipeline execution,
    including configuration loading, data preprocessing, model training, and inference.
    It serves as the central controlling function, handling initialization, errors, and
    resource management.

    :raises Exception: If the configuration file fails to load, or if any critical error
                       occurs during pipeline execution.
    :raises ValueError: If the target dataset is missing or empty.
    :returns: None
    """
    # Initialize logging
    setup_logging()

    # Load configuration
    try:
        config = load_config()
    except Exception as e:
        logging.error(f"Failed to load the configuration: {e}")
        return  # Terminate early if configuration fails

    db_manager = None  # Initialize to ensure proper cleanup
    try:
        logging.info("Initializing components for the AI pipeline...")

        # Database manager initialization
        db_manager = DatabaseManagerSQL(config["database_path"])

        # Data pipeline for fetching and preprocessing
        pipeline = DataPipeline(config["data_pipeline"])
        raw_data, target = pipeline.fetch_and_preprocess()

        # Validate target data
        if target is None or target.empty:
            raise ValueError("Target column is missing or empty in the dataset.")

        # Split data into training and validation sets
        training_manager = TrainingDataManager()
        X_train, X_val, y_train, y_val = training_manager.split_data(raw_data, target)
        logging.info("Successfully split data into training and validation sets.")

        # Train the model
        model_trainer = ModelTrainer(config["model"])
        trained_model = model_trainer.train_model(X_train, y_train)
        logging.info("Model training completed successfully.")

        # Model monitoring
        model_monitoring = ModelMonitoring(config["monitoring"])
        model_monitoring.start_monitoring(trained_model)

        # Perform inference
        inference_service = InferenceService(trained_model=trained_model, config=config.get("inference", {}))
        predictions = inference_service.predict(X_val)
        logging.info(f"Predictions: {predictions}")

        # Check for potential data issues
        data_detector = DataDetection()
        if data_detector.has_issues(raw_data):
            logging.warning("Potential data quality issues detected!")

        logging.info("Pipeline execution completed successfully.")

    except Exception as e:
        logging.error(f"Pipeline execution failed: {e}")
    finally:
        # Ensure cleanup
        if db_manager is not None:
            db_manager.close()
            logging.info("Database connection closed.")


if __name__ == "__main__":
    main()