"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""


"""
AI Feedback Loop Module

This module provides a framework for integrating user feedback into AI models for continuous improvement through active learning. 
It merges feedback into training datasets and supports automated model retraining pipelines to enhance model accuracy, adaptability, 
and reliability in dynamic environments. Designed for scalability, it works with a variety of dataset formats and ML frameworks.
"""

import logging
import numpy as np
from ai_training_data import TrainingDataManager


class FeedbackLoop:
    """
    Manages the collection of user feedback for an AI model, processes feedback, and retrains the
    model when a specified threshold is reached.

    This class serves as an interface between user-provided feedback and the model-improvement
    pipeline. It provides mechanisms to store feedback, validate provided entries, determine
    if retraining is warranted based on a threshold, and merge feedback with existing training data.

    :ivar model: Instance of the AI model to train and retrain dynamically.
    :type model: Any
    :ivar feedback_storage: Storage medium (list or custom storage) for collected feedback entries.
    :type feedback_storage: list or Any
    :ivar retrain_threshold: Minimum number of feedback entries required before model retraining.
    :type retrain_threshold: int
    """

    def __init__(self, model, feedback_storage=None, retrain_threshold=10):
        """
        Initializes the FeedbackLoop instance.

        :param model: Instance of the AI model to retrain (e.g., Scikit-learn, TensorFlow, PyTorch).
        :param feedback_storage: In-memory list or other persistence storage for user feedback.
        :param retrain_threshold: Minimum feedback entries required to trigger retraining.
        """
        self.model = model
        self.feedback_storage = feedback_storage or []
        self.retrain_threshold = retrain_threshold

    def process_feedback(self, feedback_entry):
        """
        Validates and stores a single feedback entry.

        :param feedback_entry: Dictionary containing feedback data.
               Example: {"input": [features], "target": ground_truth}
        """
        logging.info("Processing feedback entry...")
        try:
            if "input" in feedback_entry and "target" in feedback_entry:
                self.feedback_storage.append(feedback_entry)
                logging.info("Feedback stored successfully.")
            else:
                logging.error("Invalid feedback format: Missing 'input' or 'target'.")
                raise ValueError("Invalid feedback format")
        except Exception as e:
            logging.error(f"Failed to process feedback: {e}")
            raise

    def retrain_model(self):
        """
        Retrains the AI model using the accumulated feedback, if the threshold is met.
        """
        if len(self.feedback_storage) >= self.retrain_threshold:
            logging.info(f"Retraining the model with {len(self.feedback_storage)} feedback entries...")
            try:
                inputs = np.array([entry["input"] for entry in self.feedback_storage])
                targets = np.array([entry["target"] for entry in self.feedback_storage])
                self.model.fit(inputs, targets)
                self.feedback_storage.clear()  # Clear feedback after retraining
                logging.info("Model retraining completed successfully.")
            except Exception as e:
                logging.error(f"Failed to retrain the model: {e}")
                raise
        else:
            logging.info(f"Insufficient feedback for retraining. "
                         f"Collected: {len(self.feedback_storage)}/{self.retrain_threshold}.")

    @staticmethod
    def integrate_feedback(feedback_data, training_data_path):
        """
        Merges feedback into the training dataset saved in the given file path.

        :param feedback_data: List of feedback examples in dictionary format.
        :param training_data_path: Path to the training data file.
        :return: Updated training dataset after feedback integration.
        """
        logging.info("Integrating feedback into the training dataset...")
        try:
            training_manager = TrainingDataManager()
            training_data = training_manager.load_training_data(training_data_path)
            updated_training_data = training_data + feedback_data
            training_manager.save_training_data(updated_training_data, training_data_path)
            logging.info("Feedback integration successful.")
            return updated_training_data
        except Exception as e:
            logging.error(f"Feedback integration failed: {e}")
            return None


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Example AI model (Scikit-learn Logistic Regression in this case)
    from sklearn.linear_model import LogisticRegression

    model = LogisticRegression()

    # Example feedback storage
    feedback_storage = []

    # FeedbackLoop instance
    feedback_loop = FeedbackLoop(model=model, feedback_storage=feedback_storage, retrain_threshold=5)

    # Simulated user feedback
    feedback_1 = {"input": [0.5, 0.8, 1.2], "target": 1}
    feedback_2 = {"input": [0.3, 0.4, 0.9], "target": 0}
    feedback_3 = {"input": [0.6, 1.0, 1.5], "target": 1}

    # Process feedback
    feedback_loop.process_feedback(feedback_1)
    feedback_loop.process_feedback(feedback_2)
    feedback_loop.process_feedback(feedback_3)

    # Attempt to retrain model (will not retrain unless 5 feedback entries exist)
    feedback_loop.retrain_model()

    # Integrating feedback into a persisted training dataset
    training_data_path = "training_data.json"
    integrated_data = feedback_loop.integrate_feedback(
        feedback_data=feedback_storage, training_data_path=training_data_path
    )

    if integrated_data:
        logging.info(f"Integrated dataset size: {len(integrated_data)} entries.")
    else:
        logging.error("Failed to integrate feedback into the training dataset.")
