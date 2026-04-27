import logging
import pandas as pd
import re


class DataMasking:
    """
    Provides functionality for masking sensitive data in datasets.

    The DataMasking class is specifically designed for masking sensitive
    data in pandas DataFrames. Masking can be applied to entire columns,
    and format-preserving masking options are available for specific data
    types such as email addresses and phone numbers. This class also
    includes logging support for tracking the masking process.

    :ivar logger: Logger instance for logging operations within the class.
    :type logger: logging.Logger
    :ivar placeholder: Placeholder string used to replace masked data.
    :type placeholder: str
    """

    def __init__(self, placeholder="[MASKED]"):
        """
        Initialize the DataMasking class with a default placeholder for masking.
        :param placeholder: The placeholder string used to mask sensitive data.
        """
        self.logger = self._setup_logger()
        self.placeholder = placeholder

    @staticmethod
    def _setup_logger():
        """
        Configures and returns a logger instance for the DataMasking class.
        :return: A logging.Logger object.
        """
        logger = logging.getLogger("DataMasking")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def mask_columns(self, data, columns):
        """
        Mask specified columns in the dataset using the placeholder.
        :param data: Pandas DataFrame containing the dataset.
        :param columns: List of column names to mask.
        :return: Masked Pandas DataFrame.
        """
        self.logger.info("Starting the masking process for specified columns...")
        try:
            for col in columns:
                if col in data.columns:
                    self.logger.info(f"Masking column: {col}")
                    data[col] = self.placeholder
                else:
                    self.logger.warning(f"Column '{col}' not found in the DataFrame.")
            self.logger.info("Completed masking specified columns.")
            return data
        except Exception as e:
            self.logger.error(f"Error occurred while masking columns: {e}")
            raise

    def mask_with_format(self, data, column, format_type):
        """
        Mask the content of a column while preserving a specific format.
        :param data: Pandas DataFrame containing the dataset.
        :param column: The column name to be masked.
        :param format_type: Type of formatting ('email', 'phone', etc.).
        :return: DataFrame with the formatted, masked column.
        """
        self.logger.info(f"Applying format-preserving masking to column: {column}")
        if column not in data.columns:
            self.logger.error(f"Column '{column}' not found in the DataFrame.")
            raise ValueError(f"Column '{column}' does not exist in the dataset.")
        try:
            if format_type == "email":
                data[column] = data[column].apply(self._mask_email)
            elif format_type == "phone":
                data[column] = data[column].apply(self._mask_phone)
            else:
                self.logger.warning(f"Unsupported format type: {format_type}. No masking applied.")
            return data
        except Exception as e:
            self.logger.error(f"Error occurred while applying format-preserving masking: {e}")
            raise

    @staticmethod
    def _mask_email(email):
        """
        Mask an email address while retaining the domain.
        :param email: The email address as a string.
        :return: Masked email address.
        """
        try:
            domain = email.split("@")[-1]
            return f"masked_user@{domain}"
        except Exception:
            return "[MASKED]"

    @staticmethod
    def _mask_phone(phone):
        """
        Mask a phone number while keeping the last four digits visible.
        :param phone: The phone number as a string.
        :return: Masked phone number.
        """
        try:
            return re.sub(r"\d(?=\d{4})", "X", phone)
        except Exception:
            return "[MASKED]"


if __name__ == "__main__":
    # Example Usage
    # Enable logging to the console
    logging.basicConfig(level=logging.INFO)

    # Create a sample dataset
    data = pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie"],
        "Email": ["alice@example.com", "bob@example.com", "charlie@example.com"],
        "Phone": ["123-456-7890", "987-654-3210", "555-555-5555"],
        "SSN": ["123-45-6789", "987-65-4321", "567-89-1234"]
    })

    # Initialize the DataMasking class
    data_masker = DataMasking()

    # Mask specific columns entirely
    print("\n=== Mask Entire Columns ===")
    masked_data = data_masker.mask_columns(data.copy(), columns=["SSN", "Email"])
    print(masked_data)

    # Format-preserving masking for sensitive columns
    print("\n=== Mask Emails with Domain Preservation ===")
    masked_email_data = data_masker.mask_with_format(data.copy(), column="Email", format_type="email")
    print(masked_email_data)

    print("\n=== Mask Phone Numbers (Keep Last 4 Digits) ===")
    masked_phone_data = data_masker.mask_with_format(data.copy(), column="Phone", format_type="phone")
    print(masked_phone_data)