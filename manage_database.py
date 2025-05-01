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
Database Manager for SQLite - Manage and Query Metrics
===============================================================================
A robust and extensible SQLite database manager for handling metrics efficiently.
Designed for integration with the G.O.D Framework or any other Python-based system.

GitHub Repository: <Insert Repository URL here>
License: MIT License
Maintainer: G.O.D Framework Team
===============================================================================
"""

import sqlite3
import logging
from contextlib import contextmanager


class DatabaseManagerSQL:
    """
    Manages an SQLite database for storing and retrieving metrics.

    This class serves as an interface for interacting with an SQLite database,
    handling database connections, schema initialization, storing metrics, and
    executing queries. It ensures a standardized, reliable method to log and
    manage metrics while encapsulating error handling and logging.

    :ivar db_path: Path to the SQLite database file.
    :type db_path: str
    :ivar connection: SQLite connection object.
    :type connection: sqlite3.Connection or None
    :ivar cursor: SQLite cursor object.
    :type cursor: sqlite3.Cursor or None
    :ivar logger: Logger instance to log database operations.
    :type logger: logging.Logger
    """

    def __init__(self, db_path):
        """
        Initialize the database connection and ensure the schema exists.

        Args:
            db_path (str): The SQLite database file path.
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.logger = logging.getLogger("DatabaseManagerSQL")
        self._setup_logger()
        self._connect()
        self._initialize_schema()

    def _setup_logger(self):
        """
        Configures the logger to track database operations.
        """
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def _connect(self):
        """
        Establish a connection to the database.
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            self.logger.info(f"Connected to SQLite database at {self.db_path}")
        except sqlite3.Error as e:
            self.logger.error(f"Database connection error: {e}")
            raise

    def _initialize_schema(self):
        """
        Create the schema required for storing metrics if it does not exist.
        """
        try:
            self.logger.info("Initializing database schema...")
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            self.connection.commit()
            self.logger.info("Database schema initialized successfully.")
        except sqlite3.Error as e:
            self.logger.error(f"Schema initialization error: {e}")
            raise

    def save_metrics(self, metrics):
        """
        Insert metrics into the database.

        Args:
            metrics (dict): Mapping of metric names to their respective values.

        Example:
            metrics = {"accuracy": 0.95, "loss": 0.05}
        """
        try:
            self.logger.info("Saving metrics...")
            for metric_name, metric_value in metrics.items():
                self.cursor.execute('''
                    INSERT INTO metrics (metric_name, metric_value)
                    VALUES (?, ?);
                ''', (metric_name, metric_value))
            self.connection.commit()
            self.logger.info("Metrics saved successfully.")
        except sqlite3.Error as e:
            self.logger.error(f"Error saving metrics: {e}")
            raise

    def fetch_all_metrics(self):
        """
        Retrieve all rows from the metrics table.

        Returns:
            List[tuple]: A list of tuples containing all stored metrics.
        """
        try:
            self.logger.info("Fetching all metrics...")
            self.cursor.execute("SELECT * FROM metrics;")
            results = self.cursor.fetchall()
            self.logger.info(f"Fetched {len(results)} records from metrics table.")
            return results
        except sqlite3.Error as e:
            self.logger.error(f"Error fetching metrics: {e}")
            raise

    @contextmanager
    def execute_query(self, query, params=None):
        """
        Execute a custom SQL query using a context manager.

        Args:
            query (str): The SQL query.
            params (Tuple, optional): Query parameters for parameterized queries.

        Yields:
            sqlite3.Cursor: The database cursor to fetch results.

        Example:
            with db.execute_query("SELECT * FROM metrics WHERE id = ?", (1,)) as cursor:
                results = cursor.fetchall()
        """
        try:
            self.logger.info(f"Executing query: {query}")
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            yield self.cursor
            self.connection.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Error executing query: {e}")
            raise

    def close(self):
        """
        Close the database connection.
        """
        try:
            if self.connection:
                self.connection.close()
                self.logger.info("Closed the database connection successfully.")
        except sqlite3.Error as e:
            self.logger.error(f"Error closing connection: {e}")
            raise


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)

    # Path to the database
    db_path = "example_metrics.db"

    # Initialize database manager
    db_manager = DatabaseManagerSQL(db_path)

    try:
        # Save sample metrics
        metrics = {
            "accuracy": 0.96,
            "loss": 0.04,
            "precision": 0.92
        }
        db_manager.save_metrics(metrics)

        # Fetch and display all stored metrics
        all_metrics = db_manager.fetch_all_metrics()
        print("Metrics in database:")
        for row in all_metrics:
            print(row)

        # Custom query example
        with db_manager.execute_query("SELECT * FROM metrics WHERE metric_name = ?", ("accuracy",)) as cursor:
            accuracy_metrics = cursor.fetchall()
            print("\nMetrics with name 'accuracy':")
            for metric in accuracy_metrics:
                print(metric)
    finally:
        # Ensure proper resource cleanup
        db_manager.close()
