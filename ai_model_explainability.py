"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

import logging
import shap
import matplotlib.pyplot as plt


class ModelExplainability:
    """
    Provides tools for generating explainability insights using SHAP for machine learning
    models. It supports both global and local explainability methods to visualize feature
    importance and understand model predictions.

    The class is designed to work with SHAP-compatible models and data. A SHAP explainer
    is initialized upon object creation if valid data is provided. Users can generate
    global explanations to view feature importance across a dataset and local explanations
    to analyze the contributions of individual features for specific instances.

    :ivar model: Trained machine learning model provided during initialization.
    :type model: Any
    :ivar data: Optional dataset used for SHAP explainer initialization or representative
        sample of the training dataset.
    :type data: Any or None
    :ivar explainer: SHAP explainer instance, initialized if data is provided and valid.
    :type explainer: shap.Explainer or None
    """

    def __init__(self, model, data=None):
        """
        Initializes the ModelExplainability class with a trained model and optional dataset.
        :param model: Trained machine learning model (compatible with SHAP Explainer).
        :param data: Dataset used during training or representative sample for explainability (optional).
        """
        self.model = model
        self.data = data
        self.explainer = None

        if data is not None:
            logging.info("Initializing SHAP explainer...")
            try:
                self.explainer = shap.Explainer(self.model, self.data)
                logging.info("SHAP explainer initialized successfully.")
            except Exception as e:
                logging.error(f"Error initializing SHAP explainer: {e}")
                raise ValueError("Failed to initialize SHAP explainer. Ensure the data and model are valid.")

    def global_explain(self):
        """
        Generates a global explanation for the given dataset.
        Creates a SHAP summary plot to rank and visualize feature importance.

        :raises: RuntimeError if no dataset or explainer is provided.
        """
        if self.explainer is None or self.data is None:
            raise RuntimeError("Global explanation requires a SHAP explainer and a dataset.")

        logging.info("Generating global explainability (summary plot)...")
        try:
            shap_values = self.explainer(self.data)
            shap.summary_plot(shap_values, self.data, show=True)
            logging.info("Global explainability generated and displayed successfully.")
        except Exception as e:
            logging.error(f"Error generating global explanation: {e}")
            raise RuntimeError(f"Global explanation failed: {e}")

    def local_explain(self, instance):
        """
        Generates a local explanation for a single data point (instance).
        Creates a SHAP waterfall plot to visualize the impact of each feature.

        :param instance: A single data instance to be explained (array or DataFrame row).
        :raises: RuntimeError if SHAP explainer is not initialized.
        """
        if self.explainer is None:
            raise RuntimeError("Local explanation requires a SHAP explainer. Initialize with a dataset.")

        logging.info("Generating local explainability (waterfall plot)...")
        try:
            shap_values = self.explainer(instance)
            shap.waterfall_plot(shap.Explanation(shap_values[0], feature_names=self.data.columns))
            logging.info("Local explainability plot generated successfully.")
        except Exception as e:
            logging.error(f"Error generating local explanation: {e}")
            raise RuntimeError(f"Local explanation failed: {e}")


# Example: Usage of ModelExplainability class
if __name__ == "__main__":
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split

    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Load the Iris dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    feature_names = iris.feature_names
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train a Random Forest model
    logging.info("Training RandomForestClassifier on Iris dataset...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Initialize ModelExplainability with the model and training data
    explain = ModelExplainability(model=model, data=X_train)

    # Generate a global explanation (SHAP summary plot)
    logging.info("Generating global explanation...")
    explain.global_explain()

    # Pick a single instance from the test set to explain
    instance = X_test[0].reshape(1, -1)  # Reshape for compatibility
    logging.info("Generating local explanation for a specific instance...")
    explain.local_explain(instance)
