from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi

from src.routes import image, network, process, volume, log, command, terminal, auth
from src.middleware.auth import auth_middleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(auth_middleware)

# routers
app.include_router(image.router)
app.include_router(network.router)
app.include_router(process.router)
app.include_router(volume.router)
app.include_router(log.router)
app.include_router(command.router)
app.include_router(terminal.router)
app.include_router(auth.router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Docker Inspect API",
        version="1.0.0",
        description="Este projeto permite inspecionar e listar informações do ambiente Docker de forma simples através de endpoints HTTP, incluindo containers em execução, imagens, redes e volumes",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # aplica globalmente
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method].setdefault("security", [
                {"BearerAuth": []}
            ])

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# frontend separado
app.mount("/ui", StaticFiles(directory="public", html=True), name="public")


@app.get("/health")
def health():
    return {"status": "ok"}