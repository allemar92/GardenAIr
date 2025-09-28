from typing import Optional

class Agent:
    """
    A generic agent that interacts with an LLM.
    Can be customized for different domains and personalities.
    """
    def __init__(self, name="GenericAgent", model="default-model", role="helpful assistant"):
        self.name = name
        self.model = model
        self.role = role

    def ask(self, prompt: str, client: Optional[object] = None, model: Optional[str] = None) -> str:
        if client is None:
            return "Error: no client provided, use ask()."
        
        model_to_use = model or self.model

        try:
            response = client.chat.completions.create(
                model=model_to_use,
                messages=[
                    {"role": "system", "content": f"You are {self.name}, {self.role}."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"
