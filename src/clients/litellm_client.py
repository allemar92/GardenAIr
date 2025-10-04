import os
from .base_client import BaseClient
from dotenv import load_dotenv
#from litellm import LLMClient  

load_dotenv()

class LiteLLMClient(BaseClient):
    def __init__(self, model: str = None, temperature: float = 0.2, max_tokens: int = 1024):
        """
        model: model name, e.g. "gpt-4o-mini"
        temperature: temperature to set
        max_tokens: max number of tokens allowed on the answer
        """
        self.model = model or os.getenv("LITELLM_MODEL", "gpt-4o-mini")
        self.temperature = temperature
        self.max_tokens = max_tokens

    def get_client(self, model: str = None, temperature: float = None, max_tokens: int = None):
        """
        Returns the LiteLLM client with the specified parameters.
        """
        final_model = model or self.model
        final_temp = temperature if temperature is not None else self.temperature
        final_max_tokens = max_tokens if max_tokens is not None else self.max_tokens

        return LiteLLMClient(
            model=final_model,
            temperature=final_temp,
            max_tokens=final_max_tokens
        )

    
#esempi di uso
# client_wrapper = LiteLLMClient()
# client = client_wrapper.get_client()
# gardening_client = LiteLLMClient().get_client(
#     model="huggingface/falcon-7b-instruct",
#     temperature=0.5,
#     max_tokens=300
# )

# planning_client = LiteLLMClient().get_client(
#     model="gpt-4o-mini",
#     temperature=0.8,
#     max_tokens=800
# )
