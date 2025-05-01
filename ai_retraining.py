"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""


"""
ai_retraining.py

This module facilitates the retraining of machine learning models within the G.O.D Framework. 
It automates and manages the process of loading updated training data, retraining models, and deploying 
updated versions into production. The script is designed to handle data drift, performance degradation, 
and continuously evolving data streams.

Author: G.O.D Framework Team (Open Source Contributors)
License: MIT License
Version: 1.0.0
"""

import logging
from ai_training_model import ModelTrainer
from ai_training_data import TrainingDataManager
from ai_deployment import ModelDeployment


class ModelRetrainer:
    """
    Provides functionality to retrain and deploy machine learning models.

    The purpose of this class is to facilitate the retraining of models using new or updated
    training data. Models are trained based on the provided configuration and are deployed
    to a specified path upon successful retraining.

    It is a utility class that ensures seamless integration of updated training data into
    existing machine learning workflows. The functionality encompasses loading training data,
    separating features and labels, training the model as per given configurations, and finally
    deploying the retrained model.

    This class should be used in scenarios where updated data is available for improving
    or extending a model's performance, ensuring that the deployment process is streamlined.
    """

    @staticmethod
    def retrain_model(training_data_path: str, config: dict, deployment_path: str):
        """
        Retrains the machine learning model using updated or extended data.

        Args:
            training_data_path (str): Path to the updated training dataset.
            config (dict): Configuration dictionary containing model parameters.
            deployment_path (str): Path to save the updated model.

        Returns:
            object: The retrained model if successful; otherwise, returns None.
        """
        logging.info("Starting model retraining process.")
        try:
            # Load updated training data
            training_manager = TrainingDataManager()
            training_data = training_manager.load_training_data(training_data_path)

            # Separate features (X) and labels (y) from the data
            X = [item["features"] for item in training_data]
            y = [item["label"] for item in training_data]

            # Initialize and train the model using the configuration
            trainer = ModelTrainer(config["model"])
            retrained_model = trainer.train(X, y)

            # Deploy the retrained model to the specified path
            ModelDeployment.deploy_model(retrained_model, deployment_path)
            logging.info("Model successfully retrained and deployed.")

            return retrained_model

        except Exception as error:
            logging.error(f"Retraining failed: {error}")
            return None


# Example Usage
if __name__ == "__main__":
    # Basic logging configuration
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Paths for training data and model deployment
    training_data_path = "data/updated_training_data.csv"
    deployment_path = "models/retrained_model.pkl"

    # Configuration for the model
    config = {
        "model": {
            "type": "RandomForest",
            "parameters": {
                "n_estimators": 100,
                "max_depth": 10
            }
        }
    }

    # Perform retraining
    retrained_model = ModelRetrainer.retrain_model(training_data_path, config, deployment_path)

    if retrained_model:
        logging.info("Model retraining completed successfully.")
    else:
        logging.error("Model retraining process failed.")
