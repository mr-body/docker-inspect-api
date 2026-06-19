from fastapi import APIRouter, HTTPException
from src.services.network import NetworkService

router = APIRouter(
    prefix="/network",
     tags=["Network"]
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

from pydantic import BaseModel

class NetworkConnectRequest(BaseModel):
    container: str

@router.delete("/{network_id}")
def remove_network(network_id: str):
    return network_service.remove_network(network_id)

@router.post("/{network_id}/connect")
def connect_network(network_id: str, payload: NetworkConnectRequest):
    return network_service.connect_network(network_id, payload.container)

@router.post("/{network_id}/disconnect")
def disconnect_network(network_id: str, payload: NetworkConnectRequest):
    return network_service.disconnect_network(network_id, payload.container)