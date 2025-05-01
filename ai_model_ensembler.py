"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

import logging
from sklearn.ensemble import VotingClassifier


class ModelEnsembler:
    """
    Manages an ensemble of models for classification using a VotingClassifier.

    This class allows combining several base models into a single ensemble model that
    uses soft voting for prediction. It provides methods to train the ensemble, make
    predictions, and retrieve the constituent models. The primary goal of this class
    is to streamline the process of creating, training, and using an ensemble model.

    :ivar models: List of (name, model) tuples representing the base models.
    :type models: list[tuple[str, object]]

    :ivar ensembler: The VotingClassifier instance that aggregates the base models and
                     performs ensemble predictions.
    :type ensembler: sklearn.ensemble.VotingClassifier
    """

    def __init__(self, models):
        """
        Initializes the ModelEnsembler with a list of models.
        :param models: List of (name, model) tuples.
                       Example: [("logreg", LogisticRegression()), ("tree", DecisionTreeClassifier())]
        """
        if not models or not isinstance(models, list):
            raise ValueError("Models must be provided as a non-empty list of (name, model) tuples.")

        self.models = models
        self.ensembler = VotingClassifier(estimators=self.models, voting="soft")
        logging.info(f"Initialized ensemble with models: {[name for name, _ in self.models]}")

    def train(self, X_train, y_train):
        """
        Trains the ensemble model on the provided training data.
        :param X_train: Training data features.
        :param y_train: Training data labels.
        """
        logging.info("Training ensemble model...")
        try:
            self.ensembler.fit(X_train, y_train)
            logging.info("Ensemble model trained successfully.")
        except Exception as e:
            logging.error(f"Error during ensemble model training: {e}")
            raise RuntimeError(f"Failed to train ensemble model: {str(e)}")

    def predict(self, X_test):
        """
        Makes predictions using the trained ensemble model.
        :param X_test: Test data features.
        :return: Predicted labels.
        """
        logging.info("Making predictions with the ensemble model...")
        try:
            predictions = self.ensembler.predict(X_test)
            logging.info("Predictions generated successfully.")
            return predictions
        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            raise RuntimeError(f"Failed to make predictions: {str(e)}")

    def get_models(self):
        """
        Returns the list of base models in the ensemble.
        :return: List of (name, model) tuples.
        """
        return self.models


# Example: Usage of the ModelEnsembler
if __name__ == "__main__":
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.datasets import load_iris
    from sklearn.metrics import accuracy_score

    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Load the Iris dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Define base models for ensembling
    logreg = LogisticRegression(max_iter=500, random_state=42)
    tree = DecisionTreeClassifier(max_depth=3, random_state=42)

    models = [("logistic_regression", logreg), ("decision_tree", tree)]

    # Initialize the ensemble
    ensembler = ModelEnsembler(models=models)

    # Train the ensemble
    ensembler.train(X_train, y_train)

    # Make predictions
    predictions = ensembler.predict(X_test)

    # Evaluate the accuracy of the ensemble
    accuracy = accuracy_score(y_test, predictions)
    print(f"Ensemble Model Accuracy: {accuracy:.2f}")

    # Log the included models
    logging.info(f"Models in the ensemble: {ensembler.get_models()}")
