from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.schemas.user import UserResponse
from app.core.config import settings

router = APIRouter(prefix="/me", tags=["User"])


@router.get("", response_model=UserResponse)
async def me(user=Depends(get_current_user)):
    limit = (
        settings.PRO_MONTHLY_CREDITS
        if user.subscription.plan == "pro"
        else settings.FREE_MONTHLY_CREDITS
    )

    return UserResponse(
        id=user.id,
        plan=user.subscription.plan,
        used_credits=user.usage.used_credits,
    )
