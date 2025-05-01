"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

import logging
import json
import yaml
from jsonschema import validate, ValidationError
from typing import Optional, Any, Dict


class ConfigLoader:
    """
    Handles loading and validating configuration files.

    The ConfigLoader class provides static methods to load configuration from
    JSON or YAML files and validate them against a JSON schema. This class is
    intended to facilitate configuration management in applications, ensuring
    that configurations are loaded and validated correctly.

    """

    @staticmethod
    def load_config(file_path: str) -> Optional[Dict[str, Any]]:
        """
        Loads configurations from a JSON or YAML file.

        :param file_path: Path to the configuration file (JSON or YAML).
        :return: Configuration dictionary if successfully loaded, None otherwise.
        """
        logging.info(f"Loading configuration from {file_path}...")

        try:
            with open(file_path, 'r') as file:
                if file_path.endswith(".json"):
                    config = json.load(file)
                elif file_path.endswith((".yaml", ".yml")):
                    config = yaml.safe_load(file)
                else:
                    logging.error("Unsupported file format. Use JSON or YAML.")
                    return None

                logging.info("Configuration loaded successfully.")
                return config

        except FileNotFoundError:
            logging.error(f"Configuration file not found: {file_path}")
            return None
        except (json.JSONDecodeError, yaml.YAMLError) as e:
            logging.error(f"Failed to parse configuration file: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error while loading configuration: {e}")
            return None

    @staticmethod
    def validate_config(config: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """
        Validates the configuration against a given JSON schema.

        :param config: Configuration dictionary.
        :param schema: JSON schema for validation.
        :return: True if valid, raises ValueError otherwise.
        """
        logging.info("Validating configuration against schema...")

        try:
            validate(instance=config, schema=schema)
            logging.info("Configuration validated successfully.")
            return True
        except ValidationError as e:
            logging.error(f"Configuration validation failed: {e.message}")
            raise ValueError(f"Invalid configuration: {e.message}")
        except Exception as e:
            logging.error(f"Unexpected error during configuration validation: {e}")
            raise ValueError(f"Unexpected error during validation: {e}")


if __name__ == "__main__":
    # Sample schema for validation
    example_schema = {
        "type": "object",
        "properties": {
            "data_path": {"type": "string"},
            "model_params": {
                "type": "object",
                "properties": {
                    "learning_rate": {"type": "number", "minimum": 0.0},
                    "num_epochs": {"type": "integer", "minimum": 1}
                },
                "required": ["learning_rate", "num_epochs"]
            },
            "log_level": {"type": "string", "enum": ["INFO", "DEBUG", "ERROR"]}
        },
        "required": ["data_path", "model_params", "log_level"]
    }

    # Example file paths
    json_config_path = "example_config.json"  # Replace with path to your config file.

    # Enable logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Load and validate configuration
    config = ConfigLoader.load_config(json_config_path)

    if config:
        try:
            ConfigLoader.validate_config(config, example_schema)
            print("Configuration:")
            print(config)
        except ValueError as e:
            print(f"Configuration validation error: {e}")
    else:
        print("Failed to load configuration. Please check the error logs.")
