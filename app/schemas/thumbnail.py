from pydantic import BaseModel


class ThumbnailGenerateRequest(BaseModel):
    topic: str
    style: str | None = "youtube"


class ThumbnailResponse(BaseModel):
    id: int
    image_url: str
    prompt: str
