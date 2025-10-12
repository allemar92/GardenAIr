from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pipelines.garden_pipeline import run_garden_pipeline
from clients.litellm_client import LiteLLMClient

app = FastAPI(title="GardenAIr API", version="1.0")

@app.get("/")
def root():
    return {"message": "🌱 Welcome to the GardenAIr API! Use POST /ask or /run_pipeline to interact."}

class GardenRequest(BaseModel):
    location: str
    preferences: list[str]
    num_people: int

@app.post("/generate-garden")
async def generate_garden(req: GardenRequest):
    """
    Run the full garden pipeline:
    1. Plant selection
    2. Synergy discovery
    3. Gardening instructions
    4. Map summarization
    5. Image generation
    """
    try:
        client = LiteLLMClient().get_client()
        result = run_garden_pipeline(
            location=req.location,
            preferences=req.preferences,
            num_people=req.num_people,
            client=client
        )
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
