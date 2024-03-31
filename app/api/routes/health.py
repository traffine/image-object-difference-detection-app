from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter()


@router.get(
    "/health",
    name="Health check",
)
async def health():
    """Health check

    FastAPI health checks.

    Args:

    Returns:
    """
    return Response(status_code=200)
