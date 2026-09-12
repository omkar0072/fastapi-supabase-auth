from fastapi import APIRouter, Depends
from app.auth import get_current_user

router = APIRouter(prefix="/protected", tags=["Protected"])


@router.get("/profile")
async def profile(user: dict = Depends(get_current_user)):
    return {
        "message": "Profile retrieved successfully",
        "user": {
            "id": user.get("sub"),
            "email": user.get("email"),
            "role": user.get("role"),
        },
    }


@router.get("/dashboard")
async def dashboard(user: dict = Depends(get_current_user)):
    return {
        "message": "Dashboard data retrieved successfully",
        "user_email": user.get("email"),
        "stats": {"projects": 12, "tasks": 48, "completed": 35},
    }
