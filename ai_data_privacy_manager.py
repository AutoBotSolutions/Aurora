import hashlib
import logging


class DataPrivacyManager:
    """
    Manages data privacy by anonymizing sensitive fields and logging activities in a compliant manner.

    This class is designed to facilitate privacy-aware handling of data by providing methods to anonymize
    specific fields within a data record using SHA-256 hashing. It also ensures that all logged information
    is anonymized for compliance. A configurable list of fields to anonymize can be provided during
    initialization.

    :ivar anonymization_fields: List of field names to be anonymized in records.
    :type anonymization_fields: list
    :ivar logger: Logging instance configured for privacy-compliant activities.
    :type logger: logging.Logger
    """

    def __init__(self, anonymization_fields=None):
        """
        Initialize the DataPrivacyManager with configurable fields to anonymize.
        :param anonymization_fields: A list of field names to anonymize in records.
        """
        self.anonymization_fields = anonymization_fields or []
        self.logger = self._setup_logger()

    @staticmethod
    def _setup_logger():
        """
        Set up the logger configuration for privacy-compliant activities.
        :return: Configured logger instance.
        """
        logger = logging.getLogger("DataPrivacyManager")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def anonymize(self, record):
        """
        Anonymizes sensitive fields in a data record using SHA-256 hashing.
        :param record: A dictionary containing the original data record.
        :return: A dictionary with sensitive fields anonymized.
        """
        try:
            if not isinstance(record, dict):
                raise ValueError("Record must be a dictionary.")

            anonymized_record = {}
            for key, value in record.items():
                if key in self.anonymization_fields:
                    anonymized_record[key] = self._hash_value(value)
                else:
                    anonymized_record[key] = value

            self.logger.info(f"Anonymized record: {anonymized_record}")
            return anonymized_record

        except Exception as e:
            self.logger.error(f"Error during anonymization: {e}")
            raise

    @staticmethod
    def _hash_value(value):
        """
        Hash a given value using SHA-256 for irreversible anonymization.
        :param value: The value to be hashed (must be a string).
        :return: The SHA-256 hashed version of the value.
        """
        try:
            if not isinstance(value, str):
                raise ValueError("Value must be a string for hashing.")
            return hashlib.sha256(value.encode()).hexdigest()
        except Exception as e:
            raise ValueError(f"Error hashing value: {e}")

    def log_with_compliance(self, record):
        """
        Logs anonymized records for privacy compliance, ensuring no sensitive fields are exposed.
        :param record: The original data record to be logged.
        """
        try:
            anonymized_record = self.anonymize(record)
            self.logger.info(f"Compliant log: {anonymized_record}")
        except Exception as e:
            self.logger.error(f"Failed to log data with compliance: {e}")
            raise


if __name__ == "__main__":
    # Example: Demonstrating how to use DataPrivacyManager

    # Configure logging globally for better demonstration
    logging.basicConfig(level=logging.INFO)

    # Define fields to anonymize
    fields_to_anonymize = ["email", "phone_number"]

    # Initialize the privacy manager with specific fields to anonymize
    data_privacy_manager = DataPrivacyManager(anonymization_fields=fields_to_anonymize)

    # Example user data
    user_data = {
        "name": "Alice",
        "email": "alice@example.com",
        "phone_number": "1234567890",
        "address": "123 Main Street"
    }

    # Log data with anonymization for compliance
    try:
        data_privacy_manager.log_with_compliance(user_data)
    except Exception as ex:
        print(f"Error: {ex}")

    # For debugging purposes, directly anonymize records
    anonymized_data = data_privacy_manager.anonymize(user_data)
    print("\nAnonymized Data (Debugging):")
    print(anonymized_data)