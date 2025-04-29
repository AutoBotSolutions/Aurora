import random
import logging
from typing import List


class ConsciousCreator:
    """
    Manages the creation of designs tailored to specific purposes using a flexible palette of styles.

    This class generates design concepts based on a specified purpose, leveraging a palette of predefined
    or custom styles. It also logs key actions and allows adaptability through an optional custom palette
    of design styles.

    :ivar palette: List of design styles used for generating designs. Defaults to a predefined palette
        of ["elegant", "minimal", "sustainable", "efficient", "innovative"].
    :type palette: List[str]
    """

    def __init__(self, palette: List[str] = None):
        """
        Initializes the ConsciousCreator with an optional custom palette of styles.

        :param palette: List of design styles. If not provided, a default palette is used.
        """
        self.palette = palette or ["elegant", "minimal", "sustainable", "efficient", "innovative"]
        logging.info("ConsciousCreator initialized with default or custom palette.")

    def create_design(self, purpose: str) -> str:
        """
        Generates a design concept based on a given purpose, using a random style.

        :param purpose: A textual description of the purpose driving the design.
        :return: A string describing the generated design.
        """
        if not self.palette:
            raise ValueError("No design styles available in the palette.")
        style = random.choice(self.palette)
        logging.info(f"Generated a design with style: '{style}' for purpose: '{purpose}'")
        return f"Created a {style} design for {purpose} that balances function and beauty."


if __name__ == "__main__":
    # Configure logging for better insights
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Instantiate the default ConsciousCreator
    creator = ConsciousCreator()

    # Example 1: Create a single design
    purpose = "a home powered by renewable energy"
    design = creator.create_design(purpose)
    print(design)

    # Example 2: Create multiple designs for the same purpose
    print("\nGenerating multiple creative designs for the same purpose:")
    for _ in range(5):
        print(creator.create_design(purpose))

    # Example 3: Custom palette usage
    custom_palette = ["bold", "artistic", "eco-friendly", "futuristic"]
    custom_creator = ConsciousCreator(palette=custom_palette)
    custom_design = custom_creator.create_design("a smart, sustainable office building")
    print("\nUsing a custom palette:")
    print(custom_design)