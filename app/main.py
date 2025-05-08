from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.azure_openai import AzureOpenAIWrapper

app = FastAPI()
ai = AzureOpenAIWrapper()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        messages = [{"role": "user", "content": request.message}]
        response = ai.chat_completion(messages)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
