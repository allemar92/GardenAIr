from pydantic import BaseModel
from typing import List

class GardeningInput(BaseModel):
    location: str
    preferences: List[str]
    num_people: int 
    