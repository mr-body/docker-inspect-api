from fastapi import APIRouter
from src.services.process import ProcessService

router = APIRouter(
    prefix="/process",
    tags=["Process"]
)

process_service = ProcessService()

@router.get("/")
def get_process():
    return process_service.get_process()

@router.post("/{process_id}/stop")
def stop_process(process_id: str):
    return process_service.stop_process(process_id)

@router.post("/{process_id}/restart")
def restart_process(process_id: str):
    return process_service.restart_process(process_id)