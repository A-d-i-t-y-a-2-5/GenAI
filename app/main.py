import time

from fastapi import FastAPI, Request, Response
from typing import Callable, Awaitable

import uvicorn

from settings import AppSettings

app = FastAPI()
config = AppSettings()

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

