"""
===============================================================================
AI Version Control
===============================================================================
The AI Version Control module is designed to provide dynamic, structured, and
robust management of versions for models, datasets, and configurations
in AI workflows. It is lightweight, extensible, and easy to integrate
with larger systems.

GitHub Repository: <https://github.com/your-repo> (Replace with your repository link)
License: MIT License (or other preferred open-source license)
Maintainer: G.O.D Framework Team
===============================================================================
"""

import os
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional


class VersionControl:
    """
    Handles version control of serialized objects, such as models or datasets. Provides
    methods to save objects with metadata, list saved versions, load specific versions,
    and rollback to previous versions.

    This class is designed to facilitate tracking changes, enabling retrieval and management
    of serialized data objects using timestamped file versions.

    :ivar version_directory: Directory path where versioned files are stored.
    :type version_directory: str
    :ivar logger: Logger instance for logging version control activities.
    :type logger: logging.Logger
    """

    def __init__(self, version_directory: str = "versions"):
        """
        Initializes the version control system and creates version storage directory.

        Args:
            version_directory (str): Directory to store versioned files.
        """
        self.version_directory = version_directory
        os.makedirs(version_directory, exist_ok=True)
        self.logger = logging.getLogger("VersionControl")
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger.info(f"Version Control initialized. Directory: {version_directory}")

    def save_version(self, name: str, obj: Dict[str, Any], version_type: str = "model",
                     metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Saves the object as a versioned file with a timestamp and optional metadata.

        Args:
            name (str): Descriptive name for the versioned object.
            obj (Dict[str, Any]): The object to save (model, dataset, etc.)
            version_type (str): Type of the object ('model', 'data', etc.)
            metadata (Optional[Dict[str, Any]]): Additional info like author, tags.

        Returns:
            str: The file path of the saved version.
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f"{name}_{version_type}_{timestamp}.json"
        file_path = os.path.join(self.version_directory, file_name)

        versioned_data = {
            "data": obj,
            "metadata": metadata if metadata else {},
            "saved_at": timestamp
        }

        with open(file_path, "w") as fp:
            json.dump(versioned_data, fp, indent=4)

        self.logger.info(f"Version saved: {file_path}")
        return file_path

    def list_versions(self, name: Optional[str] = None) -> List[str]:
        """
        Lists all versioned files for a specified object name or all items.

        Args:
            name (Optional[str]): Name of the versioned object to filter by.
        
        Returns:
            List[str]: A list of versioned file paths.
        """
        files = os.listdir(self.version_directory)
        if name:
            files = [f for f in files if f.startswith(name)]
        files.sort()  # Sort files for better organization
        self.logger.info(f"Versions listed for '{name}': {files}")
        return files

    def load_version(self, file_name: str) -> Dict[str, Any]:
        """
        Loads a previously saved version of an object.

        Args:
            file_name (str): The name of the versioned file to load.
        
        Returns:
            Dict[str, Any]: The content of the saved version.

        Raises:
            FileNotFoundError: If the versioned file does not exist.
        """
        file_path = os.path.join(self.version_directory, file_name)

        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_name}")
            raise FileNotFoundError(f"The specified version file does not exist: {file_name}")

        with open(file_path, "r") as fp:
            data = json.load(fp)

        self.logger.info(f"Version loaded: {file_name}")
        return data

    def rollback_version(self, name: str, timestamp: str) -> str:
        """
        Rollback an object to a specified version using the timestamp.

        Args:
            name (str): The name of the versioned object.
            timestamp (str): The timestamp of the target version to rollback to.

        Returns:
            str: The file path of the rolled-back version.

        Raises:
            ValueError: If no version matches the specified criteria.
        """
        matching_files = [f for f in self.list_versions(name) if timestamp in f]
        if not matching_files:
            self.logger.error(f"No matching version found for name: {name} and timestamp: {timestamp}")
            raise ValueError("Rollback failed: Target version not found.")

        self.logger.info(f"Rollback successful for {name} to version: {matching_files[0]}")
        return matching_files[0]


if __name__ == "__main__":
    """
    Example usage of the AI Version Control module
    """
    # Initialize the version control system
    vc = VersionControl()

    # Example object to save (e.g., a model, dataset, or configuration)
    example_model = {
        "name": "ExampleModel",
        "type": "Classifier",
        "hyperparameters": {"learning_rate": 0.01, "epochs": 10},
        "accuracy": 0.92
    }

    # Save a new version
    file_path = vc.save_version("example_model", example_model, version_type="model",
                                metadata={"author": "Jane Doe", "description": "Initial version."})
    print(f"Version saved at: {file_path}")

    # List all versions
    all_versions = vc.list_versions("example_model")
    print("All versions:", all_versions)

    # Load a specific version
    latest_version_file = all_versions[-1] if all_versions else None
    if latest_version_file:
        loaded_version = vc.load_version(latest_version_file)
        print("Loaded version content:", loaded_version)

    # Simulate rollback to a previous timestamp
    if all_versions:
        timestamp_to_rollback = latest_version_file.split("_")[2].split(".")[0]  # Extract timestamp from file name
        rollback_file = vc.rollback_version("example_model", timestamp_to_rollback)
        print(f"Rollback successful to version: {rollback_file}")