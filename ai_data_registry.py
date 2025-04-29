import json
import logging
from datetime import datetime


class DataCatalog:
    """
    Handles the cataloging of datasets by maintaining a JSON-based registry. This class
    provides functionality to add, retrieve, list datasets, and persist or load the
    registry, ensuring user-defined metadata is managed effectively. It also utilizes
    logging to monitor operations and handle errors.

    :ivar registry_path: Path to the JSON file used for storing the dataset catalog.
    :type registry_path: str
    :ivar logger: Logger instance used for logging messages.
    :type logger: logging.Logger
    """

    def __init__(self, registry_path="data_registry.json", logger_name="DataCatalogLogger"):
        """
        Initialize the DataCatalog instance.
        :param registry_path: Path to the JSON file used for storing the dataset catalog.
        :param logger_name: Custom logger name for DataCatalog.
        """
        self.registry_path = registry_path
        self.logger = self._setup_logger(logger_name)
        self._initialize_registry()

    def _setup_logger(self, logger_name):
        """
        Set up a logger instance for DataCatalog.
        :param logger_name: Name of the logger.
        :return: Configured logger instance.
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        if not logger.handlers:
            logger.addHandler(handler)
        return logger

    def _initialize_registry(self):
        """
        Ensure the registry file exists. If not, create an empty registry.
        """
        try:
            with open(self.registry_path, "r") as file:
                json.load(file)  # Verify JSON format
        except FileNotFoundError:
            self._save_registry({})
            self.logger.info(f"Created new empty data registry: {self.registry_path}")
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON file detected: {self.registry_path}. Initializing empty registry.")
            self._save_registry({})

    def add_entry(self, dataset_name, metadata):
        """
        Add a new dataset entry to the registry.
        :param dataset_name: Unique name of the dataset.
        :param metadata: Dictionary containing dataset metadata (e.g., size, source, format).
        """
        try:
            if not isinstance(metadata, dict):
                raise ValueError("Metadata must be a dictionary.")

            catalog = self._load_registry()
            catalog[dataset_name] = {
                "metadata": metadata,
                "date_added": datetime.now().isoformat()
            }
            self._save_registry(catalog)
            self.logger.info(f"Dataset '{dataset_name}' added successfully.")

        except Exception as e:
            self.logger.error(f"Failed to add dataset entry: {e}")
            raise

    def get_metadata(self, dataset_name):
        """
        Retrieve metadata for a given dataset.
        :param dataset_name: Name of the dataset.
        :return: Metadata dictionary if dataset exists, otherwise None.
        """
        try:
            catalog = self._load_registry()
            metadata = catalog.get(dataset_name)
            if metadata:
                self.logger.info(f"Retrieved metadata for dataset: {dataset_name}")
                return metadata
            else:
                self.logger.warning(f"Dataset '{dataset_name}' not found in the registry.")
                return None
        except Exception as e:
            self.logger.error(f"Failed to retrieve metadata for '{dataset_name}': {e}")
            raise

    def list_datasets(self):
        """
        List all datasets currently registered.
        :return: A list of all dataset names in the registry.
        """
        try:
            catalog = self._load_registry()
            dataset_names = list(catalog.keys())
            self.logger.info(f"Listing all datasets in the registry: {dataset_names}")
            return dataset_names
        except Exception as e:
            self.logger.error(f"Failed to list datasets: {e}")
            raise

    def _load_registry(self):
        """
        Load the current dataset catalog.
        :return: Dictionary representing the dataset registry.
        """
        try:
            with open(self.registry_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            self.logger.warning(f"Registry file not found: {self.registry_path}. Returning empty registry.")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode registry JSON: {e}")
            raise

    def _save_registry(self, catalog):
        """
        Save the current dataset catalog to the registry file.
        :param catalog: Dictionary representing the dataset registry.
        """
        try:
            with open(self.registry_path, "w") as file:
                json.dump(catalog, file, indent=4)
            self.logger.info(f"Successfully saved the data registry to {self.registry_path}.")
        except Exception as e:
            self.logger.error(f"Failed to save data registry: {e}")
            raise


if __name__ == "__main__":
    # Example usage of DataCatalog
    logging.basicConfig(level=logging.INFO)  # Configure root logger for example

    # Initialize the catalog
    catalog = DataCatalog()

    # Example of adding a dataset entry
    catalog.add_entry(
        "customer_data",
        metadata={
            "source": "internal SQL database",
            "size": "1.2 GB",
            "format": "Parquet",
            "last_updated": "2023-11-01",
            "schema": {"id": "int", "name": "string", "email": "string"}
        }
    )

    # Retrieve metadata for a dataset
    metadata = catalog.get_metadata("customer_data")
    print("Metadata for 'customer_data':", metadata)

    # List all datasets in the registry
    datasets = catalog.list_datasets()
    print("Registered Datasets:", datasets)

    # Attempt to retrieve non-existent dataset
    missing_metadata = catalog.get_metadata("non_existent_data")
    print("Metadata for 'non_existent_data':", missing_metadata)