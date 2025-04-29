"""
AI Offline Support Module

A robust module for handling offline data processing, caching, and file-based workflows.
Perfect for applications functioning in low-connectivity or completely offline environments.
Supports local data ingestion, caching AI models, and managing file-based operations.

---

**Features:**
1. Read and process local data files.
2. Cache and retrieve models for offline reuse.
3. Graceful handling of common file-related errors.
4. Easily extensible for specific offline workflows (e.g., batch processing, advanced file parsing).

**Requirements:**
- Python >= 3.7
"""

import os
import pickle


class OfflineSupport:
    """
    Provides offline support by enabling caching and retrieval of models and local
    data files. The class allows users to work with pre-downloaded or cached
    resources when internet access is unavailable or limited.

    This class creates and manages a specified directory for caching and retrieving
    models or files, and provides methods for local storage and offline loading.

    :ivar cache_dir: Path to the directory used for caching models or files offline.
    :type cache_dir: str
    """

    def __init__(self, cache_dir="offline_cache"):
        """
        Initializes the offline support system with a specified cache directory.
        :param cache_dir: Path to the cache directory for storing offline models or data.
        """
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        print(f"Offline cache initialized at: {self.cache_dir}")

    def load_data_offline(self, file_path):
        """
        Reads and processes a local file instead of requiring a live connection.
        :param file_path: Path to the local file to be read.
        :return: Contents of the file as a string or an error message if the file is not found.
        """
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            return "Local file not found."
        except Exception as e:
            return f"Error reading file: {e}"

    def cache_model(self, model, model_name):
        """
        Saves a pre-trained model in the offline cache for reuse.
        :param model: Python object representing the model (e.g., ML model, data structure).
        :param model_name: Name to save the model under (without file extension).
        """
        try:
            model_path = os.path.join(self.cache_dir, f"{model_name}.pkl")
            with open(model_path, "wb") as file:
                pickle.dump(model, file)
            print(f"Model '{model_name}' successfully cached at {model_path}.")
        except Exception as e:
            print(f"Failed to cache model '{model_name}': {e}")

    def load_cached_model(self, model_name):
        """
        Loads a previously cached model from the local cache.
        :param model_name: Name of the model to load (without file extension).
        :return: The loaded model object or an error message if the file is not found.
        """
        try:
            model_path = os.path.join(self.cache_dir, f"{model_name}.pkl")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model '{model_name}' not found in cache.")
            with open(model_path, "rb") as file:
                model = pickle.load(file)
            print(f"Model '{model_name}' successfully loaded from {model_path}.")
            return model
        except FileNotFoundError as fnf_error:
            print(fnf_error)
            return None
        except Exception as e:
            print(f"Error loading model '{model_name}': {e}")
            return None


# Example Usage
if __name__ == "__main__":
    # Initialize OfflineSupport object
    offline_support = OfflineSupport()

    # Example 1: Reading a local file
    file_path = "example.txt"  # Replace with an actual file path
    file_contents = offline_support.load_data_offline(file_path)
    print("File Contents:", file_contents)

    # Example 2: Caching a model (dummy dictionary example)
    model_data = {"weights": [0.2, 0.3, 0.5], "model_type": "example_model"}
    offline_support.cache_model(model_data, "example_model")

    # Example 3: Loading a cached model
    loaded_model = offline_support.load_cached_model("example_model")
    if loaded_model:
        print("Loaded Model:", loaded_model)