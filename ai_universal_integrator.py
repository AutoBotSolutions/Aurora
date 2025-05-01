"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

"""
=====================================================================================
AI Universal Integrator
=====================================================================================
The AI Universal Integrator is a lightweight and extensible module that facilitates
seamless integration between AI workflows and external systems such as APIs, 
databases, cloud services, or other endpoints.

GitHub Repository: <https://github.com/<your-repo-link>> (Replace with your link)
License: MIT (or preferred license)
Maintainer: G.O.D Framework Team
=====================================================================================
"""

import requests
import logging
from typing import Dict, Any, Optional


class UniversalIntegrator:
    """
    Represents a universal API integrator with logging capabilities for handling
    HTTP POST requests to various endpoints.

    This class provides a mechanism to send HTTP POST requests to external APIs
    and manage their responses while logging request and response details,
    enabling debugging and monitoring.

    :ivar logger: Logger instance for recording request and response activities.
    :type logger: logging.Logger
    """

    def __init__(self):
        """
        Initializes the UniversalIntegrator with a logging mechanism.
        """
        self.logger = logging.getLogger("UniversalIntegrator")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def call_api(self, endpoint: str, payload: Optional[Dict[str, Any]] = None,
                 headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Sends a POST request to the specified API endpoint and retrieves the response.

        Args:
            endpoint (str): The URL of the API endpoint.
            payload (Optional[Dict[str, Any]]): JSON payload to send in the POST request.
            headers (Optional[Dict[str, str]]): Additional headers for the request.

        Returns:
            Dict[str, Any]: The JSON response from the API.

        Raises:
            requests.exceptions.RequestException: For network-related errors.
            ValueError: If the API response is invalid or empty.
        """
        headers = headers or {}

        self.logger.info(f"Sending POST request to {endpoint} with payload: {payload}")

        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            self.logger.info(f"Received response: {response.json()}")
            return response.json()

        except requests.exceptions.RequestException as e:
            self.logger.error(f"HTTP request to {endpoint} failed: {e}")
            raise

        except ValueError as e:
            self.logger.error(f"API response error: {e}")
            raise


if __name__ == "__main__":
    """
    Example usage of UniversalIntegrator
    """

    # Example #1: Basic API call with JSON payload
    try:
        integrator = UniversalIntegrator()
        endpoint = "https://jsonplaceholder.typicode.com/posts"
        payload = {
            "title": "AI Universal Integrator",
            "body": "This example demonstrates integration.",
            "userId": 1
        }
        response = integrator.call_api(endpoint, payload=payload)
        print("Response from API:", response)

    except Exception as e:
        print(f"Error occurred while making API call: {e}")

    # Example #2: API call with custom headers
    try:
        custom_headers = {"Authorization": "Bearer your_access_token"}
        response_with_headers = integrator.call_api(
            endpoint="https://jsonplaceholder.typicode.com/posts",
            payload=payload,
            headers=custom_headers
        )
        print("Response with headers:", response_with_headers)

    except Exception as e:
        print(f"Error occurred while making API call with headers: {e}")
