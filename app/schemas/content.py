from pydantic import BaseModel
from typing import List


class ContentGenerateRequest(BaseModel):
    topic: str


class TitleResult(BaseModel):
    text: str
    seo_score: int


class ContentGenerateResponse(BaseModel):
    titles: List[TitleResult]
    description: str
    tags: List[str]
