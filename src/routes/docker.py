from fastapi import APIRouter
from src.services.docker import DockerService

router = APIRouter(
    prefix="/docker",
    tags=["docker"]
)

docker_service = DockerService()

@router.get("/networks")
def get_networks():
    return docker_service.get_networks()

@router.get("/images")
def get_images():
    return docker_service.get_images()

@router.get("/process")
def get_process():
    return docker_service.get_process()