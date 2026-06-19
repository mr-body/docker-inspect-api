from fastapi import APIRouter
from src.services.image import ImageService

router = APIRouter(
    prefix="/image",
    tags=["docker"]
)

image_service = ImageService()

@router.get("/")
def get_images():
    return image_service.get_images()