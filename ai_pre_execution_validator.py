"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

import logging
import os
import json
import psutil

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class PreExecutionValidator:
    """
    Handles the validation of configurations, environment readiness, data integrity,
    and system resources for pipeline execution.

    This class provides utility methods to ensure that all prerequisites and
    requirements are met before initiating the execution of a pipeline. It includes
    methods for validating configuration files, ensuring required dependencies are
    installed, checking data against a defined schema, and verifying system resource
    availability.

    :ivar logger: A logger instance used for logging messages during validation processes.
    :type logger: logging.Logger
    :ivar validation_errors: Stores the list of error messages encountered during validation.
    :type validation_errors: list
    """

    @staticmethod
    def validate_config(config):
        """
        Validates that the required configuration fields are present and properly
        configured.
        :param config: Dictionary containing pipeline configuration
        :return: Boolean indicating if configuration is valid
        """
        logging.info("Validating pipeline configuration...")
        required_fields = ["data_source", "model", "training_data_path", "deployment_path"]

        try:
            missing_fields = [field for field in required_fields if field not in config]
            if missing_fields:
                logging.error(f"Missing required configuration fields: {missing_fields}")
                return False
            logging.info("Configuration validation passed.")
            return True
        except Exception as e:
            logging.error(f"Configuration validation failed with error: {e}")
            return False

    @staticmethod
    def check_environment():
        """
        Validates that essential dependencies and libraries are installed and ready.
        :return: Boolean indicating if the environment is ready
        """
        logging.info("Checking environment readiness...")
        try:
            import sklearn  # noqa: F401
            import pandas  # noqa: F401
            import matplotlib  # noqa: F401
            logging.info("All required libraries are installed.")
            return True
        except ImportError as e:
            logging.error(f"Environment validation failed. Missing dependency: {e}")
            return False

    @staticmethod
    def validate_data(data_file, schema_file):
        """
        Validates that input data conforms to the defined schema.
        :param data_file: Path to the data file (JSON format)
        :param schema_file: Path to the schema file (JSON format)
        :return: Boolean indicating if data validation passed
        """
        logging.info("Validating input data against schema...")
        try:
            with open(data_file, 'r') as data, open(schema_file, 'r') as schema:
                data = json.load(data)
                schema = json.load(schema)

                for field, properties in schema.items():
                    if field not in data:
                        logging.error(f"Missing field '{field}' in data.")
                        return False
                    if not isinstance(data[field], properties["type"]):
                        logging.error(
                            f"Field '{field}' has an incorrect type. "
                            f"Expected {properties['type']}, got {type(data[field])}."
                        )
                        return False
            logging.info("Data validation passed.")
            return True
        except FileNotFoundError as e:
            logging.error(f"File validation failed. File not found: {e}")
            return False
        except json.JSONDecodeError as e:
            logging.error(f"JSON decoding error during data validation: {e}")
            return False
        except Exception as e:
            logging.error(f"Data validation failed with error: {e}")
            return False

    @staticmethod
    def check_system_resources(min_memory_mb):
        """
        Validates that the system has adequate free memory for pipeline execution.
        :param min_memory_mb: Minimum required memory in MB
        :return: Boolean indicating if the system has sufficient memory
        """
        logging.info(f"Checking if system has at least {min_memory_mb} MB of free memory...")
        try:
            available_memory = psutil.virtual_memory().available / (1024 * 1024)  # Convert to MB
            if available_memory < min_memory_mb:
                logging.error(
                    f"Insufficient memory. Required: {min_memory_mb} MB, "
                    f"Available: {available_memory:.2f} MB."
                )
                return False
            logging.info(f"Sufficient memory available: {available_memory:.2f} MB.")
            return True
        except Exception as e:
            logging.error(f"System resource check failed with error: {e}")
            return False


if __name__ == "__main__":
    # Example usage
    validator = PreExecutionValidator()

    # Example configuration
    config = {
        "data_source": "database",
        "model": "RandomForestClassifier",
        "training_data_path": "data/input_data.json",
        "deployment_path": "deployments/output_model.pkl"
    }

    # Configuration validation
    is_config_valid = validator.validate_config(config)

    # Environment validation
    is_env_ready = validator.check_environment()

    # Data validation
    data_file = "data/input_data.json"
    schema_file = "data/schema.json"
    is_data_valid = validator.validate_data(data_file, schema_file)

    # System resource check
    min_memory_mb = 1024  # Example minimum memory requirement (1GB)
    is_memory_sufficient = validator.check_system_resources(min_memory_mb)

    # Final readiness check
    if is_config_valid and is_env_ready and is_data_valid and is_memory_sufficient:
        logging.info("Pipeline is ready for execution.")
    else:
        logging.error("Pipeline readiness validation failed. Fix the issues before proceeding.")
