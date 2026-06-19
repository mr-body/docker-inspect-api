from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from src.services.log import LogsService

router = APIRouter(
    prefix="/log",
    tags=["Process"]
)

logs_service = LogsService()


@router.get("/stream")
def stream_logs(identifier: str):

    def event_generator():
        process = logs_service.stream_logs(identifier)

        for line in process.stdout:
            yield line

    return StreamingResponse(event_generator(), media_type="text/plain")


@router.get("/tail")
def get_logs_tail(
    identifier: str,
    tail: int = Query(100, ge=1, le=1000)
):
    return logs_service.get_logs(identifier, tail)