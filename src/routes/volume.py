from fastapi import APIRouter
from src.services.volume import VolumeService

router = APIRouter(
    prefix="/volume",
    tags=["Volume"]
)

volume_service = VolumeService()

@router.get("/")
def get_volumes():
    return volume_service.get_volumes()

@router.get("/{name}")
def get_volume(name: str):
    return volume_service.inspect_volume(name)
@router.get("/{name}/files")
def list_volume_files(name: str, path: str = "/"):
    return volume_service.list_volume_files(name, path)

@router.delete("/{name}")
def remove_volume(name: str):
    return volume_service.remove_volume(name)

from fastapi.responses import StreamingResponse

@router.get("/{name}/backup")
def backup_volume(name: str):
    process_stdout = volume_service.backup_volume(name)
    return StreamingResponse(
        process_stdout, 
        media_type="application/x-tar",
        headers={"Content-Disposition": f"attachment; filename={name}_backup.tar"}
    )