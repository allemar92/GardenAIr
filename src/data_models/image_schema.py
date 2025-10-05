from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Literal

class ImageGeneratorInput(BaseModel):
    """Input schema for the garden image generator."""
    prompt: str = Field(..., min_length=10, description="The prompt text describing the garden layout.")
    size: Literal["512x512", "1024x1024"] = Field("1024x1024", description="The size of the generated image.")
    model: Optional[str] = Field("dall-e-3", description="Image generation model to use.")

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Generate a minimal black-and-white outline schema, similar to diagrams in textbooks",
                "size": "1024x1024",
                "model": "dall-e-3"
            }
        }

class ImageGeneratorOutput(BaseModel):
    """Output schema for the garden image generator."""
    image_url: HttpUrl = Field(..., description="URL of the generated image.")

    class Config:
        json_schema_extra = {
            "example": {
                "image_url": "https://example.com/garden_schema.png"
            }
        }
