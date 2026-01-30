from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.config import settings
from app.schemas.content import (
    ContentGenerateRequest,
    ContentGenerateResponse,
)
from app.services.ai_content import generate_content
from app.models.content import GeneratedContent

router = APIRouter(prefix="/content", tags=["Content"])


@router.post("/generate", response_model=ContentGenerateResponse)
async def generate(
    payload: ContentGenerateRequest,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    limit = (
        settings.PRO_MONTHLY_CREDITS
        if user.subscription.plan == "pro"
        else settings.FREE_MONTHLY_CREDITS
    )

    if user.usage.used_credits >= limit:
        raise HTTPException(
            status_code=403,
            detail="Monthly credit limit reached",
        )

    result = await generate_content(payload.topic)

    record = GeneratedContent(
        user_id=user.id,
        topic=payload.topic,
        titles=result["titles"],
        description=result["description"],
        tags=result["tags"],
        prompt_version=result["prompt_version"],
    )

    user.usage.used_credits += 1

    db.add(record)
    await db.commit()

    return result


@router.get("/history")
async def history(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from sqlalchemy import select

    result = await db.execute(
        select(GeneratedContent)
        .where(GeneratedContent.user_id == user.id)
        .order_by(GeneratedContent.id.desc())
        .limit(20)
    )

    items = result.scalars().all()

    return [
        {
            "id": c.id,
            "topic": c.topic,
            "titles": c.titles,
            "tags": c.tags,
        }
        for c in items
    ]
