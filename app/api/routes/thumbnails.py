from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.generation_job import GenerationJob
from app.schemas.job import JobCreateResponse

from sqlalchemy import select
from app.models.thumbnail import Thumbnail

from sqlalchemy import select
from app.models.thumbnail import Thumbnail

router = APIRouter(prefix="/thumbnails", tags=["Thumbnails"])


@router.post("/generate", response_model=JobCreateResponse)
async def generate_thumbnail(
    payload: dict,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    job = GenerationJob(
        user_id=user.id,
        type="thumbnail",
        input=payload,
    )

    db.add(job)
    await db.commit()
    await db.refresh(job)

    return JobCreateResponse(job_id=job.id, status=job.status)

@router.get("/history")
async def history(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Thumbnail)
        .where(Thumbnail.user_id == user.id)
        .order_by(Thumbnail.id.desc())
        .limit(20)
    )

    return [
        {
            "id": t.id,
            "image_url": t.image_url,
            "prompt": t.prompt,
        }
        for t in result.scalars().all()
    ]


@router.get("/search")
async def search_thumbnails(
    q: str,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Thumbnail)
        .where(
            Thumbnail.user_id == user.id,
            Thumbnail.topic.ilike(f"%{q}%"),
        )
    )

    return [
        {
            "id": t.id,
            "image_url": t.image_url,
            "prompt": t.prompt,
        }
        for t in result.scalars().all()
    ]
