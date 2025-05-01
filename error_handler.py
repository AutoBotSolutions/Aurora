"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

"""
===============================================================================
Error Handler Module
===============================================================================
A centralized utility for managing and logging exceptions, and retrying 
transient operations in your applications. This module ensures system 
resilience through retry mechanisms and structured error reporting.

GitHub Repository: <Insert Repository URL here>
License: MIT License
Maintainer: G.O.D Framework Team
===============================================================================
"""

import logging
import traceback


class ErrorHandler:
    """
    Manages error handling, including logging, retrying operations, and error recovery.

    The ErrorHandler class provides utilities for managing application errors more efficiently. It can
    log exceptions with appropriate context, retry failed operations based on customized rules, and handle
    errors in a controlled manner. Its primary use case is to encapsulate consistent error management
    across an application.

    The class maintains a logger to store error details in a log file for further analysis and debugging.
    Additionally, it provides retry functionality for transient errors or recoverable operations by
    utilizing customizable retry mechanisms like delays or backoff strategies.

    :ivar logger: Logger instance used for recording error logs and messages in the system.
    :type logger: logging.Logger
    """

    def __init__(self, log_file="error_handler.log"):
        """
        Initializes the ErrorHandler with a logger.

        Args:
            log_file (str): Path to the log file for error logs.
        """
        self.logger = logging.getLogger("ErrorHandler")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.info("ErrorHandler initialized successfully.")

    def log_exception(self, error, context=""):
        """
        Logs an exception with stack trace and additional context.

        Args:
            error (Exception): The exception to log.
            context (str): Additional context about the exception.
        """
        self.logger.error(f"Exception occurred: {context}\n{traceback.format_exc()}")

    def retry_operation(self, function, retries=3, context="", delay_function=None):
        """
        Retries a function in case of failure, with optional delay between attempts.

        Args:
            function (Callable): The function to be retried.
            retries (int): Number of retry attempts.
            context (str): Explanation or context about the operation.
            delay_function (Callable, optional): A function that introduces delays 
                (e.g., exponential backoff) between retries.

        Returns:
            Any: Result of the function, if successful.

        Raises:
            Exception: If all retry attempts fail.
        """
        for attempt in range(retries):
            try:
                self.logger.info(f"Attempt {attempt + 1}/{retries}: {context}")
                return function()
            except Exception as error:
                self.logger.warning(f"Attempt {attempt + 1} failed: {error}")
                self.log_exception(error, context)

                # Delay implementation for retries
                if delay_function:
                    self.logger.info(f"Applying delay through delay_function after attempt {attempt + 1}")
                    delay_function(attempt)

        self.logger.error(f"All {retries} attempts failed for operation: {context}")
        raise Exception(f"Operation failed after {retries} retries: {context}")

    def handle_error(self, error, retry_function=None, retries=3, delay_function=None):
        """
        Handles and logs an error, optionally retrying a function in case of failure.

        Args:
            error (Exception): The error/exception caught.
            retry_function (Callable): The function to retry, if any.
            retries (int): Number of retries for retryable function.
            delay_function (Callable, optional): A custom delay handler for retries.

        Returns:
            Any: Result of the retry_function, if successful.

        Raises:
            Exception: When retries are exhausted or retry_function is not specified.
        """
        self.logger.error(f"Error occurred: {error}")
        if retry_function and retries > 0:
            self.logger.info("Retrying operation using handle_error.")
            try:
                return self.retry_operation(retry_function, retries=retries, delay_function=delay_function)
            except Exception as retry_error:
                self.log_exception(retry_error, "Final retry attempt failed.")
                raise
        else:
            self.logger.error("No retries or retry function specified. Handling error as-is.")
            raise Exception(f"Unhandled error: {error}")


# Example Usage
if __name__ == "__main__":
    import time

    # Configure logging
    logging.basicConfig(
        filename="error_handler_example.log",
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


    def unreliable_function():
        """
        Performs a random operation that has a chance of failure.

        This function simulates an unreliable operation. There is a 50% chance that
        it will raise a ValueError simulating a failure; otherwise, it will succeed
        and return a success message.

        :raises ValueError: If the random operation fails, a ValueError is raised
            with an appropriate message.
        :return: If the operation is successful, a success string is returned.
        :rtype: str
        """
        import random
        if random.random() < 0.5:
            raise ValueError("Random failure occurred!")
        return "Function succeeded!"


    def delay_function(attempt):
        """
        Calculates an exponential delay based on the given attempt number and pauses
        execution for the specified time duration. The function is useful for implementing
        retry mechanisms with an increasing delay between attempts.

        :param attempt: Current attempt number used to calculate the delay duration.
        :type attempt: int
        :return: None
        """
        delay = 2 ** attempt
        print(f"Delaying for {delay} seconds...")
        time.sleep(delay)


    # Initialize ErrorHandler
    handler = ErrorHandler()

    # Example 1: Simple error logging
    try:
        raise ValueError("Example Exception")
    except ValueError as e:
        handler.log_exception(e, context="Example exception logging")
        print("Logged the exception.")

    # Example 2: Retry an unreliable function
    try:
        result = handler.retry_operation(
            unreliable_function,
            retries=3,
            context="Testing retry logic with unreliable_function",
            delay_function=delay_function
        )
        print("Result of function:", result)
    except Exception as e:
        print(f"Final failure after retries: {e}")

    # Example 3: Using handle_error with retries
    try:
        result = handler.handle_error(
            ValueError("Simulated initial error"),
            retry_function=unreliable_function,
            retries=3,
            delay_function=delay_function
        )
        print("Final result:", result)
    except Exception as e:
        print(f"Operation failed after handle_error retries: {e}")
