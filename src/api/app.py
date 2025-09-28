from fastapi import FastAPI
from pydantic import BaseModel
from agents.agent import Agent
from clients.litellm_client import LiteLLMClient

app = FastAPI(title="Multi-Agent API")

class AgentRequest(BaseModel):
    prompt: str
    agent_name: str = "Alice"
    model: str = "lite-model"

@app.post("/ask")
def ask_agent(req: AgentRequest):
    client = LiteLLMClient(model_path="src/models/litellm/my_model")
    agent = Agent(name=req.agent_name, model=req.model, role="helpful assistant")
    response = agent.ask(req.prompt, client)
    return {"agent": req.agent_name, "response": response}
