"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

"""
AI Multicultural Voice Translation

This script provides a framework for multilingual, culturally adaptive translations using Hugging Face's `transformers`. 
The `MulticulturalVoice` class simplifies integration into AI systems for real-time translations, breaking language barriers 
and promoting cultural inclusivity.

License: MIT
"""

from transformers import pipeline


class MulticulturalVoice:
    """
    Represents a multilingual translation utility that facilitates text translation between
    a source language and a target language using pre-trained translation models.

    The purpose of this class is to enable real-time text translations while allowing dynamic
    updates to the source and target language. This can be used in various multilingual
    applications such as chatbots, content localization, and more. It leverages the
    Hugging Face `pipeline` for translation tasks.

    :ivar source_lang: The source language key configured for the translation.
    :type source_lang: str
    :ivar target_lang: The target language key configured for the translation.
    :type target_lang: str
    :ivar model_name: The name of the pre-trained translation model.
    :type model_name: str
    :ivar translator: The Hugging Face translation pipeline instance.
    :type translator: callable
    """

    def __init__(self, source_lang="en", target_lang="fr"):
        """
        Initializes the MulticulturalVoice class with a translation pipeline.

        :param source_lang: Source language key (default: "en" for English).
        :param target_lang: Target language key (default: "fr" for French).
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.model_name = f"translation_{source_lang}_to_{target_lang}"  # Model configuration
        try:
            self.translator = pipeline(self.model_name)
            print(f"Translation model initialized: {self.model_name}")
        except ValueError:
            raise ValueError(f"Translation pipeline '{self.model_name}' is not supported by Hugging Face transformers.")

    def translate_message(self, text):
        """
        Translates text from the source language to the target language.

        :param text: A string of text to be translated.
        :return: A string containing translated text.
        """
        try:
            print(f"Translating text: '{text}' from {self.source_lang} to {self.target_lang}...")
            result = self.translator(text)[0]['translation_text']
            return result
        except Exception as e:
            print(f"An error occurred during translation: {str(e)}")
            return f"Error: Unable to translate text."

    def update_language_pair(self, source_lang, target_lang):
        """
        Updates the source and target language for translation, dynamically changing the pipeline.

        :param source_lang: New source language key.
        :param target_lang: New target language key.
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.model_name = f"translation_{source_lang}_to_{target_lang}"
        try:
            self.translator = pipeline(self.model_name)
            print(f"Updated translation model: {self.model_name}")
        except ValueError:
            raise ValueError(f"Translation pipeline '{self.model_name}' is not supported by Hugging Face transformers.")


# Example Usage
if __name__ == "__main__":
    # Initialize the MulticulturalVoice class
    voice = MulticulturalVoice(source_lang="en", target_lang="fr")

    # Single sentence translation
    message = "Hello, world!"
    translated_message = voice.translate_message(message)
    print(f"Translation: {translated_message}")

    # Updating the language pair for translation (e.g., English to German)
    voice.update_language_pair("en", "de")
    translated_message = voice.translate_message("How are you today?")
    print(f"Translation: {translated_message}")

    # Example error handling with unsupported translation model
    try:
        voice.update_language_pair("xx", "yy")  # Invalid language pair
    except Exception as error:
        print(f"Caught an error: {error}")
