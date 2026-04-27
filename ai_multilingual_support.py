"""
AI Multilingual Support

A lightweight translation module enabling seamless translation across multiple languages.
Built on the Googletrans library, this solution facilitates global communication and
language adaptation for a variety of applications.

---

**Key Features:**
1. Simple API for translating text between source and target languages.
2. Supports over 100 languages via Googletrans.
3. Includes error handling for invalid or unsupported languages.
4. Easily extensible for custom use cases (e.g., batch processing, hybrid models).
5. Suitable for integration in chatbots, web platforms, or backend systems.

**Requirements:**
- python >= 3.7
- Install the required library via: `pip install googletrans==4.0.0-rc1`

---
"""

from googletrans import Translator


class MultilingualSupport:
    """
    Handles translation and language detection functionalities for textual content.

    This class provides methods to translate a given text from a source
    language to a target language, as well as to detect the original language
    of a given text. It uses an underlying translation service for these tasks.

    :ivar translator: The instance of Translator used for performing translations
                      and language detections.
    :type translator: Translator
    """

    def __init__(self):
        """
        Initializes the Translator instance for managing translations.
        """
        self.translator = Translator()

    def translate_text(self, text, source_lang="auto", target_lang="en"):
        """
        Translates the input text to the desired target language.

        :param text: str - The text to be translated.
        :param source_lang: str - The source language of the text. Defaults to 'auto' for automatic detection.
        :param target_lang: str - The target language for translation. Defaults to 'en' (English).
        :return: str - The translated text or an error message if translation fails.
        """
        try:
            # Perform the translation
            translation = self.translator.translate(text, src=source_lang, dest=target_lang)
            return translation.text
        except Exception as e:
            return f"Translation failed: {e}"

    def detect_language(self, text):
        """
        Detects the source language of the provided text.

        :param text: str - The text for which to detect the source language.
        :return: str - The detected language code or an error message if detection fails.
        """
        try:
            detection = self.translator.detect(text)
            return detection.lang
        except Exception as e:
            return f"Language detection failed: {e}"


# Example Usage
if __name__ == "__main__":
    # Initialize translator
    multi_lang = MultilingualSupport()

    # Example 1: Translate text to a specific language
    text = "Hello, how can I assist you?"
    translated_text = multi_lang.translate_text(text, target_lang="fr")
    print("Translated Text (French):", translated_text)  # Output: Bonjour, comment puis-je vous aider?

    # Example 2: Detect the source language of a text
    source_text = "Hola, ¿cómo estás?"
    detected_language = multi_lang.detect_language(source_text)
    print("Detected Language:", detected_language)  # Output: es (Spanish)

    # Example 3: Translate dynamically between languages
    text = "Good morning"
    dynamic_translation = multi_lang.translate_text(text, source_lang="en", target_lang="de")  # Translate to German
    print("Translated Text (German):", dynamic_translation)  # Output: Guten Morgen