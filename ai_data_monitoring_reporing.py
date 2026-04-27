import logging


class DataMonitoringReporting:
    """
    Class for monitoring dataset quality and generating reports.

    This class provides functionality to analyze data for missing or inconsistent
    values, calculate quality metrics, and produce a human-readable summary report.
    Additionally, it includes a logging setup to track the execution process and
    debug any potential issues that may arise during the analysis or reporting.

    :ivar logger: Configured logger instance for debugging and process tracking.
    :type logger: logging.Logger
    """

    def __init__(self):
        """
        Initialize the DataMonitoringReporting class and configure logging.
        """
        self.logger = self._setup_logger()

    @staticmethod
    def _setup_logger():
        """
        Configure logging for consistency and debugging.
        :return: Configured logger instance.
        """
        logger = logging.getLogger("DataMonitoringReporting")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def monitor_data_quality(self, data):
        """
        Monitor the quality of the dataset to identify inconsistency or missing data.
        :param data: List or iterable containing the dataset to analyze.
        :return: A dictionary-based quality report.
        """
        self.logger.info("Starting data quality monitoring...")

        try:
            total_values = len(data)
            missing_values = sum(1 for item in data if item is None)
            coverage_percentage = (
                (total_values - missing_values) / total_values * 100
                if total_values > 0
                else 0
            )

            quality_report = {
                "total_values": total_values,
                "missing_values": missing_values,
                "coverage": round(coverage_percentage, 2),
            }

            self.logger.info(f"Data quality report generated: {quality_report}")
            return quality_report

        except Exception as ex:
            self.logger.error(f"Error while monitoring data quality: {ex}")
            raise

    def generate_report(self, quality_report):
        """
        Generate a high-level summary report based on the dataset monitoring results.
        :param quality_report: Data quality report dictionary created by monitor_data_quality.
        :return: A human-readable string summarizing the findings.
        """
        self.logger.info("Generating a summary report...")
        try:
            if not quality_report or not isinstance(quality_report, dict):
                self.logger.error(
                    "Invalid quality report provided. Cannot generate summary."
                )
                return "Error: Could not generate the report. Invalid quality report data."

            report = (
                "=== Data Quality Report ===\n"
                f"Total Values: {quality_report.get('total_values', 0)}\n"
                f"Missing Values: {quality_report.get('missing_values', 0)}\n"
                f"Coverage: {quality_report.get('coverage', 0)}%\n"
            )
            self.logger.info("Summary report generated successfully.")
            return report

        except Exception as ex:
            self.logger.error(f"Error while generating the report: {ex}")
            raise


if __name__ == "__main__":
    # Example usage to demonstrate the functionality of the DataMonitoringReporting class.
    logging.basicConfig(level=logging.INFO)

    # Initialize the DataMonitoringReporting class
    data_monitoring = DataMonitoringReporting()

    # Example dataset
    dataset = [1, None, 2, 3, None, 4, 5, 6]

    # Monitor data quality
    quality_report = data_monitoring.monitor_data_quality(dataset)

    # Print the quality report
    print(f"Quality Report: {quality_report}")

    # Generate and display the report
    print("\n", data_monitoring.generate_report(quality_report))