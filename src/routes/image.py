from fastapi import APIRouter
from src.services.image import ImageService

router = APIRouter(
    prefix="/image",
    tags=["Image"]
)

image_service = ImageService()

from pydantic import BaseModel

class RunImageRequest(BaseModel):
    image: str
    name: str | None = None
    ports: str | None = None
    volumes: str | None = None

@router.get("/")
def get_images():
    return image_service.get_images()

@router.delete("/{image_id}")
def remove_image(image_id: str):
    return image_service.remove_image(image_id)

@router.post("/run")
def run_image(payload: RunImageRequest):
    return image_service.run_image(payload.model_dump())