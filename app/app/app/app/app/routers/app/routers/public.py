from fastapi import APIRouter

router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/info")
async def public_info():
    return {
        "message": "This is a public endpoint. No authentication required.",
        "version": "1.0.0",
    }
