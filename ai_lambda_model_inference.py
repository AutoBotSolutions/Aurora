"""
AI Lambda Model Inference
=========================

This script enables serverless execution of machine learning model inference using
AWS Lambda. It supports fetching serialized models from S3, processing input payloads,
and returning predictions in real-time.

License: MIT
Author: G.O.D Framework Team
"""

import boto3
import json
import pickle
import logging
import numpy as np
from botocore.exceptions import BotoCoreError, ClientError

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Global S3 client (Reuse for Lambda runtime performance optimization)
s3_client = boto3.client('s3')


def load_model(bucket_name: str, model_key: str):
    """
    Loads a serialized model from an S3 bucket using the given bucket name and key.
    This function fetches the object from the specified S3 bucket and key, then deserializes
    the model using pickle. It logs the progress and raises appropriate runtime errors if any
    issues occur during the process.

    :param bucket_name: The name of the S3 bucket containing the model.
    :param model_key: The key of the object within the S3 bucket where the model is stored.
    :return: The deserialized model loaded from the S3 bucket.
    :rtype: Any
    :raises RuntimeError: If there is an error fetching the model from S3 or deserializing it.
    """
    try:
        logger.info(f"Fetching model from S3 bucket: {bucket_name}, Key: {model_key}")
        response = s3_client.get_object(Bucket=bucket_name, Key=model_key)
        model = pickle.loads(response['Body'].read())
        logger.info("Model loaded successfully.")
        return model
    except (BotoCoreError, ClientError) as e:
        logger.error(f"Failed to fetch model from S3: {e}")
        raise RuntimeError("Error loading model from S3.") from e
    except pickle.UnpicklingError as e:
        logger.error(f"Error deserializing model: {e}")
        raise RuntimeError("Error unpickling model file.") from e


def parse_input(event_body: str):
    """
    Parses the input JSON string into a NumPy array of features. The function expects a
    JSON string containing a `features` key, which associates with an iterable of numerical
    values. The input is reshaped into a single-row, multi-column format suitable for
    further processing. It logs both successful parsing and any errors encountered.

    :param event_body: JSON-encoded string with input data containing a 'features' key
        associated with an iterable of numerical values.
    :type event_body: str
    :return: A NumPy array containing the parsed features reshaped to a 2D array
        with one row.
    :rtype: numpy.ndarray
    :raises ValueError: If the JSON string is not decodable, the `features` key is
        missing, or the value under `features` is not valid.
    """
    try:
        data = json.loads(event_body)
        features = np.array(data['features']).reshape(1, -1)
        logger.info(f"Input features successfully parsed: {features}")
        return features
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        logger.error(f"Failed to parse input: {e}")
        raise ValueError("Invalid input format. Ensure the 'features' key is present.") from e


def lambda_handler(event, context):
    """
    Invokes a Lambda function to handle a request, involving loading a machine
    learning model from an S3 bucket, processing input data, and generating
    predictions.

    This function retrieves a model from a specified S3 bucket, processes the
    input payload passed through the event, and infers predictions by invoking the
    machine learning model. If successful, it returns a response containing the
    predictions. Otherwise, it sends an error response.

    :param event: A dictionary passed to the Lambda function that includes the
        input payload. It is expected to contain the `body` key with all required
        input features.
    :type event: dict
    :param context: An AWS Lambda Context runtime object. It provides runtime
        information to the handler function.
    :type context: Any
    :return: A dictionary containing the status code and JSON-serialized body with
        predictions in case of success or an error message in case of failure.
    :rtype: dict
    """
    # Configuration - Define the S3 bucket and model key
    bucket_name = "my-ml-models"  # Replace with your S3 bucket name
    model_key = "models/iris_model.pkl"  # Replace with the path to your model in S3

    try:
        # Load the model
        model = load_model(bucket_name=bucket_name, model_key=model_key)

        # Parse input data
        input_features = parse_input(event['body'])

        # Perform inference
        predictions = model.predict(input_features)
        logger.info(f"Generated predictions: {predictions}")

        # Build and return response
        return {
            "statusCode": 200,
            "body": json.dumps({"predictions": predictions.tolist()})
        }

    except Exception as e:
        logger.error(f"Error during inference: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


# ===== Example: Local Testing =====
if __name__ == "__main__":
    # Example payload for local testing
    example_event = {
        "body": json.dumps({
            "features": [5.1, 3.5, 1.4, 0.2]  # Example input
        })
    }
    # Call the Lambda handler for testing
    print(lambda_handler(example_event, None))