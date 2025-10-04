import os
from dotenv import load_dotenv
from openai import OpenAI
from .base_image_client import BaseImageClient

load_dotenv()

class OpenAIImageClient(BaseImageClient):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def generate_image(self, prompt: str, size: str = "1024x1024") -> str:
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            #n=1,
            size=size
        )
        return response.data[0].url
