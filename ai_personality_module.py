"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

"""
AI Personality Module

The AI Personality Module enables developers to customize the behavior, tone, and enthusiasm of AI responses. It is designed for conversational AI systems, chatbots, and customer interaction tools, where tailored personality traits enhance user experience and engagement.

---

**Key Features**:
1. **Configurable Tone and Enthusiasm**:
   - Tones: "formal" or "casual"
   - Enthusiasm Levels: "low", "moderate", "high"

2. **Dynamic Response Generation**:
   - Adapts responses dynamically to the user's input and the selected personality traits.

3. **Extensibility**:
   - Easily extendable to support additional tones, enthusiasm levels, or personality traits.

4. **Lightweight and Open-Source**:
   - Built with simplicity in mind and ready to integrate into any Python application requiring personality-driven AI responses.

**Author**: G.O.D Framework Team
"""
from typing import Any


class PersonalityModule:
    """
    Provides a customizable personality interface for generating AI responses.

    This class allows users to set a communication tone and enthusiasm level,
    which are then reflected in the generated AI responses. It is designed to
    simulate varied conversational styles, ranging from formal to casual and with
    differing levels of enthusiasm.

    :ivar tone: The communication style of the AI. Can be "formal" (reserved and
        professional) or "casual" (informal and relaxed).
    :type tone: str
    :ivar enthusiasm: The energy level in responses. Options are "low" (neutral and
        minimal enthusiasm), "moderate" (balanced enthusiasm), or "high" (energetic
        and expressive).
    :type enthusiasm: str
    """

    def __init__(self, tone: str = "formal", enthusiasm: str = "moderate"):
        """
        Initializes the PersonalityModule class with a given tone and enthusiasm level.

        :param tone: Communication style (default is "formal"). Options:
            - "formal": Reserved and professional tone.
            - "casual": Informal and relaxed tone.
        :param enthusiasm: Response enthusiasm (default is "moderate"). Options:
            - "low": Neutral and minimal enthusiasm.
            - "moderate": Balanced enthusiasm.
            - "high": Energetic and expressive enthusiasm.
        """
        if tone not in ("formal", "casual"):
            raise ValueError("Invalid tone. Choose from 'formal' or 'casual'.")
        if enthusiasm not in ("low", "moderate", "high"):
            raise ValueError("Invalid enthusiasm level. Choose from 'low', 'moderate', or 'high'.")

        self.tone = tone
        self.enthusiasm = enthusiasm

    def respond(self, message: str) -> str:
        """
        Generates a personalized AI response based on the tone and enthusiasm settings.

        :param message: User input string.
        :return: A dynamically generated response string tailored to the personality settings.
        """
        base_response = f"I received your message: '{message}'."

        # Add a tone-specific addition to the response
        if self.tone == "formal":
            base_response += " Thank you for reaching out."
        elif self.tone == "casual":
            base_response += " Cool, got it!"

        # Add enthusiasm-specific addition to the response
        if self.enthusiasm == "high":
            base_response += " I'm super excited about this!"
        elif self.enthusiasm == "low":
            base_response += " I'm here to assist you."

        return base_response


# Example Usage
if __name__ == "__main__":
    # Create personality instances with different configurations
    formal_personality = PersonalityModule(tone="formal", enthusiasm="moderate")
    casual_personality = PersonalityModule(tone="casual", enthusiasm="high")

    # Get and display responses based on configurations
    user_message = "Tell me about today."

    print("Formal Response:")
    print(formal_personality.respond(user_message))
    # Output: I received your message: 'Tell me about today.'. Thank you for reaching out.

    print("\nCasual Response:")
    print(casual_personality.respond(user_message))
    # Output: I received your message: 'Tell me about today.'. Cool, got it! I'm super excited about this!
