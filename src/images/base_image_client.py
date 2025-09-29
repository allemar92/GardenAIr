from abc import ABC, abstractmethod

class BaseImageClient(ABC):
    @abstractmethod
    def generate_image(self, prompt: str, size: str = "1024x1024") -> str:
        """
        Generate an image based on a prompt.
        Returns a URL or path to the generated image.
        """
        pass