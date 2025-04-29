"""
AI Environment Manager
=======================

The AI Environment Manager is a lightweight and extensible framework for detecting runtime
environments dynamically. It identifies deployment platforms such as AWS, Azure, Google Cloud,
or local environments based on system-specific environment variables.

---

Key Features:
1. **Runtime Environment Detection**: Automatically detects platforms using well-known environment variables.
2. **Dynamic Runtime Adjustments**: Enables platform-specific configurations (e.g., storage paths, logging).
3. **Scalable Deployment Support**: Adaptable to development, staging, and production across multiple platforms.
4. **Extensible Framework**: Easily extendable to support additional platforms or custom identifiers.
5. **Minimal Dependencies**: Built with only the standard library (no external packages required).

---

Author: G.O.D Team
License: MIT
"""

import os


class EnvironmentManager:
    """
    Manages the detection of the current runtime environment based on
    environment variables.

    This class provides a method to determine the operational environment
    where the application is running. It identifies various cloud service
    providers like AWS, Google Cloud, and Azure, or defaults to a local
    environment if none of the specific indicators are present.
    """

    def detect_environment(self) -> str:
        """
        Detects the current runtime environment based on environment variables.

        :return: A string representing the detected environment
                 ('AWS', 'Google Cloud', 'Azure', or 'Local').
        """
        if "AWS_EXECUTION_ENV" in os.environ:
            return "AWS"
        elif "GOOGLE_CLOUD_PROJECT" in os.environ:
            return "Google Cloud"
        elif "AZURE_HTTP_USER_AGENT" in os.environ:
            return "Azure"
        else:
            return "Local"


# ===== Example Usage Section =====
if __name__ == "__main__":
    # Initialize the Environment Manager
    env_manager = EnvironmentManager()

    # Detect the runtime environment
    current_environment = env_manager.detect_environment()

    # Display the detected environment
    print(f"Detected Environment: {current_environment}")


    # Environment-specific configurations (example usage)
    def get_configuration() -> dict:
        """
        Fetches and returns a dictionary containing storage configuration details for
        various platforms.

        Each key in the returned dictionary represents a platform, and the value is a
        description of the storage method used for that platform.

        :return: A dictionary where keys represent storage platforms (e.g., AWS, Google
            Cloud, Azure, Local), and values are descriptions of the corresponding
            storage methods.
        :rtype: dict
        """
        return {
            "AWS": "Using S3 buckets for storage.",
            "Google Cloud": "Using GCS buckets for storage.",
            "Azure": "Using Azure Blob Storage.",
            "Local": "Using local filesystem storage."
        }


    # Retrieve and print platform-specific configuration
    configurations = get_configuration()
    print(f"Configuration: {configurations.get(current_environment, 'No configuration available')}")