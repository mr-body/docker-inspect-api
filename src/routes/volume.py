from fastapi import APIRouter
from src.services.volume import VolumeService

router = APIRouter(
    prefix="/volume",
    tags=["docker"]
)

volume_service = VolumeService()

@router.get("/")
def get_volumes():
    return volume_service.get_process()

@router.get("/{name}")
def get_volume(name: str):
    return volume_service.inspect_volume(name)