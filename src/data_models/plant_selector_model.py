from pydantic import BaseModel, Field
from typing import List

class PlantSelectorInput(BaseModel):
    """Input model for the Plant Selector agent."""
    location: str = Field(..., description="Location or climate zone (e.g., Toscana, Firenze, Italia)")
    preferences: List[str] = Field(..., description="List of preferred vegetables and berries (e.g., tomatoes, lettuce, carrots)")
    num_people: int = Field(..., description="Number of people to feed")

    class Config:
        json_schema_extra = {
            "example": {
                "location": "Toscana",
                "preferences": ["tomatoes", "lettuce", "carrots"],
                "num_people": 4
            }
        }

class PlantSelectorOutput(BaseModel):
    """Output model for the Plant Selector agent."""
    plant_list: List[str] = Field(..., description="List of suggested plants for the garden")

    class Config:
        json_schema_extra = {
            "example": {
                "plant_list": ["tomatoes", "lettuce", "carrots", "basil"]
            }
        }
