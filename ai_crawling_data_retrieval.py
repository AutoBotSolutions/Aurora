"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""


import logging
import requests
from threading import Thread


class DataRetrieval:
    """
    Manages the process of retrieving and handling data from multiple external sources.

    This class is designed to handle concurrent data fetching from various URLs or API
    endpoints using multi-threading. It initializes with a list of sources and provides
    methods to fetch data in parallel while logging the process. It ensures error
    handling during data retrieval for robust performance.

    :ivar sources: List of data sources (URLs or API endpoints) to fetch data from.
    :type sources: list
    :ivar data: A dictionary storing the fetched data or error messages for each source.
    :type data: dict
    :ivar logger: A logger instance for logging the data retrieval process.
    :type logger: logging.Logger
    """

    def __init__(self, sources):
        """
        Initializes the DataRetrieval instance with a list of data sources.

        :param sources: List of URLs or API endpoints to retrieve data from.
        """
        self.sources = sources
        self.data = {}
        self.logger = self._setup_logger()

    @staticmethod
    def _setup_logger():
        """
        Configures and returns a logger instance.

        :return: Configured logger instance.
        """
        logger = logging.getLogger('DataRetrieval')
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        return logger

    def fetch_external_data(self, source):
        """
        Fetch data from a given URL or API endpoint.

        :param source: Target URL or API endpoint.
        """
        self.logger.info(f"Fetching data from: {source}")
        try:
            response = requests.get(source, timeout=10)  # Set a timeout of 10 seconds
            response.raise_for_status()
            self.data[source] = response.json()  # Parse JSON response
            self.logger.info(f"Data retrieved successfully from {source}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error occurred while fetching data from {source}: {e}")
            self.data[source] = {"error": str(e)}

    def start_crawling(self):
        """
        Starts the parallel data retrieval process using multi-threading.
        """
        threads = []
        for source in self.sources:
            thread = Thread(target=self.fetch_external_data, args=(source,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.logger.info("Crawling completed. Retrieved data from all sources.")
        return self.data


if __name__ == "__main__":
    # Example usage of the DataRetrieval class
    logging.basicConfig(level=logging.INFO)

    # List of example API endpoints for testing
    data_sources = [
        "https://jsonplaceholder.typicode.com/posts",
        "https://jsonplaceholder.typicode.com/comments",
        "https://api.spacexdata.com/v4/launches/latest"
    ]

    # Instantiate and use the DataRetrieval module
    data_retriever = DataRetrieval(data_sources)
    retrieved_data = data_retriever.start_crawling()

    # Display the retrieved data
    for source, data in retrieved_data.items():
        print(f"Source: {source}")
        print(f"Data: {data}\n")
