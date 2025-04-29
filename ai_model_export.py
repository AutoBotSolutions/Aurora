import logging
import pickle
import os


class ModelExporter:
    """
    Handles exporting machine learning models to a specified directory with optional versioning.

    This class provides functionality to save trained models in a specified directory using
    a specified serialization format. Additionally, it supports versioning for exported models and
    allows listing all exported models in the designated directory.

    :ivar export_directory: Directory where exported models are saved.
    :type export_directory: str
    :ivar versioning: If True, appends version numbers to the exported model files.
    :type versioning: bool
    """

    def __init__(self, export_directory="exported_models", versioning=True):
        """
        Initializes the ModelExporter with options for export directory and versioning.

        :param export_directory: Directory where exported models are saved.
        :param versioning: If True, appends version numbers to the exported model files.
        """
        self.export_directory = export_directory
        self.versioning = versioning
        os.makedirs(self.export_directory, exist_ok=True)
        logging.info(f"Export directory set to: {self.export_directory}")

    def export_model(self, model, model_name="model", file_format="pickle"):
        """
        Exports a trained model to a file.

        :param model: Trained model to be exported.
        :param model_name: The name of the model file (without extension).
        :param file_format: Serialization format for the model. Supported: "pickle".
        :return: The full file path of the exported model.
        :raises ValueError: If file_format is unsupported.
        """
        # Validate serialization format
        if file_format != "pickle":
            raise ValueError("Unsupported file format! Currently, only 'pickle' is supported.")

        # Generate versioned filename if versioning is enabled
        version_suffix = "_v1" if self.versioning else ""
        file_name = f"{model_name}{version_suffix}.{file_format}"
        file_path = os.path.join(self.export_directory, file_name)

        # Serialize and export the model
        logging.info(f"Exporting model to {file_path}...")
        try:
            with open(file_path, "wb") as model_file:
                pickle.dump(model, model_file)
            logging.info("Model exported successfully.")
            return file_path
        except Exception as e:
            logging.error(f"Failed to export model: {e}")
            raise RuntimeError(f"Model export failed: {e}")

    def list_exports(self):
        """
        Lists all exported models in the export directory.

        :return: A list of exported model files in the directory.
        """
        try:
            exported_files = [
                file for file in os.listdir(self.export_directory) if
                os.path.isfile(os.path.join(self.export_directory, file))
            ]
            logging.info(f"Exported models: {exported_files}")
            return exported_files
        except Exception as e:
            logging.error(f"Failed to list exported models: {e}")
            return []


# Example usage of the ModelExporter
if __name__ == "__main__":
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import load_iris

    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Load the Iris dataset
    iris = load_iris()
    X, y = iris.data, iris.target

    # Train a model (RandomForestClassifier)
    logging.info("Training RandomForestClassifier on Iris dataset...")
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)

    # Initialize the ModelExporter
    exporter = ModelExporter(export_directory="models", versioning=True)

    # Export the model in pickle format
    exported_file = exporter.export_model(model, model_name="iris_random_forest", file_format="pickle")
    logging.info(f"Model exported to: {exported_file}")

    # List all exported models in the directory
    logging.info("Listing all exported models:")
    exported_files = exporter.list_exports()
    print("Exported models:", exported_files)