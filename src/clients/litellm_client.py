import os
import time
import logging
from dotenv import load_dotenv
from litellm import completion
from utils.logging_config import setup_logger

load_dotenv()
logger = setup_logger("litellm_client")

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

        logger.info(f"Initialized LiteLLMClient with model={self.model}, temperature={self.temperature}, max_tokens={self.max_tokens}")

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
                model_to_use = model or self.parent.model
                temp_to_use = temperature if temperature is not None else self.parent.temperature
                max_tokens_to_use = max_tokens or self.parent.max_tokens    

                logger.info(f"LiteLLM request to model='{model_to_use}'")
                logger.debug(f"Messages preview: {messages[:2] if messages else 'No messages'}")

                start_time = time.time()

                try:
                    # Prepare parameters
                    params = {
                        "model": model_to_use,
                        "messages": messages,
                        "temperature": temp_to_use,
                        "max_tokens": max_tokens_to_use,
                    }
                    
                    

                    # Add response_format if provided (for JSON mode)
                    if response_format:
                        params["response_format"] = response_format
                    
                    # Add any additional kwargs
                    params.update(kwargs)
                    
                    response = completion(**params)

                    elapsed = time.time() - start_time
                    logger.info(f"LiteLLM response received from '{model_to_use}' in {elapsed:.2f}s")


                    try:
                        preview = response["choices"][0]["message"]["content"]
                        logger.debug(f"Response preview: {preview[:300]!r}")
                    except Exception:
                        logger.debug("Response format not standard (no preview available).")

                    return response
                except Exception as e:
                    logger.error(f"❌ LiteLLM request failed: {e}", exc_info=True)
                    raise RuntimeError(f"LiteLLM completion error: {e}")
    
    def get_client(self):
        """
        Returns the instance itself, for compatibility with the pipeline.
        """
        logger.debug("Returning LiteLLMClient instance as client reference.")
        return self
    