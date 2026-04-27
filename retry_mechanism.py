"""
===============================================================================
Retry Mechanism - Resilient Operations with Configurable Retry Policies
===============================================================================
A reusable Python module designed to handle transient errors in operations such
as API requests, database interactions, or any function prone to failure.

GitHub Repository: <Insert Repository URL here>
License: MIT License
Maintainer: G.O.D Framework Team
===============================================================================
"""

import time
import logging
from functools import wraps


class RetryMechanism:
    """
    Implements a retry mechanism as a decorator to apply retry logic to any
    function. The retry mechanism supports customizable parameters such as
    maximum retries, initial delay, exponential backoff, and a set of
    exceptions to retry on. This functionality is useful for scenarios where
    operations may intermittently fail (e.g., network requests) and subsequent
    attempts may succeed.

    :ivar max_retries: Maximum number of retry attempts for the decorated function.
    :type max_retries: int
    :ivar delay: Initial delay between retry attempts, specified in seconds.
    :type delay: int
    :ivar backoff: Exponential backoff multiplier applied to the delay after each retry.
    :type backoff: int
    :ivar exceptions: Tuple of exception classes on which retries will be attempted.
    :type exceptions: tuple
    :ivar logger: Optional logger instance used to track and log retry events.
        If not provided, retry messages are printed to the console.
    :type logger: logging.Logger or None
    """

    @staticmethod
    def retry(
            max_retries=3,
            delay=2,
            backoff=2,
            exceptions=(Exception,),
            logger=None
    ):
        """
        Retry decorator to add retry logic to any function.

        Args:
            max_retries (int): The maximum number of retry attempts.
            delay (int): The initial delay between retries (in seconds).
            backoff (int): The multiplier for exponential backoff (e.g., a value of 2 doubles the delay after each retry).
            exceptions (tuple): A tuple of exception classes to retry on.
            logger (logging.Logger): Optional logger instance for tracking retries.

        Returns:
            function: Decorated function with retry logic.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                _retries = 0
                _delay = delay
                while _retries < max_retries:
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        _retries += 1
                        if logger:
                            logger.warning(
                                f"Retry {_retries}/{max_retries} for {func.__name__} failed: {str(e)}. Retrying in {_delay} seconds..."
                            )
                        else:
                            print(
                                f"Retry {_retries}/{max_retries} for {func.__name__} failed: {str(e)}. Retrying in {_delay} seconds..."
                            )
                        time.sleep(_delay)
                        _delay *= backoff
                # After all retries fail
                if logger:
                    logger.error(f"Function {func.__name__} failed after {max_retries} retries.")
                else:
                    print(f"Function {func.__name__} failed after {max_retries} retries.")
                raise

            return wrapper

        return decorator


# Example Usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("RetryMechanism")


    @RetryMechanism.retry(
        max_retries=5,
        delay=1,
        backoff=2,
        exceptions=(ValueError,),
        logger=logger
    )
    def unstable_function():
        """
        Retry decorated function to handle transient errors gracefully with
        exponential backoff and retry mechanism.

        The function ``unstable_function`` is executed with configurable retry
        logic, which retries upon encountering specified exceptions up to a
        maximum number of retries with delay and backoff settings. The retry
        behavior can be monitored using the provided logger.

        :raises ValueError: Raised when a transient error is encountered and
            cannot be resolved after all retries.
        :return: A string indicating the successful execution of the function or
            an exception if all retries fail.
        :rtype: str
        """
        import random
        if random.choice([True, False]):
            raise ValueError("Simulated transient error!")
        return "Function executed successfully!"


    try:
        result = unstable_function()
        logger.info(f"Function succeeded with result: {result}")
    except Exception as e:
        logger.error(f"Function failed: {str(e)}")