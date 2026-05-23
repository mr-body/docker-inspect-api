from fastapi import FastAPI
from src.routes import docker

app = FastAPI()

app.include_router(docker.router)

@app.get("/health")
def health():
    return {"status": "ok"}