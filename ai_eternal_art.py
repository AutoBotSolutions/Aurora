"""
Home: https://autobotsolutions.com
Wiki: https://autobotsolutions.com/god/stats/doku.php?id=start
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT https://autobotsolutions.com/god/docs/LICENSE
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

"""
AI Eternal Art
==============

The AI Eternal Art System generates evocative artistic pieces based on themes and randomness.
It leverages advanced AI techniques, including Generative Adversarial Networks (GANs),
to deliver dynamic outputs in the form of visual art while providing extensibility for further art forms.

---

Main Features:
1. **Theme-Based Artistic Generation**: Produces unique artworks aligned with user-defined themes.
2. **Supports StyleGAN2**: Utilizes pre-trained GAN models for high-quality visual art generation.
3. **Customizable Output**: Generate themed art based on random seeds for reproducibility.
4. **Creative Potential**: Ideal for digital art, storytelling, gaming, and creative exploration.

---

Author: G.O.D Team
License: MIT
"""

import torch
import torchvision.transforms as transforms
from PIL import Image
from models.stylegan2 import StyleGAN2


class EternalArt:
    """
    A system for generating digital artwork using a pre-trained StyleGAN2 model.

    This class facilitates loading a pre-trained StyleGAN2 model, applying transformations,
    and generating artwork based on input parameters. It includes functionality for saving
    the generated artwork as an image file.

    :ivar model_path: Path to the pre-trained GAN model.
    :type model_path: str
    :ivar device: Device to use for computation, either CPU or CUDA.
    :type device: torch.device
    :ivar model: Loaded pre-trained StyleGAN2 model.
    :type model: StyleGAN2
    :ivar transform: Transformation pipeline to preprocess images.
    :type transform: torchvision.transforms.Compose
    """

    def __init__(self, model_path="models/pretrained_stylegan2.pt"):
        """
        Initialize the EternalArt system with the pre-trained StyleGAN2 model.

        :param model_path: Path to the pre-trained GAN model (default: `"models/pretrained_stylegan2.pt"`).
        """
        self.model_path = model_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model()
        self.transform = self._get_transform()

    def _load_model(self):
        """
        Load the pre-trained StyleGAN2 model from the specified path.

        :return: The loaded StyleGAN2 model.
        """
        try:
            model = StyleGAN2.load_pretrained(self.model_path).to(self.device)
            model.eval()  # Set model to evaluation mode
            return model
        except Exception as e:
            raise RuntimeError(f"Failed to load the model from {self.model_path}: {str(e)}")

    def _get_transform(self):
        """
        Define the transformation pipeline to preprocess images.

        :return: Transformation pipeline that resizes and normalizes images.
        """
        return transforms.Compose([
            transforms.Resize((512, 512)),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])

    def generate_art(self, seed=None, style=None):
        """
        Generate a unique artwork, optionally guided by a random seed and style.

        :param seed: Random seed for reproducibility (optional).
        :param style: Optional parameter to define conditional inputs for the artistic style (future implementation).
        :return: A PIL image of the generated artwork.
        """
        if seed is not None:
            torch.manual_seed(seed)

        try:
            noise = torch.randn(1, self.model.latent_dim).to(self.device)  # Generate noise vector
            generated_image = self.model.generate(noise)
            return self._tensor_to_image(generated_image)
        except Exception as e:
            raise RuntimeError(f"Error occurred during art generation: {str(e)}")

    def _tensor_to_image(self, tensor):
        """
        Convert a tensor to a PIL image for visualization.

        :param tensor: A PyTorch tensor representing a single image.
        :return: A PIL Image object of the generated artwork.
        """
        tensor = tensor.squeeze(0).permute(1, 2, 0).cpu().detach()
        tensor = (tensor * 0.5 + 0.5).clamp(0, 1)  # Rescale to [0, 1]
        return Image.fromarray((tensor.numpy() * 255).astype('uint8'))

    def save_art(self, image, file_path="output/artwork.png"):
        """
        Save the generated artwork as an image file.

        :param image: A PIL image of the artwork to save.
        :param file_path: File path to save the artwork (default: `"output/artwork.png"`).
        """
        try:
            image.save(file_path, format="PNG")
            print(f"Artwork saved to: {file_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to save artwork: {str(e)}")


# ===== Example Usage =====
if __name__ == "__main__":
    # Initialize the EternalArt generator
    art_generator = EternalArt("models/pretrained_stylegan2.pt")

    # Generate an artwork from a specific seed
    try:
        seed = 42
        artwork = art_generator.generate_art(seed=seed)
        artwork.show()  # Display the artwork
        art_generator.save_art(artwork, file_path="output/example_artwork.png")  # Save to file
    except RuntimeError as e:
        print(f"Error: {e}")
