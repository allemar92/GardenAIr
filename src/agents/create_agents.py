from clients.litellm_client import LiteLLMClient
from agents.agent import Agent

lite_client = LiteLLMClient(model="gpt-4o-mini", temperature=0.2, max_tokens=1024)
client = lite_client.get_client()

#first agent Plant Selector
plant_selector = Agent(
    name="PlantSelector",
    model="gpt-4o-mini",
    role=" a helpful gardening assistant specialized in synergistic gardening."
    )


