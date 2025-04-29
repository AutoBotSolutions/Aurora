import boto3
import json
import pickle
import logging
import numpy as np
from pymongo import MongoClient

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# MongoDB Storage Handler class
class MongoDBStorage:
    """
    Handles interaction with a MongoDB database.

    This class provides methods to save and retrieve data from a MongoDB database.
    It manages the database connection and simplifies data manipulation processes
    for various operations.

    :ivar client: MongoClient instance for connecting to the MongoDB server.
    :type client: pymongo.MongoClient
    :ivar db: Reference to a specific MongoDB database.
    :type db: pymongo.database.Database
    """

    def __init__(self, db_url, db_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]

    def save_data(self, collection, data):
        """
        Save data to a MongoDB collection.
        :param collection: MongoDB collection name
        :param data: Data to store
        """
        logging.info(f"Saving data to collection '{collection}'...")
        self.db[collection].insert_one(data)
        logging.info("Data saved successfully.")

    def retrieve_data(self, collection, query):
        """
        Retrieve data from a MongoDB collection.
        :param collection: MongoDB collection name
        :param query: MongoDB query
        :return: Retrieved data
        """
        logging.info(f"Retrieving data from collection '{collection}'...")
        result = self.db[collection].find_one(query)
        logging.info("Data retrieved successfully.")
        return result


# AWS S3 model loader
def load_model_from_s3(bucket_name, model_key):
    """
    Loads a serialized machine learning model from an S3 bucket.

    This function connects to an Amazon S3 bucket, retrieves a serialized model
    from the given `bucket_name` and `model_key`, and deserializes it for use.

    :param bucket_name: The name of the S3 bucket that contains the serialized model.
    :type bucket_name: str
    :param model_key: The object key for the serialized model file in the S3 bucket.
    :type model_key: str
    :return: The deserialized machine learning model loaded from the specified S3 bucket.
    :rtype: Any
    :raises Exception: If there is an error during the download process or
        model deserialization.
    """
    s3 = boto3.client('s3')
    try:
        logger.info(f"Downloading model from S3 bucket: {bucket_name}, Key: {model_key}")
        response = s3.get_object(Bucket=bucket_name, Key=model_key)
        model = pickle.loads(response['Body'].read())
        logger.info("Model loaded successfully.")
        return model
    except Exception as e:
        logger.error(f"Error loading model from S3: {str(e)}")
        raise e


# AWS Lambda Handler
def lambda_handler(event, context):
    """
    Handles an AWS Lambda event to perform inference using a machine learning
    model stored in an S3 bucket. The event should include the S3 bucket name,
    the key to the model file, and the input data for which predictions are
    to be made. The function processes the input, retrieves the model, and
    makes predictions, returning the result or error response.

    :param event: Dictionary containing the input payload. It is expected to
        include the following keys:
        - bucket: str - The name of the S3 bucket containing the model.
        - model_key: str - The key of the model file in the S3 bucket.
        - data: str - A JSON-formatted string containing the features for
          prediction.
    :param context: AWS Lambda context object providing metadata about the
        invocation, function configuration, and execution environment.
    :return: Dictionary containing the HTTP status code and response body:
        - If successful, a 200 status code and predictions in a JSON format.
        - If validation fails or an error occurs, a 400 or 500 status code
          with an appropriate error message.
    """
    try:
        # Extract input parameters from the event
        bucket_name = event.get('bucket', '').strip()
        model_key = event.get('model_key', '').strip()
        input_data = event.get('data', '')

        if not bucket_name or not model_key or not input_data:
            raise ValueError("Missing required parameters: 'bucket', 'model_key', or 'data'.")

        # Load the model from S3
        model = load_model_from_s3(bucket_name, model_key)

        # Parse input data and prepare for inference
        input_data = json.loads(input_data)
        features = np.array(list(input_data.values())).reshape(1, -1)  # Assuming data is a dictionary
        logger.info(f"Input features for prediction: {features}")

        # Perform prediction
        predictions = model.predict(features)
        logger.info(f"Prediction successful: {predictions}")

        # Prepare successful response
        response = {
            "statusCode": 200,
            "body": json.dumps({"predictions": predictions.tolist()})
        }

    except ValueError as ve:
        logger.error(f"ValueError: {str(ve)}")
        response = {
            "statusCode": 400,
            "body": json.dumps({"error": str(ve)})
        }
    except Exception as e:
        logger.error(f"Error during inference: {str(e)}")
        response = {
            "statusCode": 500,
            "body": json.dumps({"error": "Inference failed. Check logs for details."})
        }

    return response


# Optional: Local testing
if __name__ == "__main__":
    # Example MongoDB usage (replace with actual connection details)
    mongo_handler = MongoDBStorage(db_url="mongodb://localhost:27017", db_name="ml_inference_db")

    # Example data to save in MongoDB
    test_data = {"id": 1, "name": "Sample Data", "prediction": [0.8, 0.2]}
    mongo_handler.save_data(collection="predictions", data=test_data)
    query_result = mongo_handler.retrieve_data(collection="predictions", query={"id": 1})
    print(f"Retrieved from MongoDB: {query_result}")

    # Example Lambda invocation for local testing
    event = {
        "bucket": "my-ml-models",
        "model_key": "iris_model.pkl",
        "data": json.dumps({"feature1": 5.1, "feature2": 3.5, "feature3": 1.4, "feature4": 0.2})
    }
    print(lambda_handler(event, None))