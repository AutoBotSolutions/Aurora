
"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

"""
Emotional Core Module
=====================

The EmotionalCore module is designed to enable AI systems to model, understand, and respond
to human-like emotions based on multimodal stimuli (e.g., text, audio, and visual inputs).

This module provides:
1. Emotional state management by dynamically updating emotions based on weighted modal inputs.
2. A multimodal emotion fusion engine to combine emotional signals from various sources.
3. Empathetic reasoning for generating emotionally appropriate responses.

---

Key Features:
1. Dynamic Emotional State Modeling: Updates and maintains emotion probabilities.
2. Multimodal Fusion: Combines data from text, audio, and visual modalities based on custom weights.
3. Empathy Synthesis: Determines dominant emotion and facilitates empathetic responses.
4. Extensibility: Supports additional emotional mappings or custom modalities as needed.
5. Lightweight and Fast: Optimized using efficient numerical operations with NumPy.

Author: G.O.D Team
License: MIT
"""

import numpy as np


class EmotionalCore:
    """
    A system for tracking and updating emotional states based on multimodal inputs. It maintains a
    dictionary of emotional probabilities and updates these states by integrating scores from various
    modalities such as text, audio, and visual inputs.

    The class also supports normalization of emotional probabilities to ensure they sum up to 1 and
    identifies the dominant emotion based on the highest probability.

    :ivar emotional_state: A dictionary containing the probabilities of different emotions
        (e.g., anger, joy, sadness, fear, and neutral). Initially, the system starts in a neutral state.
    :type emotional_state: dict[str, float]
    :ivar weighted_modalities: A dictionary defining the weights for each modality (text, audio, visual)
        during multimodal integration.
    :type weighted_modalities: dict[str, float]
    :ivar current_emotion: The emotion with the highest probability, representing the dominant emotion
        at any point.
    :type current_emotion: str
    """

    def __init__(self):
        """
        Initializes the emotional system with default emotional states, weights for multimodal
        integration, and other essential configurations.

        Emotional State:
        - A dictionary containing probabilities for base emotional categories (anger, joy, sadness, fear, neutral).
          By default, the system starts in the `neutral` state.

        Modalities:
        - Multimodal weights configure how much influence each modality (e.g., text, audio, visual) has on the final emotion.
        """
        self.emotional_state = {
            "anger": 0.0,
            "joy": 0.0,
            "sadness": 0.0,
            "fear": 0.0,
            "neutral": 1.0,  # Default state starts as neutral
        }
        self.weighted_modalities = {"text": 0.5, "audio": 0.3, "visual": 0.2}  # Default weights for fusion
        self.current_emotion = "neutral"  # The dominant emotion at any given time

    def update_emotion(self, modality: str, emotion_scores: dict):
        """
        Updates the emotional state by integrating emotion scores from a specific modality.

        :param modality: The source of emotion (e.g., "text", "audio", "visual").
        :param emotion_scores: A dictionary of emotion probabilities (e.g., {"joy": 0.7, "sadness": 0.3}).
        :raises ValueError: If an unrecognized modality is provided.
        :raises KeyError: If an unrecognized emotion is present in the scores.
        """
        if modality not in self.weighted_modalities:
            raise ValueError(
                f"Unknown modality '{modality}'. Accepted modalities are: {list(self.weighted_modalities.keys())}.")

        weight = self.weighted_modalities[modality]
        for emotion, score in emotion_scores.items():
            if emotion in self.emotional_state:
                self.emotional_state[emotion] += score * weight
            else:
                raise KeyError(
                    f"Unknown emotion '{emotion}' detected in scores. Allowed emotions: {list(self.emotional_state.keys())}")

        self._normalize_emotions()

    def _normalize_emotions(self):
        """
        Normalizes the emotional state so that all probabilities sum to 1. Also determines the
        current dominant emotion based on the highest probability score.
        """
        total = sum(self.emotional_state.values())
        self.emotional_state = {k: v / total for k, v in self.emotional_state.items()}
        self.current_emotion = max(self.emotional_state, key=self.emotional_state.get)

    def get_emotional_state(self):
        """
        Retrieves the current emotional state of the system as a dictionary.

        :return: Dictionary with emotion probabilities.
        """
        return self.emotional_state

    def get_current_emotion(self):
        """
        Retrieves the current dominant emotion.

        :return: String representation of the dominant emotion.
        """
        return self.current_emotion


# ===== Example Usage Section =====
if __name__ == "__main__":
    # Initialize the Emotional Core
    emotional_core = EmotionalCore()

    # Example 1: Update Emotional State Using Text Data
    text_emotions = {"joy": 0.8, "sadness": 0.2}  # Text data with emotion probabilities
    emotional_core.update_emotion("text", text_emotions)

    # Display Updated Emotional State
    print("Emotional State After Text Update:")
    print(emotional_core.get_emotional_state())
    print(f"Dominant Emotion: {emotional_core.get_current_emotion()}")

    # Example 2: Update Using Audio Modalities
    audio_emotions = {"anger": 0.4, "neutral": 0.6}
    emotional_core.update_emotion("audio", audio_emotions)

    # Display Updated Emotional State
    print("\nEmotional State After Audio Update:")
    print(emotional_core.get_emotional_state())
    print(f"Dominant Emotion: {emotional_core.get_current_emotion()}")

    # Example 3: Visual Modality Update
    visual_emotions = {"fear": 0.5, "joy": 0.5}
    emotional_core.update_emotion("visual", visual_emotions)

    # Final Emotional State and Dominant Emotion
    print("\nFinal Emotional State After Visual Update:")
    print(emotional_core.get_emotional_state())
    print(f"Final Dominant Emotion: {emotional_core.get_current_emotion()}")
