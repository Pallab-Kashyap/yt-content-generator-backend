from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.content import GeneratedContent
from app.schemas.analytics import (
    TrendingKeyword,
    OutlierVideoRequest,
    OutlierVideoResponse,
)
from app.services.trend_service import get_trending_keywords
from app.services.outlier_service import detect_outlier

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/trending", response_model=list[TrendingKeyword])
async def trending_keywords(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(GeneratedContent.topic)
        .where(GeneratedContent.user_id == user.id)
    )

    topics = [r[0] for r in result.all()]

    trends = await get_trending_keywords(topics)

    return trends

@router.post("/outlier", response_model=OutlierVideoResponse)
async def outlier_detection(payload: OutlierVideoRequest):
    result = detect_outlier(
        views=payload.views,
        avg_channel_views=payload.avg_channel_views,
        title=payload.title,
    )

    return OutlierVideoResponse(**result)
