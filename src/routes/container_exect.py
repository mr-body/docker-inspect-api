from fastapi import APIRouter, HTTPException
from src.services.exec import ExecService, ExecRequest

router = APIRouter(
    prefix="/command",
    tags=["docker"]
)

exec_service = ExecService()


@router.post("/")
def execute(payload: ExecRequest):
    try:
        result = exec_service.exec_command(payload)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Execution failed: {str(e)}"
        )