from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.routes import image, network, process, volume, log, command, terminal

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(image.router)
app.include_router(network.router)
app.include_router(process.router)
app.include_router(volume.router)
app.include_router(log.router)
app.include_router(command.router)
app.include_router(terminal.router)

# frontend separado
app.mount("/ui", StaticFiles(directory="public", html=True), name="public")


@app.get("/health")
def health():
    return {"status": "ok"}