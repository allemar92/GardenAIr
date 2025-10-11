from typing import Optional
from typing import Union, Optional, Type
from pydantic import BaseModel
from clients.litellm_client import LiteLLMClient

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

    def ask(self, prompt: Union[str, BaseModel], client: Optional[object] = None, model: Optional[str] = None) -> str:
        if client is None:
            return "Error: no client provided, use ask()."
        
        model_to_use = model or self.model

        if isinstance(prompt, BaseModel):
                    prompt_text = prompt.model_dump_json(indent=2)
        else:
            prompt_text=prompt

        try:
            response = client.chat.completions.create(
                model=model_to_use,
                messages=[
                    {"role": "system", "content": f"You are {self.name}, {self.role}."},
                    {"role": "user", "content": prompt_text}
                ]
            )
            content = response.choices[0].message.content.strip()

            if self.output_model:
                try:
                    return self.output_model.model_validate_json(content)
                except Exception as e:
                    return f"Error parsing output to {self.output_model.__name__}: {e}"
            return content
        
        except Exception as e:
            return f"Error: {e}"
