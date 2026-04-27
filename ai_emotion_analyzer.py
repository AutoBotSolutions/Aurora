"""
AI Emotion Analyzer Module
==========================

The AI Emotion Analyzer is designed to detect and classify emotional tones in textual inputs. Using transformer-based models 
from Hugging Face, this module provides sentiment labels (e.g., POSITIVE, NEGATIVE, NEUTRAL) along with confidence scores. 
It is suitable for chatbots, user feedback analysis, and emotionally-aware AI systems.

---

Author: G.O.D Team
License: MIT
"""

from transformers import pipeline


class EmotionAnalyzer:
    """
    Provides functionality to analyze emotional tone in text using a pre-trained sentiment analysis model.

    The EmotionAnalyzer class leverages Hugging Face's 'transformers' library to detect sentiment in textual
    input. It uses a specified model to identify the emotional label (e.g., positive, negative) along with
    the associated confidence score.

    :ivar analyzer: The Hugging Face pipeline object initialized for sentiment analysis.
    :type analyzer: transformers.pipelines.Pipeline
    """

    def __init__(self, model="distilbert-base-uncased-finetuned-sst-2-english"):
        """
        Initializes the EmotionAnalyzer with a pre-trained sentiment analysis model.
        
        :param model: The Hugging Face pre-trained model to use for sentiment analysis. Defaults to SST-2 fine-tuned DistilBERT.
        """
        self.analyzer = pipeline("sentiment-analysis", model=model)

    def detect_emotion(self, text):
        """
        Analyzes the emotional tone in a given text and returns the sentiment label and score.
        
        :param text: The input text to analyze (string).
        :return: Tuple containing the detected emotion label (str) and confidence score (float).
        """
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string.")

        try:
            result = self.analyzer(text)
            return result[0]['label'], result[0]['score']
        except Exception as e:
            raise RuntimeError(f"Error during emotion detection: {e}")


if __name__ == "__main__":
    # Example Usage
    print("===== AI Emotion Analyzer =====")

    # Initialize the EmotionAnalyzer
    emotion_analyzer = EmotionAnalyzer()

    # Example text for emotion detection
    messages = [
        "I'm having such a hard day, nothing is working!",
        "This is the best day of my life! I feel amazing.",
        "I'm feeling neutral about the outcome.",
        "Thank you so much for everything you've done!"
    ]

    # Analyze each message
    for message in messages:
        try:
            emotion, confidence = emotion_analyzer.detect_emotion(message)
            print(f"Message: \"{message}\"")
            print(f" -> Emotion Detected: {emotion} with confidence {confidence:.4f}\n")
        except Exception as e:
            print(f"Error analyzing message: \"{message}\". Details: {e}")