import time

from fastapi import FastAPI, Request, Response
from langchain_openrouter import ChatOpenRouter
from typing import Callable, Awaitable

from pydantic import BaseModel
import uvicorn

from settings import AppSettings

app = FastAPI()
config = AppSettings()
model = ChatOpenRouter(
    model_name=f"{config.llm.provider}/{config.llm.model}",
    api_key=config.llm.api_key,
    temperature=config.llm.temperature,
    max_tokens=config.llm.max_tokens,
)

class ChatRequest(BaseModel):
    query: str = "What is the capital of France?"

@app.get("/", summary="Check server status", description="Returns a message indicating that the server is up and running.")
async def root():
    return {"status": "Server is up and running"}

@app.middleware("http")
async def log_request(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    response_time = round(time.perf_counter() - start_time, 4)
    response.headers["X-Response-Time"] = str(response_time)
    return response

if __name__ == "__main__": 
    uvicorn.run(app, host=config.host, port=config.port)

