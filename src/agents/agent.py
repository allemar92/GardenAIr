import logging
from src.utils.logging_config import setup_logger
from typing import Union, Optional, Type
from pydantic import BaseModel
from src.clients.litellm_client import LiteLLMClient

logger = setup_logger("agent")


def get_client(model: str = "gpt-4o-mini", temperature: float = 0.2, max_tokens: int = 1024):
    """
    Returns a LiteLLM client with chosen parameters.
    """
    lite_client = LiteLLMClient(model=model, temperature=temperature, max_tokens=max_tokens)
    return lite_client.get_client()

class Agent:
    """
    A generic agent that interacts with an LLM.
    Can be customized for different domains and personalities.
    """
    def __init__(self, 
                name: str ="GenericAgent", 
                model: str ="default-model",
                role: str ="helpful assistant",
                temperature: float = 0.2,
                max_tokens: int = 1024,
                input_model: Optional[Type[BaseModel]] = None,
                output_model: Optional[Type[BaseModel]] = None):
        self.name = name
        self.model = model
        self.role = role
        self.input_model= input_model
        self.output_model= output_model
        self.client = get_client(model=self.model, temperature=temperature, max_tokens=max_tokens)
        logger.info(f"Initialized agent '{self.name}' with model '{self.model}', role='{self.role}'")

    def ask(self, prompt: Union[str, BaseModel], client: Optional[object] = None, model: Optional[str] = None) -> str:
        if client is None:
            return "Error: no client provided, use ask()."
        
        model_to_use = model or self.model

        if isinstance(prompt, BaseModel):
                    prompt_text = prompt.model_dump_json(indent=2)
        else:
            prompt_text=prompt

        logger.info(f"Agent '{self.name}' asking with model '{model_to_use}'")
        logger.debug(f"Prompt (first 300 chars): {prompt_text[:300]!r}")
        try:
            response = client.chat.completions.create(
                model=model_to_use,
                messages=[
                    {"role": "system", "content": f"You are {self.name}, {self.role}."},
                    {"role": "user", "content": prompt_text}
                ]
            )
            content = response.choices[0].message.content.strip()
            logger.info(f"{self.name}: Received response from model")
            logger.debug(f"Raw response: {content[:300]}...")
            if self.output_model:
                logger.info(f"{self.name}: Parsing response into {self.output_model.__name__}")
                try:
                    return self.output_model.model_validate_json(content)
                except Exception as e:
                    logger.error(f"❌ {self.name}: Failed to parse response: {e}", exc_info=True)
                    return f"Error parsing output to {self.output_model.__name__}: {e}"
                    
            return content
        
        except Exception as e:
            logger.error(f"{self.name}: Request failed with error: {e}", exc_info=True)
            return f"Error: {e}"
