from fastapi import APIRouter
from src.services.image import ImageService

router = APIRouter(
    prefix="/image",
    tags=["docker"]
)

imaage_service = ImageService()

@router.get("/")
def get_images():
    return imaage_service.get_images()