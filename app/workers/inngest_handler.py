from fastapi import APIRouter
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.generation_job import GenerationJob
from app.models.content import GeneratedContent
from app.services.ai_content import generate_content

from app.services.ai_thumbnail import (
    generate_thumbnail_prompt,
    generate_image,
)
from app.models.thumbnail import Thumbnail
from app.utils.storage import save_image

router = APIRouter(prefix="/workers", tags=["Workers"])


@router.post("/content/{job_id}")
async def process_content_job(job_id: int):
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(GenerationJob).where(GenerationJob.id == job_id)
        )
        job = result.scalar_one_or_none()

        if not job or job.status != "PENDING":
            return {"ignored": True}

        try:
            job.status = "RUNNING"
            await db.commit()

            result = await generate_content(job.input["topic"])

            content = GeneratedContent(
                user_id=job.user_id,
                topic=job.input["topic"],
                titles=result["titles"],
                description=result["description"],
                tags=result["tags"],
                prompt_version=result["prompt_version"],
            )

            job.status = "COMPLETED"
            job.output = result

            db.add(content)
            await db.commit()

        except Exception as e:
            job.status = "FAILED"
            job.error = str(e)
            await db.commit()

        if job.type == "thumbnail":
            topic = job.input["topic"]
            style = job.input.get("style", "youtube")

            prompt = await generate_thumbnail_prompt(topic, style)
            image_bytes = await generate_image(prompt)
            image_url = await save_image(image_bytes)

            thumbnail = Thumbnail(
                user_id=job.user_id,
                topic=topic,
                prompt=prompt,
                image_url=image_url,
            )

    job.output = {
        "image_url": image_url,
        "prompt": prompt,
    }
    job.status = "COMPLETED"

    db.add(thumbnail)
    await db.commit()


    return {"status": "done"}

    except Exception as e:
    job.retry_count += 1

    if job.retry_count >= job.max_retries:
        job.status = "FAILED"
        job.error = str(e)
    else:
        job.status = "PENDING"

    await db.commit()

