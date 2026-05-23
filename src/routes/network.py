from fastapi import APIRouter
from src.services.network import NetworkService

router = APIRouter(
    prefix="/network",
    tags=["docker"]
)

network_service = NetworkService()

@router.get("/")
def get_networks():
    return network_service.get_networks()

@router.get("/{id}")
def get_network(id: str):
    return network_service.inspect_network(id)
