from pydantic import BaseModel, Field
from typing import List

class SummarizeMapAgentInput(BaseModel):
    """Input model for the Map Summarizer agent."""
    plants_and_synergy: List[str] = Field(..., description="List of garden plants and synergies")
    gardening_instruction: str = Field(..., description="Gardening instructions to set up the garden")

    class Config:
        json_schema_extra = {
            "example": {
                "plants_and_synergy": ["tomatoes", "basil", "carrots"],
                "gardening_instruction": "Plant basil near tomatoes and carrots for pest resistance and soil health."
            }
        }

class SummarizeMapAgentOutput(BaseModel):
    """Output model for the Map Summarizer agent."""
    summarized_map: str = Field(..., description="Summarized garden layout description")

    class Config:
        json_schema_extra = {
            "example": {
                "summarized_map": "Bed 1: tomatoes next to basil and carrots. Bed 2: lettuce next to onions."
            }
        }