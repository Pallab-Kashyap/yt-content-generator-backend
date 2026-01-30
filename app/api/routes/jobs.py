from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.config import settings
from app.models.generation_job import GenerationJob
from app.schemas.job import JobCreateResponse, JobStatusResponse

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/content", response_model=JobCreateResponse)
async def create_content_job(
    payload: dict,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    limit = (
        settings.PRO_MONTHLY_CREDITS
        if user.subscription.plan == "pro"
        else settings.FREE_MONTHLY_CREDITS
    )

    if user.usage.used_credits >= limit:
        raise HTTPException(403, "Monthly credit limit reached")

    job = GenerationJob(
        user_id=user.id,
        type="content",
        input=payload,
    )

    user.usage.used_credits += 1
    db.add(job)
    await db.commit()
    await db.refresh(job)

    return JobCreateResponse(job_id=job.id, status=job.status)


@router.get("/{job_id}", response_model=JobStatusResponse)
async def get_job_status(
    job_id: int,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(GenerationJob)
        .where(
            GenerationJob.id == job_id,
            GenerationJob.user_id == user.id,
        )
    )

    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(404, "Job not found")

    return JobStatusResponse(
        id=job.id,
        status=job.status,
        output=job.output,
        error=job.error,
    )
