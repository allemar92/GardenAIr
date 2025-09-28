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

    def ask(self, prompt: str, client=None):
        if client is None:
            return "Error: no client provided, use ask()."
        
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are {self.name}, {self.role}."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"
