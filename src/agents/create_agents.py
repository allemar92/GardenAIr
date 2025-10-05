
from agents.agent import Agent
from data_models.plant_selector_model import PlantSelectorInput, PlantSelectorOutput
from data_models.synergy_agent_model import SynergyAgentInput, SynergyAgentOutput
from data_models.garden_agent_model import GardenAgentInput, GardenAgentOutput
from data_models.map_summarizer_model import SummarizeMapAgentInput, SummarizeMapAgentOutput



def create_plant_selector():
    """
    Returns the gardening PlantSelector agent.
    """
    return Agent(
        name="PlantSelector",
        model="gpt-4o-mini",
        role="a helpful gardening assistant specialized in synergistic gardening.",
        max_tokens=800
    )

def create_synergy_agent():
    """
    Returns the plant's synergy expert agent.
    """
    return Agent(
        name="SynergyAgent",
        model="gpt-4o-mini",
        role="a helpful gardening assistant specialized in synergistic gardening.",
        max_tokens=1500
    )

def create_garden_agent():
    """
    Returns the gardening agent
    """
    return Agent(
        name="GardenAgent",
        model="gpt-4o-mini",
        role="a helpful gardening assistant specialized in synergistic gardening.",
        max_tokens=3000
    )

def create_summarize_map_agent():
    """
    Returns the summarize map agent
    """
    return Agent(
        name="SummarizeMapAgent",
        model="gpt-4o-mini",
        role="a helpful gardening assistant specialized in synergistic gardening.",
        max_tokens=1000
    )