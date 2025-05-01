"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

import pandas as pd
import logging


class DataValidator:
    """
    DataValidator class for data validation and preprocessing.

    The purpose of this class is to provide methods for validating a pandas DataFrame
    against an expected schema, handling missing values, and ensuring the data is clean
    and ready for further processing. It logs details of the validation process and
    supports multiple strategies for dealing with missing data.

    :ivar schema: Dictionary that maps column names to their expected data types. It is
        used for schema validations.
    :type schema: dict
    :ivar logger: Logger instance for logging validation activities and errors.
    :type logger: logging.Logger
    """

    def __init__(self, schema=None, logger_name="DataValidatorLogger"):
        """
        Initialize the DataValidator class.

        :param schema: Dictionary mapping column names to expected data types (optional).
        :param logger_name: Name of the logger used for validation messages.
        """
        self.schema = schema if schema else {}
        self.logger = self._setup_logger(logger_name)

    def _setup_logger(self, logger_name):
        """
        Set up the logger for the validation process.

        :param logger_name: The name of the logger to create.
        :return: A configured logger instance.
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()  # Output to console
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        if not logger.handlers:
            logger.addHandler(handler)
        return logger

    def validate_schema(self, dataframe):
        """
        Validate the input dataframe against the expected schema.

        :param dataframe: Input pandas DataFrame to validate.
        :return: Boolean indicating whether the schema validation passed.
        """
        self.logger.info("Starting schema validation.")

        for column, expected_type in self.schema.items():
            if column not in dataframe.columns:
                self.logger.error(f"Schema Validation Error: Missing required column '{column}'.")
                return False
            if not self._check_column_type(dataframe[column], expected_type):
                self.logger.error(f"Schema Validation Error: Column '{column}' is not of type '{expected_type}'.")
                return False

        self.logger.info("Schema validation passed.")
        return True

    @staticmethod
    def _check_column_type(column, expected_type):
        """
        Internal utility to check if a column matches the expected data type.

        :param column: The DataFrame column to check.
        :param expected_type: The expected data type (e.g., 'numeric', 'string', 'datetime').
        :return: Boolean indicating if the column matches the expected type.
        """
        try:
            if expected_type == "numeric":
                return pd.api.types.is_numeric_dtype(column)
            elif expected_type == "string":
                return pd.api.types.is_string_dtype(column)
            elif expected_type == "datetime":
                return pd.api.types.is_datetime64_any_dtype(column)
        except Exception:  # Catch any unexpected errors
            return False
        return False

    def handle_missing_values(self, dataframe, strategy="mean"):
        """
        Handles missing values in the dataset using the specified strategy.

        :param dataframe: Input pandas DataFrame with potential missing values.
        :param strategy: The strategy to handle missing values ('mean', 'median', 'mode', or 'drop').
        :return: Cleaned pandas DataFrame.
        """
        self.logger.info(f"Handling missing values using the '{strategy}' strategy.")

        for column in dataframe.columns:
            if dataframe[column].isnull().sum() > 0:  # Check if the column contains missing values
                if strategy == "mean" and pd.api.types.is_numeric_dtype(dataframe[column]):
                    dataframe[column].fillna(dataframe[column].mean(), inplace=True)
                    self.logger.info(f"Column '{column}': Filled missing values with mean.")
                elif strategy == "median" and pd.api.types.is_numeric_dtype(dataframe[column]):
                    dataframe[column].fillna(dataframe[column].median(), inplace=True)
                    self.logger.info(f"Column '{column}': Filled missing values with median.")
                elif strategy == "mode":
                    dataframe[column].fillna(dataframe[column].mode()[0], inplace=True)
                    self.logger.info(f"Column '{column}': Filled missing values with mode.")
                elif strategy == "drop":
                    dataframe.dropna(subset=[column], inplace=True)
                    self.logger.info(f"Column '{column}': Dropped rows with missing values.")

        self.logger.info("Missing value handling completed.")
        return dataframe

    def validate(self, dataframe):
        """
        Perform complete validation on the input dataframe:
        1. Ensures it matches the schema (if defined).
        2. Checks for and logs missing values.

        :param dataframe: Input pandas DataFrame.
        :return: Boolean indicating if the data passed all validation steps.
        """
        self.logger.info("Starting full data validation.")
        if self.schema and not self.validate_schema(dataframe):
            self.logger.error("Validation failed during schema check.")
            return False

        if dataframe.isnull().any().any():
            self.logger.warning("Validation Warning: Data contains missing values.")
            return False

        self.logger.info("Data validation passed.")
        return True


if __name__ == "__main__":
    # Example Usage
    logging.basicConfig(level=logging.INFO)  # Configure logging at the root level

    # Define a sample schema for validation
    schema = {
        "id": "numeric",
        "name": "string",
        "age": "numeric",
        "signup_date": "datetime",
    }

    # Instantiate the DataValidator
    validator = DataValidator(schema)

    # Example DataFrame
    data = {
        "id": [1, 2, 3, None],
        "name": ["Alice", "Bob", None, "Eve"],
        "age": [25, None, 30, 22],
        "signup_date": ["2023-01-01", "2023-02-01", "invalid_date", None],
    }
    df = pd.DataFrame(data)

    # Ensure 'signup_date' is parsed as datetime, handling errors
    try:
        df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
    except Exception as e:
        logging.error(f"Error while parsing dates: {e}")

    print("Original DataFrame:")
    print(df)

    # Validate schema
    print("\nSchema validation result:")
    schema_valid = validator.validate_schema(df)
    print(f"Schema Validation: {'Passed' if schema_valid else 'Failed'}")

    # Handle missing values
    print("\nHandling missing values with 'mean' strategy:")
    clean_df = validator.handle_missing_values(df, strategy="mean")
    print(clean_df)

    # Perform full data validation
    print("\nFull validation result:")
    is_valid = validator.validate(clean_df)
    print(f"Full Validation: {'Passed' if is_valid else 'Failed'}")
