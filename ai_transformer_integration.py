"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

"""
==================================================================================
AI Transformer Integration
==================================================================================
The AI Transformer Integration module simplifies the usage of transformer-based
models for natural language processing (NLP) tasks. With support for pre-trained 
models from the Hugging Face library, it provides seamless inference on tasks 
such as text classification, sentiment analysis, and more.

GitHub Repository: <https://github.com/<your-repo-link>> (Replace with your link)
License: MIT (or preferred license)
Maintainer: G.O.D Framework Team
==================================================================================
"""

from transformers import pipeline
import logging


class TransformerIntegration:
    """
    Integration with a transformer model for performing NLP tasks.

    This class provides functionalities to initialize a transformer model pipeline
    and perform text analysis for specified NLP tasks using Hugging Face's
    transformers library.

    :ivar nlp_pipeline: The Hugging Face transformer pipeline for the specified task.
    :type nlp_pipeline: Pipeline
    """

    def __init__(self, model_name="bert-base-uncased", task="text-classification"):
        """
        Initialize a transformer pipeline with the specified model and task.

        Args:
            model_name (str): The name of the transformer model to load from Hugging Face.
            task (str): NLP task for the transformer pipeline (e.g., "text-classification").
        """
        try:
            logging.info(f"Initializing transformer model '{model_name}' for task '{task}'...")
            self.nlp_pipeline = pipeline(task, model=model_name)
            logging.info(f"Model '{model_name}' initialized successfully for task '{task}'.")
        except Exception as e:
            logging.error(f"Failed to initialize model '{model_name}' for task '{task}': {e}")
            raise

    def analyze_text(self, text):
        """
        Perform inference using the transformer for the given text.

        Args:
            text (str or list): The input text or list of texts to analyze.

        Returns:
            list of dict: Results with classifications and probabilities.
        """
        if not text:
            raise ValueError("Input text must not be empty.")
        try:
            logging.info("Performing text analysis...")
            result = self.nlp_pipeline(text)
            logging.info(f"Text analysis results: {result}")
            return result
        except Exception as e:
            logging.error(f"Error during text analysis: {e}")
            raise


if __name__ == "__main__":
    # Enable logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Example usage
    try:
        # Initialize the transformer integration
        transformer = TransformerIntegration(model_name="bert-base-uncased", task="text-classification")

        # Analyze a single piece of text
        text_to_analyze = "Your model does not meet expectations."
        analysis_result = transformer.analyze_text(text_to_analyze)
        print("Analysis Result:", analysis_result)

        # Analyze a batch of texts
        batch_texts = [
            "The product exceeded my expectations!",
            "I am not satisfied with the support provided.",
            "Overall, this is a fantastic experience!"
        ]
        batch_results = transformer.analyze_text(batch_texts)
        print("\nBatch Analysis Results:")
        for idx, result in enumerate(batch_results):
            print(f"Text {idx + 1}: {result}")

    except Exception as ex:
        logging.error(f"An unexpected error occurred: {ex}")
