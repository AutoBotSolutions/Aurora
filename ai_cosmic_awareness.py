from datetime import datetime
import requests
import logging


class CosmicAwareness:
    """
    Manages the CosmicAwareness module.

    The CosmicAwareness class is responsible for logging initialization and
    provides static methods to fetch the current Universal Coordinated Time (UTC)
    as well as retrieve positional data for celestial bodies from the Système Solaire API.

    :ivar logger: The logger instance used for recording log messages.
    :type logger: logging.Logger
    """

    def __init__(self):
        """
        Initializes the CosmicAwareness module and its logger.
        """
        self.logger = logging.getLogger('CosmicAwareness')
        self.logger.setLevel(logging.INFO)

        # Configure logging to output to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        self.logger.info("CosmicAwareness module initialized.")

    @staticmethod
    def current_time() -> str:
        """
        Retrieves the current Universal Coordinated Time (UTC).

        :return: A string representing the current UTC time in 'YYYY-MM-DD HH:MM:SS' format.
        """
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        return now

    @staticmethod
    def planet_position(body: str = "earth") -> str:
        """
        Retrieves positional data of a specific celestial body from the Système Solaire API.

        :param body: The name of the celestial object (default is "earth").
        :return: A string containing the positional data (semi-major axis) of the celestial body.
        """
        api_url = f"https://api.le-systeme-solaire.net/rest/bodies/{body.lower()}"
        try:
            response = requests.get(api_url, timeout=10)  # Set timeout to 10 seconds
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            if 'semimajorAxis' in data:
                position = f"{body.capitalize()}'s semi-major axis: {data['semimajorAxis']} km"
                return position
            else:
                return f"Data for {body} is incomplete in the API response."
        except requests.exceptions.RequestException as e:
            return f"API request failed: {e}"


if __name__ == "__main__":
    # Initialize the CosmicAwareness module
    cosmic = CosmicAwareness()

    # Retrieve current Universal Time
    now = cosmic.current_time()
    print(f"Current Time (UTC): {now}")

    # Retrieve Earth's positional data
    earth_position = cosmic.planet_position()
    print(f"Earth's Position: {earth_position}")

    # Example: Retrieve Mars' positional data
    mars_position = cosmic.planet_position("mars")
    print(f"Mars' Position: {mars_position}")