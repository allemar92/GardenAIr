from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from src.pipelines.garden_pipeline import run_garden_pipeline
from src.clients.litellm_client import LiteLLMClient
from src.utils.logging_config import setup_logger

logger = setup_logger("main_api")

app = FastAPI(title="GardenAIr API", version="1.0")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"New request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Completed request: {request.method} {request.url} with status {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error handling request: {request.method} {request.url} - {e}", exc_info=True)
        raise e

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
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
    logger.info(f"Received garden generation request: {req.dict()}")
    try:
        client = LiteLLMClient().get_client()
        result = run_garden_pipeline(
            location=req.location,
            preferences=req.preferences,
            num_people=req.num_people,
            client=client
        )
        logger.info(f"Pipeline completed successfully for location={req.location}")
        return result

    except Exception as e:
        logger.error(f"❌ Pipeline failed for {req.location}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
