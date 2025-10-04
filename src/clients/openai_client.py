import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class OpenAIClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def get_client(self):
        return self.client