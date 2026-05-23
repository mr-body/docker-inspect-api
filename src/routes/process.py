from fastapi import APIRouter
from src.services.process import ProcessService

router = APIRouter(
    prefix="/process",
    tags=["docker"]
)

process_service = ProcessService()

@router.get("/")
def get_process():
    return process_service.get_process()