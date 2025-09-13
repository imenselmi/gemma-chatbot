from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from mlflow_logger import log_interaction

app = FastAPI(title="Gemma Chatbot Proxy API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_methods=["*"],
    allow_headers=["*"]
)

GEMMA_API_URL = "http://localhost:8018/v1/chat/completions"

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    payload = {
        "model": "gemma-3-27b-it",
        "messages": [{"role": "user", "content": request.message}]
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(GEMMA_API_URL, json=payload, timeout=120)
        result = response.json()
    
    # Extract model text (Gemma response format)
    model_output = result.get("choices", [{}])[0].get("message", {}).get("content", "")
    
    # Log to MLflow
    log_interaction(request.message, model_output)
    
    return {"response": model_output}

@app.get("/health")
async def health():
    return {"status": "ok"}
