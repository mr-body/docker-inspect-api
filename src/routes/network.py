from fastapi import APIRouter, HTTPException
from src.services.network import NetworkService

router = APIRouter(
    prefix="/network",
     tags=["docker"]
)

network_service = NetworkService()

@router.get("/")
def get_networks():
    result = network_service.get_networks()

    if not result:
        raise HTTPException(status_code=404, detail="Network not found")

    return result

@router.get("/{network_id}")
def get_network(network_id: str):
    result = network_service.inspect_network(network_id)

    if not result:
        raise HTTPException(status_code=404, detail="Network not found")

    return result