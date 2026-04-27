"""
===============================================================================
Data Fetcher Module
===============================================================================
A reusable, modular system for fetching data from various sources, such as 
local files, REST APIs, and caching mechanisms. This script is designed to 
support scalability, error recovery, and integration with AI/ML pipelines.

GitHub Repository: <Insert Repository URL here>
License: MIT License
Maintainer: G.O.D Framework Team
===============================================================================
"""

import os
import logging
import requests
import time
from functools import lru_cache


class DataFetcher:
    """
    Provides functionalities for fetching data from local files or REST APIs while supporting optional
    caching and error notification mechanisms.

    This class is designed for scenarios involving data retrieval from various sources such as local files or
    remote APIs. It includes features for retry logic on API calls, configurable request headers, and error
    notification handling for better robustness in data-fetching workflows.

    :ivar base_url: The base URL for REST API endpoints.
    :type base_url: str
    :ivar headers: HTTP headers to be included in API requests.
    :type headers: dict
    :ivar logger: Logger instance for logging class activities and events.
    :type logger: logging.Logger
    """

    def __init__(self, base_url=None, headers=None):
        """
        Initializes the DataFetcher class with optional API base URL and headers.
        
        Args:
            base_url (str): Base URL for REST API requests.
            headers (dict): HTTP headers to include in API requests.
        """
        self.base_url = base_url
        self.headers = headers or {"Content-Type": "application/json"}
        self.logger = logging.getLogger("DataFetcher")

    @staticmethod
    def fetch_from_file(file_path):
        """
        Fetches data from a local file.

        Args:
            file_path (str): Path to the file to be fetched.

        Returns:
            str: Contents of the file.
        
        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If there is an issue reading the file.
        """
        logging.info(f"Fetching data from file: {file_path}...")
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        try:
            with open(file_path, "r") as file:
                data = file.read()
                logging.info("Data fetched successfully from file.")
                return data
        except IOError as e:
            logging.error(f"Failed to read file {file_path}: {e}")
            raise

    def fetch_from_api(self, endpoint, params=None, max_retries=3):
        """
        Fetches data from a REST API endpoint with retry logic.

        Args:
            endpoint (str): API endpoint to fetch data from.
            params (dict): Optional query parameters for the API call.
            max_retries (int): Number of retry attempts for failed requests.

        Returns:
            dict: Parsed JSON response from the API.

        Raises:
            Exception: If the maximum retry limit is exceeded without success.
        """
        url = f"{self.base_url}{endpoint}"
        retries = 0

        while retries < max_retries:
            try:
                self.logger.info(f"Fetching data from API: {url}, attempt {retries + 1}/{max_retries}")
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
                response.raise_for_status()
                self.logger.info("Data fetched successfully from API.")
                return response.json()
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"API request failed ({retries + 1}/{max_retries}): {e}")
                retries += 1
                time.sleep(2 ** retries)  # Exponential backoff
            except Exception as e:
                self.logger.error(f"Unexpected error during API request: {e}")
                raise

        self.logger.error(f"Failed to fetch data from API after {max_retries} attempts.")
        raise Exception(f"Failed to fetch data from API: {url}")

    @lru_cache(maxsize=512)
    def fetch_with_caching(self, endpoint, params=None):
        """
        Fetches data from a REST API endpoint and caches the result.

        Args:
            endpoint (str): API endpoint to fetch data from.
            params (dict): Optional query parameters for the API call.

        Returns:
            dict: Cached or newly fetched JSON response from the API.
        """
        self.logger.info(f"Fetching data with caching for endpoint: {endpoint}")
        return self.fetch_from_api(endpoint, params)

    def notify_error(self, error_message):
        """
        Logs and optionally notifies about an error.

        Args:
            error_message (str): The error message to handle.
        """
        self.logger.error(f"Data Fetcher Error: {error_message}")
        # Placeholder for integration with Slack, email, or other notification tools


# Example usage
if __name__ == "__main__":
    # Configure logger
    logging.basicConfig(
        filename="data_fetcher.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Fetch data from a file
    try:
        file_path = "path/to/local_file.txt"
        content = DataFetcher.fetch_from_file(file_path)
        print("File Data:", content)
    except Exception as e:
        print(f"Error fetching file: {e}")

    # Fetch data from an API (if base_url is configured)
    try:
        api_base_url = "https://api.example.com"
        fetcher = DataFetcher(base_url=api_base_url)
        api_data = fetcher.fetch_from_api("/data", params={"query": "example"})
        print("API Data:", api_data)
    except Exception as e:
        print(f"Error fetching API data: {e}")