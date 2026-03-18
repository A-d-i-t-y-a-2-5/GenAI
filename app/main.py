from fastapi import FastAPI
import uvicorn

from settings import AppSettings

app = FastAPI()
config = AppSettings()

@app.get("/", summary="Check server status", description="Returns a message indicating that the server is up and running.")
async def root():
    return {"status": "Server is up and running"}

if __name__ == "__main__": 
    uvicorn.run(app, host=config.host, port=config.port)

