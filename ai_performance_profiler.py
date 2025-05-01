"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

"""
Performance Profiler

The Performance Profiler is an essential tool for analyzing, profiling, and optimizing pipeline performance in AI workflows. It provides execution time tracking for pipeline stages, result caching for computational efficiency, and detailed logging for auditing and debugging purposes.

---

**Key Features**:
1. **Execution Time Profiling**: Measures the execution time of pipeline stages and logs the results.
2. **Caching**: Avoids redundant computations for expensive functions using Python's `lru_cache`.
3. **Integrated Logging**: Logs all profiling and caching events into a file for performance tracking.

**Open Source Readiness**:
- Modular design for easy integration within larger frameworks (e.g., G.O.D Framework).
- Compatible with Python 3.7+ and uses minimal dependencies for broader applicability.

**Author**: G.O.D Framework Team
"""

import time
import logging
from functools import lru_cache
from typing import Any, Callable


class PerformanceProfiler:
    """
    A utility class for profiling the performance of functions and caching results.

    The `PerformanceProfiler` class provides tools to measure execution times of specific
    functions or pipeline stages and cache results of expensive function calls. This can
    be helpful for optimizing performance-critical sections in a program, identifying slow
    processes, and avoiding redundant computations.

    :ivar log_file: File name where performance logs will be written.
    :type log_file: str
    """

    def __init__(self, log_file: str = "performance.log"):
        """
        Initializes the Performance Profiler and sets up logging.

        :param log_file: File name where performance logs will be written.
        """
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s]: %(message)s",
        )
        logging.info("Performance Profiler initialized.")

    def profile_stage(self, stage_name: str, func: Callable, *args, **kwargs) -> Any:
        """
        Measures and logs the execution time of a specific function or pipeline stage.

        :param stage_name: A descriptive name for the pipeline stage (used in logs).
        :param func: The function whose performance will be profiled.
        :param args: Positional arguments to be passed to the function.
        :param kwargs: Keyword arguments to be passed to the function.
        :return: The result of the function execution.
        """
        logging.info(f"Starting stage: '{stage_name}'")
        start_time = time.time()

        # Execute the function
        result = func(*args, **kwargs)

        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        logging.info(f"Stage '{stage_name}' completed in {elapsed_time:.2f} seconds.")
        return result

    @staticmethod
    def cache_step(maxsize: int = 10) -> Callable:
        """
        A decorator to cache results of expensive function calls to avoid redundant computations.

        :param maxsize: Maximum size of the cache (number of stored function calls).
        :return: A decorator for caching functions.
        """

        def decorator(func: Callable) -> Callable:
            @lru_cache(maxsize=maxsize)
            def wrapped_function(*args, **kwargs):
                # Logging the cache usage
                logging.info(f"Caching result for function '{func.__name__}' with args {args}, kwargs {kwargs}")
                return func(*args, **kwargs)

            wrapped_function.cache_clear = func.cache_clear  # Allow clearing the cache if needed
            return wrapped_function

        return decorator


# Example Usage
if __name__ == "__main__":
    # Step 1: Initialize the profiler
    profiler = PerformanceProfiler(log_file="performance_metrics.log")


    # Step 2: Sample function to profile
    def sample_task(data: list):
        """
        Processes a list of numbers by doubling each element after simulating
        a delay to represent a computationally intensive task.

        :param data: A list of numerical values to be processed
        :type data: list
        :return: A new list where each element of the input list is doubled
        :rtype: list
        """
        time.sleep(2)  # Simulate a heavy computation
        return [item * 2 for item in data]


    # Step 3: Profile the sample task
    data = [1, 2, 3, 4, 5]
    result = profiler.profile_stage("Sample Task Execution", sample_task, data)
    print(f"Result: {result}")


    # Step 4: Add a computationally expensive function with caching
    @profiler.cache_step(maxsize=5)
    def expensive_computation(x: int):
        """
        Performs an expensive computation by squaring the given integer.

        This function simulates a time-intensive operation by inducing a delay
        of 3 seconds. It uses caching to store the results for up to five unique
        inputs, improving performance for repeated calls with the same arguments.

        :param x: The integer input to be squared.
        :type x: int
        :return: The square of the input integer.
        :rtype: int
        """
        time.sleep(3)  # Simulating an expensive calculation
        return x ** 2


    # Step 5: Call the cached function
    print("First call (cached result not available):", expensive_computation(10))
    print("Second call (cached result available):", expensive_computation(10))
    print("Third call with new input (cached result not available):", expensive_computation(15))
