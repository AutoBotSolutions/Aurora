"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

"""
AI Infinite Creativity
=======================

A flexible generative AI framework designed to produce visual, creative outputs such as generative art.
This script combines randomness with procedural logic, enabling scalable and customizable artistic exploration.

License: MIT
Author: G.O.D Team

Features:
---------
1. Generative artwork creation using mathematical randomness and sine waves.
2. Extensibility for additional creative domains (e.g., music, 3D modeling).
3. Visualization of creative outputs using matplotlib.
4. Lightweight and accessible design for developers, artists, and educators.
"""

import matplotlib.pyplot as plt
import numpy as np


class InfiniteCreativity:
    """
    Represents a utility for creating generative art by manipulating mathematical sine
    waves combined with noise. This class provides a static method for visualizing the
    generated art. It is designed to inspire creativity through randomness and mathematical
    principles. Intended for experimentation and educational purposes.

    :ivar None: This class does not contain instance attributes.
    """

    @staticmethod
    def generate_art(noise=100):
        """
        Produces simple generative art by combining sine waves and random noise.

        :param noise: Controls the complexity and resolution of the output (higher = more detail).
        :return: Displays the generative art visualization.
        """
        x = np.linspace(0, 10, noise)
        y = np.sin(x) + np.random.normal(scale=0.5, size=noise)  # Add randomness to sine wave
        plt.plot(x, y, color='purple', alpha=0.8)  # Configure line appearance
        plt.title("Generative Imagination: Art")
        plt.xlabel("x-axis")
        plt.ylabel("y-axis")
        plt.grid(True)
        plt.show()


class AdvancedCreativity(InfiniteCreativity):
    """
    Extends the InfiniteCreativity class to provide additional functionalities
    for generating advanced generative art with customizable parameters.

    This class enables users to create visually appealing, customizable plots
    that combine mathematical functions and random perturbations, useful for
    artistic visualizations or data exploration.

    :ivar base_creativity: Reference to the base InfiniteCreativity class instance.
    :type base_creativity: InfiniteCreativity
    :ivar output_format: Preferred format for saving visual outputs.
    :type output_format: str
    """

    @staticmethod
    def generate_advanced_art(noise=200, color='blue', alpha=0.6, grid=True):
        """
        Creates customizable generative art with additional parameters.
        
        :param noise: Controls the complexity of the output.
        :param color: Defines the color of the plot.
        :param alpha: Sets the transparency of the plot line.
        :param grid: Toggles the display of the grid.
        :return: Displays the generative art visualization.
        """
        x = np.linspace(0, 15, noise)
        y = np.cos(x) * np.sin(x) + np.random.normal(scale=0.4, size=noise)  # Combine cosine and sine randomness
        plt.plot(x, y, color=color, alpha=alpha)  # Apply user-defined styling
        plt.title("Advanced Generative Art")
        plt.xlabel("x-axis")
        plt.ylabel("y-axis")
        if grid:
            plt.grid(True)
        plt.show()


class SavingCreativity(InfiniteCreativity):
    """
    Summary of what the class does.

    Detailed description of the class, its purpose, and usage.

    :ivar attribute1: Description of attribute1.
    :type attribute1: type
    :ivar attribute2: Description of attribute2.
    :type attribute2: type
    """

    @staticmethod
    def generate_and_save_art(file_name='generative_art.png', noise=150):
        """
        Generates and saves the generative art visualization to an image file.

        :param file_name: File name for the output image (e.g., .png, .jpg).
        :param noise: Controls the complexity and resolution of the visual output.
        :return: A confirmation message indicating where the image was saved.
        """
        x = np.linspace(0, 10, noise)
        y = np.sin(x) + np.random.normal(scale=0.4, size=noise)
        plt.figure(figsize=(10, 6))  # Configure the figure size
        plt.plot(x, y, color='orange', alpha=0.7)
        plt.title("Saved Generative Art")
        plt.xlabel("x-axis")
        plt.ylabel("y-axis")
        plt.grid(True)
        plt.savefig(file_name)
        plt.close()  # Close the figure to avoid display overhead
        return f"Art successfully saved to {file_name}"


def multi_layered_art(layers=5, noise=100):
    """
    Generates and displays a multi-layered generative art plot.

    This function creates a visual representation of multiple sinusoidal layers with
    added noise to simulate abstract generative art. Each layer is offset and plotted
    independently, resulting in an overlapping visually-rich output.

    :param layers: Number of sinusoidal layers to generate and plot.
                   Each layer is offset by 0.5 units.
    :type layers: int
    :param noise: Number of data points for each layer; defines the resolution of the plot.
    :type noise: int
    :return: None
    """
    x = np.linspace(0, 15, noise)
    plt.figure(figsize=(12, 8))
    for layer in range(layers):
        y = np.sin(x + (layer * 0.5)) + np.random.normal(scale=0.3, size=noise)
        plt.plot(x, y, label=f"Layer {layer + 1}", alpha=0.6)
    plt.title("Layered Generative Art")
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.legend()
    plt.grid(True)
    plt.show()


# ===== Examples =====
if __name__ == "__main__":
    # Example 1: Basic Infinite Creativity
    print("-- Example 1: Basic Generative Art --")
    creator = InfiniteCreativity()
    creator.generate_art()

    # Example 2: Advanced Creativity with Custom Parameters
    print("\n-- Example 2: Advanced Custom Generative Art --")
    advanced_creator = AdvancedCreativity()
    advanced_creator.generate_advanced_art(noise=300, color="green", alpha=0.7)

    # Example 3: Saving generative art to a file
    print("\n-- Example 3: Save Generative Art to File --")
    saving_creator = SavingCreativity()
    result = saving_creator.generate_and_save_art(file_name="my_generated_art.png", noise=250)
    print(result)

    # Example 4: Layered Generative Art
    print("\n-- Example 4: Multi-Layered Generative Art --")
    multi_layered_art(layers=5, noise=200)
