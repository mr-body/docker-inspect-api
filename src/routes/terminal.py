from fastapi import APIRouter, WebSocket
from src.services.terminal import handle_terminal

router = APIRouter(prefix="/terminal", tags=["docker"])


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