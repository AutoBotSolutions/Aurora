"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

import logging
from datetime import datetime
from typing import Optional, Dict


class AuditLogger:
    """
    Handles logging for audit purposes by providing a structured and centralized logging mechanism.

    This class is designed to centralize and standardize the logging of events for auditing
    purposes. The logger can log events to both a file and the console with support for
    customizable log levels. It allows logging of event names, statuses, and optional metadata.

    :ivar log_file: Path to the audit log file where logs are stored.
    :type log_file: str
    :ivar logger: Internal logger instance used for writing audit logs.
    :type logger: logging.Logger
    """

    def __init__(self, log_file: str = "audit.log", log_level: int = logging.INFO):
        """
        Initializes the logging system and sets up the audit log configuration.

        :param log_file: Path to the audit log file (default: "audit.log").
        :param log_level: Logging level (default: logging.INFO).
        """
        self.log_file = log_file
        self.logger = logging.getLogger("AuditLogger")
        self.logger.setLevel(log_level)

        # Configure file handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))
        self.logger.addHandler(file_handler)

        # Configure stream handler to log to console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))
        self.logger.addHandler(console_handler)

    def log_event(self, event_name: str, details: Optional[Dict] = None, status: str = "SUCCESS") -> None:
        """
        Logs an event with a standardized structure for auditing purposes.

        :param event_name: Name or description of the event.
        :param details: Optional details or metadata about the event.
        :param status: Status of the event. Options: "SUCCESS", "FAILURE", "WARNING" (default: "SUCCESS").
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        details = details if details else {}
        log_message = f"{timestamp} | {event_name} | STATUS: {status} | DETAILS: {details}"

        if status.upper() == "SUCCESS":
            self.logger.info(log_message)
        elif status.upper() == "FAILURE":
            self.logger.error(log_message)
        elif status.upper() == "WARNING":
            self.logger.warning(log_message)
        else:
            self.logger.info(f"UNKNOWN STATUS: {log_message}")


# Example usage of the AuditLogger class
if __name__ == "__main__":
    # Initialize the AuditLogger
    logger = AuditLogger(log_file="audit.log")

    # Log some example events
    logger.log_event("System Initialization", {"config_file": "settings.yml"}, "SUCCESS")
    logger.log_event("Data Ingestion", {"rows_loaded": 5000}, "SUCCESS")
    logger.log_event("Data Validation", {"validation_errors": 3}, "WARNING")
    logger.log_event("Model Training Step 2", {"training_time": "35m"}, "SUCCESS")
    logger.log_event("Model Inference Failed", {"error": "Out of memory"}, "FAILURE")
