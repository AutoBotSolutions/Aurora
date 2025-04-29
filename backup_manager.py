"""
===============================================================================
Backup Manager for G.O.D Framework
===============================================================================
A Python-based backup management system designed to automate backup creation,
data integrity validation, and restoration. Provides seamless integration with
AI workflows and disaster recovery systems.

GitHub Repository: <Insert Repository URL here>
License: MIT License
Maintainer: G.O.D Framework Team
===============================================================================
"""

import logging
import os
import shutil
from datetime import datetime


class BackupManager:
    """
    Manages backup creation, restoration, and listing of backups.

    This class provides functionality to create compressed backups of
    directories, restore them to a specified location, and list all
    available backups within the designated backup directory.

    :ivar backup_dir: Root directory for storing backup files.
    :type backup_dir: str
    """

    def __init__(self, backup_dir="backups/"):
        """
        Initializes the BackupManager with a designated directory for backups.

        Args:
            backup_dir (str): Root directory for storing backup files.
        """
        self.backup_dir = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)
        logging.info(f"BackupManager initialized with backup directory: {self.backup_dir}")

    def create_backup(self, source_dir):
        """
        Creates a compressed backup of the source directory.

        Args:
            source_dir (str): Directory to back up.

        Returns:
            str: The absolute path to the created backup file.

        Raises:
            FileNotFoundError: If the source directory does not exist.
            Exception: For other unexpected errors.
        """
        if not os.path.exists(source_dir):
            logging.error(f"Source directory '{source_dir}' does not exist.")
            raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")

        try:
            # Generate unique backup file name with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{os.path.basename(source_dir)}_backup_{timestamp}.zip"
            backup_path = os.path.join(self.backup_dir, backup_name)

            # Create compressed archive of the source directory
            shutil.make_archive(backup_path.replace(".zip", ""), 'zip', source_dir)
            logging.info(f"Backup created successfully: {backup_path}")
            return backup_path
        except Exception as e:
            logging.error(f"Failed to create backup for '{source_dir}': {e}")
            raise

    def restore_backup(self, backup_file, restore_dir):
        """
        Restores a backup file to a specified directory.

        Args:
            backup_file (str): The name of the backup file to restore.
            restore_dir (str): The destination directory where the backup will be restored.

        Returns:
            bool: True if the restoration is successful.

        Raises:
            FileNotFoundError: If the backup file does not exist.
            Exception: For other unexpected errors.
        """
        backup_path = os.path.join(self.backup_dir, backup_file)

        if not os.path.exists(backup_path):
            logging.error(f"Backup file '{backup_file}' does not exist in '{self.backup_dir}'.")
            raise FileNotFoundError(f"Backup file '{backup_file}' does not exist in '{self.backup_dir}'.")

        try:
            os.makedirs(restore_dir, exist_ok=True)
            shutil.unpack_archive(backup_path, restore_dir)
            logging.info(f"Backup '{backup_file}' restored successfully to '{restore_dir}'.")
            return True
        except Exception as e:
            logging.error(f"Failed to restore backup '{backup_file}': {e}")
            raise

    def list_backups(self):
        """
        Lists all available backup files in the backup directory.

        Returns:
            list: A list of backup file names.
        """
        try:
            backups = [f for f in os.listdir(self.backup_dir) if f.endswith('.zip')]
            logging.info(f"List of backups retrieved: {backups}")
            return backups
        except Exception as e:
            logging.error(f"Failed to list backups: {e}")
            return []


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

# Example usage
if __name__ == "__main__":
    # Initialize the BackupManager
    manager = BackupManager()

    # Define sample source directory, backup directory, and restore directory
    source_directory = "data_to_backup"
    restore_directory = "restored_data"

    try:
        # Create a backup
        logging.info("Starting backup creation...")
        backup_file = manager.create_backup(source_directory)

        # List all backups
        logging.info("Listing all backups...")
        available_backups = manager.list_backups()
        logging.info(f"Available backups: {available_backups}")

        # Restore the created backup
        logging.info("Restoring the backup...")
        if backup_file:
            backup_name = os.path.basename(backup_file)
            manager.restore_backup(backup_name, restore_directory)

    except Exception as e:
        logging.error(f"An error occurred: {e}")