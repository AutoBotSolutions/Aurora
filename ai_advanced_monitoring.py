import logging
import time
import psutil


class AdvancedMonitoring:
    """
    Provides advanced monitoring functionality for system performance, including
    real-time metrics collection, periodic logging, and logging configuration.

    The class contains static methods to monitor system performance with details
    such as CPU usage, memory usage, and latency. It supports periodic logging
    of these metrics and allows configuring the logging behavior for customization.

    :ivar attribute1: No attributes are defined in this class as it contains
                      only static methods.
    """

    @staticmethod
    def monitor_performance():
        """
        Monitors real-time system performance and returns a performance report.

        :return: dict containing performance metrics such as CPU usage, memory usage, and latency.
        """
        logging.info("Starting advanced performance monitoring...")

        # Collecting system metrics using psutil
        cpu_usage = psutil.cpu_percent(interval=1)  # CPU usage as percentage
        memory_info = psutil.virtual_memory()  # Memory usage information
        latency = AdvancedMonitoring.simulated_latency()  # Simulated latency for demonstration

        # Creating a performance report
        performance_report = {
            "cpu_usage": f"{cpu_usage}%",
            "memory_usage": f"{memory_info.used / (1024 ** 2):.2f} MB",  # Convert to MB
            "latency": f"{latency} ms"
        }

        # Logging the report
        logging.info("Performance Monitoring Report Generated.")
        logging.debug(f"Performance Details: {performance_report}")
        return performance_report

    @staticmethod
    def simulated_latency():
        """
        Simulates latency measurement for demonstration purposes.
        Replace this with actual model or process latency in real implementations.

        :return: Simulated latency in milliseconds.
        """
        # Simulating latency measurement
        return round(200 + (time.time() % 10))  # Example: fluctuates slightly for a realistic demo

    @staticmethod
    def log_periodic_metrics(interval=60):
        """
        Logs system performance metrics at regular intervals.

        :param interval: Time interval in seconds for periodic logging.
        """
        logging.info("Starting periodic performance logging...")
        try:
            while True:
                metrics = AdvancedMonitoring.monitor_performance()
                logging.info(f"Periodic Metrics: {metrics}")
                time.sleep(interval)
        except KeyboardInterrupt:
            logging.info("Advanced Monitoring terminated by user.")

    @staticmethod
    def setup_logging(level=logging.INFO, log_file=None):
        """
        Configures the logging setup for monitoring.

        :param level: Logging level (default: logging.INFO).
        :param log_file: Optional file path to save logs, logs to console by default.
        """
        handlers = [logging.StreamHandler()]
        if log_file:
            handlers.append(logging.FileHandler(log_file))

        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=handlers,
        )


if __name__ == "__main__":
    # Example execution of the script
    AdvancedMonitoring.setup_logging(level=logging.DEBUG)  # Setting up logging
    logging.info("Starting AI Advanced Monitoring script...")
    AdvancedMonitoring.log_periodic_metrics(interval=30)  # Start periodic monitoring every 30 seconds
