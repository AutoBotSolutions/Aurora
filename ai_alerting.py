"""
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT (or choose your open-source license)
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

import smtplib
from email.mime.text import MIMEText
import logging
import os


class AlertingSystem:
    """
    A system for sending email alerts using SMTP settings.

    This class facilitates the sending of alert emails. It requires SMTP
    configuration details including server address, port number, sender's and
    receiver's email addresses, and the sender’s email password. This system
    ensures secure communication using TLS encryption before sending emails.

    :ivar smtp_settings: Dictionary containing the following SMTP credentials and settings:
        - smtp_server: SMTP server address
        - port: SMTP server port
        - sender_email: The sender's email address
        - receiver_email: The recipient's email address
        - password: The sender's email password
    :type smtp_settings: dict
    """

    def __init__(self, smtp_settings):
        """
        Initialize the AlertingSystem with specified SMTP settings.

        :param smtp_settings: Dictionary containing SMTP credentials and settings:
            - smtp_server: SMTP server address
            - port: SMTP server port
            - sender_email: The sender's email address
            - receiver_email: The recipient's email address
            - password: The sender's email password
        """
        self.smtp_settings = smtp_settings

    def send_email_alert(self, subject, body):
        """
        Sends an alert email to the specified recipient.

        :param subject: Subject of the email
        :param body: Content of the email
        """
        try:
            # Create the email message
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = self.smtp_settings["sender_email"]
            msg["To"] = self.smtp_settings["receiver_email"]

            # Connect to the SMTP server and send the email
            with smtplib.SMTP(self.smtp_settings["smtp_server"], self.smtp_settings["port"]) as server:
                server.starttls()  # Upgrade the connection to secure
                server.login(self.smtp_settings["sender_email"], self.smtp_settings["password"])
                server.sendmail(
                    self.smtp_settings["sender_email"],
                    self.smtp_settings["receiver_email"],
                    msg.as_string()
                )
                logging.info("Alert email sent successfully.")

        except Exception as e:
            logging.error(f"Failed to send email alert: {e}")


def setup_logging(level=logging.INFO, log_file=None):
    """
    Sets up logging for the application by configuring the log level,
    log format, and output handlers. The function allows the logs
    to be displayed in the console and optionally saved to a file.

    :param level: The logging level (e.g., logging.INFO, logging.DEBUG).
    :type level: int
    :param log_file: The path to a file where logs should be written. If not
        provided, logs will only appear in the console.
    :type log_file: str or None
    :return: None
    """
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=handlers
    )


if __name__ == "__main__":
    # Configure logging
    setup_logging(log_file="alerting.log")

    # SMTP configuration: Use environment variables or secure storage for sensitive data
    smtp_settings = {
        "smtp_server": os.getenv("SMTP_SERVER", "smtp.mailtrap.io"),
        "port": int(os.getenv("SMTP_PORT", 587)),
        "sender_email": os.getenv("SMTP_SENDER_EMAIL", "sender@example.com"),
        "receiver_email": os.getenv("SMTP_RECEIVER_EMAIL", "receiver@example.com"),
        "password": os.getenv("SMTP_PASSWORD", "your_password"),
    }

    # Initialize the alerting system
    alert = AlertingSystem(smtp_settings)

    # Example: Simulating pipeline execution and error alerting
    try:
        logging.info("Starting pipeline execution...")
        # Simulated function: execute_pipeline()
        raise RuntimeError("Simulated pipeline failure for testing alert email.")
    except Exception as e:
        logging.error(f"Pipeline error detected: {e}")
        alert.send_email_alert(
            subject="Pipeline Execution Failure!",
            body=f"The pipeline encountered an error: {e}"
        )
