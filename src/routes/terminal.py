from fastapi import APIRouter, WebSocket
from src.services.terminal import handle_terminal, handle_host_terminal

router = APIRouter(prefix="/terminal", tags=["Terminal"])


@router.websocket("/container")
async def terminal_container(ws: WebSocket):

    await ws.accept()

    container = ws.query_params.get("container")
    shell = ws.query_params.get("shell", "bash")

    await handle_terminal(
        ws,
        container=container,
        shell=shell,
    )

@router.websocket("/local")
async def host_terminal(ws: WebSocket):
    await ws.accept()
    await handle_host_terminal(ws)