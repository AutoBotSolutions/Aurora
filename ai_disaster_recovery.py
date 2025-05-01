"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

import os
import shutil
import logging
from datetime import datetime


class DisasterRecovery:
    """
    Handles disaster recovery operations, including saving, restoring, and managing
    checkpoints and backups to protect data during pipeline execution or other tasks.

    The DisasterRecovery class provides utilities for saving and retrieving
    checkpoints, creating and restoring backups for data, and enforcing retention
    policies to manage storage usage effectively.

    :ivar backup_dir: Directory where all backups and checkpoints are stored.
    :type backup_dir: str
    :ivar retention_policy: Maximum number of backups to retain. Oldest backups
        exceeding this count are deleted automatically.
    :type retention_policy: int
    :ivar checkpoints: A dictionary storing in-memory checkpoints for different
        pipeline steps, allowing for quick rollback without accessing disk.
    :type checkpoints: dict
    """

    def __init__(self, backup_dir="./backups", retention_policy=5):
        """
        Initializes the disaster recovery manager with default or user-defined settings.

        :param backup_dir: Directory to store backups.
        :param retention_policy: Maximum number of backups to retain.
        """
        self.backup_dir = backup_dir
        self.retention_policy = retention_policy
        self.checkpoints = {}

        # Ensure backup directory exists
        os.makedirs(self.backup_dir, exist_ok=True)

        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        logging.info(
            f"Initialized DisasterRecovery with backup_dir='{self.backup_dir}' and retention_policy={self.retention_policy}.")

    def save_checkpoint(self, step_name: str, data: dict):
        """
        Saves a checkpoint for the given step in memory and optionally to disk.

        :param step_name: Unique name of the pipeline step.
        :param data: Data/state to save in the checkpoint.
        """
        # Save in memory
        self.checkpoints[step_name] = data
        logging.info(f"Checkpoint for step '{step_name}' saved in memory.")

        # Save to disk
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_dir, f"{step_name}_checkpoint_{timestamp}.json")
        try:
            # Write checkpoint to file (JSON serialization for simplicity)
            with open(backup_path, "w") as checkpoint_file:
                checkpoint_file.write(str(data))  # Transform data into a string (can include custom serialization)
            logging.info(f"Checkpoint for step '{step_name}' successfully saved to disk at '{backup_path}'.")
        except Exception as e:
            logging.error(f"Failed to save checkpoint for step '{step_name}' to disk: {e}")

        self._enforce_retention_policy()

    def rollback_to_checkpoint(self, step_name: str):
        """
        Retrieves a checkpoint by step name from memory.

        :param step_name: Name of the pipeline step to roll back to.
        :return: Data saved for the step, or None if not found.
        """
        checkpoint_data = self.checkpoints.get(step_name, None)
        if checkpoint_data:
            logging.info(f"Rolled back to checkpoint '{step_name}' from memory.")
            return checkpoint_data

        # Optionally, implement logic to search for backups from disk if needed.

        logging.warning(f"Checkpoint '{step_name}' not found in memory.")
        return None

    def create_backup(self, source_dir: str):
        """
        Creates a snapshot (backup) of the specified source directory.

        :param source_dir: Directory to snapshot.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}")
        try:
            shutil.copytree(source_dir, backup_path)
            logging.info(f"Backup of directory '{source_dir}' created at '{backup_path}'.")
            self._enforce_retention_policy()
        except Exception as e:
            logging.error(f"Failed to create backup from directory '{source_dir}': {e}")

    def restore_backup(self, backup_name: str, target_dir: str):
        """
        Restores a specific backup to the target directory.

        :param backup_name: Name of the backup to restore.
        :param target_dir: Target directory to restore the backup into.
        """
        backup_path = os.path.join(self.backup_dir, backup_name)
        if not os.path.exists(backup_path):
            logging.error(f"Backup '{backup_name}' does not exist.")
            return False

        try:
            shutil.copytree(backup_path, target_dir, dirs_exist_ok=True)
            logging.info(f"Backup '{backup_name}' successfully restored to '{target_dir}'.")
            return True
        except Exception as e:
            logging.error(f"Failed to restore backup '{backup_name}' to '{target_dir}': {e}")
            return False

    def _enforce_retention_policy(self):
        """
        Ensures the backup directory retains only the most recent backups
        according to the retention policy.
        """
        try:
            backups = sorted(
                [b for b in os.listdir(self.backup_dir) if os.path.isdir(os.path.join(self.backup_dir, b))],
                key=lambda x: os.path.getmtime(os.path.join(self.backup_dir, x))
            )
            while len(backups) > self.retention_policy:
                oldest_backup = backups.pop(0)
                shutil.rmtree(os.path.join(self.backup_dir, oldest_backup))
                logging.info(f"Removed old backup: {oldest_backup}")
        except Exception as e:
            logging.error(f"Failed to enforce retention policy: {e}")


# Example usage as a standalone script
if __name__ == "__main__":
    recovery = DisasterRecovery(backup_dir="./backups", retention_policy=3)

    # Save a few checkpoints
    recovery.save_checkpoint("step_1", {"status": "completed", "data": [1, 2, 3]})
    recovery.save_checkpoint("step_2", {"status": "processing", "data": [4, 5, 6]})

    # Roll back to a checkpoint
    restored_data = recovery.rollback_to_checkpoint("step_2")
    print(f"Restored data: {restored_data}")

    # Create and restore backups
    recovery.create_backup(source_dir="./example_data")
    recovery.restore_backup("backup_20231101_120000", target_dir="./restored_example_data")
