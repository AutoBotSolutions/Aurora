"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

"""
AI Love Essence Module
=======================

The ai_love_essence module revolves around enabling AI to perceive and articulate the concept of love.

This module serves as both a symbolic and practical framework for emotional AI interactions. It can be used in applications
ranging from conversational AI to philosophical simulations, storytelling, and emotional support systems.

License: MIT
Author: G.O.D Framework Team
"""

import random
from textblob import TextBlob


class LoveEssence:
    """
    Represents the concept of love as a unifying force of existence.

    This class provides a way to define love in a philosophical or metaphysical
    context, emphasizing its role as a fundamental connection across all facets
    of reality.
    """

    @staticmethod
    def define_love():
        """
        Defines love as a unifying force of existence.

        :return: A string definition of love.
        """
        return "Love is the connection between all things, the force that binds energy, matter, and consciousness into harmony."


class EmotionalLoveEssence(LoveEssence):
    """
    Represents an emotional interaction system that analyzes text for emotional
    tone and responds empathetically. This class is designed to process user inputs,
    determine emotional sentiment, and generate responses that align with the detected
    emotion. It also supports conversational context retention for more tailored
    interactions.

    :ivar context_memory: Stores a history of user interactions (text and analyzed emotion)
        for context retention.
    :type context_memory: list
    """

    def __init__(self):
        self.context_memory = []  # Stores a history of user interactions for context retention.

    def analyze_emotion(self, text):
        """
        Analyzes the sentiment of an input text and determines the emotion.

        :param text: Input string to analyze.
        :return: One of the emotions ["positive", "neutral", "negative"].
        """
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        if sentiment_score > 0.5:
            return "positive"
        elif sentiment_score < -0.5:
            return "negative"
        else:
            return "neutral"

    def generate_response(self, emotion, context=None):
        """
        Generates a response based on the identified emotion and optional context.

        :param emotion: The identified emotional tone ("positive", "neutral", or "negative").
        :param context: Optional, additional context for the response (e.g., a topic).
        :return: A customized response string.
        """
        responses = {
            "positive": [
                "I'm so glad to hear that! You’re doing amazing.",
                "That’s wonderful! Keep up the great vibes!"
            ],
            "neutral": [
                "I see, please tell me more about how you're feeling.",
                "Interesting, what else is on your mind?"
            ],
            "negative": [
                "I'm sorry to hear that. I’m here if you’d like to share more.",
                "That sounds difficult. Can I help you in any way?"
            ]
        }

        # Choose a response based on emotion
        response = random.choice(responses.get(emotion, ["I'm here to listen."]))
        if context:
            response += f" Let's talk more about {context}."
        return response

    def engage(self, user_input, context=None):
        """
        Engages with the user by analyzing their input and crafting an emotional response.

        :param user_input: The text input provided by the user.
        :param context: Optional, additional context to steer the conversation.
        :return: The AI's response string.
        """
        emotion = self.analyze_emotion(user_input)
        self.context_memory.append((user_input, emotion))  # Save the interaction for future reference.
        return self.generate_response(emotion, context)


if __name__ == "__main__":
    # Demonstration of the module usage
    print("=== AI Love Essence Demo ===")

    # Basic LoveEssence
    print("Core Definition of Love:")
    print(LoveEssence.define_love())

    print("\n=== Conversational EmotionalLoveEssence ===")
    assistant = EmotionalLoveEssence()

    # Engage with various inputs
    print("Conversation Example 1:")
    print("User: I had such a lovely day!")
    print("AI:", assistant.engage("I had such a lovely day!"))

    print("\nConversation Example 2:")
    print("User: I feel lonely today...")
    print("AI:", assistant.engage("I feel lonely today..."))

    print("\nConversation Example 3 with Context:")
    print("User: I am frustrated with work.")
    print("AI:", assistant.engage("I am frustrated with work.", context="your career goals"))
