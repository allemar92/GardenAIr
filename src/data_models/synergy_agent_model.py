from pydantic import BaseModel, Field
from typing import List

class SynergyAgentInput(BaseModel):
    """Input model for the Synergy agent."""
    plant_list: List[str] = Field(..., description="List of selected plants for the garden")
    location: str = Field(..., description="Location or climate zone (e.g., Toscana, Firenze, Italia)")

    class Config:
        json_schema_extra = {
            "example": {
                "plant_list": ["tomatoes", "peppers", "carrots"],
                "location": "Firenze"
            }
        }

class SynergyAgentOutput(BaseModel):
    """Output model for the Synergy agent."""
    plants_and_synergy: List[str] = Field(..., description="List of plants including additional synergistic plants for the garden")

    class Config:
        json_schema_extra = {
            "example": {
                "plants_and_synergy": ["tomatoes", "peppers", "carrots", "basil"]
            }
        }