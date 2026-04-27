"""
AI Error Tracker
=================

The AI Error Tracker is a robust framework for logging, monitoring, and analyzing application errors.
It integrates with a SQLite database to record structured logs of errors, including timestamps, error
messages, severity levels, and execution context.

---

Main Features:
1. **Error Categorization**: Log errors with severity levels (LOW, MEDIUM, HIGH, CRITICAL).
2. **Persistent Logs**: Store logs using SQLite database for long-term analysis.
3. **Dynamic Retrieval**: Query and retrieve errors conditionally based on severity or other metadata.
4. **Minimal Dependencies**: Relies only on Python’s standard library for seamless deployment.

---

Author: G.O.D Team
License: MIT
"""

import sqlite3
import logging
from datetime import datetime


class ErrorTracker:
    """
    Manages error tracking using an SQLite database for structured logging and retrieval.

    The ErrorTracker class allows users to log errors with context and severity levels,
    fetch logged errors (optionally filtered by severity), and clear all error data from the
    database. A SQLite database is used to persist the error-related data.

    :ivar db_path: Path to the SQLite database file.
    :type db_path: str
    """

    def __init__(self, db_path="errors.db"):
        """
        Initialize the ErrorTracker instance and set up the database schema if needed.

        :param db_path: Path to SQLite database file (default: `errors.db`).
        """
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        """
        Initializes the SQLite database schema for error tracking.
        If the table does not exist, it creates it.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS errors (
                                    id INTEGER PRIMARY KEY,
                                    timestamp TEXT,
                                    error_message TEXT,
                                    context TEXT,
                                    severity TEXT
                                  )''')
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Failed to initialize error database: {e}")

    def log_error(self, error_message, context=None, severity="LOW"):
        """
        Log an error into the database.

        :param error_message: Description of the error you want to log.
        :param context: Contextual information or the subsystem where the error occurred.
        :param severity: Error severity (default: 'LOW'). Options: 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'.
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO errors (timestamp, error_message, context, severity)
                                  VALUES (?, ?, ?, ?)''', (timestamp, error_message, context, severity))
                conn.commit()
                logging.info(f"Error logged: {error_message} (Severity: {severity})")
        except sqlite3.Error as e:
            logging.error(f"Failed to log error: {e}")

    def fetch_errors(self, severity=None):
        """
        Retrieve logged errors from the database.

        :param severity: Optional parameter to filter errors by severity level.
        :return: List of errors as tuples (id, timestamp, error_message, context, severity).
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = "SELECT * FROM errors"
                params = []
                if severity:
                    query += " WHERE severity = ?"
                    params.append(severity)
                cursor.execute(query, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Failed to fetch errors: {e}")
            return []

    def delete_all_errors(self):
        """
        Clear all the error logs from the database. Useful for testing or maintenance purposes.

        :return: Number of rows deleted.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                result = cursor.execute("DELETE FROM errors")
                conn.commit()
                logging.info("All error logs have been cleared.")
                return result.rowcount
        except sqlite3.Error as e:
            logging.error(f"Failed to clear all error logs: {e}")
            return 0


# ===== Example Usage =====
if __name__ == "__main__":
    # Initialize an ErrorTracker instance
    tracker = ErrorTracker()

    # Example of logging an error
    try:
        # Simulate some faulty logic
        result = 1 / 0
    except ZeroDivisionError as e:
        tracker.log_error(
            error_message=f"ZeroDivisionError: {str(e)}",
            context="Math Module",
            severity="CRITICAL"
        )

    # Fetch and display all errors
    print("=== Logged Errors ===")
    for error in tracker.fetch_errors():
        print(error)

    # Clean up: Clear all errors (for testing purposes)
    tracker.delete_all_errors()