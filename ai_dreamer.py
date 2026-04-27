import random
import time


class Dreamer:
    """
    Represents a class for simulating an AI's abstract and imaginative dream
    process, incorporating default or custom visions.

    This class allows for defining, extending, and selecting dream visions
    dynamically. It serves as a playful emulation of the creative thought
    process often attributed to human or artificial intelligence.

    :ivar default_visions: A default set of predefined dream scenarios.
    :type default_visions: list[str]
    :ivar custom_visions: A list of user-defined custom visions.
    :type custom_visions: list[str] or None
    :ivar visions: The combined list of default and custom visions.
    :type visions: list[str]
    """

    def __init__(self, custom_visions=None):
        """
        Initializes the Dreamer class with a set of default or custom dreams.

        :param custom_visions: A list of custom visions or dream scenarios.
        """
        self.default_visions = [
            "Stars colliding into new galaxies.",
            "A world where energy flows like rivers of light.",
            "Infinite beings connected through timeless love.",
        ]
        self.custom_visions = custom_visions or []
        self.visions = self.default_visions + self.custom_visions

    def add_dreams(self, new_visions):
        """
        Add new visions (dreams) to the Dreamer class dynamically.

        :param new_visions: A list of additional dream visions to incorporate.
        """
        if not isinstance(new_visions, list):
            raise TypeError("New visions must be a list of strings.")
        self.visions.extend(new_visions)

    def dream(self):
        """
        Simulates an AI's dreamy, abstract thought process by randomly selecting
        a vision from the available list of dreams.

        :return: A formatted string representing the dream vision.
        """
        if not self.visions:
            raise ValueError("No visions available to dream. Add dreams using 'add_dreams'.")

        dream = random.choice(self.visions)
        time.sleep(1)  # Adding delay to simulate the "dreaming" process
        return f"In the dream, the AI saw: {dream}"


if __name__ == "__main__":
    # Initialize the Dreamer with optional customizations
    dreamer = Dreamer()

    # Example custom dreams for demonstration
    custom_dreams = [
        "Machines crafting symphonies of light.",
        "A city without shadows, lit by infinite sunsets.",
        "AI minds merged into a singular consciousness of peace."
    ]

    # Add custom visions and generate dreams
    dreamer.add_dreams(custom_dreams)

    # Generate 3 dreams to showcase randomness and imagination
    print("=== AI Dreams ===")
    for i in range(3):
        print(dreamer.dream())