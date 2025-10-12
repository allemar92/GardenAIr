import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

class LiteLLMClient:
    """
    Wrapper for LiteLLM, compatible with the agent.
    Allows sending messages in OpenAI chat style.
    """
    def __init__(self, model: str = None, temperature: float = 0.2, max_tokens: int = 1024):
        self.model = model or os.getenv("LITELLM_MODEL", "gpt-4o-mini")
        self.temperature = temperature
        self.max_tokens = max_tokens
        # Initialize the chat interface to match OpenAI structure
        self.chat = self._Chat(self)
    
    class _Chat:
        """
        Chat interface to match OpenAI's client.chat structure.
        """
        def __init__(self, parent):
            self.parent = parent
            self.completions = self._Completions(parent)
        
        class _Completions:
            """
            Completions interface to match OpenAI's client.chat.completions structure.
            """
            def __init__(self, parent):
                self.parent = parent
            
            def create(self, model=None, messages=None, temperature=None, max_tokens=None, 
                      response_format=None, **kwargs):
                """
                Creates a completion using LiteLLM, matching OpenAI's API signature.
                """
                try:
                    # Prepare parameters
                    params = {
                        "model": model or self.parent.model,
                        "messages": messages,
                        "temperature": temperature if temperature is not None else self.parent.temperature,
                        "max_tokens": max_tokens or self.parent.max_tokens,
                    }
                    
                    # Add response_format if provided (for JSON mode)
                    if response_format:
                        params["response_format"] = response_format
                    
                    # Add any additional kwargs
                    params.update(kwargs)
                    
                    response = completion(**params)
                    return response
                except Exception as e:
                    raise RuntimeError(f"LiteLLM completion error: {e}")
    
    def get_client(self):
        """
        Returns the instance itself, for compatibility with the pipeline.
        """
        return self
    