"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

import logging
from flask import Flask, request, jsonify
import joblib
import os
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class ModelDeployment:
    """
    Handles the deployment and utilization of machine learning models.

    This class provides functionality to load a trained machine learning
    model, deploy it to a specified environment, and make predictions using
    the deployed model. Configuration settings are passed during initialization.
    The configuration must include paths and deployment details required
    for seamless operation.

    :ivar config: Configuration settings for the deployment. It must include:
                  - deployment_url: The URL for the deployment environment.
                  - model_path: The file path for the trained model.
    :type config: dict
    :ivar model: The loaded machine learning model. It will be `None` if the
                 model is not loaded or loading failed.
    :type model: Optional[object]
    """

    def __init__(self, config):
        """
        Initialize the deployment with specific configurations.

        :param config: Dictionary containing deployment configurations:
                       - deployment_url (required)
                       - model_path (required)
        """
        self.config = config
        self.model = None

    def load_model(self):
        """
        Load the trained model from the configured path.
        """
        logging.info("Loading the model...")
        try:
            model_path = self.config.get("model_path")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")

            self.model = joblib.load(model_path)
            logging.info(f"Model loaded successfully from {model_path}.")
        except Exception as e:
            logging.error(f"Error while loading the model: {e}")
            self.model = None

    def deploy(self):
        """
        Deploy the model to the specified environment.

        - Logs deployment details.
        - Ensures the model is loaded before deployment.
        """
        if not self.model:
            logging.error("Deployment failed: Model is not loaded.")
            return False

        logging.info(f"Deploying model to {self.config['deployment_url']}...")
        try:
            # Placeholder logic for deployment
            success = True  # Mock deployment success
            if success:
                logging.info("Model deployed successfully.")
                return True
            else:
                raise RuntimeError("Deployment failed due to an unknown reason.")
        except Exception as e:
            logging.error(f"Deployment error: {e}")
            return False

    def predict(self, input_data):
        """
        Make predictions with the loaded model.

        :param input_data: List of inputs for prediction.
        :return: List of predictions or an error message.
        """
        if not self.model:
            logging.error("Prediction failed: Model is not loaded.")
            return {"error": "Model is not loaded."}

        try:
            predictions = self.model.predict(input_data)
            logging.info("Prediction successful.")
            return {"predictions": predictions.tolist()}
        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            return {"error": str(e)}


# Flask API for Deployment
app = Flask(__name__)
deployment_config_path = "deployment_config.json"


def load_deployment_config():
    """
    Loads the deployment configuration from a specified file path in JSON format.

    This function attempts to read and load the deployment configuration file,
    which should be present at the `deployment_config_path` defined in the code
    context. If the file is successfully read and the JSON is parsed correctly,
    the configuration dictionary is returned. Otherwise, an error is logged, and
    the function returns `None`.

    :raises Exception: May occur if the file cannot be opened, read, or the
        contents are not properly formatted as JSON.

    :return: A dictionary containing the deployment configuration if successfully
        loaded, or `None` if an error occurred.
    :rtype: dict or None
    """
    try:
        with open(deployment_config_path, "r") as config_file:
            config = json.load(config_file)
            logging.info(f"Deployment configuration loaded from {deployment_config_path}.")
            return config
    except Exception as e:
        logging.error(f"Failed to load deployment configuration: {e}")
        return None


# Load the deployment configuration and initialize the ModelDeployment instance
deployment_config = load_deployment_config()
if deployment_config:
    model_deployment = ModelDeployment(deployment_config)
    model_deployment.load_model()
else:
    logging.error("Deployment configuration is missing. Exiting.")
    model_deployment = None


@app.route("/predict", methods=["POST"])
def predict():
    """
    Handles prediction requests sent as a POST request to the configured endpoint. The function
    extracts input data from the request, passes it to the predictive model, and returns the
    predicted results in JSON format. If the deployment system is not initialized or if errors
    occur during processing, the function responds with an appropriate error message and HTTP
    status code.

    :raises KeyError: If the requested data does not contain the required input field.
    :raises Exception: For any other unexpected errors during processing.
    :raises ValueError: If the user-provided input data is not correctly formatted.

    :return: JSON response containing the prediction results or an error message with an
        HTTP status code.
    """
    if not model_deployment:
        return jsonify({"error": "Deployment system not initialized."}), 500

    try:
        request_data = request.get_json()
        input_data = request_data.get("input", [])
        if not input_data:
            return jsonify({"error": "Input data is missing."}), 400

        result = model_deployment.predict(input_data)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error in prediction request: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/status", methods=["GET"])
def status():
    """
    Handles the status check endpoint for the application. This endpoint provides
    information about the health status of the model deployment. If the model is
    not loaded or failed to deploy, it returns a status indicating an error along
    with a corresponding message. If the deployment is healthy, it indicates so
    through the response.

    :return: A JSON response with the status of the model deployment. If the
        deployment is healthy, it returns {"status": "ok", "message": "Deployment
        is healthy."} with a 200 HTTP status code.
        If the deployment failed (e.g., model not loaded or failed deployment),
        it returns {"status": "error", "message": "Model is not loaded or
        deployment failed."} with a 500 HTTP status code.
    :rtype: flask.Response
    """
    if not model_deployment or not model_deployment.model:
        return jsonify({"status": "error", "message": "Model is not loaded or deployment failed."}), 500

    return jsonify({"status": "ok", "message": "Deployment is healthy."})


if __name__ == "__main__":
    app_port = deployment_config.get("port", 5000) if deployment_config else 5000
    app.run(host="0.0.0.0", port=app_port)
