from fastapi import FastAPI
from src.routes import image, network, process, volume

app = FastAPI()

app.include_router(image.router)
app.include_router(network.router)
app.include_router(process.router)
app.include_router(volume.router)

@app.get("/health")
def health():
    return {"status": "ok"}