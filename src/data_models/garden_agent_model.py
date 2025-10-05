from pydantic import BaseModel, Field
from typing import List

class GardenAgentInput(BaseModel):
    """Input model for the Garden agent."""
    plants_and_synergy: List[str] = Field(..., description="List of garden plants and synergies")
    num_people: int = Field(..., description="Number of people to feed")

    class Config:
        json_schema_extra = {
            "example": {
                "plants_and_synergy": ["tomatoes", "basil", "carrots"],
                "num_people": 4
            }
        }

class GardenAgentOutput(BaseModel):
    """Output model for the Garden agent."""
    gardening_instruction: str = Field(..., description="Gardening instructions to set up the garden")

    class Config:
        json_schema_extra = {
            "example": {
                "gardening_instruction": "Plant basil near tomatoes and carrots for pest resistance and soil health."
            }
        }