from clients.litellm_client import LiteLLMClient
from agents.agent import Agent

def get_client(model: str = "gpt-4o-mini", temperature: float = 0.2, max_tokens: int = 1024):
    """
    Returns a LiteLLM client with chosen parameters.
    """
    lite_client = LiteLLMClient(model=model, temperature=temperature, max_tokens=max_tokens)
    return lite_client.get_client()


def create_plant_selector():
    """
    Returns the gardening PlantSelector agent.
    """
    return Agent(
        name="PlantSelector",
        model="gpt-4o-mini",
        role="a helpful gardening assistant specialized in synergistic gardening."
    )

def create_synergy_agent():
    """
    Returns the plant's synergy expert agent.
    """
    return Agent(
        name="SynergyAgent",
        model="gpt-4o-mini",
        role="a helpful gardening assistant specialized in synergistic gardening."
    )

def create_garden_agent():
    """
    Returns the gardening agent
    """
    return Agent(
        name="GardenAgent",
        model="gpt-4o-mini",
        role="a helpful gardening assistant specialized in synergistic gardening."
    )